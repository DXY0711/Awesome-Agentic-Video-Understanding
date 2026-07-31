from __future__ import annotations

import argparse
import json
import re
import time
import xml.etree.ElementTree as ET
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen

from pypdf import PdfReader

import generate_readme as readme


OUTPUT = readme.REPO_ROOT / "data" / "paper_links.json"
OVERRIDES = readme.REPO_ROOT / "data" / "verified_link_overrides.json"
ARXIV_API = "https://export.arxiv.org/api/query"
ARXIV_RE = re.compile(r"(?:arXiv\s*:\s*|arxiv\.org/(?:abs|pdf)/)(\d{4}\.\d{4,5})", re.I)
URL_RE = re.compile(r"https?://[^\s<>\]\[{}\"']+", re.I)
ATOM = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

BLOCKED_WEB_HOSTS = {
    "arxiv.org",
    "www.arxiv.org",
    "youtube.com",
    "www.youtube.com",
    "youtu.be",
    "mturk.com",
    "www.mturk.com",
    "amazon.com",
    "www.amazon.com",
    "orcid.org",
    "creativecommons.org",
}
PUBLICATION_HOSTS = {
    "openaccess.thecvf.com",
    "proceedings.mlr.press",
    "aclanthology.org",
    "dl.acm.org",
    "openreview.net",
    "ieeexplore.ieee.org",
    "link.springer.com",
    "doi.org",
}
GENERIC_TOKENS = {
    "a", "an", "and", "agent", "agents", "for", "from", "in", "of", "on", "the", "to",
    "towards", "using", "via", "video", "videos", "understanding", "with", "large", "language",
    "multimodal", "model", "models", "learning", "reasoning", "benchmark", "framework",
}


def cited_keys() -> set[str]:
    paths = [
        readme.SOURCE_ROOT / "main.tex",
        readme.SOURCE_ROOT / "Appendix.tex",
        readme.SOURCE_ROOT / "images" / "method_paper_master_table_main.tex",
        readme.SOURCE_ROOT / "images" / "method_paper_master_table_appendix.tex",
    ]
    keys: set[str] = set()
    for path in paths:
        keys |= readme.cite_keys(path.read_text(encoding="utf-8"))
    return keys


def clean_url(value: str) -> str:
    value = value.strip().replace("\\", "").rstrip(".,;:!?)\\")
    if not value.startswith(("http://", "https://")):
        return ""
    try:
        parts = urlsplit(value)
    except ValueError:
        return ""
    host = parts.netloc.lower().removeprefix("www.")
    if not host:
        return ""
    return urlunsplit((parts.scheme.lower(), parts.netloc, parts.path.rstrip("/"), parts.query, ""))


def pdf_evidence(path: Path) -> tuple[set[str], str]:
    urls = {clean_url(url) for url in readme.extract_pdf_links(path)}
    text = ""
    try:
        reader = PdfReader(str(path), strict=False)
        text = "\n".join((page.extract_text() or "") for page in reader.pages[:3])
        urls |= {clean_url(url) for url in URL_RE.findall(text)}
    except Exception:
        pass
    return {url for url in urls if url}, text


def title_similarity(left: str, right: str) -> float:
    a = readme.normalized(left)
    b = readme.normalized(right)
    if not a or not b:
        return 0.0
    at = set(a.split()) - GENERIC_TOKENS
    bt = set(b.split()) - GENERIC_TOKENS
    jaccard = len(at & bt) / max(1, len(at | bt))
    return 0.55 * SequenceMatcher(None, a, b).ratio() + 0.45 * jaccard


def url_tokens(url: str) -> set[str]:
    parts = urlsplit(url)
    return set(readme.normalized(parts.netloc + " " + parts.path).split()) - GENERIC_TOKENS


def significant_tokens(title: str, method: str = "") -> set[str]:
    tokens = set(readme.normalized(title + " " + method).split()) - GENERIC_TOKENS
    return {token for token in tokens if len(token) >= 3}


