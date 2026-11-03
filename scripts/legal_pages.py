"""Public English documents, deliberately excluded from the search sitemap."""

from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import re
from typing import Final


LEGAL_PAGES: Final = (
    ("privacy", "Privacy policy", "How Sleep2Story handles account information, stories, voice recordings and usage data."),
    ("terms", "Terms of use", "The terms for using Sleep2Story to create and listen to narrated stories."),
    ("voice-consent", "Voice consent", "What permission is needed before creating a synthetic voice in Sleep2Story."),
    ("support", "Support", "Get help with your Sleep2Story account, narration, playback or privacy request."),
)
LEGAL_ROUTES: Final = frozenset(f"/{slug}/" for slug, _, _ in LEGAL_PAGES)


def load_operator(root: Path) -> dict[str, str]:
    path = root / "site" / "legal-operator.json"
    values = json.loads(path.read_text(encoding="utf-8"))
    for key in ("name", "country", "email", "updated"):
        value = values.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Set the confirmed public operator {key!r} in {path} before publishing.")
        values[key] = value.strip()
    if not re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", values["email"]):
        raise ValueError(f"Invalid public contact email in {path}")
    updated = date.fromisoformat(values["updated"])
    return {
        **{f"operator.{key}": value for key, value in values.items()},
        "updated_label": f"{updated.day} {updated.strftime('%B %Y')}",
    }


def footer_links(current: str = "") -> str:
    links = []
    for slug, title, _ in LEGAL_PAGES:
        active = ' aria-current="page"' if slug == current else ""
        label = {"privacy": "Privacy", "terms": "Terms"}.get(slug, title)
        links.append(f'<a href="/{slug}/" lang="en"{active}>{label}</a>')
    return '<nav class="legal-links" aria-label="Legal and support" lang="en">' + "".join(links) + "</nav>"
