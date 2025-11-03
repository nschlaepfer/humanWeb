"""GPT-5 helper utilities built on the OpenAI responses API."""

from __future__ import annotations

import textwrap
from typing import Iterable, List, Sequence

from openai import OpenAI

from ._compat import slotted_dataclass


def _parse_list(raw: str) -> List[str]:
    """Convert a numbered or bulleted list response into a list of strings."""

    items: List[str] = []
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped[0].isdigit() and "." in stripped:
            stripped = stripped.split(".", 1)[1].strip()
        elif stripped.startswith(("-", "*")):
            stripped = stripped[1:].strip()
        items.append(stripped)
    return [item for item in items if item]


def _extract_text(response) -> str:
    """Best-effort extraction of textual content from an OpenAI response."""

    if hasattr(response, "output_text") and response.output_text:
        return response.output_text.strip()

    chunks: List[str] = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            text = getattr(content, "text", None)
            if text:
                chunks.append(text)
    return "\n".join(chunks).strip()


@slotted_dataclass
class GPTResearchAgent:
    """High-level wrapper that orchestrates GPT-5 prompts used by the tool."""

    client: OpenAI
    model: str = "gpt-5"

    def _call(self, system_prompt: str, user_prompt: str, *, effort: str = "medium") -> str:
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": [{"type": "input_text", "text": system_prompt}],
                },
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": user_prompt}],
                },
            ],
            text={"format": {"type": "text"}},
            reasoning={"effort": effort, "summary": "auto"},
        )
        return _extract_text(response)

    def plan_search_queries(self, primary_question: str, count: int) -> List[str]:
        system_prompt = (
            "You are an elite research strategist. Craft a minimal, high-impact sequence of "
            "search queries that will explore a topic comprehensively."
        )
        user_prompt = textwrap.dedent(
            f"""
            Core research question: {primary_question}
            Produce exactly {count} Google search queries. Each query should focus on a distinct
            sub-problem or angle. Return the list in the order the searches should be executed.
            """
        ).strip()

        return _parse_list(self._call(system_prompt, user_prompt))[:count]

    def analyse_source(
        self,
        *,
        initial_question: str,
        active_query: str,
        title: str,
        url: str,
        content_snippet: str,
        network_summary: str,
        performance_metrics: Sequence[str],
    ) -> str:
        system_prompt = (
            "You are a senior intelligence analyst. Extract novel, actionable insights from "
            "web content. Focus on facts, figures, causal relationships, and critical context."
        )

        formatted_metrics = "\n".join(performance_metrics)
        user_prompt = textwrap.dedent(
            f"""
            Research programme: {initial_question}
            Current search query: {active_query}
            Source title: {title}
            URL: {url}

            Network observations:
            {network_summary or 'No network data captured.'}

            Performance metrics:
            {formatted_metrics or 'No DevTools performance metrics available.'}

            Extracted text (truncated to relevant portion):
            {content_snippet}

            Deliver a concise markdown section with:
            - Bullet-point insights referencing the URL inline.
            - Quantitative data where possible.
            - A short implications paragraph.
            """
        ).strip()

        return self._call(system_prompt, user_prompt, effort="high")

    def synthesise_report(self, initial_question: str, insights: Iterable[str]) -> str:
        system_prompt = (
            "You are the lead author of a professional intelligence brief. Integrate all findings "
            "into a compelling, source-backed report."
        )
        body = "\n\n".join(insights)
        user_prompt = textwrap.dedent(
            f"""
            Draft a multi-section report addressing: {initial_question}
            - Start with an executive summary.
            - Develop thematic sections drawing from the provided insight snippets.
            - Use inline citations referencing the original URLs embedded in the snippets.
            - End with recommended follow-up actions and outstanding questions.

            Source material:
            {body}
            """
        ).strip()

        return self._call(system_prompt, user_prompt, effort="high")

    def assess_report(self, initial_question: str, report: str, evidence: Iterable[str]) -> str:
        system_prompt = (
            "You are a rigorous quality assurance reviewer. Score the report for coverage, "
            "accuracy, and clarity. Provide explicit remediation guidance."
        )
        evidence_block = "\n\n".join(evidence)
        user_prompt = textwrap.dedent(
            f"""
            Target objective: {initial_question}
            Report under review:
            {report}

            Evidence packets:
            {evidence_block}

            Return:
            - An overall score out of 10 with justification.
            - A list of factual gaps or contradictions.
            - Recommended improvements.
            """
        ).strip()

        return self._call(system_prompt, user_prompt)
