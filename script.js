const papers = [
  {
    method: "WorldMM",
    title: "Dynamic Multimodal Memory Agent for Long Video Reasoning",
    year: 2026,
    challenge: "context",
    paradigm: "Graph of entities",
    learning: "Training-free",
    url: "https://arxiv.org/abs/2512.02425"
  },
  {
    method: "VideoARM",
    title: "Agentic Reasoning over Hierarchical Memory for Long-Form Video Understanding",
    year: 2026,
    challenge: "context",
    paradigm: "Graph of entities",
    learning: "Training-free",
    url: ""
  },
  {
    method: "HAVEN",
    title: "Hierarchical Long Video Understanding with Audiovisual Entity Cohesion and Agentic Search",
    year: 2026,
    challenge: "context",
    paradigm: "Graph of entities",
    learning: "Training-free",
    url: "https://arxiv.org/abs/2601.13719"
  },
  {
    method: "StreamMeCo",
    title: "Long-Term Agent Memory Compression for Efficient Streaming Video Understanding",
    year: 2026,
    challenge: "context",
    paradigm: "Graph of entities",
    learning: "Training-free",
    url: "https://arxiv.org/abs/2604.09000"
  },
  {
    method: "VideoExplorer",
    title: "Think With Videos for Agentic Long-Video Understanding",
    year: 2025,
    challenge: "evidence",
    paradigm: "Graph of entities",
    learning: "SFT + RL",
    url: "https://arxiv.org/abs/2506.10821"
  },
  {
    method: "FrameThinker",
    title: "Learning to Think with Long Videos via Multi-Turn Frame Spotlighting",
    year: 2025,
    challenge: "evidence",
    paradigm: "Bag of frames",
    learning: "SFT + RL",
    url: "https://arxiv.org/abs/2509.24304"
  },
  {
    method: "ReWatch-R1",
    title: "Boosting Complex Video Reasoning through Agentic Data Synthesis",
    year: 2025,
    challenge: "evidence",
    paradigm: "Temporal sequence",
    learning: "SFT + RL",
    url: "https://arxiv.org/abs/2509.23652"
  },
  {
    method: "VideoSeek",
    title: "Long-Horizon Video Agent with Tool-Guided Seeking",
    year: 2026,
    challenge: "evidence",
    paradigm: "Temporal sequence",
    learning: "Training-free",
    url: ""
  },
  {
    method: "VideoMind",
    title: "A Chain-of-LoRA Agent for Temporal-Grounded Video Reasoning",
    year: 2026,
    challenge: "temporal",
    paradigm: "Temporal sequence",
    learning: "SFT",
    url: "https://arxiv.org/abs/2503.13444"
  },
  {
    method: "ThinkStream",
    title: "Thinking in Streaming Video",
    year: 2026,
    challenge: "temporal",
    paradigm: "Evolving world state",
    learning: "RL",
    url: "https://arxiv.org/abs/2603.12938"
  },
  {
    method: "StreamAgent",
    title: "Towards Anticipatory Agents for Streaming Video Understanding",
    year: 2025,
    challenge: "temporal",
    paradigm: "Evolving world state",
    learning: "SFT",
    url: "https://arxiv.org/abs/2508.01875"
  },
  {
    method: "AViLA",
    title: "Asynchronous Vision-Language Agent for Streaming Multimodal Data Interaction",
    year: 2025,
    challenge: "temporal",
    paradigm: "Evolving world state",
    learning: "Training-free",
    url: "https://arxiv.org/abs/2506.18472"
  },
  {
    method: "MAGNET",
    title: "Finding Audio-Visual Needles by Reasoning over Multi-Video Haystacks",
    year: 2025,
    challenge: "multimodal",
    paradigm: "Graph of entities",
    learning: "Training-free",
    url: "https://arxiv.org/abs/2506.07016"
  },
  {
    method: "SciEducator",
    title: "Scientific Video Understanding and Educating via Deming-Cycle Multi-Agent System",
    year: 2025,
    challenge: "multimodal",
    paradigm: "Graph of entities",
    learning: "Training-free",
    url: "https://arxiv.org/abs/2511.17943"
  },
  {
    method: "Symphony",
    title: "A Cognitively-Inspired Multi-Agent System for Long-Video Understanding",
    year: 2026,
    challenge: "multimodal",
    paradigm: "Temporal sequence",
    learning: "Training-free",
    url: ""
  },
  {
    method: "VideoChat-M1",
    title: "Collaborative Policy Planning via Multi-Agent Reinforcement Learning",
    year: 2026,
    challenge: "multimodal",
    paradigm: "Temporal sequence",
    learning: "RL",
    url: ""
  }
];

