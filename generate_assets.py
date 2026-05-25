#!/usr/bin/env python3
"""Generate SVG badges and project logos for the GitHub profile README."""

from __future__ import annotations

import base64
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
TEXT = ROOT / "text"

GRADIENT = """
<linearGradient id="grad" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="#6366F1"/>
  <stop offset="50%" stop-color="#8B5CF6"/>
  <stop offset="100%" stop-color="#A855F7"/>
</linearGradient>
"""

ICON_PATHS = {
    "research": '<path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44L6.5 17H4a2 2 0 0 1-2-2v-2a2 2 0 0 1 2-2h2.5l.54-2.94A2.5 2.5 0 0 1 9.5 2Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44L17.5 17H20a2 2 0 0 0 2-2v-2a2 2 0 0 0-2-2h-2.5l-.54-2.94A2.5 2.5 0 0 0 14.5 2Z"/>',
    "llm": '<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/>',
    "legal": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    "product": '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/>',
    "vision": '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
    "nlp": '<path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/>',
    "bio": '<path d="M10 2v7.31"/><path d="M14 9.3V1.99"/><path d="M8.5 2h7"/><path d="M14 9.3a6.5 6.5 0 1 1-4 0"/><path d="M5.52 16h12.96"/>',
    "xai": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/>',
    "thesis": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
}


def estimate_text_width(label: str, char_px: float = 8.4) -> int:
    return max(36, int(len(label) * char_px) + 28)


def write_text_logo(name: str, label: str) -> None:
    width = estimate_text_width(label)
    svg = textwrap.dedent(
        f"""\
        <svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="22" viewBox="0 0 {width} 22">
          <defs>{GRADIENT}</defs>
          <text x="0" y="16" fill="url(#grad)" font-family="Verdana, Geneva, DejaVu Sans, sans-serif" font-size="15" font-weight="600">{label}</text>
        </svg>
        """
    ).strip()
    (TEXT / f"{name}.svg").write_text(svg + "\n", encoding="utf-8")


def write_icon(name: str, icon_key: str) -> None:
    path = ICON_PATHS[icon_key]
    svg = textwrap.dedent(
        f"""\
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24">
          <defs>{GRADIENT}</defs>
          <g fill="none" stroke="url(#grad)" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">{path}</g>
        </svg>
        """
    ).strip()
    (TEXT / f"{name}-icon.svg").write_text(svg + "\n", encoding="utf-8")


TECH_COLORS: dict[str, tuple[str, str]] = {
    "python": ("#1D4E89", "#3776AB"),
    "pytorch": ("#B02A1B", "#EE4C2C"),
    "tensorflow": ("#C2410C", "#EA580C"),
    "docker": ("#1D7AD8", "#2496ED"),
    "aws": ("#CC7A00", "#FF9900"),
    "langgraph": ("#0F766E", "#14B8A6"),
    "rag": ("#5B21B6", "#7C3AED"),
    "fastapi": ("#00796B", "#009688"),
    "postgresql": ("#1F4E6D", "#336791"),
    "mysql": ("#2F5D85", "#4479A1"),
    "c": ("#004482", "#00599C"),
    "cpp": ("#003B6F", "#659AD2"),
    "matlab": ("#A63D00", "#E67300"),
    "latex": ("#006D6D", "#20B2AA"),
    "arduino": ("#006B6E", "#00979D"),
}


