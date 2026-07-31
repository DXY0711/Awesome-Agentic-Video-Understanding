[![Survey](https://img.shields.io/badge/Survey-Agentic%20Video%20Understanding-0b6b4f?style=flat-square)](#agentic-video-understanding-a-survey)
[![Paper List](https://img.shields.io/badge/Core%20Methods-94-f26b38?style=flat-square)](#1-challenge-to-design-taxonomy)
[![Benchmarks](https://img.shields.io/badge/Benchmarks-28-1d4ed8?style=flat-square)](#5-benchmarks)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-8b5cf6?style=flat-square)](#contributing)

# 🎬 Agentic Video Understanding: A Survey

| <img width="100%" src="docs/assets/figure1.png" alt="From video networks and Video LLMs to video agents"> |
|:--:|
| **From passive video processing to adaptive action control.** |

This repository accompanies the survey paper **"Agentic Video Understanding: A Survey"** and tracks research on video understanding agents: systems that use video as their primary evidence source and adaptively select actions that change evidence access, internal state, tool use, interaction, or termination.

The survey traces the transition from recognition-centered video networks and fixed-inference Video LLMs to agents that can inspect video segments, acquire missing evidence, maintain task-relevant state, invoke tools, coordinate specialized roles, and decide when to respond.

## Contributions

1. **Definition and scope.** We formally define video understanding agents through adaptive state construction and action selection, distinguishing them from Video LLMs with fixed sampling and one-pass decoding.
2. **Challenge-to-design taxonomy.** We connect context bottlenecks, evidence sparsity, temporal causality, and multimodal ambiguity to the agentic mechanisms required to address them.
3. **State-space taxonomy.** We organize operative video states as a bag of frames, a temporal sequence, a graph of entities, or an evolving world state.
4. **Learning and supervision.** We consolidate training-free control, supervised imitation, reinforcement learning, trajectory supervision, grounding supervision, and preference or reward signals.
5. **Curated field map.** We organize 94 core video-agent methods and 28 representative benchmarks in a consistent, updateable paper list.

## Citation

The manuscript is currently anonymized. Please replace the author and venue metadata after public release.

```bibtex
@article{anonymous2026agenticvideo,
  title   = {Agentic Video Understanding: A Survey},
  author  = {Anonymous Authors},
  journal = {Manuscript},
  year    = {2026}
}
```

## Table of Contents

- [**0. Background and Scope**](#0-background-and-scope)
  - [Foundational Video Networks](#foundational-video-networks)
  - [Video Language Models](#video-language-models)
  - [Related Surveys](#related-surveys)
  - [Adjacent Agentic Areas](#adjacent-agentic-areas)
- [**1. Challenge-to-Design Taxonomy**](#1-challenge-to-design-taxonomy)
  - [Context Bottleneck](#context-bottleneck)
  - [Evidence Sparsity](#evidence-sparsity)
  - [Temporal Causality](#temporal-causality)
  - [Multimodal Ambiguity](#multimodal-ambiguity)
- [**2. State-Space Paradigms**](#2-state-space-paradigms)
  - [Video as a Bag of Frames](#paradigm-i-video-as-a-bag-of-frames)
  - [Video as a Temporal Sequence](#paradigm-ii-video-as-a-temporal-sequence)
  - [Video as a Graph of Entities](#paradigm-iii-video-as-a-graph-of-entities)
  - [Video as an Evolving World State](#paradigm-iv-video-as-an-evolving-world-state)
- [**3. Learning Paradigms**](#3-learning-paradigms)
  - [Training-Free and Inference-Time Control](#training-free-and-inference-time-control)
  - [Supervised Fine-Tuning and Imitation Learning](#supervised-fine-tuning-and-imitation-learning)
  - [Reinforcement Learning](#reinforcement-learning)
- [**4. Data and Supervision**](#4-data-and-supervision)
  - [Trajectory Supervision](#trajectory-supervision)
  - [Grounding Supervision](#grounding-supervision)
  - [Preference and Reward Supervision](#preference-and-reward-supervision)
- [**5. Benchmarks**](#5-benchmarks)
  - [Capability-Oriented Benchmarks](#capability-oriented-benchmarks)
  - [Agent-Oriented Benchmarks](#agent-oriented-benchmarks)
- [**6. Additional Cited Works**](#6-additional-cited-works)

# 0. Background and Scope

A **video understanding agent** uses video as its primary source and solves a task through adaptive evidence-state construction and action selection. It must select at least one action that changes subsequent evidence access, state update, tool use, interaction, or termination.

> Papers are ordered chronologically within each section. Core video-agent papers appear exactly once under their primary challenge. Orthogonal dimensions are represented through tags and linked indexes rather than duplicated metadata rows.

### Foundational Video Networks

> In chronological order, from the earliest to the latest.

| Model | Paper | Venue | Website | GitHub |
|:-:|:-|:-:|:-:|:-:|
||
| <a id="paper-tran2015learning"></a>`C3D` | Learning spatiotemporal features with 3d convolutional networks | ICCV '15 | - | - |
| <a id="paper-donahue2015long"></a>`LRCN` | Long-term recurrent convolutional networks for visual recognition and description | CVPR '15 | - | - |
| <a id="paper-carreira2017quo"></a>`I3D` | Quo vadis, action recognition? a new model and the kinetics dataset | CVPR '17 | - | - |
| <a id="paper-bertasius2021space"></a>`TimeSformer` | Is space-time attention all you need for video understanding? | ICML '21 | - | - |
||

### Video Language Models

> In chronological order, from the earliest to the latest.

| Model | Paper | Venue | Website | GitHub |
|:-:|:-|:-:|:-:|:-:|
||
| <a id="paper-yang2023vid2seq"></a>`Vid2Seq` | Vid2seq: Large-scale pretraining of a visual language model for dense video captioning | CVPR '23 | - | - |
| <a id="paper-song2024moviechat"></a>`MovieChat` | Moviechat: From dense token to sparse memory for long video understanding | CVPR '24 | - | - |
| <a id="paper-ren2024timechat"></a>`TimeChat` | Timechat: A time-sensitive multimodal large language model for long video understanding | CVPR '24 | - | - |
| <a id="paper-huang2024vtimellm"></a>`VTimeLLM` | Vtimellm: Empower llm to grasp video moments | CVPR '24 | - | - |
||

### Related Surveys

> In chronological order, from the earliest to the latest.

| Model | Paper | Venue | Website | GitHub |
|:-:|:-|:-:|:-:|:-:|
||
| <a id="paper-madan2024foundation"></a>`Video Foundation Models` | [![arXiv](https://img.shields.io/badge/arXiv-2405.03770-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2405.03770)<br>Foundation models for video understanding: A survey | arXiv '24 | - | - |
| <a id="paper-nguyen2024video"></a>`Video-LLM Survey` | Video-language understanding: A survey from model architecture, model training, and data perspectives | ACL '24 | - | - |
| <a id="paper-tang2025video"></a>`Video Understanding Survey` | Video understanding with large language models: A survey | IEEE Transactions on Circuits and Systems for Video Technology '25 | - | - |
||

### Adjacent Agentic Areas

> In chronological order, from the earliest to the latest.

| Model | Paper | Venue | Website | GitHub |
|:-:|:-|:-:|:-:|:-:|
||
| <a id="paper-wang2024lave"></a>`LAVE` | Lave: Llm-powered agent assistance and language augmentation for video editing | Proceedings of the 29th International Conference on Intelligent User Interfaces '24 | - | - |
| <a id="paper-tu2026spagent"></a>`SPAgent` | Spagent: Adaptive task decomposition and model selection for general video generation and editing | IEEE Transactions on Image Processing '26 | - | - |
||

# 1. Challenge-to-Design Taxonomy

The primary paper catalog uses the survey's challenge-to-design taxonomy. Each core method has one canonical placement; paradigm, learning, and supervision dimensions are shown as tags.

### Context Bottleneck

Long, streaming, and multi-source videos exceed practical context and compute budgets. Hierarchical evidence memory retains compact, addressable, and provenance-aware video evidence.

> In chronological order, from the earliest to the latest.

| Model | Paper | Venue | Website | GitHub |
|:-:|:-|:-:|:-:|:-:|
||
| <a id="paper-fan2024videoagent"></a>`VideoAgent (Fan et al.)`<br><sub>P-III · Training-Free</sub> | Videoagent: A memory-augmented multimodal agent for video understanding | ECCV '24 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://videoagent.github.io) | - |
| <a id="paper-qian2024streaming"></a>`VideoStreaming`<br><sub>P-IV · SFT · Grounding supervision</sub> | Streaming long video understanding with large language models | NeurIPS '24 | - | - |
| <a id="paper-zhang2026adavideorag"></a>`AdaVideoRAG`<br><sub>P-III · Training-Free</sub> | AdaVideoRAG: Omni-Contextual Adaptive Retrieval-Augmented Efficient Long Video Understanding | NeurIPS '25 | - | [![GitHub](https://img.shields.io/github/stars/xzc-zju/AdaVideoRAG?style=flat-square&logo=github)](https://github.com/xzc-zju/AdaVideoRAG) |
| <a id="paper-gao2025agentic"></a>`AVI`<br><sub>P-III · Training-Free</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2511.14446-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2511.14446)<br>Agentic Video Intelligence: A Flexible Framework for Advanced Video Exploration and Understanding | arXiv '25 | - | - |
| <a id="paper-ma2025drvideo"></a>`DrVideo`<br><sub>P-III · Training-Free</sub> | Drvideo: Document retrieval based long video understanding | CVPR '25 | - | - |
| <a id="paper-zhang2025flash"></a>`Flash-VStream`<br><sub>P-III · Unspecified learning</sub> | Flash-vstream: Efficient real-time understanding for long video streams | ICCV '25 | - | - |
| <a id="paper-long2025seeing"></a>`M3-Agent`<br><sub>P-III · SFT · RL · Grounding supervision · Reward supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2508.09736-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2508.09736)<br>Seeing, listening, remembering, and reasoning: A multimodal agent with long-term memory | arXiv '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://m3-agent.github.io) | [![GitHub](https://img.shields.io/github/stars/bytedance-seed/m3-agent?style=flat-square&logo=github)](https://github.com/bytedance-seed/m3-agent) |
| <a id="paper-pang2025mr"></a>`Mr. Video`<br><sub>P-III · Training-Free</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2504.16082-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2504.16082)<br>Mr. video:" mapreduce" is the principle for long video understanding | arXiv '25 | - | [![GitHub](https://img.shields.io/github/stars/ziqipang/MR-Video?style=flat-square&logo=github)](https://github.com/ziqipang/MR-Video) |
| <a id="paper-chatterjee2025memory"></a>`ProVideLLM`<br><sub>P-IV · Unspecified learning</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2504.13915-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2504.13915)<br>Memory-efficient streaming videollms for real-time procedural video understanding | arXiv '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://dibschat.github.io/ProVideLLM) | - |
| <a id="paper-di2025streaming"></a>`ReKV`<br><sub>P-III · Unspecified learning</sub> | Streaming video question-answering with in-context video kv-cache retrieval | ICLR '25 | - | - |
| <a id="paper-xiong2025streaming"></a>`StreamChat`<br><sub>P-III · Training-Free</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2501.13468-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2501.13468)<br>Streaming video understanding and multi-round interaction with memory-enhanced knowledge | arXiv '25 | - | [![GitHub](https://img.shields.io/github/stars/hmxiong/StreamChat?style=flat-square&logo=github)](https://github.com/hmxiong/StreamChat) |
| <a id="paper-luo2026video"></a>`Video-RAG`<br><sub>P-III · Training-Free</sub> | Video-rag: Visually-aligned retrieval-augmented long video comprehension | NeurIPS '25 | - | [![GitHub](https://img.shields.io/github/stars/Leon1207/Video-RAG-master?style=flat-square&logo=github)](https://github.com/Leon1207/Video-RAG-master) |
| <a id="paper-wang2025videollamb"></a>`VideoLLaMB`<br><sub>P-III · Unspecified learning</sub> | Videollamb: Long streaming video understanding with recurrent memory bridges | ICCV '25 | - | [![GitHub](https://img.shields.io/github/stars/bigai-nlco/VideoLLaMB?style=flat-square&logo=github)](https://github.com/bigai-nlco/VideoLLaMB) |
| <a id="paper-zuo2026videolucy"></a>`VideoLucy`<br><sub>P-III · Training-Free</sub> | Videolucy: Deep memory backtracking for long video understanding | NeurIPS '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://videolucy.github.io/) | - |
| <a id="paper-yang2026graph"></a>`G2F-RAG`<br><sub>P-III · Training-Free</sub> | Graph-to-Frame RAG: Visual-Space Knowledge Fusion for Training-Free and Auditable Video Reasoning | CVPR '26 | - | - |
| <a id="paper-yin2026hierarchical"></a>`HAVEN`<br><sub>P-III · Training-Free</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2601.13719-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2601.13719)<br>Hierarchical Long Video Understanding with Audiovisual Entity Cohesion and Agentic Search | arXiv '26 | - | - |
| <a id="paper-liu2026efficient"></a>`R3-Streaming`<br><sub>P-IV · RL · Reward supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2605.17921-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2605.17921)<br>An Efficient Streaming Video Understanding Framework with Agentic Control | arXiv '26 | - | - |
| <a id="paper-wang2026streammeco"></a>`StreamMeCo`<br><sub>P-III · Training-Free</sub> | Streammeco: Long-term agent memory compression for efficient streaming video understanding | ACL '26 | - | - |
| <a id="paper-xie2026streamrag"></a>`StreamRAG`<br><sub>P-III · Training-Free</sub> | StreamRAG: Enhancing Real-Time Video Understanding with Retrieval Augmentation | CVPR '26 | - | - |
| <a id="paper-yin2026videoarm"></a>`VideoARM`<br><sub>P-III · Training-Free</sub> | Videoarm: Agentic reasoning over hierarchical memory for long-form video understanding | CVPR '26 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://milvlg.github.io/videoarm/) | - |
| <a id="paper-yeo2026worldmm"></a>`WorldMM`<br><sub>P-III · Training-Free</sub> | Worldmm: Dynamic multimodal memory agent for long video reasoning | CVPR '26 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://worldmm.github.io) | - |
||

### Evidence Sparsity

Answer-critical evidence is often sparse. Active evidence acquisition lets an agent decide where, when, and at what granularity to inspect video.

> In chronological order, from the earliest to the latest.

| Model | Paper | Venue | Website | GitHub |
|:-:|:-|:-:|:-:|:-:|
||
| <a id="paper-zhang2024omagent"></a>`OmAgent`<br><sub>P-III · Training-Free</sub> | Omagent: A multi-modal agent framework for complex video understanding with task divide-and-conquer | EMNLP '24 | - | [![GitHub](https://img.shields.io/github/stars/om-ai-lab/OmAgent?style=flat-square&logo=github)](https://github.com/om-ai-lab/OmAgent) |
| <a id="paper-kim2025salova"></a>`SALOVA`<br><sub>P-I · Unspecified learning</sub> | Salova: Segment-augmented long video assistant for targeted retrieval and routing in long-form video analysis | CVPR '24 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://ivy-lvlm.github.io/SALOVA/) | - |
| <a id="paper-nie2024slowfocus"></a>`SlowFocus`<br><sub>P-II · Unspecified learning</sub> | Slowfocus: Enhancing fine-grained temporal understanding in video llm | NeurIPS '24 | - | [![GitHub](https://img.shields.io/github/stars/fudan-zvg/SlowFocus?style=flat-square&logo=github)](https://github.com/fudan-zvg/SlowFocus) |
| <a id="paper-wang2024videoagent"></a>`VideoAgent (Wang et al.)`<br><sub>P-II · Training-Free</sub> | Videoagent: Long-form video understanding with large language model as agent | ECCV '24 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://wxh1996.github.io/VideoAgent-Website/) | - |
| <a id="paper-shi2025enhancing"></a>`AoTD`<br><sub>P-II · SFT · Trajectory supervision</sub> | Enhancing video-llm reasoning via agent-of-thoughts distillation | CVPR '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://zhengrongz.github.io/AoTD/) | - |
| <a id="paper-liu2025commonsense"></a>`Commonsense Video QA`<br><sub>P-II · Training-Free · Grounding supervision</sub> | Commonsense video question answering through video-grounded entailment tree reasoning | CVPR '25 | - | - |
| <a id="paper-zhang2026deep"></a>`DVD`<br><sub>P-III · Training-Free</sub> | Deep video discovery: Agentic search with tool use for long-form video understanding | NeurIPS '25 | - | [![GitHub](https://img.shields.io/github/stars/microsoft/DeepVideoDiscovery?style=flat-square&logo=github)](https://github.com/microsoft/DeepVideoDiscovery) |
| <a id="paper-liu2025flow4agent"></a>`Flow4Agent`<br><sub>P-I · Unspecified learning</sub> | Flow4agent: Long-form video understanding via motion prior from optical flow | ICCV '25 | - | - |
| <a id="paper-he2025framethinker"></a>`FrameThinker`<br><sub>P-I · SFT · RL · Trajectory supervision · Reward supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2509.24304-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2509.24304)<br>Framethinker: Learning to think with long videos via multi-turn frame spotlighting | arXiv '25 | - | [![GitHub](https://img.shields.io/github/stars/lcqysl/FrameThinker-RL?style=flat-square&logo=github)](https://github.com/lcqysl/FrameThinker-RL) |
| <a id="paper-yang2026longvt"></a>`LongVT`<br><sub>P-II · SFT · RL · Reward supervision</sub> | Longvt: Incentivizing" thinking with long videos" via native tool calling | CVPR '25 | - | - |
| <a id="paper-lvagent2025"></a>`LVAgent`<br><sub>P-I · Training-Free</sub> | Lvagent: Long video understanding by multi-round dynamical collaboration of mllm agents | ICCV '25 | - | - |
| <a id="paper-song2025modularized"></a>`MSR-ViR`<br><sub>P-II · SFT · RL · Grounding supervision · Reward supervision</sub> | Modularized self-reflected video reasoner for multimodal llm with application to video question answering | ICML '25 | - | - |
| <a id="paper-reagentv2025"></a>`ReAgent-V`<br><sub>P-I · RL · Reward supervision</sub> | Reagent-v: A reward-driven multi-agent framework for video understanding | NeurIPS '25 | - | [![GitHub](https://img.shields.io/github/stars/aiming-lab/ReAgent-V?style=flat-square&logo=github)](https://github.com/aiming-lab/ReAgent-V) |
| <a id="paper-li2026select"></a>`Select Less, Reason More`<br><sub>P-I · RL · Grounding supervision · Reward supervision</sub> | Select less, reason more: Prioritizing evidence purity for video reasoning | CVPR '25 | - | - |
| <a id="paper-zhang2026thinking"></a>`Thinking with Videos`<br><sub>P-II · RL · Reward supervision</sub> | Thinking with videos: Multimodal tool-augmented reinforcement learning for long video reasoning | CVPR '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://zhang9302002.github.io/thinkingwithvideos-page/) | - |
| <a id="paper-yang2025vca"></a>`VCA`<br><sub>P-II · Training-Free</sub> | Vca: Video curious agent for long video understanding | ICCV '25 | - | - |
| <a id="paper-zhi2025videoagent2"></a>`VideoAgent2`<br><sub>P-II · Training-Free</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2504.04471-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2504.04471)<br>Videoagent2: Enhancing the llm-based agent system for long-form video understanding by uncertainty-aware cot | arXiv '25 | - | - |
| <a id="paper-yuan2025videoexplorer"></a>`VideoExplorer`<br><sub>P-III · SFT · RL · Trajectory supervision · Reward supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2506.10821-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2506.10821)<br>VideoExplorer: Think With Videos For Agentic Long-Video Understanding | arXiv '25 | - | - |
| <a id="paper-a4vl2026"></a>`A4VL`<br><sub>P-I · Training-Free</sub> | A Multi-Agent Perception-Action Alliance for Efficient Long Video Reasoning | CVPR '26 | - | [![GitHub](https://img.shields.io/github/stars/git-disl/A4VL?style=flat-square&logo=github)](https://github.com/git-disl/A4VL) |
| <a id="paper-du2026appo"></a>`APPO`<br><sub>P-I · RL · Reward supervision</sub> | APPO: Attention-guided Perception Policy Optimization for Video Reasoning | CVPR '26 | - | - |
| <a id="paper-zhang2026eva"></a>`EVA`<br><sub>P-I · SFT · RL · Reward supervision</sub> | EVA: Efficient Reinforcement Learning for End-to-End Video Agent | CVPR '26 | - | [![GitHub](https://img.shields.io/github/stars/wangruohui/EfficientVideoAgent?style=flat-square&logo=github)](https://github.com/wangruohui/EfficientVideoAgent) |
| <a id="paper-li2026lenswalk"></a>`LensWalk`<br><sub>P-II · Training-Free</sub> | LensWalk: Agentic video understanding by planning how you see in videos | CVPR '26 | - | - |
| <a id="paper-qiu2026longvideo"></a>`LongVideo-R1`<br><sub>P-II · SFT · RL · Reward supervision</sub> | Longvideo-r1: Smart navigation for low-cost long video understanding | CVPR '26 | - | - |
| <a id="paper-xing2026native"></a>`OmniAgent`<br><sub>P-IV · SFT · RL · Trajectory supervision · Reward supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2606.19341-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2606.19341)<br>Native Active Perception as Reasoning for Omni-Modal Understanding | arXiv '26 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://huggingface.co/harryhsing/OmniAgent-RL-7B) | [![GitHub](https://img.shields.io/github/stars/harryhsing/OmniAgent?style=flat-square&logo=github)](https://github.com/harryhsing/OmniAgent) |
| <a id="paper-xu2026towards"></a>`ReViSe`<br><sub>P-I · SFT · RL · Reward supervision</sub> | Towards Sparse Video Understanding and Reasoning | CVPR '26 | - | - |
| <a id="paper-jain2026sage"></a>`SAGE`<br><sub>P-II · RL · Reward supervision</sub> | Sage: Training smart any-horizon agents for long video reasoning with reinforcement learning | CVPR '26 | - | [![GitHub](https://img.shields.io/github/stars/allenai/SAGE?style=flat-square&logo=github)](https://github.com/allenai/SAGE) |
| <a id="paper-xie2025video"></a>`Video-MTR`<br><sub>P-II · RL · Reward supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2508.20478-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2508.20478)<br>Video-mtr: Reinforced multi-turn reasoning for long video understanding | arXiv '26 | - | [![GitHub](https://img.shields.io/github/stars/Xyuan13/Video-MTR?style=flat-square&logo=github)](https://github.com/Xyuan13/Video-MTR) |
| <a id="paper-zou2026videobrain"></a>`VideoBrain`<br><sub>P-I · SFT · RL · Trajectory supervision · Reward supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2602.04094-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2602.04094)<br>VideoBrain: Learning Adaptive Frame Sampling for Long Video Understanding | arXiv '26 | - | [![GitHub](https://img.shields.io/github/stars/junbo-zou/VideoBrain?style=flat-square&logo=github)](https://github.com/junbo-zou/VideoBrain) |
| <a id="paper-wang2026videochat"></a>`VideoChat-A1`<br><sub>P-II · Training-Free</sub> | Videochat-a1: Thinking with long videos by chain-of-shot reasoning | Proceedings of the AAAI Conference on Artificial Intelligence '26 | - | - |
| <a id="paper-qiu2026videoseal"></a>`VideoSEAL`<br><sub>P-II · RL · Grounding supervision · Reward supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2605.12571-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2605.12571)<br>VideoSEAL: Mitigating Evidence Misalignment in Agentic Long Video Understanding by Decoupling Answer Authority | arXiv '26 | - | [![GitHub](https://img.shields.io/github/stars/Echochef/VideoSEAL?style=flat-square&logo=github)](https://github.com/Echochef/VideoSEAL) |
| <a id="paper-lin2026videoseek"></a>`VideoSeek`<br><sub>P-II · Training-Free</sub> | VideoSeek: Long-Horizon Video Agent with Tool-Guided Seeking | CVPR '26 | - | [![GitHub](https://img.shields.io/github/stars/jylins/videoseek?style=flat-square&logo=github)](https://github.com/jylins/videoseek) |
||

### Temporal Causality

Video is an ordered record of change. State and process tracking preserve transitions, causal dependencies, and response readiness.

> In chronological order, from the earliest to the latest.

| Model | Paper | Venue | Website | GitHub |
|:-:|:-|:-:|:-:|:-:|
||
| <a id="paper-yang2024agent"></a>`AVT`<br><sub>P-II · Training-Free</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2412.09513-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2412.09513)<br>Agent-based Video Trimming | arXiv '24 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://ylingfeng.github.io/AVT) | - |
| <a id="paper-yang2024doraemongpt"></a>`DoraemonGPT`<br><sub>P-III · Training-Free</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2401.08392-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2401.08392)<br>Doraemongpt: Toward understanding dynamic scenes with large language models (exemplified as a video agent) | arXiv '24 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://z-x-yang.github.io/doraemon-gpt) | - |
| <a id="paper-pmlr-v235-fei24a"></a>`Video-of-Thought`<br><sub>P-III · Training-Free · SFT · Grounding supervision</sub> | [![Paper](https://img.shields.io/badge/Paper-Link-b31b1b?style=flat-square)](https://proceedings.mlr.press/v235/fei24a.html)<br>Video-of-Thought: Step-by-Step Video Reasoning from Perception to Cognition | ICML '24 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://haofei.vip/VoT) | - |
| <a id="paper-zhang2025avila"></a>`AViLA`<br><sub>P-IV · Training-Free · Grounding supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2506.18472-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2506.18472)<br>Avila: Asynchronous vision-language agent for streaming multimodal data interaction | arXiv '25 | - | - |
| <a id="paper-chen2025egoagent"></a>`EgoAgent`<br><sub>P-IV · SFT · Trajectory supervision</sub> | EgoAgent: a joint predictive agent model in egocentric worlds | ICCV '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://www.nasonline.org/directory-entry/linda-b-smith-v0ddqs/) | [![GitHub](https://img.shields.io/github/stars/zju3dv/EgoAgent?style=flat-square&logo=github)](https://github.com/zju3dv/EgoAgent) |
| <a id="paper-fan2025embodied"></a>`Embodied VideoAgent`<br><sub>P-IV · Training-Free</sub> | Embodied videoagent: Persistent memory from egocentric videos and embodied sensors enables dynamic scene understanding | ICCV '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://embodied-videoagent.github.io/) | - |
| <a id="paper-yu2026eyes"></a>`Eyes Wide Open`<br><sub>P-IV · SFT · Trajectory supervision</sub> | Eyes Wide Open: Ego Proactive Video-LLM for Streaming Video | NeurIPS '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://zhangyl4.github.io/publications/eyes-wide-open/) | - |
| <a id="paper-chu2025graphvideoagent"></a>`GraphVideoAgent`<br><sub>P-III · Training-Free</sub> | GraphVideoAgent: Enhancing Long-form Video Understanding with Entity Relation Graphs | ACM MM '25 | - | - |
| <a id="paper-li2025lion"></a>`LION-FS`<br><sub>P-IV · SFT · Trajectory supervision</sub> | Lion-fs: Fast & slow video-language thinker as online video assistant | CVPR '25 | - | [![GitHub](https://img.shields.io/github/stars/JiuTian-VL/LION-FS?style=flat-square&logo=github)](https://github.com/JiuTian-VL/LION-FS) |
| <a id="paper-wang2025mobile"></a>`Mobile-Agent-V`<br><sub>P-II · SFT · Trajectory supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2502.17110-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2502.17110)<br>Mobile-Agent-V: A Video-Guided Approach for Effortless and Efficient Operational Knowledge Injection in Mobile Automation | arXiv '25 | - | - |
| <a id="paper-jang2025scalable"></a>`MONDAY`<br><sub>P-II · SFT · Trajectory supervision</sub> | Scalable video-to-dataset generation for cross-platform mobile agents | CVPR '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://monday-dataset.github.io) | - |
| <a id="paper-yang2026panda"></a>`PANDA`<br><sub>P-IV · Training-Free</sub> | Panda: Towards generalist video anomaly detection via agentic ai engineer | NeurIPS '25 | - | - |
| <a id="paper-zhang2025rewatch"></a>`ReWatch-R1`<br><sub>P-II · SFT · RL · Trajectory supervision · Grounding supervision · Reward supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2509.23652-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2509.23652)<br>ReWatch-R1: Boosting Complex Video Reasoning in Large Vision-Language Models through Agentic Data Synthesis | arXiv '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://rewatch-r1.github.io) | - |
| <a id="paper-han2025roomtour3d"></a>`RoomTour3D`<br><sub>P-II · SFT · Trajectory supervision</sub> | Roomtour3d: Geometry-aware video-instruction tuning for embodied navigation | CVPR '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://roomtour3d.github.io) | - |
| <a id="paper-wu2026season"></a>`SEASON`<br><sub>P-II · Training-Free</sub> | Season: Mitigating temporal hallucination in video large language models via self-diagnostic contrastive decoding | CVPR '25 | - | - |
| <a id="paper-wang2026streambridge"></a>`StreamBridge`<br><sub>P-IV · SFT · Trajectory supervision</sub> | Streambridge: Turning your offline video large language model into a proactive streaming assistant | NeurIPS '25 | - | - |
| <a id="paper-wang2026time"></a>`Time-R1`<br><sub>P-II · RL · Reward supervision</sub> | Time-r1: Post-training large vision language model for temporal video grounding | NeurIPS '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://xuboshen.github.io/Time-R1/) | - |
| <a id="paper-feng2026video"></a>`Video-R1`<br><sub>P-II · RL · Reward supervision</sub> | Video-r1: Reinforcing video reasoning in mllms | NeurIPS '25 | - | [![GitHub](https://img.shields.io/github/stars/tulerfeng/Video-R1?style=flat-square&logo=github)](https://github.com/tulerfeng/Video-R1) |
| <a id="paper-lu2025videoagenttrek"></a>`VideoAgentTrek`<br><sub>P-II · SFT · Trajectory supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2510.19488-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2510.19488)<br>VideoAgentTrek: Computer Use Pretraining from Unlabeled Videos | arXiv '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://videoagenttrek.github.io/) | - |
| <a id="paper-lu2025vited"></a>`VITED`<br><sub>P-II · SFT · Trajectory supervision</sub> | Vited: Video temporal evidence distillation | CVPR '25 | - | - |
| <a id="paper-zhang2025vtimecot"></a>`VTimeCoT`<br><sub>P-III · SFT · Trajectory supervision</sub> | Vtimecot: Thinking by drawing for video temporal grounding and reasoning | ICCV '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://vtimecot.github.io) | - |
| <a id="paper-luo2026thinking"></a>`When Thinking Drifts`<br><sub>P-II · RL · Reward supervision</sub> | When thinking drifts: Evidential grounding for robust video reasoning | NeurIPS '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://vision.cs.utexas.edu/projects/video-ver/) | - |
| <a id="paper-rege2026agentic"></a>`EGAgent`<br><sub>P-III · Training-Free</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2601.18157-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2601.18157)<br>Agentic Very Long Video Understanding | arXiv '26 | - | [![GitHub](https://img.shields.io/github/stars/facebookresearch/egagent?style=flat-square&logo=github)](https://github.com/facebookresearch/egagent) |
| <a id="paper-yan2026proact"></a>`Proact-VL`<br><sub>P-IV · SFT · Trajectory supervision · Grounding supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2603.03447-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2603.03447)<br>Proact-vl: A proactive videollm for real-time ai companions | arXiv '26 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://proact-vl.github.io) | - |
| <a id="paper-jiang2026referagent"></a>`Refer-Agent`<br><sub>P-I · Training-Free · Grounding supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2602.03595-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2602.03595)<br>Refer-Agent: A Collaborative Multi-Agent System with Reasoning and Reflection for Referring Video Object Segmentation | arXiv '26 | - | [![GitHub](https://img.shields.io/github/stars/iSEE-Laboratory/Refer-Agent?style=flat-square&logo=github)](https://github.com/iSEE-Laboratory/Refer-Agent) |
| <a id="paper-yang2025streamagent"></a>`StreamAgent`<br><sub>P-IV · SFT · Trajectory supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2508.01875-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2508.01875)<br>Streamagent: Towards anticipatory agents for streaming video understanding | arXiv '26 | - | - |
| <a id="paper-yao2026harnessing"></a>`Streaming Harness`<br><sub>P-IV · SFT · Trajectory supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2606.08615-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2606.08615)<br>Harnessing Streaming Video in the Wild | arXiv '26 | - | - |
| <a id="paper-azad2026streamready"></a>`StreamReady`<br><sub>P-IV · SFT · Grounding supervision</sub> | Streamready: Learning what to answer and when in long streaming videos | CVPR '26 | - | - |
| <a id="paper-yang2026svagent"></a>`SVAgent`<br><sub>P-III · Training-Free</sub> | SVAgent: Storyline-Guided Long Video Understanding via Cross-Modal Multi-Agent Collaboration | CVPR '26 | - | - |
| <a id="paper-tang2026asynchronous"></a>`Takusen`<br><sub>P-IV · SFT · Trajectory supervision</sub> | Asynchronous Temporal Modeling with Two-Agent Framework for Streaming Dense Video Captioning | CVPR '26 | - | - |
| <a id="paper-liu2026thinking"></a>`ThinkStream`<br><sub>P-IV · RL · Reward supervision</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2603.12938-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2603.12938)<br>Thinking in streaming video | arXiv '26 | - | [![GitHub](https://img.shields.io/github/stars/johncaged/ThinkStream?style=flat-square&logo=github)](https://github.com/johncaged/ThinkStream) |
| <a id="paper-wang2026think"></a>`VideoHV-Agent`<br><sub>P-II · Training-Free · Grounding supervision</sub> | Think, Then Verify: A Hypothesis-Verification Multi-Agent Framework for Long Video Understanding | CVPR '26 | - | - |
| <a id="paper-liu2025videomind"></a>`VideoMind`<br><sub>P-III · SFT · Grounding supervision</sub> | VideoMind: A Chain-of-LoRA Agent for Temporal-Grounded Video Reasoning | NeurIPS 2025 Workshop on Bridging Language, Agent, and World Models for Reasoning and Planning '26 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://videomind.github.io/) | - |
||

### Multimodal Ambiguity

Vision, speech, audio, OCR, motion, and interaction cues may conflict. Role-specialized coordination separates and reconciles heterogeneous evidence.

> In chronological order, from the earliest to the latest.

| Model | Paper | Venue | Website | GitHub |
|:-:|:-|:-:|:-:|:-:|
||
| <a id="paper-zhang2024internlm"></a>`IXC2.5-OL`<br><sub>P-IV · Training-Free</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2412.09596-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2412.09596)<br>Internlm-xcomposer2. 5-omnilive: A comprehensive multimodal system for long-term streaming video and audio interactions | arXiv '24 | - | [![GitHub](https://img.shields.io/github/stars/InternLM/InternLM-XComposer?style=flat-square&logo=github)](https://github.com/InternLM/InternLM-XComposer/tree/main/InternLM-XComposer-2.5-OmniLive) |
| <a id="paper-chowdhury2026magnet"></a>`MAGNET`<br><sub>P-III · Training-Free</sub> | Magnet: A multi-agent framework for finding audio-visual needles by reasoning over multi-video haystacks | NeurIPS '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://schowdhury671.github.io/magnet_project/) | - |
| <a id="paper-chen2025multimodal"></a>`MAViD`<br><sub>P-II · SFT</sub> | A Multimodal Video Understanding Agent Based on Video-Audio Multi-Task Joint Fine-Tuning and State Machine Scheduling | Proceedings of the 2025 8th International Conference on Computer Information Science and Artificial Intelligence '25 | - | - |
| <a id="paper-xu2026scieducator"></a>`SciEducator`<br><sub>P-III · Training-Free</sub> | SciEducator: Scientific Video Understanding and Educating via Deming-Cycle Multi-Agent System | CVPR '25 | - | - |
| <a id="paper-fu2025vispeak"></a>`ViSpeak`<br><sub>P-IV · SFT · Trajectory supervision</sub> | Vispeak: Visual instruction feedback in streaming videos | ICCV '25 | - | [![GitHub](https://img.shields.io/github/stars/HumanMLLM/ViSpeak?style=flat-square&logo=github)](https://github.com/HumanMLLM/ViSpeak) |
| <a id="paper-guo2026agentic"></a>`AgenticVS`<br><sub>P-II · Training-Free · SFT · Trajectory supervision</sub> | Agentic Video Summarization via Self-Reflecting Multimodal Understanding | CVPR '26 | - | - |
| <a id="paper-yan2026symphony"></a>`Symphony`<br><sub>P-II · Training-Free</sub> | Symphony: A Cognitively-Inspired Multi-Agent System for Long-Video Understanding | CVPR '26 | - | - |
| <a id="paper-park2025v"></a>`V-Agent`<br><sub>P-I · Training-Free</sub> | [![arXiv](https://img.shields.io/badge/arXiv-2512.16925-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2512.16925)<br>V-Agent: An Interactive Video Search System Using Vision-Language Models | arXiv '26 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct) | - |
| <a id="paper-chen2026videochat"></a>`VideoChat-M1`<br><sub>P-II · RL · Reward supervision</sub> | Videochat-m1: Collaborative policy planning for video understanding via multi-agent reinforcement learning | CVPR '26 | - | - |
||

# 2. State-Space Paradigms

These are orthogonal indexes over the canonical Challenge-to-Design tables. Links return to the paper's unique metadata row.

### Paradigm I: Video as a Bag of Frames

Selected frames, keyframes, clips, shots, or candidate segments serve as discrete evidence units.

[`A4VL`](#paper-a4vl2026) · [`APPO`](#paper-du2026appo) · [`EVA`](#paper-zhang2026eva) · [`Flow4Agent`](#paper-liu2025flow4agent) · [`FrameThinker`](#paper-he2025framethinker) · [`LVAgent`](#paper-lvagent2025) · [`ReAgent-V`](#paper-reagentv2025) · [`Refer-Agent`](#paper-jiang2026referagent) · [`ReViSe`](#paper-xu2026towards) · [`SALOVA`](#paper-kim2025salova) · [`Select Less, Reason More`](#paper-li2026select) · [`V-Agent`](#paper-park2025v) · [`VideoBrain`](#paper-zou2026videobrain)

### Paradigm II: Video as a Temporal Sequence

The operative state preserves ordering and temporal relations among observations.

[`AgenticVS`](#paper-guo2026agentic) · [`AoTD`](#paper-shi2025enhancing) · [`AVT`](#paper-yang2024agent) · [`Commonsense Video QA`](#paper-liu2025commonsense) · [`LensWalk`](#paper-li2026lenswalk) · [`LongVideo-R1`](#paper-qiu2026longvideo) · [`LongVT`](#paper-yang2026longvt) · [`MAViD`](#paper-chen2025multimodal) · [`Mobile-Agent-V`](#paper-wang2025mobile) · [`MONDAY`](#paper-jang2025scalable) · [`MSR-ViR`](#paper-song2025modularized) · [`ReWatch-R1`](#paper-zhang2025rewatch) · [`RoomTour3D`](#paper-han2025roomtour3d) · [`SAGE`](#paper-jain2026sage) · [`SEASON`](#paper-wu2026season) · [`SlowFocus`](#paper-nie2024slowfocus) · [`Symphony`](#paper-yan2026symphony) · [`Thinking with Videos`](#paper-zhang2026thinking) · [`Time-R1`](#paper-wang2026time) · [`VCA`](#paper-yang2025vca) · [`Video-MTR`](#paper-xie2025video) · [`Video-R1`](#paper-feng2026video) · [`VideoAgent (Wang et al.)`](#paper-wang2024videoagent) · [`VideoAgent2`](#paper-zhi2025videoagent2) · [`VideoAgentTrek`](#paper-lu2025videoagenttrek) · [`VideoChat-A1`](#paper-wang2026videochat) · [`VideoChat-M1`](#paper-chen2026videochat) · [`VideoHV-Agent`](#paper-wang2026think) · [`VideoSEAL`](#paper-qiu2026videoseal) · [`VideoSeek`](#paper-lin2026videoseek) · [`VITED`](#paper-lu2025vited) · [`When Thinking Drifts`](#paper-luo2026thinking)

### Paradigm III: Video as a Graph of Entities

Persistent entities and evidence links support long-range association and multimodal retrieval.

[`AdaVideoRAG`](#paper-zhang2026adavideorag) · [`AVI`](#paper-gao2025agentic) · [`DoraemonGPT`](#paper-yang2024doraemongpt) · [`DrVideo`](#paper-ma2025drvideo) · [`DVD`](#paper-zhang2026deep) · [`EGAgent`](#paper-rege2026agentic) · [`Flash-VStream`](#paper-zhang2025flash) · [`G2F-RAG`](#paper-yang2026graph) · [`GraphVideoAgent`](#paper-chu2025graphvideoagent) · [`HAVEN`](#paper-yin2026hierarchical) · [`M3-Agent`](#paper-long2025seeing) · [`MAGNET`](#paper-chowdhury2026magnet) · [`Mr. Video`](#paper-pang2025mr) · [`OmAgent`](#paper-zhang2024omagent) · [`ReKV`](#paper-di2025streaming) · [`SciEducator`](#paper-xu2026scieducator) · [`StreamChat`](#paper-xiong2025streaming) · [`StreamMeCo`](#paper-wang2026streammeco) · [`StreamRAG`](#paper-xie2026streamrag) · [`SVAgent`](#paper-yang2026svagent) · [`Video-of-Thought`](#paper-pmlr-v235-fei24a) · [`Video-RAG`](#paper-luo2026video) · [`VideoAgent (Fan et al.)`](#paper-fan2024videoagent) · [`VideoARM`](#paper-yin2026videoarm) · [`VideoExplorer`](#paper-yuan2025videoexplorer) · [`VideoLLaMB`](#paper-wang2025videollamb) · [`VideoLucy`](#paper-zuo2026videolucy) · [`VideoMind`](#paper-liu2025videomind) · [`VTimeCoT`](#paper-zhang2025vtimecot) · [`WorldMM`](#paper-yeo2026worldmm)

### Paradigm IV: Video as an Evolving World State

A partial, time-indexed state is revised as observations arrive and future evidence remains unavailable.

[`AViLA`](#paper-zhang2025avila) · [`EgoAgent`](#paper-chen2025egoagent) · [`Embodied VideoAgent`](#paper-fan2025embodied) · [`Eyes Wide Open`](#paper-yu2026eyes) · [`IXC2.5-OL`](#paper-zhang2024internlm) · [`LION-FS`](#paper-li2025lion) · [`OmniAgent`](#paper-xing2026native) · [`PANDA`](#paper-yang2026panda) · [`Proact-VL`](#paper-yan2026proact) · [`ProVideLLM`](#paper-chatterjee2025memory) · [`R3-Streaming`](#paper-liu2026efficient) · [`StreamAgent`](#paper-yang2025streamagent) · [`StreamBridge`](#paper-wang2026streambridge) · [`Streaming Harness`](#paper-yao2026harnessing) · [`StreamReady`](#paper-azad2026streamready) · [`Takusen`](#paper-tang2026asynchronous) · [`ThinkStream`](#paper-liu2026thinking) · [`VideoStreaming`](#paper-qian2024streaming) · [`ViSpeak`](#paper-fu2025vispeak)

# 3. Learning Paradigms

A method can use more than one learning regime; repeated names below are index links, not duplicated paper records.

### Training-Free and Inference-Time Control

Prompts, tools, retrieval procedures, memory rules, verification, waiting, and stopping criteria specify agent behavior at inference time.

[`A4VL`](#paper-a4vl2026) · [`AdaVideoRAG`](#paper-zhang2026adavideorag) · [`AgenticVS`](#paper-guo2026agentic) · [`AVI`](#paper-gao2025agentic) · [`AViLA`](#paper-zhang2025avila) · [`AVT`](#paper-yang2024agent) · [`Commonsense Video QA`](#paper-liu2025commonsense) · [`DoraemonGPT`](#paper-yang2024doraemongpt) · [`DrVideo`](#paper-ma2025drvideo) · [`DVD`](#paper-zhang2026deep) · [`EGAgent`](#paper-rege2026agentic) · [`Embodied VideoAgent`](#paper-fan2025embodied) · [`G2F-RAG`](#paper-yang2026graph) · [`GraphVideoAgent`](#paper-chu2025graphvideoagent) · [`HAVEN`](#paper-yin2026hierarchical) · [`IXC2.5-OL`](#paper-zhang2024internlm) · [`LensWalk`](#paper-li2026lenswalk) · [`LVAgent`](#paper-lvagent2025) · [`MAGNET`](#paper-chowdhury2026magnet) · [`Mr. Video`](#paper-pang2025mr) · [`OmAgent`](#paper-zhang2024omagent) · [`PANDA`](#paper-yang2026panda) · [`Refer-Agent`](#paper-jiang2026referagent) · [`SciEducator`](#paper-xu2026scieducator) · [`SEASON`](#paper-wu2026season) · [`StreamChat`](#paper-xiong2025streaming) · [`StreamMeCo`](#paper-wang2026streammeco) · [`StreamRAG`](#paper-xie2026streamrag) · [`SVAgent`](#paper-yang2026svagent) · [`Symphony`](#paper-yan2026symphony) · [`V-Agent`](#paper-park2025v) · [`VCA`](#paper-yang2025vca) · [`Video-of-Thought`](#paper-pmlr-v235-fei24a) · [`Video-RAG`](#paper-luo2026video) · [`VideoAgent (Fan et al.)`](#paper-fan2024videoagent) · [`VideoAgent (Wang et al.)`](#paper-wang2024videoagent) · [`VideoAgent2`](#paper-zhi2025videoagent2) · [`VideoARM`](#paper-yin2026videoarm) · [`VideoChat-A1`](#paper-wang2026videochat) · [`VideoHV-Agent`](#paper-wang2026think) · [`VideoLucy`](#paper-zuo2026videolucy) · [`VideoSeek`](#paper-lin2026videoseek) · [`WorldMM`](#paper-yeo2026worldmm)

### Supervised Fine-Tuning and Imitation Learning

Answer labels, component objectives, or demonstrated trajectories supervise agent decisions.

[`AgenticVS`](#paper-guo2026agentic) · [`AoTD`](#paper-shi2025enhancing) · [`EgoAgent`](#paper-chen2025egoagent) · [`EVA`](#paper-zhang2026eva) · [`Eyes Wide Open`](#paper-yu2026eyes) · [`FrameThinker`](#paper-he2025framethinker) · [`LION-FS`](#paper-li2025lion) · [`LongVideo-R1`](#paper-qiu2026longvideo) · [`LongVT`](#paper-yang2026longvt) · [`M3-Agent`](#paper-long2025seeing) · [`MAViD`](#paper-chen2025multimodal) · [`Mobile-Agent-V`](#paper-wang2025mobile) · [`MONDAY`](#paper-jang2025scalable) · [`MSR-ViR`](#paper-song2025modularized) · [`OmniAgent`](#paper-xing2026native) · [`Proact-VL`](#paper-yan2026proact) · [`ReViSe`](#paper-xu2026towards) · [`ReWatch-R1`](#paper-zhang2025rewatch) · [`RoomTour3D`](#paper-han2025roomtour3d) · [`StreamAgent`](#paper-yang2025streamagent) · [`StreamBridge`](#paper-wang2026streambridge) · [`Streaming Harness`](#paper-yao2026harnessing) · [`StreamReady`](#paper-azad2026streamready) · [`Takusen`](#paper-tang2026asynchronous) · [`Video-of-Thought`](#paper-pmlr-v235-fei24a) · [`VideoAgentTrek`](#paper-lu2025videoagenttrek) · [`VideoBrain`](#paper-zou2026videobrain) · [`VideoExplorer`](#paper-yuan2025videoexplorer) · [`VideoMind`](#paper-liu2025videomind) · [`VideoStreaming`](#paper-qian2024streaming) · [`ViSpeak`](#paper-fu2025vispeak) · [`VITED`](#paper-lu2025vited) · [`VTimeCoT`](#paper-zhang2025vtimecot)

### Reinforcement Learning

Outcome and process rewards optimize evidence acquisition, grounding, efficiency, timing, or reasoning validity.

[`APPO`](#paper-du2026appo) · [`EVA`](#paper-zhang2026eva) · [`FrameThinker`](#paper-he2025framethinker) · [`LongVideo-R1`](#paper-qiu2026longvideo) · [`LongVT`](#paper-yang2026longvt) · [`M3-Agent`](#paper-long2025seeing) · [`MSR-ViR`](#paper-song2025modularized) · [`OmniAgent`](#paper-xing2026native) · [`R3-Streaming`](#paper-liu2026efficient) · [`ReAgent-V`](#paper-reagentv2025) · [`ReViSe`](#paper-xu2026towards) · [`ReWatch-R1`](#paper-zhang2025rewatch) · [`SAGE`](#paper-jain2026sage) · [`Select Less, Reason More`](#paper-li2026select) · [`Thinking with Videos`](#paper-zhang2026thinking) · [`ThinkStream`](#paper-liu2026thinking) · [`Time-R1`](#paper-wang2026time) · [`Video-MTR`](#paper-xie2025video) · [`Video-R1`](#paper-feng2026video) · [`VideoBrain`](#paper-zou2026videobrain) · [`VideoChat-M1`](#paper-chen2026videochat) · [`VideoExplorer`](#paper-yuan2025videoexplorer) · [`VideoSEAL`](#paper-qiu2026videoseal) · [`When Thinking Drifts`](#paper-luo2026thinking)

# 4. Data and Supervision

The former Appendix material is promoted here as a first-class part of the survey taxonomy.

### Trajectory Supervision

Step-by-step observations, tool calls, state changes, revisions, failures, and stopping decisions.

[`AgenticVS`](#paper-guo2026agentic) · [`AoTD`](#paper-shi2025enhancing) · [`EgoAgent`](#paper-chen2025egoagent) · [`Eyes Wide Open`](#paper-yu2026eyes) · [`FrameThinker`](#paper-he2025framethinker) · [`LION-FS`](#paper-li2025lion) · [`Mobile-Agent-V`](#paper-wang2025mobile) · [`MONDAY`](#paper-jang2025scalable) · [`OmniAgent`](#paper-xing2026native) · [`Proact-VL`](#paper-yan2026proact) · [`ReWatch-R1`](#paper-zhang2025rewatch) · [`RoomTour3D`](#paper-han2025roomtour3d) · [`StreamAgent`](#paper-yang2025streamagent) · [`StreamBridge`](#paper-wang2026streambridge) · [`Streaming Harness`](#paper-yao2026harnessing) · [`Takusen`](#paper-tang2026asynchronous) · [`VideoAgentTrek`](#paper-lu2025videoagenttrek) · [`VideoBrain`](#paper-zou2026videobrain) · [`VideoExplorer`](#paper-yuan2025videoexplorer) · [`ViSpeak`](#paper-fu2025vispeak) · [`VITED`](#paper-lu2025vited) · [`VTimeCoT`](#paper-zhang2025vtimecot)

### Grounding Supervision

Temporal intervals, regions, tracks, entities, audio cues, OCR spans, and state changes that support a claim.

[`AViLA`](#paper-zhang2025avila) · [`Commonsense Video QA`](#paper-liu2025commonsense) · [`M3-Agent`](#paper-long2025seeing) · [`MSR-ViR`](#paper-song2025modularized) · [`Proact-VL`](#paper-yan2026proact) · [`Refer-Agent`](#paper-jiang2026referagent) · [`ReWatch-R1`](#paper-zhang2025rewatch) · [`Select Less, Reason More`](#paper-li2026select) · [`StreamReady`](#paper-azad2026streamready) · [`Video-of-Thought`](#paper-pmlr-v235-fei24a) · [`VideoHV-Agent`](#paper-wang2026think) · [`VideoMind`](#paper-liu2025videomind) · [`VideoSEAL`](#paper-qiu2026videoseal) · [`VideoStreaming`](#paper-qian2024streaming)

### Preference and Reward Supervision

Comparative or scalar signals over evidence choice, reasoning quality, response timing, or complete rollouts.

[`APPO`](#paper-du2026appo) · [`EVA`](#paper-zhang2026eva) · [`FrameThinker`](#paper-he2025framethinker) · [`LongVideo-R1`](#paper-qiu2026longvideo) · [`LongVT`](#paper-yang2026longvt) · [`M3-Agent`](#paper-long2025seeing) · [`MSR-ViR`](#paper-song2025modularized) · [`OmniAgent`](#paper-xing2026native) · [`R3-Streaming`](#paper-liu2026efficient) · [`ReAgent-V`](#paper-reagentv2025) · [`ReViSe`](#paper-xu2026towards) · [`ReWatch-R1`](#paper-zhang2025rewatch) · [`SAGE`](#paper-jain2026sage) · [`Select Less, Reason More`](#paper-li2026select) · [`Thinking with Videos`](#paper-zhang2026thinking) · [`ThinkStream`](#paper-liu2026thinking) · [`Time-R1`](#paper-wang2026time) · [`Video-MTR`](#paper-xie2025video) · [`Video-R1`](#paper-feng2026video) · [`VideoBrain`](#paper-zou2026videobrain) · [`VideoChat-M1`](#paper-chen2026videochat) · [`VideoExplorer`](#paper-yuan2025videoexplorer) · [`VideoSEAL`](#paper-qiu2026videoseal) · [`When Thinking Drifts`](#paper-luo2026thinking)

# 5. Benchmarks

Benchmarks are grouped by their primary role in agentic video understanding.

### Capability-Oriented Benchmarks

> In chronological order, from the earliest to the latest.

| Model | Paper | Venue | Website | GitHub |
|:-:|:-|:-:|:-:|:-:|
||
| <a id="paper-gao2017tall"></a>`Charades-STA` | Tall: Temporal activity localization via language query | ICCV '17 | - | - |
| <a id="paper-10-1145-3123266-3123427"></a>`MSRVTT-QA` | [![Paper](https://img.shields.io/badge/Paper-Link-b31b1b?style=flat-square)](https://doi.org/10.1145/3123266.3123427)<br>Video Question Answering via Gradually Refined Attention over Appearance and Motion | ACM MM '17 | - | - |
| <a id="paper-zhou2018towards"></a>`YouCook2` | Towards Automatic Learning of Procedures from Web Instructional Videos | Proceedings of the AAAI Conference on Artificial Intelligence '18 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](http://youcook2.eecs.umich.edu) | - |
| <a id="paper-yu2019activitynet"></a>`ActivityNet-QA` | Activitynet-qa: A dataset for understanding complex web videos via question answering | Proceedings of the AAAI conference on artificial intelligence '19 | - | - |
| <a id="paper-li2020hero"></a>`How2QA` | Hero: Hierarchical encoder for video+ language omni-representation pre-training | EMNLP '20 | - | - |
| <a id="paper-xiao2021next"></a>`NExT-QA` | Next-qa: Next phase of question-answering to explaining temporal actions | CVPR '21 | - | [![GitHub](https://img.shields.io/github/stars/doc-doc/NExT-QA?style=flat-square&logo=github)](https://github.com/doc-doc/NExT-QA.git) |
| <a id="paper-mangalam2023egoschema"></a>`EgoSchema` | EgoSchema: A Diagnostic Benchmark for Very Long-form Video Language Understanding | NeurIPS '23 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](http://egoschema.github.io) | - |
| <a id="paper-zala2023hierarchical"></a>`HiREST` | Hierarchical video-moment retrieval and step-captioning | CVPR '23 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://www.mturk.com) | [![GitHub](https://img.shields.io/github/stars/j-min/HiREST?style=flat-square&logo=github)](https://github.com/j-min/HiREST) |
| <a id="paper-patraucean2023perception"></a>`Perception Test` | Perception test: A diagnostic benchmark for multimodal video models | NeurIPS '23 | - | [![GitHub](https://img.shields.io/github/stars/deepmind/perception_test?style=flat-square&logo=github)](https://github.com/deepmind/perception_test) |
| <a id="paper-grauman2024ego"></a>`Ego-Exo4D` | Ego-exo4d: Understanding skilled human activity from first-and third-person perspectives | CVPR '24 | - | - |
| <a id="paper-wu2024longvideobench"></a>`LongVideoBench` | Longvideobench: A benchmark for long-context interleaved video-language understanding | NeurIPS '24 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://longvideobench.github.io) | - |
| <a id="paper-fang2024mmbench"></a>`MMBench-Video` | Mmbench-video: A long-form multi-shot benchmark for holistic video understanding | NeurIPS '24 | - | [![GitHub](https://img.shields.io/github/stars/open-compass/VLMEvalKit?style=flat-square&logo=github)](https://github.com/open-compass/VLMEvalKit) |
| <a id="paper-li2024mvbench"></a>`MVBench` | Mvbench: A comprehensive multi-modal video understanding benchmark | CVPR '24 | - | - |
| <a id="paper-wu2024star"></a>`STAR` | [![arXiv](https://img.shields.io/badge/arXiv-2405.09711-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2405.09711)<br>Star: A benchmark for situated reasoning in real-world videos | arXiv '24 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](http://star.csail.mit.edu) | - |
| <a id="paper-liu2024tempcompass"></a>`TempCompass` | Tempcompass: Do video llms really understand videos? | ACL '24 | - | [![GitHub](https://img.shields.io/github/stars/llyx97/TempCompass?style=flat-square&logo=github)](https://github.com/llyx97/TempCompass) |
| <a id="paper-geng2025longvale"></a>`LongVALE` | Longvale: Vision-audio-language-event benchmark towards time-aware omni-modal perception of long videos | CVPR '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://ttgeng233.github.io/LongVALE/) | - |
| <a id="paper-wang2025lvbench"></a>`LVBench` | Lvbench: An extreme long video understanding benchmark | ICCV '25 | - | - |
| <a id="paper-zhou2025mlvu"></a>`MLVU` | Mlvu: Benchmarking multi-task long video understanding | CVPR '25 | - | - |
| <a id="paper-ning2025video"></a>`Video-Bench` | Video-bench: A comprehensive benchmark and toolkit for evaluating video-based large language models | Computational Visual Media '25 | - | [![GitHub](https://img.shields.io/github/stars/PKU-YuanGroup/Video-Bench?style=flat-square&logo=github)](https://github.com/PKU-YuanGroup/Video-Bench) |
| <a id="paper-fu2025video"></a>`Video-MME` | Video-mme: The first-ever comprehensive evaluation benchmark of multi-modal llms in video analysis | CVPR '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://video-mme.github.io) | - |
| <a id="paper-zhang2025towards"></a>`Video-TT` | Towards video thinking test: A holistic benchmark for advanced video reasoning and understanding | ICCV '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://zhangyuanhan-ai.github.io/video-tt/) | - |
| <a id="paper-hu2026video"></a>`Video-MMMU` | Video-MMMU: Evaluating Knowledge Acquisition from Multidisciplinary Professional Videos | ACL '26 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://videommmu.github.io/) | - |
||

### Agent-Oriented Benchmarks

> In chronological order, from the earliest to the latest.

| Model | Paper | Venue | Website | GitHub |
|:-:|:-|:-:|:-:|:-:|
||
| <a id="paper-wang2025omnimmi"></a>`OmniMMI` | Omnimmi: A comprehensive multi-modal interaction benchmark in streaming video contexts | CVPR '25 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://omnimmi.github.io) | - |
| <a id="paper-niu2025ovo"></a>`OVO-Bench` | Ovo-bench: How far is your video-llms from real-world online video understanding? | CVPR '25 | - | [![GitHub](https://img.shields.io/github/stars/JoeLeelyf/OVO-Bench?style=flat-square&logo=github)](https://github.com/JoeLeelyf/OVO-Bench) |
| <a id="paper-yu2026ego2web"></a>`Ego2Web` | Ego2Web: A Web Agent Benchmark Grounded in Egocentric Videos | CVPR '26 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://ego2web.github.io) | [![GitHub](https://img.shields.io/github/stars/Yui010206/Ego2Web?style=flat-square&logo=github)](https://github.com/Yui010206/Ego2Web) |
| <a id="paper-zhao2026omnipro"></a>`OmniPro` | [![arXiv](https://img.shields.io/badge/arXiv-2605.18577-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2605.18577)<br>OmniPro: A Comprehensive Benchmark for Omni-Proactive Streaming Video Understanding | arXiv '26 | [![Project](https://img.shields.io/badge/Project-Page-f59e0b?style=flat-square)](https://ruixiangzhao.github.io/OmniPro/) | - |
| <a id="paper-lin2026streamingbench"></a>`StreamingBench` | Streamingbench: Assessing the gap for mllms to achieve streaming video understanding | ICASSP 2026-2026 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) '26 | - | [![GitHub](https://img.shields.io/github/stars/THUNLP-MT/StreamingBench?style=flat-square&logo=github)](https://github.com/THUNLP-MT/StreamingBench) |
| <a id="paper-liu2026watching"></a>`VideoDR` | [![arXiv](https://img.shields.io/badge/arXiv-2601.06943-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2601.06943)<br>Watching, reasoning, and searching: A video deep research benchmark on open web for agentic video reasoning | arXiv '26 | - | [![GitHub](https://img.shields.io/github/stars/QuantaAlpha/VideoDR-Benchmark?style=flat-square&logo=github)](https://github.com/QuantaAlpha/VideoDR-Benchmark) |
||

# 6. Additional Cited Works

The following cited works are not part of the 94-row core method table or the benchmark catalog, but are discussed in the survey's scope, learning, or supervision sections.

| Model | Paper | Venue | Website | GitHub |
|:-:|:-|:-:|:-:|:-:|
||
| <a id="paper-ma2024hierarchical"></a>`Hierarchical diffusion policy for kinematics-awa` | Hierarchical diffusion policy for kinematics-aware multi-task robotic manipulation | CVPR '24 | - | - |
| <a id="paper-zhao2025drivedreamer4d"></a>`Drivedreamer4d` | Drivedreamer4d: World models are effective data machines for 4d driving scene representation | CVPR '25 | - | - |
| <a id="paper-hassan2025gem"></a>`Gem` | Gem: A generalizable ego-vision multimodal world model for fine-grained ego-motion, object dynamics, and scene composition control | CVPR '25 | - | - |
| <a id="paper-park2026deepvideo"></a>`Deepvideo-r1` | Deepvideo-r1: Video reinforcement fine-tuning via difficulty-aware regressive grpo | NeurIPS '26 | - | [![GitHub](https://img.shields.io/github/stars/mlvlab/DeepVideoR1?style=flat-square&logo=github)](https://github.com/mlvlab/DeepVideoR1) |
| <a id="paper-wang2026streameqa"></a>`Streameqa` | Streameqa: Towards streaming video understanding for embodied scenarios | CVPR '26 | - | [![GitHub](https://img.shields.io/github/stars/MrYF-Wang/StreamEQA?style=flat-square&logo=github)](https://github.com/MrYF-Wang/StreamEQA) |
||

## Contributing

Contributions are welcome. For a new paper, please include:

- title, venue, year, and stable paper URL;
- project page and GitHub repository when available;
- one primary challenge and one state-space paradigm;
- all applicable learning regimes and supervision signals;
- one sentence explaining why the method satisfies the survey's agent definition.

<div align="center">

**[⬆ Back to Top](#agentic-video-understanding-a-survey)**

*Generated from the survey LaTeX tables and BibTeX source.*

</div>