const challengeLabels = {
  context: "Context bottleneck",
  evidence: "Evidence sparsity",
  temporal: "Temporal causality",
  multimodal: "Multimodal ambiguity"
};

const paperGrid = document.querySelector("#paper-grid");
const paperSearch = document.querySelector("#paper-search");
const paperCount = document.querySelector("#paper-count");
const emptyState = document.querySelector("#empty-state");
const filterButtons = [...document.querySelectorAll(".filter-button")];
let activeFilter = "all";

function paperCard(paper) {
  const link = paper.url
    ? `<a class="paper-link" href="${paper.url}" target="_blank" rel="noreferrer" aria-label="Open ${paper.method} paper">
        <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 15 15 5M7 5h8v8"/></svg>
      </a>`
    : `<span class="paper-link disabled" title="Public link pending" aria-label="Public link pending">—</span>`;

  return `<article class="paper-card">
    <div>
      <div class="paper-card-top">
        <span class="paper-year">${paper.year}</span>
        <span class="paper-challenge ${paper.challenge}">${challengeLabels[paper.challenge]}</span>
      </div>
      <h3>${paper.method}</h3>
      <p>${paper.title}</p>
      <div class="paper-meta">
        <span>${paper.paradigm}</span>
        <span>${paper.learning}</span>
      </div>
    </div>
    ${link}
  </article>`;
}

function renderPapers() {
  const query = paperSearch.value.trim().toLowerCase();
  const filtered = papers.filter((paper) => {
    const matchesFilter = activeFilter === "all" || paper.challenge === activeFilter;
    const searchable = `${paper.method} ${paper.title} ${paper.paradigm} ${paper.learning} ${challengeLabels[paper.challenge]}`.toLowerCase();
    return matchesFilter && searchable.includes(query);
  });

  paperGrid.innerHTML = filtered.map(paperCard).join("");
  paperCount.textContent = `${filtered.length} ${filtered.length === 1 ? "paper" : "papers"}`;
  emptyState.hidden = filtered.length !== 0;
}

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    activeFilter = button.dataset.filter;
    filterButtons.forEach((item) => item.classList.toggle("active", item === button));
    renderPapers();
  });
});

paperSearch.addEventListener("input", renderPapers);
renderPapers();

const header = document.querySelector(".site-header");
const menuButton = document.querySelector(".menu-button");
const siteNav = document.querySelector(".site-nav");

function updateHeader() {
  header.classList.toggle("scrolled", window.scrollY > 18);
  if (window.scrollY < 320) {
    siteNav.querySelectorAll("a.active").forEach((link) => link.classList.remove("active"));
  }
}

updateHeader();
window.addEventListener("scroll", updateHeader, { passive: true });

menuButton.addEventListener("click", () => {
  const nextState = menuButton.getAttribute("aria-expanded") !== "true";
  menuButton.setAttribute("aria-expanded", String(nextState));
  siteNav.classList.toggle("open", nextState);
  document.body.classList.toggle("menu-open", nextState);
});

siteNav.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    menuButton.setAttribute("aria-expanded", "false");
    siteNav.classList.remove("open");
    document.body.classList.remove("menu-open");
  });
});

const revealObserver = new IntersectionObserver(
  (entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
);

document.querySelectorAll(".reveal").forEach((element) => revealObserver.observe(element));

const navLinks = [...siteNav.querySelectorAll('a[href^="#"]')];
const trackedSections = navLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

const sectionObserver = new IntersectionObserver(
  (entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!visible) return;
    navLinks.forEach((link) => {
      link.classList.toggle("active", link.getAttribute("href") === `#${visible.target.id}`);
    });
  },
  { rootMargin: "-20% 0px -68% 0px", threshold: [0.05, 0.25, 0.6] }
);

trackedSections.forEach((section) => sectionObserver.observe(section));

const copyButton = document.querySelector("#copy-citation");
copyButton.addEventListener("click", async () => {
  const citation = document.querySelector("#citation-code").textContent;
  try {
    await navigator.clipboard.writeText(citation);
    copyButton.textContent = "Copied";
    window.setTimeout(() => {
      copyButton.textContent = "Copy";
    }, 1600);
  } catch {
    copyButton.textContent = "Select text";
  }
});
