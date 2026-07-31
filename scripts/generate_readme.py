from __future__ import annotations

import re
import json
from collections import defaultdict
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import quote

from pypdf import PdfReader


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent
SOURCE_ROOT = WORKSPACE_ROOT / "Article" / "Video_Agent_Survey"
PAPER_ROOT = WORKSPACE_ROOT / "paper"
LINK_CACHE = REPO_ROOT / "data" / "paper_links.json"
LINK_OVERRIDES = REPO_ROOT / "data" / "verified_link_overrides.json"


@dataclass
class BibEntry:
    key: str
    entry_type: str
    fields: dict[str, str]

    @property
    def title(self) -> str:
        return clean_latex(self.fields.get("title", self.key))

    @property
    def year(self) -> str:
        return clean_latex(self.fields.get("year", ""))


@dataclass
class Method:
    method: str
    key: str
    year: str
    challenge: str
    paradigm: str
    learning: list[str] = field(default_factory=list)
    supervision: list[str] = field(default_factory=list)


def clean_latex(value: str) -> str:
    value = value.replace("\\&", "&").replace("--", "-")
    value = re.sub(r"\\(?:textit|textbf|emph|textsc)\{([^{}]*)\}", r"\1", value)
    value = re.sub(r"\\[a-zA-Z]+", "", value)
    value = value.replace("{", "").replace("}", "")
    value = re.sub(r"\s+", " ", value)
    return value.strip().strip(",")


def parse_bibtex(path: Path) -> dict[str, BibEntry]:
    text = path.read_text(encoding="utf-8")
    entries: dict[str, BibEntry] = {}
    header = re.compile(r"@(\w+)\s*\{\s*([^,]+),", re.I)
    position = 0
    while match := header.search(text, position):
        entry_type, key = match.group(1), match.group(2).strip()
        opening = text.find("{", match.start())
        depth = 0
        closing = len(text)
        for index in range(opening, len(text)):
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
                if depth == 0:
                    closing = index
                    break
        body = text[match.end():closing]
        fields: dict[str, str] = {}
        cursor = 0
        field_header = re.compile(r"(?m)^\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*")
        while field_match := field_header.search(body, cursor):
            name = field_match.group(1).lower()
            start = field_match.end()
            if start >= len(body):
                break
            if body[start] == "{":
                nested = 0
                end = start + 1
                for end in range(start, len(body)):
                    if body[end] == "{":
                        nested += 1
                    elif body[end] == "}":
                        nested -= 1
                        if nested == 0:
                            break
                value = body[start + 1:end]
                cursor = end + 1
            elif body[start] == '"':
                end = start + 1
                while end < len(body):
                    if body[end] == '"' and body[end - 1] != "\\":
                        break
                    end += 1
                value = body[start + 1:end]
                cursor = end + 1
            else:
                end = body.find(",", start)
                if end == -1:
                    end = len(body)
                value = body[start:end]
                cursor = end + 1
            fields[name] = value.strip()
        entries[key] = BibEntry(key=key, entry_type=entry_type, fields=fields)
        position = closing + 1
    return entries


def parse_methods(path: Path) -> list[Method]:
    methods: list[Method] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = re.sub(r"^\\rowcolor\{[^}]+\}\s*", "", raw.strip())
        if "&" not in line or "\\cite{" not in line:
            continue
        cells = [cell.strip() for cell in line.rsplit("\\\\", 1)[0].split("&")]
        if len(cells) != 10:
            continue
        match = re.search(r"^(.*?)~\\cite\{([^}]+)\}", cells[0])
        if not match:
            continue
        learning = [
            label
            for label, cell in zip(["Training-Free", "SFT", "RL"], cells[4:7])
            if "\\learnstar" in cell
        ]
        supervision = [
            label
            for label, cell in zip(["Trajectory", "Grounding", "Reward"], cells[7:10])
            if "\\datastar" in cell
        ]
        methods.append(
            Method(
                method=clean_latex(match.group(1)),
                key=match.group(2).strip(),
                year=cells[1],
                challenge=cells[2],
                paradigm=cells[3],
                learning=learning,
                supervision=supervision,
            )
        )
    return methods


