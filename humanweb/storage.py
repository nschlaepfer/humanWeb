"""Persistent storage helpers for research runs."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Sequence

from .browser import PageInsights, SearchResult


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "session"


@dataclass(slots=True)
class ResearchStorage:
    """Manages the directory structure used to persist research artefacts."""

    topic: str
    base_path: Path = field(init=False)
    reports_path: Path = field(init=False)
    qa_path: Path = field(init=False)
    summaries: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        slug = _slugify(self.topic)
        self.base_path = Path("Searches") / slug
        self.reports_path = Path("Reports") / slug
        self.qa_path = Path("QA") / slug

        for path in (self.base_path, self.reports_path, self.qa_path):
            path.mkdir(parents=True, exist_ok=True)

    def log_search_results(self, query: str, results: Sequence[SearchResult]) -> Path:
        query_slug = _slugify(query)
        output_file = self.base_path / f"{query_slug}_results.json"
        serialisable = [result.__dict__ for result in results]
        output_file.write_text(json.dumps(serialisable, indent=2, ensure_ascii=False))
        return output_file

    def persist_page_insights(
        self,
        query: str,
        result: SearchResult,
        insights: PageInsights,
        summary: str,
    ) -> None:
        query_slug = _slugify(query)
        result_slug = _slugify(result.title or result.url)
        artefact_dir = self.base_path / query_slug / result_slug
        artefact_dir.mkdir(parents=True, exist_ok=True)

        (artefact_dir / "insights.json").write_text(
            json.dumps(
                {
                    "searchResult": result.__dict__,
                    "pageInsights": {
                        "url": insights.url,
                        "title": insights.title,
                        "text_content": insights.text_content,
                        "performance_metrics": insights.performance_metrics,
                        "network_requests": insights.network_requests,
                        "console_messages": insights.console_messages,
                        "screenshot_path": str(insights.screenshot_path) if insights.screenshot_path else None,
                        "trace_path": str(insights.trace_path) if insights.trace_path else None,
                    },
                },
                indent=2,
                ensure_ascii=False,
            )
        )

        (artefact_dir / "summary.md").write_text(summary)

        if insights.screenshot_path and insights.screenshot_path.exists():
            target = artefact_dir / insights.screenshot_path.name
            if insights.screenshot_path != target:
                target.write_bytes(insights.screenshot_path.read_bytes())

        if insights.trace_path and insights.trace_path.exists():
            target = artefact_dir / insights.trace_path.name
            if insights.trace_path != target:
                target.write_bytes(insights.trace_path.read_bytes())

        self.summaries.append(summary)

    def save_report(self, query_label: str, report: str) -> Path:
        query_slug = _slugify(query_label)
        report_path = self.reports_path / f"report_{query_slug}.md"
        report_path.write_text(report)
        return report_path

    def save_quality_review(self, query_label: str, qa_markdown: str) -> Path:
        query_slug = _slugify(query_label)
        qa_path = self.qa_path / f"review_{query_slug}.md"
        qa_path.write_text(qa_markdown)
        return qa_path

    def iter_summaries(self) -> Iterable[str]:
        return list(self.summaries)

