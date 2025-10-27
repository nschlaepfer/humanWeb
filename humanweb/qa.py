"""Quality review helpers built on GPT-5."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from openai import OpenAI


@dataclass(slots=True)
class ReportReviewer:
    client: OpenAI
    model: str = "gpt-5"

    def review(self, *, objective: str, report: str, evidence: Iterable[str]) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "You are a critical reviewer grading a research report. Highlight"
                                " factual gaps and improvement opportunities."
                            ),
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                f"Objective: {objective}\n\nReport:\n{report}\n\nEvidence packets:\n"
                                + "\n\n".join(evidence)
                                + "\n\nReturn a markdown assessment with score, strengths, weaknesses, and actionable next steps."
                            ),
                        }
                    ],
                },
            ],
            text={"format": {"type": "text"}},
            reasoning={"effort": "medium", "summary": "auto"},
        )

        if hasattr(response, "output_text") and response.output_text:
            return response.output_text.strip()

        parts = []
        for item in getattr(response, "output", []) or []:
            for content in getattr(item, "content", []) or []:
                text = getattr(content, "text", None)
                if text:
                    parts.append(text)
        return "\n".join(parts).strip()