def normalized(text: str) -> str:
    text = clean_latex(text).lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def match_pdf(entry: BibEntry, pdfs: list[Path]) -> tuple[Path | None, float]:
    title = normalized(entry.title)
    if not title:
        return None, 0.0
    title_tokens = set(title.split())
    best: Path | None = None
    best_score = 0.0
    for pdf in pdfs:
        stem = normalized(pdf.stem)
        stem_tokens = set(stem.split())
        overlap = len(title_tokens & stem_tokens) / max(1, len(title_tokens | stem_tokens))
        sequence = SequenceMatcher(None, title, stem).ratio()
        contains = 1.0 if title in stem or stem in title else 0.0
        score = 0.45 * sequence + 0.45 * overlap + 0.10 * contains
        if score > best_score:
            best, best_score = pdf, score
    return (best, best_score) if best_score >= 0.48 else (None, best_score)


def extract_pdf_links(path: Path) -> list[str]:
    links: set[str] = set()
    try:
        reader = PdfReader(str(path), strict=False)
        for page in reader.pages[:3]:
            for reference in page.get("/Annots") or []:
                try:
                    action = reference.get_object().get("/A")
                    if action and action.get("/URI"):
                        links.add(str(action.get("/URI")))
                except Exception:
                    continue
    except Exception:
        return []
    return sorted(links)


def link_metadata(entries: dict[str, BibEntry], cited_keys: set[str]) -> dict[str, dict[str, str]]:
    pdfs = sorted(PAPER_ROOT.glob("*.pdf"))
    pdf_link_cache: dict[Path, list[str]] = {}
    metadata: dict[str, dict[str, str]] = {}
    for key in cited_keys:
        entry = entries.get(key)
        if not entry:
            continue
        pdf, _ = match_pdf(entry, pdfs)
        urls = []
        if pdf:
            urls = pdf_link_cache.setdefault(pdf, extract_pdf_links(pdf))
        github = next((url for url in urls if "github.com" in url.lower()), "")
        project_candidates = [
            url
            for url in urls
            if not any(
                blocked in url.lower()
                for blocked in [
                    "github.com", "arxiv.org", "doi.org", "openreview.net", "orcid.org",
                    "creativecommons.org", "youtube.com", "youtu.be", "mailto:",
                    "ieee.org", "acm.org", "springer.com", "sciencedirect.com",
                ]
            )
            and url.startswith(("http://", "https://"))
        ]
        project_candidates.sort(
            key=lambda url: (
                0 if ".github.io" in url or "huggingface.co" in url else 1,
                len(url),
            )
        )
        metadata[key] = {
            "arxiv": arxiv_id(entry),
            "web": project_candidates[0] if project_candidates else "",
            "github": github,
            "local_pdf": pdf.name if pdf else "",
        }
    for source in [LINK_CACHE, LINK_OVERRIDES]:
        if not source.exists():
            continue
        cached = json.loads(source.read_text(encoding="utf-8"))
        for key in cited_keys:
            if key not in cached:
                continue
            metadata.setdefault(key, {})
            for field_name in ["arxiv", "web", "github", "local_pdf"]:
                if field_name in cached[key]:
                    metadata[key][field_name] = cached[key][field_name]
    return metadata


def cite_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for group in re.findall(r"\\cite\{([^}]+)\}", text):
        keys.update(key.strip() for key in group.split(",") if key.strip() and key.strip() != "#2")
    return keys


def venue_label(entry: BibEntry, year_override: str | None = None) -> str:
    raw = clean_latex(entry.fields.get("booktitle") or entry.fields.get("journal") or "")
    lowered = raw.lower()
    aliases = [
        ("computer vision and pattern recognition", "CVPR"),
        ("international conference on computer vision", "ICCV"),
        ("european conference on computer vision", "ECCV"),
        ("advances in neural information processing systems", "NeurIPS"),
        ("international conference on machine learning", "ICML"),
        ("international conference on learning representations", "ICLR"),
        ("empirical methods in natural language processing", "EMNLP"),
        ("association for computational linguistics", "ACL"),
        ("acm international conference on multimedia", "ACM MM"),
        ("arxiv", "arXiv"),
    ]
    abbreviations = {
        "cvpr": "CVPR",
        "iccv": "ICCV",
        "eccv": "ECCV",
        "neurips": "NeurIPS",
        "icml": "ICML",
        "iclr": "ICLR",
        "emnlp": "EMNLP",
        "acl": "ACL",
    }
    venue = abbreviations.get(lowered) or next((label for needle, label in aliases if needle in lowered), raw)
    if not venue:
        venue = "arXiv" if arxiv_id(entry) else "-"
    year = year_override or entry.year
    return f"{venue} '{year[-2:]}" if year and venue != "-" else venue


