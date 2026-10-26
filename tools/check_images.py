"""Падает, если картинки из Markdown не попали в собранный HTML.

mkdocs-glightbox 0.5.2 вместе с selectolax 1.0.1 молча вырезал <img> и оставлял
пустые <p></p>: сборка проходила, сайт публиковался без картинок.
Запускать после mkdocs build: python tools/check_images.py docs site
"""
import re
import sys
from pathlib import Path

MD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
HTML_IMAGE_RE = re.compile(r'<img[^>]+src="([^"]*)"')


def page_html(docs: Path, md: Path, site: Path) -> Path:
    rel = md.relative_to(docs).with_suffix("")
    if rel.name == "index":
        return site / rel.parent / "index.html"
    return site / rel / "index.html"


def main(docs_dir: str, site_dir: str) -> int:
    docs, site = Path(docs_dir), Path(site_dir)
    problems = []
    for md in sorted(docs.rglob("*.md")):
        expected = len(MD_IMAGE_RE.findall(md.read_text(encoding="utf-8")))
        if not expected:
            continue
        html = page_html(docs, md, site)
        if not html.exists():
            problems.append(f"{md}: не собрана страница {html}")
            continue
        # счётчик Яндекс.Метрики есть на каждой странице и картинкой не считается
        actual = sum(
            1 for src in HTML_IMAGE_RE.findall(html.read_text(encoding="utf-8"))
            if "mc.yandex.ru" not in src
        )
        if actual < expected:
            problems.append(f"{md}: в Markdown {expected} картинок, в HTML {actual}")
    if problems:
        print("Картинки потерялись при сборке:", *problems, sep="\n  ", file=sys.stderr)
        return 1
    print("Все картинки из Markdown попали в HTML")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