def badge(
    label: str,
    icon_svg: str,
    width: int | None = None,
    color_start: str = "#6366F1",
    color_end: str = "#A855F7",
) -> str:
    text_len = len(label) * 70 + 40
    badge_width = width or max(58, text_len // 10 + 24)
    grad_id = f"grad-{label.lower().replace(' ', '-').replace('+', 'plus')}"
    icon_b64 = base64.b64encode(icon_svg.encode("utf-8")).decode("ascii")
    gradient = f"""
<linearGradient id="{grad_id}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="{color_start}"/>
  <stop offset="100%" stop-color="{color_end}"/>
</linearGradient>
"""
    return textwrap.dedent(
        f"""\
        <svg xmlns="http://www.w3.org/2000/svg" width="{badge_width}" height="20" role="img" aria-label="{label}">
          <title>{label}</title>
          <defs>{gradient}</defs>
          <rect width="{badge_width}" height="20" fill="url(#{grad_id})" rx="10"/>
          <image x="5" y="3" width="14" height="14" href="data:image/svg+xml;base64,{icon_b64}"/>
          <text x="24" y="14" fill="#fff" font-family="Verdana, Geneva, DejaVu Sans, sans-serif" font-size="11" font-weight="600">{label}</text>
        </svg>
        """
    ).strip()


def lucide_icon(name: str, path: str) -> None:
    svg = textwrap.dedent(
        f"""\
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24">
          <defs>{GRADIENT}</defs>
          <g fill="none" stroke="url(#grad)" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">{path}</g>
        </svg>
        """
    ).strip()
    (ASSETS / name).write_text(svg + "\n", encoding="utf-8")


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    TEXT.mkdir(exist_ok=True)

    lucide_icon("lucide-map-pin.svg", '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>')
    lucide_icon("lucide-brain.svg", '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/><path d="M17.599 6.5a3 3 0 0 0 .399-1.375"/><path d="M6.003 5.125A3 3 0 0 0 6.401 6.5"/><path d="M3.477 10.896a4 4 0 0 1 .585-.396"/><path d="M19.938 10.5a4 4 0 0 1 .585.396"/><path d="M6 18a4 4 0 0 1-1.967-.516"/><path d="M19.967 17.484A4 4 0 0 1 18 18"/>')

    tech_icons = {
        "python": '<path fill="white" d="M14.25.18l.9.2.73.26.59.3.45.32.34.34.25.34.16.33.1.3.04.26.02.2-.01.13V8.5l-.05.63-.13.55-.21.46-.26.38-.3.31-.33.25-.35.19-.35.14-.33.1-.3.07-.26.04-.21.02H8.77l-.69.05-.59.14-.5.22-.41.27-.33.32-.27.35-.2.36-.15.37-.1.35-.07.32-.04.27-.02.21v3.06H3.17l-.21-.03-.28-.07-.32-.12-.35-.18-.36-.26-.36-.36-.35-.46-.32-.59-.28-.73-.21-.88-.14-1.05-.05-1.23.06-1.22.16-1.04.24-.87.32-.71.36-.57.4-.44.42-.33.42-.24.4-.16.36-.1.32-.05.24-.01h.16l.06.01h8.16v-.83H6.18l-.01-2.75-.02-.37.05-.34.11-.31.17-.28.25-.26.31-.23.38-.2.44-.18.51-.15.58-.12.64-.1.71-.06.77-.04.84-.02 1.27.05z"/>',
        "pytorch": '<path fill="white" d="M12 2c5.523 0 10 4.477 10 10s-4.477 10-10 10S2 17.523 2 12 6.477 2 12 2Zm-1.2 5.2v3.2l-2.8 1.6v3.2l5.6 3.2 5.6-3.2v-3.2l-2.8-1.6V7.2L12 4.8 10.8 7.2Z"/>',
        "tensorflow": '<path fill="white" d="M4 4h16v16H4V4Zm2 2v12h12V6H6Zm2 2h8v2H8V8Zm0 4h8v2H8v-2Zm0 4h5v2H8v-2Z"/>',
        "docker": '<path fill="white" d="M4 10h2v2H4v-2Zm3 0h2v2H7v-2Zm3 0h2v2h-2v-2Zm3 0h2v2h-2v-2Zm3 0h2v2h-2v-2ZM2 13h18v5H2v-5Zm2 2v1h14v-1H4Z"/>',
        "aws": '<path fill="white" d="M6 17l3-10h2l3 10h-2l-.5-2H8.5L8 17H6Zm2.2-4h1.6L9.8 9.8 8.2 13Zm5.8 4V7h2v10h-2Z"/>',
        "langgraph": '<path fill="white" d="M5 7h14v2H5V7Zm0 4h10v2H5v-2Zm0 4h14v2H5v-2Z"/>',
        "fastapi": '<path fill="white" d="M4 5h16v14H4V5Zm2 2v10h12V7H6Zm2 2h8v2H8V9Zm0 4h6v2H8v-2Z"/>',
        "postgresql": '<path fill="white" d="M6 4h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-4l-2 2-2-2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Z"/>',
        "mysql": '<path fill="white" d="M5 5h14v14H5V5Zm2 2v10h10V7H7Zm2 2h6v2H9V9Zm0 4h6v2H9v-2Z"/>',
        "c": '<path fill="white" d="M7 5h10v14H7V5Zm2 2v10h6V7H9Z"/>',
        "cpp": '<path fill="white" d="M5 5h14v14H5V5Zm2 2v10h10V7H7Zm1 2h8v2H8V9Zm0 4h8v2H8v-2Z"/>',
        "matlab": '<path fill="white" d="M4 6h16v12H4V6Zm2 2v8h12V8H6Zm2 2h8v2H8v-2Zm0 4h5v2H8v-2Z"/>',
        "latex": '<path fill="white" d="M5 7h14v2H5V7Zm0 4h10v2H5v-2Zm0 4h14v2H5v-2Z"/>',
        "arduino": '<path fill="white" d="M8 8h8v8H8V8Zm-2 2h12v4H6v-4Z"/>',
        "rag": '<path fill="white" d="M6 6h12v12H6V6Zm2 2v8h8V8H8Zm2 2h4v2h-4v-2Zm0 4h4v2h-4v-2Z"/>',
        "pytorch-alt": '<circle fill="white" cx="12" cy="12" r="8"/>',
    }

    for name, icon in tech_icons.items():
        label = {
            "python": "Python",
            "pytorch": "PyTorch",
            "tensorflow": "TensorFlow",
            "docker": "Docker",
            "aws": "AWS",
            "langgraph": "LangGraph",
            "fastapi": "FastAPI",
            "postgresql": "PostgreSQL",
            "mysql": "MySQL",
            "c": "C",
            "cpp": "C++",
            "matlab": "MATLAB",
            "latex": "LaTeX",
            "arduino": "Arduino",
            "rag": "RAG",
        }[name if name != "pytorch-alt" else "pytorch"]
        if name == "pytorch-alt":
            continue
        start, end = TECH_COLORS[name]
        (ASSETS / f"{name}.svg").write_text(
            badge(
                label,
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">{icon}</svg>',
                color_start=start,
                color_end=end,
            )
            + "\n",
            encoding="utf-8",
        )

    social_icons = {
        "linkedin": '<path fill="white" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 1 1-2.063-2.065 2.063 2.063 0 0 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>',
        "email": '<path fill="white" d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline fill="none" stroke="white" stroke-width="2" points="22,6 12,13 2,6"/>',
        "website": '<circle fill="white" cx="12" cy="12" r="9"/><path fill="none" stroke="#8B5CF6" stroke-width="2" d="M2 12h20"/><path fill="none" stroke="#8B5CF6" stroke-width="2" d="M12 2a15 15 0 0 1 0 20"/><path fill="none" stroke="#8B5CF6" stroke-width="2" d="M12 2a15 15 0 0 0 0 20"/>',
        "github": '<path fill="white" d="M12 .5C5.73.5.98 5.24.98 11.5c0 4.85 3.15 8.96 7.52 10.41.55.1.75-.24.75-.53 0-.26-.01-1.14-.01-2.07-3.06.67-3.71-1.47-3.71-1.47-.5-1.27-1.22-1.61-1.22-1.61-.99-.68.08-.67.08-.67 1.09.08 1.67 1.12 1.67 1.12.98 1.67 2.57 1.19 3.2.91.1-.71.38-1.19.69-1.46-2.44-.28-5.01-1.22-5.01-5.43 0-1.2.43-2.18 1.13-2.95-.11-.28-.49-1.42.11-2.96 0 0 .92-.29 3.02 1.12a10.4 10.4 0 0 1 2.75-.37c.93 0 1.86.12 2.75.37 2.1-1.41 3.02-1.12 3.02-1.12.6 1.54.22 2.68.11 2.96.7.77 1.13 1.75 1.13 2.95 0 4.22-2.58 5.15-5.03 5.43.39.34.74 1.01.74 2.04 0 1.47-.01 2.66-.01 3.02 0 .29.2.64.76.53A10.53 10.53 0 0 0 23.02 11.5C23.02 5.24 18.27.5 12 .5z"/>',
    }

    for name, icon in social_icons.items():
        label = {"linkedin": "LinkedIn", "email": "Email", "website": "Portfolio", "github": "GitHub"}[name]
        width = {"linkedin": 75, "email": 58, "website": 78, "github": 68}[name]
        (ASSETS / f"{name}.svg").write_text(
            badge(label, f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">{icon}</svg>', width=width) + "\n",
            encoding="utf-8",
        )

    projects = [
        ("langdepth", "LangDepth", "research"),
        ("llama3-rag", "Llama3 RAG", "llm"),
        ("legalrag", "LegalRAG", "legal"),
        ("visionshopper", "VisionShopper", "product"),
        ("adadepthclip", "AdaDepthCLIP", "vision"),
        ("fairseq-en-fa", "FAIRSEQ EN-FA", "nlp"),
        ("multinli", "MultiNLI", "llm"),
        ("ngs-data-analyser", "NGS Analyser", "bio"),
        ("diabet-xai", "Diabet XAI", "xai"),
        ("bachelors-thesis", "Bachelor Thesis", "thesis"),
        ("arxiv-paper", "LangDepth Paper", "research"),
        ("website-link", "Full Portfolio", "link"),
    ]

    for slug, label, icon_key in projects:
        write_text_logo(slug, label)
        write_icon(slug, icon_key)

    print(f"Generated assets in {ASSETS} and {TEXT}")


if __name__ == "__main__":
    main()