def arxiv_id(entry: BibEntry) -> str:
    eprint = clean_latex(entry.fields.get("eprint", ""))
    if re.fullmatch(r"\d{4}\.\d{4,5}", eprint):
        return eprint
    for value in entry.fields.values():
        match = re.search(r"(?:arXiv:|abs/)(\d{4}\.\d{4,5})", value, re.I)
        if match:
            return match.group(1)
    return ""


def paper_url(entry: BibEntry) -> str:
    identifier = arxiv_id(entry)
    if identifier:
        return f"https://arxiv.org/abs/{identifier}"
    url = clean_latex(entry.fields.get("url", ""))
    if url.startswith(("http://", "https://")):
        return url
    doi = clean_latex(entry.fields.get("doi", ""))
    return f"https://doi.org/{doi}" if doi else ""


def publication_url(entry: BibEntry) -> str:
    url = clean_latex(entry.fields.get("url", ""))
    if url.startswith(("http://", "https://")) and "arxiv.org" not in url.lower():
        return url
    doi = clean_latex(entry.fields.get("doi", ""))
    return f"https://doi.org/{doi}" if doi else ""


def badge(entry: BibEntry) -> str:
    url = paper_url(entry)
    identifier = arxiv_id(entry)
    if identifier:
        image = f"https://img.shields.io/badge/arXiv-{identifier}-b31b1b?style=flat-square&logo=arxiv"
        return f"[![arXiv]({image})]({url})"
    if url:
        image = "https://img.shields.io/badge/Paper-Link-b31b1b?style=flat-square"
        return f"[![Paper]({image})]({url})"
    return ""


def github_badge(url: str) -> str:
    if not url:
        return "-"
    match = re.search(r"github\.com/([^/]+/[^/#?]+)", url, re.I)
    if not match:
        return f"[GitHub]({url})"
    repo = match.group(1).removesuffix(".git")
    return f"[![GitHub](https://img.shields.io/github/stars/{repo}?style=flat-square&logo=github)]({url})"


def arxiv_badge(identifier: str) -> str:
    if not identifier:
        return "-"
    url = f"https://arxiv.org/abs/{identifier}"
    image = f"https://img.shields.io/badge/arXiv-{identifier}-b31b1b?style=flat-square&logo=arxiv"
    return f"[![arXiv]({image})]({url})"


def web_badge(url: str) -> str:
    if not url:
        return "-"
    return f"[![Web](https://img.shields.io/badge/Web-Page-f59e0b?style=flat-square&logo=googlechrome&logoColor=white)]({url})"


def slug(key: str) -> str:
    return "paper-" + re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-")


def row(
    short_name: str,
    key: str,
    entries: dict[str, BibEntry],
    links: dict[str, dict[str, str]],
    tags: list[str] | None = None,
    year_override: str | None = None,
) -> str:
    entry = entries.get(key, BibEntry(key, "misc", {"title": key}))
    anchor = f'<a id="{slug(key)}"></a>'
    tag_html = ""
    if tags:
        tag_html = "<br><sub>" + " · ".join(tags) + "</sub>"
    published = publication_url(entry)
    paper_cell = f"[{entry.title}]({published})" if published else entry.title
    identifier = links.get(key, {}).get("arxiv", "") or arxiv_id(entry)
    web = links.get(key, {}).get("web", "")
    github = github_badge(links.get(key, {}).get("github", ""))
    return f"| {anchor}`{short_name}`{tag_html} | {paper_cell} | {venue_label(entry, year_override)} | {arxiv_badge(identifier)} | {web_badge(web)} | {github} |"


def method_index(methods: list[Method]) -> str:
    return " · ".join(f"[`{method.method}`](#{slug(method.key)})" for method in sorted(methods, key=lambda item: item.method.lower()))


