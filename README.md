# Karpathy Explainer Skill (`karpathy-explainer`)

An agent skill for **Claude Code**, **OpenAI Codex**, and modern AI assistants to convert normal prompts into high-bandwidth understanding artifacts based on **Andrej Karpathy's Ladder of Understanding**:

1. **Controlled Writing**: ASD-STE100 (and softened 80% ASD-STE100) aerospace maintenance technical English.
2. **Visual Diagrams**: Mermaid.js and SVG architecture/flow diagrams.
3. **Interactive Web Pages**: Standalone, single-file HTML micro-simulators with state controls and reactive boards.
4. **Bespoke Explainer Videos**: 3Blue1Brown-style Manim animation scripts with synced TTS narration (free `edge-tts` / macOS `say` or ElevenLabs).

---

## Background

> *"We'll be spending a lot more time trying to understand the outputs of language models... As LLMs get better, they will do more and more of the legwork autonomously, and a lot more of our work will rise up the abstractions into oversight and understanding."*  
> — **Andrej Karpathy**

When intelligence and code generation are abundant, the human cognitive reading bandwidth is the bottleneck. Rather than reading 2,000 words of conversational prose, you can ask for **discardable software artifacts** tailored for instant comprehension.

---

## Directory Structure

```
karpathy-explainer/
├── SKILL.md                          # Master skill instruction for Claude & Codex
├── README.md                         # Documentation and setup guide
├── scripts/
│   └── compile_prompt.py             # CLI prompt compiler & ASD-STE100 linter
├── references/
│   ├── asd-ste100-cheatsheet.md      # Full ASD-STE100 specification guide & dictionary
│   └── karpathy-ladder.md            # Conceptual framework & ladder rungs
└── tests/
    └── test_compiler.py              # Zero-dependency test suite
```

---

## Installation

### For Claude Code
To use in any repo or project:
```bash
# Link into project .claude/skills
mkdir -p .claude/skills
ln -s /Volumes/SamirDrive/Development/karpathy-explainer .claude/skills/karpathy-explainer
```

### For OpenAI Codex CLI
```bash
# Link into project .codex/skills
mkdir -p .codex/skills
ln -s /Volumes/SamirDrive/Development/karpathy-explainer .codex/skills/karpathy-explainer
```

### For Universal Agent Standard (`.agents/skills`)
```bash
mkdir -p .agents/skills
ln -s /Volumes/SamirDrive/Development/karpathy-explainer .agents/skills/karpathy-explainer
```

---

## CLI Usage: `compile_prompt.py`

### 1. Compile a Normal Prompt into Karpathy High-Bandwidth Format
```bash
# Generate complete 4-tier prompt
python3 scripts/compile_prompt.py "Explain Raft consensus"

# Generate specific tier (e.g., interactive HTML simulator)
python3 scripts/compile_prompt.py --tier html "Explain B-Tree node splitting"

# Generate 80% ASD-STE100 controlled English prompt
python3 scripts/compile_prompt.py --tier 80-ste100 "Explain TLS 1.3 handshake"

# Generate 3b1b video explainer with free local TTS
python3 scripts/compile_prompt.py --tier video --tts edge-tts "Explain Fourier Transform"
```

### 2. Lint Existing Text Against ASD-STE100 Rules
```bash
python3 scripts/compile_prompt.py --lint "Ensure the database utilizes replication prior to commencing operations."
```
Output:
```text
=== ASD-STE100 Lint Report (Score: 70/100) ===
Total Sentences: 1 | Total Issues: 3

[UNAPPROVED_WORD] Sentence 1: Unapproved word 'ensure' found. Replace with 'make sure'.
[UNAPPROVED_WORD] Sentence 1: Unapproved word 'utilizes' found. Replace with 'uses'.
[UNAPPROVED_WORD] Sentence 1: Unapproved word 'prior to' found. Replace with 'before'.
```

---

## Testing

Run the assert-based test suite:
```bash
python3 tests/test_compiler.py
```
Outputs:
```text
ALL TESTS PASSED: compile_prompt and STE-100 validator verified successfully.
```
