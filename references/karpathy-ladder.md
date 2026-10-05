# The Ladder of Understanding: Karpathy High-Bandwidth Artifacts

> *"We'll be spending a lot more time trying to understand the outputs of language models... As LLMs get better, they will do more and more of the legwork autonomously, and a lot more of our work will rise up the abstractions into oversight and understanding."*  
> — **Andrej Karpathy**

---

## 1. The Core Insight: Abundant Intelligence vs Bottlenecked Oversight

As AI models increase in capability:
1. **Generation is cheap and abundant**: Code, explanations, refactors, and architectures can be produced in seconds.
2. **Human attention and cognitive parsing are the scarce bottlenecks**: Reading 2,000 words of conversational, repetitive prose is the slowest and most tiring way to understand complex systems.
3. **The Solution: Discardable Software Artifacts**: Instead of standard chat text, request custom, purpose-built, discardable artifacts (interactive web sandboxes, SVG diagrams, controlled prose, programmatic video explainers) that maximize human bandwidth.

---

## 2. The Four Rungs of the Ladder

```
 ▲ Rung 4: Bespoke Explainer Videos (3b1b / Manim / Canvas + Synced TTS)
 │   └── Maximum temporal & audio-visual intuition. Code-driven animations with narration.
 │
 ▲ Rung 3: Interactive Web Pages (Single-File Discardable HTML / JS / Canvas)
 │   └── Hands-on simulation: sliders, step-by-step state machines, zero build setup.
 │
 ▲ Rung 2: Structured Diagrams (Mermaid.js / Standalone SVG)
 │   └── Spatial cognition: architecture flows, state transitions, message sequences.
 │
 █ Rung 1: Controlled Writing (ASD-STE100 / 80% Softened STE)
     └── Linguistic precision: ≤25 words/sentence, active voice, zero purple prose.
```

---

### Rung 1: Controlled Technical Writing (ASD-STE100)
- **Problem**: Default LLM prose is verbose, bloated with hedges, buzzwords (*delve, leverage, tapestry, robust*), and nested passive clauses.
- **Solution**: Enforce **ASD-STE100** (aerospace maintenance controlled language) or **80% ASD-STE100**.
- **Impact**: Sentences drop to ≤20-25 words. Verbs are active and imperative. Cognitive friction drops dramatically.

### Rung 2: Visual Diagrams & Mental Models
- **Problem**: Linear text struggles to convey multi-agent interactions, network consensus, data pipelines, or lifecycle states.
- **Solution**: Ask for **Mermaid.js** (`flowchart TD`, `sequenceDiagram`, `stateDiagram-v2`) or inline **SVG** vector diagrams.
- **Impact**: The human brain parses spatial relationships and flow order in milliseconds.

### Rung 3: Discardable Interactive Web Artifacts (HTML)
- **Problem**: Static diagrams cannot show dynamic state evolution, race conditions, or parameter sensitivity.
- **Solution**: Ask the LLM for a **single-file standalone HTML/JS page** (`open index.html`).
- **Features**:
  - Interactive state steppers (Play, Pause, Step Forward, Reset).
  - Parameter sliders with immediate live recalculation.
  - Zero build step, zero dependencies: pure vanilla JS + modern CSS or Tailwind CDN.
- **Impact**: The user learns by interacting with a running micro-simulator. Once understood, the artifact is discarded.

### Rung 4: Bespoke Explainer Videos (3b1b / Manim / Remotion + TTS)
- **Problem**: Deep conceptual topics (Fourier transform, Transformer attention head scores, Paxos leader failover) require synchronized temporal demonstration and narrative pacing.
- **Solution**: Ask for a **3Blue1Brown-style programmatic video**:
  - **Animation Code**: Python `manim` (Community Edition) script or HTML5 Canvas / GSAP / Remotion frame sequence.
  - **Narrative Audio Script**: Timed script with marker cues (`[00:00]`, `[00:08]`).
  - **TTS Narration**:
    - *Cloud API*: ElevenLabs API key.
    - *Free / Local Compute*: Python `edge-tts` (Microsoft Neural voices, zero cost, zero API key) or macOS native `say` command.
- **Impact**: Full video explainer generated autonomously on any arbitrary topic from scratch.