def github_candidate(urls: set[str]) -> str:
    candidates: list[str] = []
    for url in urls:
        parts = urlsplit(url)
        if parts.netloc.lower().removeprefix("www.") != "github.com":
            continue
        segments = [segment for segment in parts.path.split("/") if segment]
        if len(segments) < 2 or segments[0].lower() in {"features", "marketplace", "search", "topics"}:
            continue
        candidates.append(url)
    return sorted(candidates, key=lambda value: (value.count("/"), len(value)))[0] if candidates else ""


def web_candidate(urls: set[str], title: str, method: str, entry: readme.BibEntry) -> str:
    paper_tokens = significant_tokens(title, method)
    scored: list[tuple[float, str]] = []
    publication: list[str] = []
    for url in urls:
        parts = urlsplit(url)
        host = parts.netloc.lower().removeprefix("www.")
        if host in BLOCKED_WEB_HOSTS or host == "github.com" or "arxiv.org" in host:
            continue
        if host in PUBLICATION_HOSTS:
            publication.append(url)
            continue
        overlap = len(url_tokens(url) & paper_tokens)
        score = float(overlap)
        if host.endswith(".github.io"):
            score += 4.0
        if (host.endswith(".ai") and overlap) or "project" in parts.path.lower() or "sites.google.com/view" in url.lower():
            score += 2.0
        if "huggingface.co" in host and overlap == 0:
            continue
        if overlap == 0 and score < 2.0:
            continue
        scored.append((score, url))
    if scored:
        return sorted(scored, key=lambda item: (-item[0], len(item[1])))[0][1]

    raw_url = readme.clean_latex(entry.fields.get("url", ""))
    if raw_url.startswith(("http://", "https://")) and "arxiv.org" not in raw_url.lower():
        return clean_url(raw_url)
    doi = readme.clean_latex(entry.fields.get("doi", ""))
    if doi:
        return f"https://doi.org/{doi}"
    return sorted(publication, key=len)[0] if publication else ""


def parse_arxiv_feed(payload: bytes) -> list[dict[str, str]]:
    root = ET.fromstring(payload)
    records: list[dict[str, str]] = []
    for node in root.findall("a:entry", ATOM):
        identifier_match = re.search(r"/(\d{4}\.\d{4,5})(?:v\d+)?$", node.findtext("a:id", "", ATOM))
        if not identifier_match:
            continue
        text = " ".join(
            filter(
                None,
                [
                    node.findtext("a:summary", "", ATOM),
                    node.findtext("arxiv:comment", "", ATOM),
                ],
            )
        )
        records.append(
            {
                "arxiv": identifier_match.group(1),
                "title": " ".join(node.findtext("a:title", "", ATOM).split()),
                "text": text,
            }
        )
    return records


def arxiv_request(params: dict[str, str], retries: int = 2) -> list[dict[str, str]]:
    url = ARXIV_API + "?" + urlencode(params)
    for attempt in range(retries):
        try:
            request = Request(url, headers={"User-Agent": "agentic-video-survey-link-audit/1.0"})
            with urlopen(request, timeout=30) as response:
                return parse_arxiv_feed(response.read())
        except Exception as exc:
            if attempt + 1 == retries:
                print(f"arXiv request failed: {exc}")
                return []
            time.sleep(4)
    return []


def update_from_arxiv_record(record: dict[str, str], item: dict[str, object]) -> None:
    item["arxiv"] = record["arxiv"]
    urls = {clean_url(url) for url in URL_RE.findall(record["text"])}
    urls.discard("")
    github = github_candidate(urls)
    if github and not item.get("github"):
        item["github"] = github
        item["evidence"].append("arXiv metadata: GitHub")
    if urls:
        item["arxiv_urls"] = sorted(urls)