def table_header() -> list[str]:
    return [
        "| Method | Paper | Venue | arXiv | Web | GitHub |",
        "|:-:|:-|:-:|:-:|:-:|:-:|",
    ]


def mark(active: bool) -> str:
    return "✓" if active else "–"


def taxonomy_matrix(methods: list[Method]) -> list[str]:
    lines = [
        "| Method | Year | Challenge | State Space | TF | SFT | RL | Traj. | Ground. | Reward |",
        "|:-|:-:|:-|:-:|:-:|:-:|:-:|:-:|:-:|:-:|",
    ]
    for method in sorted(methods, key=lambda item: (item.year, item.method.lower())):
        linked = f"[`{method.method}`](#{slug(method.key)})"
        paradigm = method.paradigm.replace("Paradigm ", "P-")
        values = [
            mark("Training-Free" in method.learning),
            mark("SFT" in method.learning),
            mark("RL" in method.learning),
            mark("Trajectory" in method.supervision),
            mark("Grounding" in method.supervision),
            mark("Reward" in method.supervision),
        ]
        lines.append(f"| {linked} | {method.year} | {method.challenge} | {paradigm} | " + " | ".join(values) + " |")
    return lines


def build_readme() -> str:
    entries = parse_bibtex(SOURCE_ROOT / "video_understanding_agent_references.bib")
    methods = parse_methods(SOURCE_ROOT / "images" / "method_paper_master_table_main.tex")
    methods += parse_methods(SOURCE_ROOT / "images" / "method_paper_master_table_appendix.tex")

    tex_paths = [
        SOURCE_ROOT / "main.tex",
        SOURCE_ROOT / "Appendix.tex",
        SOURCE_ROOT / "images" / "method_paper_master_table_main.tex",
        SOURCE_ROOT / "images" / "method_paper_master_table_appendix.tex",
    ]
    all_cited: set[str] = set()
    for path in tex_paths:
        all_cited |= cite_keys(path.read_text(encoding="utf-8"))

    background_groups = {
        "Foundational Video Networks": ["tran2015learning", "carreira2017quo", "donahue2015long", "bertasius2021space"],
        "Video Language Models": ["yang2023vid2seq", "ren2024timechat", "song2024moviechat", "huang2024vtimellm"],
        "Related Surveys": ["nguyen2024video", "madan2024foundation", "tang2025video"],
        "Adjacent Agentic Areas": ["wang2024lave", "tu2026spagent"],
    }
    short_names = {
        "tran2015learning": "C3D", "carreira2017quo": "I3D", "donahue2015long": "LRCN",
        "bertasius2021space": "TimeSformer", "yang2023vid2seq": "Vid2Seq", "ren2024timechat": "TimeChat",
        "song2024moviechat": "MovieChat", "huang2024vtimellm": "VTimeLLM", "nguyen2024video": "Video-LLM Survey",
        "madan2024foundation": "Video Foundation Models", "tang2025video": "Video Understanding Survey",
        "wang2024lave": "LAVE", "tu2026spagent": "SPAgent",
    }

    benchmark_names = {
        "gao2017tall": "Charades-STA", "10.1145/3123266.3123427": "MSRVTT-QA",
        "zhou2018towards": "YouCook2", "yu2019activitynet": "ActivityNet-QA", "li2020hero": "How2QA",
        "xiao2021next": "NExT-QA", "mangalam2023egoschema": "EgoSchema", "li2024mvbench": "MVBench",
        "grauman2024ego": "Ego-Exo4D", "zala2023hierarchical": "HiREST", "patraucean2023perception": "Perception Test",
        "ning2025video": "Video-Bench", "wu2024longvideobench": "LongVideoBench", "wang2025lvbench": "LVBench",
        "zhou2025mlvu": "MLVU", "lin2026streamingbench": "StreamingBench", "liu2024tempcompass": "TempCompass",
        "fu2025video": "Video-MME", "fang2024mmbench": "MMBench-Video", "geng2025longvale": "LongVALE",
        "wu2024star": "STAR", "niu2025ovo": "OVO-Bench", "hu2026video": "Video-MMMU",
        "wang2025omnimmi": "OmniMMI", "zhang2025towards": "Video-TT", "yu2026ego2web": "Ego2Web",
        "zhao2026omnipro": "OmniPro", "liu2026watching": "VideoDR",
    }
    agent_benchmarks = {
        "lin2026streamingbench", "niu2025ovo", "wang2025omnimmi",
        "zhao2026omnipro", "yu2026ego2web", "liu2026watching",
    }

    assigned = {method.key for method in methods}
    for keys in background_groups.values():
        assigned.update(keys)
    assigned.update(benchmark_names)
    additional = sorted(all_cited - assigned)
    links = link_metadata(entries, all_cited)

    lines: list[str] = [
        "[![Survey](https://img.shields.io/badge/Survey-Agentic%20Video%20Understanding-0b6b4f?style=flat-square)](#agentic-video-understanding-a-survey)",
        "[![Paper List](https://img.shields.io/badge/Core%20Methods-94-f26b38?style=flat-square)](#1-challenge-to-design-taxonomy)",
        "[![Benchmarks](https://img.shields.io/badge/Benchmarks-28-1d4ed8?style=flat-square)](#5-benchmarks)",
        "[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-8b5cf6?style=flat-square)](#contributing)",
        "",
        "# 🎬 Agentic Video Understanding: A Survey",
        "",
        '| <img width="100%" src="docs/assets/figure1.png" alt="From video networks and Video LLMs to video agents"> |',
        "|:--:|",
        "| **From passive video processing to adaptive action control.** |",
        "",
        "This repository accompanies the survey paper **\"Agentic Video Understanding: A Survey\"** and tracks research on video understanding agents: systems that use video as their primary evidence source and adaptively select actions that change evidence access, internal state, tool use, interaction, or termination.",
        "",
        "The survey traces the transition from recognition-centered video networks and fixed-inference Video LLMs to agents that can inspect video segments, acquire missing evidence, maintain task-relevant state, invoke tools, coordinate specialized roles, and decide when to respond.",
        "",
        "## Contributions",
        "",
        "1. **Definition and scope.** We formally define video understanding agents through adaptive state construction and action selection, distinguishing them from Video LLMs with fixed sampling and one-pass decoding.",
        "2. **Challenge-to-design taxonomy.** We connect context bottlenecks, evidence sparsity, temporal causality, and multimodal ambiguity to the agentic mechanisms required to address them.",
        "3. **State-space taxonomy.** We organize operative video states as a bag of frames, a temporal sequence, a graph of entities, or an evolving world state.",
        "4. **Learning and supervision.** We consolidate training-free control, supervised imitation, reinforcement learning, trajectory supervision, grounding supervision, and preference or reward signals.",
        "5. **Curated field map.** We organize 94 core video-agent methods and 28 representative benchmarks in a consistent, updateable paper list.",
        "",
        "## Citation",
        "",
        "The manuscript is currently anonymized. Please replace the author and venue metadata after public release.",
        "",
        "```bibtex",
        "@article{anonymous2026agenticvideo,",
        "  title   = {Agentic Video Understanding: A Survey},",
        "  author  = {Anonymous Authors},",
        "  journal = {Manuscript},",
        "  year    = {2026}",
        "}",
        "```",
        "",
        "## Table of Contents",
        "",
        "- [**0. Background and Scope**](#0-background-and-scope)",
        "  - [Foundational Video Networks](#foundational-video-networks)",
        "  - [Video Language Models](#video-language-models)",
        "  - [Related Surveys](#related-surveys)",
        "  - [Adjacent Agentic Areas](#adjacent-agentic-areas)",
        "- [**1. Challenge-to-Design Taxonomy**](#1-challenge-to-design-taxonomy)",
        "  - [Context Bottleneck](#context-bottleneck)",
        "  - [Evidence Sparsity](#evidence-sparsity)",
        "  - [Temporal Causality](#temporal-causality)",
        "  - [Multimodal Ambiguity](#multimodal-ambiguity)",
        "- [**2. State-Space Paradigms**](#2-state-space-paradigms)",
        "- [**3. Learning Paradigms**](#3-learning-paradigms)",
        "- [**4. Data and Supervision**](#4-data-and-supervision)",
        "  - [Complete Taxonomy Matrix](#complete-taxonomy-matrix)",
        "- [**5. Benchmarks**](#5-benchmarks)",
        "  - [Capability-Oriented Benchmarks](#capability-oriented-benchmarks)",
        "  - [Agent-Oriented Benchmarks](#agent-oriented-benchmarks)",
        "- [**6. Additional Cited Works**](#6-additional-cited-works)",
        "",
        "# 0. Background and Scope",
        "",
        "A **video understanding agent** uses video as its primary source and solves a task through adaptive evidence-state construction and action selection. It must select at least one action that changes subsequent evidence access, state update, tool use, interaction, or termination.",
        "",
        "> Papers are ordered chronologically within each section. Core video-agent papers appear exactly once under their primary challenge. Orthogonal dimensions are represented through tags and linked indexes rather than duplicated metadata rows.",
    ]

    for heading, keys in background_groups.items():
        lines += ["", f"### {heading}", "", "> In chronological order, from the earliest to the latest.", ""]
        lines += table_header()
        for key in sorted(keys, key=lambda item: (entries.get(item, BibEntry(item, "misc", {})).year, short_names.get(item, item).lower())):
            lines.append(row(short_names.get(key, key), key, entries, links))
        lines += [""]

    challenge_intros = {
        "Context Bottleneck": "Long, streaming, and multi-source videos exceed practical context and compute budgets. Hierarchical evidence memory retains compact, addressable, and provenance-aware video evidence.",
        "Evidence Sparsity": "Answer-critical evidence is often sparse. Active evidence acquisition lets an agent decide where, when, and at what granularity to inspect video.",
        "Temporal Causality": "Video is an ordered record of change. State and process tracking preserve transitions, causal dependencies, and response readiness.",
        "Multimodal Ambiguity": "Vision, speech, audio, OCR, motion, and interaction cues may conflict. Role-specialized coordination separates and reconciles heterogeneous evidence.",
    }
    lines += ["", "# 1. Challenge-to-Design Taxonomy", "", "The primary paper catalog uses the survey's challenge-to-design taxonomy. Each core method has one canonical placement; paradigm, learning, and supervision dimensions are shown as tags."]
    for challenge in ["Context Bottleneck", "Evidence Sparsity", "Temporal Causality", "Multimodal Ambiguity"]:
        subset = [method for method in methods if method.challenge == challenge]
        lines += ["", f"### {challenge}", "", challenge_intros[challenge], "", "> In chronological order, from the earliest to the latest.", ""]
        lines += table_header()
        for method in sorted(subset, key=lambda item: (item.year, item.method.lower())):
            tags = [method.paradigm.replace("Paradigm ", "P-")]
            tags += method.learning or ["Unspecified learning"]
            tags += [f"{signal} supervision" for signal in method.supervision]
            lines.append(row(method.method, method.key, entries, links, tags, method.year))
        lines += [""]

    paradigm_descriptions = {
        "Paradigm I": ("Paradigm I: Video as a Bag of Frames", "Selected frames, keyframes, clips, shots, or candidate segments serve as discrete evidence units."),
        "Paradigm II": ("Paradigm II: Video as a Temporal Sequence", "The operative state preserves ordering and temporal relations among observations."),
        "Paradigm III": ("Paradigm III: Video as a Graph of Entities", "Persistent entities and evidence links support long-range association and multimodal retrieval."),
        "Paradigm IV": ("Paradigm IV: Video as an Evolving World State", "A partial, time-indexed state is revised as observations arrive and future evidence remains unavailable."),
    }
    lines += [
        "", "# 2. State-Space Paradigms", "",
        "The four paradigms describe the operative state exposed to the agent. The complete method-level assignments appear once in the taxonomy matrix below.", "",
        "| Code | State-space view | Operational meaning | Methods |",
        "|:-:|:-|:-|:-:|",
    ]
    for paradigm, (heading, description) in paradigm_descriptions.items():
        subset = [method for method in methods if method.paradigm == paradigm]
        lines.append(f"| **{paradigm.replace('Paradigm ', 'P-')}** | {heading.split(': ', 1)[1]} | {description} | **{len(subset)}** |")

    learning_descriptions = {
        "Training-Free": ("Training-Free and Inference-Time Control", "Prompts, tools, retrieval procedures, memory rules, verification, waiting, and stopping criteria specify agent behavior at inference time."),
        "SFT": ("Supervised Fine-Tuning and Imitation Learning", "Answer labels, component objectives, or demonstrated trajectories supervise agent decisions."),
        "RL": ("Reinforcement Learning", "Outcome and process rewards optimize evidence acquisition, grounding, efficiency, timing, or reasoning validity."),
    }
    lines += [
        "", "# 3. Learning Paradigms", "",
        "Learning regimes are multi-label: one method may combine supervised initialization, reinforcement learning, and inference-time control.", "",
        "| Code | Learning regime | What is optimized or specified | Methods |",
        "|:-:|:-|:-|:-:|",
    ]
    for label, (heading, description) in learning_descriptions.items():
        subset = [method for method in methods if label in method.learning]
        lines.append(f"| **{label}** | {heading} | {description} | **{len(subset)}** |")

    supervision_descriptions = {
        "Trajectory": ("Trajectory Supervision", "Step-by-step observations, tool calls, state changes, revisions, failures, and stopping decisions."),
        "Grounding": ("Grounding Supervision", "Temporal intervals, regions, tracks, entities, audio cues, OCR spans, and state changes that support a claim."),
        "Reward": ("Preference and Reward Supervision", "Comparative or scalar signals over evidence choice, reasoning quality, response timing, or complete rollouts."),
    }
    lines += [
        "", "# 4. Data and Supervision", "",
        "The former Appendix material is promoted here as a first-class part of the taxonomy. Supervision signals are also multi-label.", "",
        "| Code | Supervision signal | What the signal contains | Methods |",
        "|:-:|:-|:-|:-:|",
    ]
    for label, (heading, description) in supervision_descriptions.items():
        subset = [method for method in methods if label in method.supervision]
        lines.append(f"| **{label}** | {heading} | {description} | **{len(subset)}** |")
    lines += [
        "", "### Complete Taxonomy Matrix", "",
        "Each method appears here as a compact linked index. Click a method name to jump to its unique paper record in the Challenge-to-Design catalog.", "",
        "**Legend:** TF = training-free control; SFT = supervised fine-tuning; RL = reinforcement learning; Traj. = trajectory supervision; Ground. = grounding supervision.", "",
    ]
    lines += taxonomy_matrix(methods)

    capability = [key for key in benchmark_names if key not in agent_benchmarks]
    agent = [key for key in benchmark_names if key in agent_benchmarks]
    lines += ["", "# 5. Benchmarks", "", "Benchmarks are grouped by their primary role in agentic video understanding."]
    for heading, keys in [("Capability-Oriented Benchmarks", capability), ("Agent-Oriented Benchmarks", agent)]:
        lines += ["", f"### {heading}", "", "> In chronological order, from the earliest to the latest.", ""]
        lines += table_header()
        for key in sorted(keys, key=lambda item: (entries.get(item, BibEntry(item, "misc", {})).year, benchmark_names[item].lower())):
            lines.append(row(benchmark_names[key], key, entries, links))
        lines += [""]

    lines += ["", "# 6. Additional Cited Works", "", "The following cited works are not part of the 94-row core method table or the benchmark catalog, but are discussed in the survey's scope, learning, or supervision sections.", ""]
    lines += table_header()
    for key in sorted(additional, key=lambda item: (entries.get(item, BibEntry(item, "misc", {})).year, entries.get(item, BibEntry(item, "misc", {"title": item})).title.lower())):
        title = entries.get(key, BibEntry(key, "misc", {"title": key})).title
        short = title.split(":", 1)[0][:48]
        lines.append(row(short, key, entries, links))
    lines += ["", "## Contributing", "", "Contributions are welcome. For a new paper, please include:", "", "- title, venue, year, and stable paper URL;", "- arXiv link, project page, and GitHub repository when available;", "- one primary challenge and one state-space paradigm;", "- all applicable learning regimes and supervision signals;", "- one sentence explaining why the method satisfies the survey's agent definition.", "", "<div align=\"center\">", "", "**[⬆ Back to Top](#agentic-video-understanding-a-survey)**", "", "*Generated from the survey LaTeX tables and BibTeX source.*", "", "</div>", ""]

    return "\n".join(lines)


if __name__ == "__main__":
    output = build_readme()
    target = REPO_ROOT / "README.md"
    target.write_text(output, encoding="utf-8", newline="\n")
    print(f"Wrote {target} ({len(output.splitlines())} lines)")
