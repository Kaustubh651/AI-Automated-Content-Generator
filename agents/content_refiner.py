# agents/content_refiner.py

import re
from textwrap import fill


class ContentRefiner:
    def __init__(self, max_length=1200):
        self.max_length = max_length

    def refine(self, text: str, style: str) -> str:
        """
        Refines generated content without changing meaning or style.
        """
        if not text or not isinstance(text, str):
            return ""

        text = self._clean_text(text)
        text = self._structure_text(text, style)
        text = self._trim_length(text)

        return text.strip()

    def _clean_text(self, text: str) -> str:
        # Remove extra spaces and blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        return text.strip()

    def _structure_text(self, text: str, style: str) -> str:
        """
        Adds light structure depending on style
        """
        paragraphs = text.split("\n")

        if style.lower() == "linkedin":
            return self._linkedin_structure(paragraphs)

        if style.lower() == "twitter":
            return self._twitter_structure(text)

        # Default: blog/article
        return "\n\n".join(paragraphs)

    def _linkedin_structure(self, paragraphs):
        refined = []
        for p in paragraphs:
            if len(p.strip()) > 0:
                refined.append(fill(p.strip(), width=90))
        return "\n\n".join(refined)

    def _twitter_structure(self, text):
        # Twitter-friendly trimming
        return text[:280]

    def _trim_length(self, text: str) -> str:
        if len(text) > self.max_length:
            return text[: self.max_length].rsplit(" ", 1)[0] + "..."
        return text
