"""Chrome DevTools driven browser automation helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Optional

from bs4 import BeautifulSoup
from playwright.async_api import (  # type: ignore[import]
    Browser,
    Error as PlaywrightError,
    Page,
    Playwright,
    TimeoutError as PlaywrightTimeoutError,
    async_playwright,
)

from ._compat import slotted_dataclass


@slotted_dataclass
class SearchResult:
    """A single Google search hit."""

    title: str
    url: str
    snippet: str


@slotted_dataclass
class PageInsights:
    """Data collected from a webpage using Chrome DevTools."""

    url: str
    title: str
    text_content: str
    screenshot_path: Optional[Path]
    trace_path: Optional[Path]
    performance_metrics: Dict[str, float]
    network_requests: List[Dict[str, object]]
    console_messages: List[Dict[str, object]]


class ChromeDevToolsSession:
    """Manage a Chromium instance instrumented via the Chrome DevTools protocol."""

    def __init__(
        self,
        *,
        headless: bool = True,
        navigation_timeout: float = 30.0,
        slow_mo: Optional[float] = None,
    ) -> None:
        self._headless = headless
        self._navigation_timeout = navigation_timeout
        self._slow_mo = slow_mo
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._page: Optional[Page] = None

    async def __aenter__(self) -> "ChromeDevToolsSession":
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=self._headless, slow_mo=self._slow_mo
        )
        context = await self._browser.new_context()
        self._page = await context.new_page()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._page:
            await self._page.context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    @property
    def page(self) -> Page:
        if not self._page:
            raise RuntimeError("Browser session has not been started yet.")
        return self._page

    async def search(self, query: str, limit: int = 5) -> List[SearchResult]:
        """Perform a Google search and return structured results."""

        page = self.page
        await page.goto("https://www.google.com", wait_until="load")

        search_box = await page.wait_for_selector("textarea[name='q']", timeout=self._navigation_timeout * 1000)
        await search_box.fill(query)
        await search_box.press("Enter")

        await page.wait_for_selector("div#search", timeout=self._navigation_timeout * 1000)

        results: List[SearchResult] = []
        cards = await page.query_selector_all("div#search div.g")
        for card in cards:
            if len(results) >= limit:
                break

            link = await card.query_selector("a")
            title_el = await card.query_selector("h3")
            if not link or not title_el:
                continue
            href = await link.get_attribute("href")
            if not href or "youtube.com" in href.lower():
                continue

            title = (await title_el.inner_text()).strip()
            snippet_el = await card.query_selector("div.VwiC3b")
            snippet = (await snippet_el.inner_text()).strip() if snippet_el else ""

            results.append(SearchResult(title=title, url=href, snippet=snippet))

        return results

    async def collect_page_insights(
        self,
        url: str,
        *,
        output_dir: Path,
        artifact_prefix: str,
    ) -> PageInsights:
        """Navigate to a URL and collect a variety of debugging artefacts."""

        output_dir.mkdir(parents=True, exist_ok=True)
        context = self.page.context
        page = await context.new_page()

        console_messages: List[Dict[str, object]] = []
        network_requests: List[Dict[str, object]] = []

        page.on(
            "console",
            lambda msg: console_messages.append(
                {
                    "type": msg.type,
                    "text": msg.text,
                    "location": msg.location,
                }
            ),
        )

        def _record_response(response):
            try:
                network_requests.append(
                    {
                        "url": response.url,
                        "status": response.status,
                        "resourceType": response.request.resource_type,
                    }
                )
            except Exception:
                pass

        page.on("response", _record_response)

        screenshot_path: Optional[Path] = output_dir / f"{artifact_prefix}.png"
        trace_path: Optional[Path] = output_dir / f"{artifact_prefix}_trace.zip"

        await context.tracing.start(screenshots=True, snapshots=True, sources=True)

        try:
            try:
                await page.goto(url, wait_until="load", timeout=self._navigation_timeout * 1000)
            except PlaywrightTimeoutError:
                await page.goto(url, wait_until="domcontentloaded")

            html = await page.content()
            soup = BeautifulSoup(html, "html.parser")
            text_content = soup.get_text("\n", strip=True)
            title = await page.title()

            if screenshot_path:
                try:
                    await page.screenshot(path=str(screenshot_path), full_page=True)
                except PlaywrightError:
                    screenshot_path = None

            performance_metrics: Dict[str, float] = {}
            try:
                session = await context.new_cdp_session(page)
                await session.send("Performance.enable")
                metrics = await session.send("Performance.getMetrics")
                for entry in metrics.get("metrics", []):
                    name = entry.get("name")
                    value = entry.get("value")
                    if isinstance(name, str) and isinstance(value, (float, int)):
                        performance_metrics[name] = float(value)
            except PlaywrightError:
                performance_metrics = {}

        finally:
            try:
                await context.tracing.stop(path=str(trace_path))
            except PlaywrightError:
                trace_path = None

            await page.close()

        return PageInsights(
            url=url,
            title=title if "title" in locals() else url,
            text_content=text_content if "text_content" in locals() else "",
            screenshot_path=screenshot_path if screenshot_path and screenshot_path.exists() else None,
            trace_path=trace_path if trace_path and trace_path.exists() else None,
            performance_metrics=performance_metrics,
            network_requests=network_requests,
            console_messages=console_messages,
        )


def summarise_network(requests: Iterable[Dict[str, object]], limit: int = 8) -> str:
    """Create a condensed textual summary of captured network requests."""

    rows: List[str] = []
    for entry in requests:
        url = str(entry.get("url", ""))
        status = entry.get("status", "?")
        resource_type = entry.get("resourceType", "")
        trimmed_url = url.split("?")[0][:120]
        rows.append(f"- {status} {resource_type}: {trimmed_url}")
        if len(rows) >= limit:
            break
    return "\n".join(rows)