def enrich_arxiv(data: dict[str, dict[str, object]], entries: dict[str, readme.BibEntry]) -> None:
    missing = [key for key, item in data.items() if not item.get("arxiv")]
    for offset in range(0, len(missing), 6):
        batch = missing[offset:offset + 6]
        query = " OR ".join(f'ti:"{entries[key].title.replace(chr(34), " ")}"' for key in batch)
        records = arxiv_request({"search_query": query, "start": "0", "max_results": "30"})
        for key in batch:
            ranked = sorted(
                ((title_similarity(entries[key].title, record["title"]), record) for record in records),
                key=lambda item: item[0],
                reverse=True,
            )
            if ranked and ranked[0][0] >= 0.82:
                update_from_arxiv_record(ranked[0][1], data[key])
                data[key]["evidence"].append(f"arXiv title match ({ranked[0][0]:.2f})")
        print(f"arXiv title search: {min(offset + len(batch), len(missing))}/{len(missing)}")
        if offset + len(batch) < len(missing):
            time.sleep(3.1)

    known = [(key, str(item["arxiv"])) for key, item in data.items() if item.get("arxiv")]
    by_id = {identifier: key for key, identifier in known}
    identifiers = list(by_id)
    for offset in range(0, len(identifiers), 20):
        batch = identifiers[offset:offset + 20]
        records = arxiv_request({"id_list": ",".join(batch), "start": "0", "max_results": str(len(batch))})
        for record in records:
            key = by_id.get(record["arxiv"])
            if key:
                update_from_arxiv_record(record, data[key])
        if offset + len(batch) < len(identifiers):
            time.sleep(3.1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a verified arXiv/Web/GitHub link cache for the survey README.")
    parser.add_argument("--offline", action="store_true", help="Use BibTeX and local PDFs only.")
    args = parser.parse_args()

    entries = readme.parse_bibtex(readme.SOURCE_ROOT / "video_understanding_agent_references.bib")
    keys = cited_keys()
    methods = readme.parse_methods(readme.SOURCE_ROOT / "images" / "method_paper_master_table_main.tex")
    methods += readme.parse_methods(readme.SOURCE_ROOT / "images" / "method_paper_master_table_appendix.tex")
    method_by_key = {method.key: method.method for method in methods}
    pdfs = sorted(readme.PAPER_ROOT.glob("*.pdf"))

    prior: dict[str, dict[str, object]] = {}
    overrides: dict[str, dict[str, object]] = {}
    if OUTPUT.exists():
        prior = json.loads(OUTPUT.read_text(encoding="utf-8"))
    if OVERRIDES.exists():
        overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
        for key, values in overrides.items():
            prior.setdefault(key, {}).update(values)

    cache: dict[Path, tuple[set[str], str]] = {}
    data: dict[str, dict[str, object]] = {}
    for key in sorted(keys):
        entry = entries[key]
        item: dict[str, object] = {
            "arxiv": readme.arxiv_id(entry),
            "web": "",
            "github": "",
            "local_pdf": "",
            "evidence": [],
        }
        pdf, score = readme.match_pdf(entry, pdfs)
        urls: set[str] = set()
        text = ""
        if pdf:
            urls, text = cache.setdefault(pdf, pdf_evidence(pdf))
            item["local_pdf"] = pdf.name
            item["evidence"].append(f"local PDF title match ({score:.2f})")
        identifiers = set(ARXIV_RE.findall(text))
        for url in urls:
            identifiers |= set(ARXIV_RE.findall(url))
        if not item["arxiv"] and identifiers:
            item["arxiv"] = sorted(identifiers)[0]
            item["evidence"].append("local PDF arXiv identifier")
        item["github"] = github_candidate(urls)
        if item["github"]:
            item["evidence"].append("local PDF GitHub link")
        item["web"] = web_candidate(urls, entry.title, method_by_key.get(key, ""), entry)
        if item["web"]:
            item["evidence"].append("local PDF/BibTeX web link")

        for field in ["arxiv", "web", "github"]:
            if key in overrides and field in overrides[key]:
                item[field] = overrides[key][field]
                item["evidence"].append(f"verified override: {field}")
            elif prior.get(key, {}).get(field):
                item[field] = prior[key][field]
        data[key] = item

    if not args.offline:
        enrich_arxiv(data, entries)
        for key, item in data.items():
            extra_urls = set(item.pop("arxiv_urls", []))
            if extra_urls:
                if not item.get("github"):
                    item["github"] = github_candidate(extra_urls)
                if not item.get("web"):
                    item["web"] = web_candidate(extra_urls, entries[key].title, method_by_key.get(key, ""), entries[key])

    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    counts = {field: sum(bool(item.get(field)) for item in data.values()) for field in ["arxiv", "web", "github"]}
    print(f"Wrote {OUTPUT} for {len(data)} cited papers: {counts}")


if __name__ == "__main__":
    main()
