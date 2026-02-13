# services/meme_engine/content_refiner.py

import re
from difflib import SequenceMatcher


class ContentRefiner:
    def __init__(self, similarity_threshold: float = 0.88):
        self.similarity_threshold = similarity_threshold

    # ================= CORE =================
    def refine(self, text: str, style: str) -> str:
        """
        Clean, deduplicate and format generated text
        according to the target platform style.
        """
        style = style.lower()

        cleaned_text = self._remove_prompt_artifacts(text)
        lines = self._split_lines(cleaned_text)
        lines = self._deduplicate(lines)

        if style == "twitter":
            return self._format_twitter(lines)
        elif style == "medium":
            return self._format_medium(lines)
        elif style == "youtube":
            return self._format_youtube(lines)
        else:
            return "\n".join(lines)

    # ================= CLEANING =================
    def _remove_prompt_artifacts(self, text: str) -> str:
        # Remove instruction blocks and bullets
        patterns = [
            r"You are .*",
            r"Rules:.*",
            r"Structure:.*",
            r"Tone:.*",
            r"Article:.*",
            r"Write .*",
            r"Read the article .*",
            r"- Confident tone.*",
            r"- Slightly controversial.*",
            r"- .*tweets.*",
            r"- No emojis.*",
            r"- Strong hook.*",
            r"- Explain impact.*",
            r"- Simple language.*",
            r"- End with call to action.*"
        ]

        for p in patterns:
            text = re.sub(p, "", text, flags=re.IGNORECASE)

        # Remove leftover bullet-only lines
        text = "\n".join(
            line for line in text.split("\n")
            if not re.match(r"^\s*-\s*", line)
        )

        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


    def _split_lines(self, text: str):
        return [line.strip() for line in text.split("\n") if line.strip()]

    def _deduplicate(self, lines):
        unique_lines = []
        for line in lines:
            if not any(self._is_similar(line, existing) for existing in unique_lines):
                unique_lines.append(line)
        return unique_lines

    def _is_similar(self, a: str, b: str) -> bool:
        return (
            SequenceMatcher(None, a.lower(), b.lower()).ratio()
            > self.similarity_threshold
        )

    # ================= FORMATTERS =================
    def _format_twitter(self, lines):
        tweets = lines[:7]
        return "\n\n".join(f"{i+1}/ {tweet}" for i, tweet in enumerate(tweets))

    def _format_medium(self, lines):
        if not lines:
            return ""

        title = lines[0] if len(lines[0]) > 20 else "The Rise of Autonomous AI Agents"
        body = lines[1:]

        sections = []
        buffer = []

        for line in body:
            buffer.append(line)
            if len(buffer) == 4:
                sections.append(buffer)
                buffer = []

        formatted = [f"# {title}\n"]

        for idx, section in enumerate(sections[:3], start=1):
            formatted.append(
                f"## Section {idx}\n" + " ".join(section)
            )

        formatted.append(
            "## Conclusion\n"
            "The real impact of this shift depends on how responsibly "
            "and thoughtfully the technology is adopted."
        )

        return "\n\n".join(formatted)

    def _format_youtube(self, lines):
        if not lines:
            return ""

        hook = lines[0]
        body = lines[1:6]

        outro = (
            "If this trend continues, it could completely reshape how the industry works.\n\n"
            "Subscribe for more tech breakdowns and drop your thoughts in the comments."
        )

        return "\n\n".join([hook] + body + [outro])
