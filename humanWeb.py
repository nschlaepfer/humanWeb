"""Command line entry-point for the GPT-5 powered humanWeb assistant."""

from __future__ import annotations

import asyncio
import os
import shutil
from typing import List

from dotenv import load_dotenv
from openai import OpenAI

from humanweb import ChromeDevToolsSession, GPTResearchAgent, ResearchStorage
from humanweb.browser import summarise_network
from humanweb.qa import ReportReviewer


def _truncate_text(text: str, limit: int = 6000) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n...[truncated]"


async def run() -> None:
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set. Please configure your environment before running the tool.")

    client = OpenAI()
    researcher = GPTResearchAgent(client)
    reviewer = ReportReviewer(client)

    print("\nWelcome to the GPT-5 edition of humanWeb!\n")
    num_results = int(input("Number of websites to visit per query (default 3): ") or 3)
    initial_query = input("Enter your research objective: ").strip()
    if not initial_query:
        raise ValueError("A research objective is required to proceed.")
    num_queries = int(input("How many follow-up searches should we perform? (default 4): ") or 4)

    storage = ResearchStorage(initial_query)

    planned_queries: List[str] = researcher.plan_search_queries(initial_query, num_queries)
    if initial_query not in planned_queries:
        planned_queries.insert(0, initial_query)

    print("\nExecuting research plan:\n" + "\n".join(f"  - {query}" for query in planned_queries))

    async with ChromeDevToolsSession(headless=True) as browser:
        for query_index, query in enumerate(planned_queries, start=1):
            print(f"\nSearching for: {query}")
            results = await browser.search(query, limit=num_results)
            if not results:
                print("  No results returned by Google.")
                continue

            storage.log_search_results(query, results)
            for result_index, result in enumerate(results, start=1):
                print(f"  [{result_index}/{len(results)}] Fetching {result.title}")
                staging_dir = storage.base_path / "_staging" / f"{query_index:02d}_{result_index:02d}"
                insights = await browser.collect_page_insights(
                    result.url,
                    output_dir=staging_dir,
                    artifact_prefix="capture",
                )

                snippet = _truncate_text(insights.text_content)
                network_summary = summarise_network(insights.network_requests)
                metrics_summary = [f"{key}: {value:.2f}" for key, value in sorted(insights.performance_metrics.items())[:10]]

                summary = researcher.analyse_source(
                    initial_question=initial_query,
                    active_query=query,
                    title=insights.title or result.title,
                    url=result.url,
                    content_snippet=snippet,
                    network_summary=network_summary,
                    performance_metrics=metrics_summary,
                )

                storage.persist_page_insights(query, result, insights, summary)

                if staging_dir.exists():
                    shutil.rmtree(staging_dir, ignore_errors=True)

    if not storage.summaries:
        print("No insights were gathered. Exiting.")
        return

    report = researcher.synthesise_report(initial_query, storage.iter_summaries())
    report_path = storage.save_report(initial_query, report)
    print(f"\nReport saved to {report_path}")

    review = reviewer.review(objective=initial_query, report=report, evidence=storage.iter_summaries())
    review_path = storage.save_quality_review(initial_query, review)
    print(f"Quality review saved to {review_path}")


if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nInterrupted by user.")

