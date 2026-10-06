#!/usr/bin/env python3
"""
Karpathy Explainer — Prompt Compiler and ASD-STE100 Validator
Converts standard prompts into Karpathy high-bandwidth understanding prompts:
  1. Controlled text (ASD-STE100 / 80% ASD-STE100)
  2. Structural diagrams (Mermaid / SVG)
  3. Interactive single-file HTML micro-simulators
  4. Bespoke 3b1b explainer video scripts with synced TTS narration
Also includes a zero-dependency linter for ASD-STE100 writing rules.
"""

import argparse
import json
import re
import sys
from typing import Dict, List, Tuple

# Unapproved words in STE-100 mapped to approved replacements
STE_REPLACEMENTS = {
    "ensure": "make sure",
    "prior to": "before",
    "replenish": "fill",
    "utilize": "use",
    "utilizes": "uses",
    "utilized": "used",
    "commence": "start",
    "commences": "starts",
    "commenced": "started",
    "approximately": "about",
    "in order to": "to",
    "terminate": "stop",
    "terminates": "stops",
    "terminated": "stopped",
    "modify": "change",
    "modifies": "changes",
    "modified": "changed",
    "obtain": "get",
    "obtains": "gets",
    "obtained": "got",
    "subsequent to": "after",
    "close to": "near",
}

# AI slop buzzwords & marketing adjectives that degrade technical density
AI_BUZZWORDS = [
    "delve", "leverage", "tapestry", "seamless", "seamlessly",
    "revolutionize", "testament", "beacon", "cutting-edge",
    "game-changer", "transformative", "crucial", "paramount",
    "foster", "holistic", "multifaceted", "interplay",
    "effortless", "effortlessly", "blazing-fast", "world-class",
    "state-of-the-art"
]

# Soft phrasal verbs to avoid in technical documentation (STE Rule 9.3)
PHRASAL_VERBS = {
    "spin up": "start",
    "spun up": "started",
    "reach out": "contact",
    "dive into": "read / analyze",
    "kick off": "begin / start",
    "circle back": "return",
    "touch base": "communicate"
}


def build_ste100_prompt(topic: str, softened: bool = True) -> str:
    """Generate prompt requesting ASD-STE100 controlled English explanation."""
    spec_label = "80% ASD-STE100 (Simplified Technical English, softened for computer science/engineering)" if softened else "Strict ASD-STE100 (Simplified Technical English)"
    
    rules = (
        "- Strict sentence length caps: Procedural sentences <= 20 words; Descriptive sentences <= 25 words.\n"
        "- Active voice and imperative commands for instructions ('Make sure that...', 'Run...', 'Check...').\n"
        "- Simple tenses only (Simple Present, Simple Past, Simple Future, Infinitive). Ban progressive (-ing) and perfect tenses.\n"
        "- No semicolons (Rule 8.1): STE bans semicolons outright. Split thoughts into separate sentences.\n"
        "- No nominalizations (Rule 3.7): Use direct verbs ('analyze', not 'perform an analysis of'; 'install', not 'carry out the installation').\n"
        "- No soft phrasal verbs (Rule 9.3): Use single plain verbs ('start', not 'spin up'; 'read', not 'dive into').\n"
        "- Max 3 words per noun cluster. Never omit articles (the, a, this).\n"
        "- Plain verb replacements: 'make sure' (not 'ensure'), 'before' (not 'prior to'), 'use' (not 'utilize'), 'start' (not 'commence').\n"
        "- Zero marketing adjectives & AI filler (no 'delve', 'leverage', 'tapestry', 'seamless', 'revolutionize', 'blazing-fast').\n"
        "- Preserve modality: Keep hedges ('may have failed', 'could cause') as hedges. Never upgrade uncertainty into a false certainty.\n"
        "- Maximum 6 sentences per paragraph. One clear topic per paragraph. Use vertical lists for steps."
    )
    if softened:
        rules += "\n- Retain all technical domain nouns (e.g. idempotency, mutex, raft, sharding) while enforcing STE sentence structure."

    return (
        f"Explain the following topic using {spec_label}:\n\n"
        f"Topic: {topic}\n\n"
        f"Formatting & Linguistic Rules:\n"
        f"{rules}\n\n"
        f"Output structure:\n"
        f"1. Executive Definition (max 2 descriptive sentences, <=25 words each)\n"
        f"2. Core Mechanism (numbered procedural steps, <=20 words per step)\n"
        f"3. Key Guarantees & Constraints (vertical list, simple present tense)\n"
        f"4. Failure Scenarios (WARNING: command + risk format)"
    )


def build_diagram_prompt(topic: str) -> str:
    """Generate prompt requesting structural architecture and flow diagrams."""
    return (
        f"Create high-bandwidth visual diagrams explaining the following topic:\n\n"
        f"Topic: {topic}\n\n"
        f"Output Requirements:\n"
        f"1. Primary Architectural Flow: Generate a self-contained, valid Mermaid.js diagram (`flowchart TD` or `sequenceDiagram`).\n"
        f"2. State Machine / Lifecycle: If state transitions exist, provide a Mermaid `stateDiagram-v2`.\n"
        f"3. Data / Topology Map: Use crisp node labels, directional arrows with explicit payload notes, and logical clustering/subgraphs.\n"
        f"4. Key Invariants Table: A 3-column table [Component | Responsibilities | Invariants] summarizing the diagram."
    )


def build_html_prompt(topic: str) -> str:
    """Generate prompt requesting a standalone, interactive single-file HTML explainer."""
    return (
        f"Build a complete, standalone, interactive single-file HTML/CSS/JS explainer for the following topic:\n\n"
        f"Topic: {topic}\n\n"
        f"Engineering Constraints:\n"
        f"- Pure single file: All HTML, CSS, and JavaScript inside ONE self-contained `.html` file. Zero bundlers, zero external npm installs.\n"
        f"- Can use Tailwind CSS via CDN or clean vanilla CSS with dark mode (#0d1117 / #161b22, crisp monospace accent tokens).\n"
        f"- Interactive Micro-Simulator: Include live controls (Step Forward, Step Backward, Auto-Play, Reset, Speed Slider).\n"
        f"- Visual State Display: Render an SVG or Canvas or reactive DOM state board illustrating real-time state changes on click.\n"
        f"- Side-by-Side Inspector: Clicking any step reveals the internal variables, state changes, and ASD-STE100 summary of what happened.\n"
        f"- Must open and function immediately when opened via `open explainer.html` in any browser."
    )


def build_video_prompt(topic: str, tts_engine: str = "edge-tts") -> str:
    """Generate prompt requesting a 3b1b-style programmatic video explainer + synced TTS narration."""
    tts_guidance = {
        "elevenlabs": "Generate an ElevenLabs Python script (`narrate.py`) using `elevenlabs` SDK to render voiceover with Adam/Rachel voice.",
        "edge-tts": "Generate a free, zero-API-key local shell command using `edge-tts --voice en-US-ChristopherNeural --text '...' --write-media narration.mp3`.",
        "macos-say": "Generate a zero-dependency macOS `say -v Samantha -r 175` audio narration generator script.",
    }.get(tts_engine, "Provide timed voiceover text for TTS narration.")

    return (
        f"Generate a complete 3Blue1Brown-style programmatic video explainer for the following topic:\n\n"
        f"Topic: {topic}\n\n"
        f"Deliverables:\n"
        f"1. Manim Python Script (`scene.py`):\n"
        f"   - Fully runnable Manim Community Edition (`manim -pql scene.py MainScene`) script.\n"
        f"   - High-contrast visual palette (dark background #0e1117, bright vectors #58a6ff, #3fb950, #f85149).\n"
        f"   - Staggered animations: TransformMatchingShapes, Create, FadeIn, Arrow indicators, and moving frame camera.\n"
        f"2. Synced Voiceover Transcript (`voiceover.md`):\n"
        f"   - Timestamped narrative script with visual sync markers (e.g., `[00:00 - FadeIn title]`, `[00:08 - Trigger pulse]`).\n"
        f"   - Phrased in clean, active voice (80% ASD-STE100 pace) matching scene durations.\n"
        f"3. Audio Narration Pipeline (`narrate.sh`):\n"
        f"   - {tts_guidance}\n"
        f"   - Command to combine Manim video + TTS audio using ffmpeg: `ffmpeg -i scene.mp4 -i narration.mp3 -c:v copy -c:a aac output_explainer.mp4`"
    )


def build_ladder_prompt(topic: str, tts_engine: str = "edge-tts") -> str:
    """Generate comprehensive multi-tier Karpathy Ladder of Understanding prompt."""
    return (
        f"# Complete Karpathy High-Bandwidth Explainer Package\n\n"
        f"Topic: {topic}\n\n"
        f"Execute all 4 rungs of Karpathy's Ladder of Understanding to provide total comprehension:\n\n"
        f"## Rung 1: Controlled Technical Summary (80% ASD-STE100)\n"
        f"{build_ste100_prompt(topic, softened=True)}\n\n"
        f"---\n\n"
        f"## Rung 2: Architecture & State Diagrams\n"
        f"{build_diagram_prompt(topic)}\n\n"
        f"---\n\n"
        f"## Rung 3: Discardable Interactive Single-File Web Artifact\n"
        f"{build_html_prompt(topic)}\n\n"
        f"---\n\n"
        f"## Rung 4: Bespoke 3b1b Explainer Video & Narration Pipeline\n"
        f"{build_video_prompt(topic, tts_engine=tts_engine)}\n"
    )


def lint_text(text: str) -> Dict:
    """Lint text against ASD-STE100 rules and return diagnostics."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    issues: List[Dict] = []
    
    for idx, s in enumerate(sentences, start=1):
        clean_s = s.strip()
        if not clean_s:
            continue
        words = clean_s.split()
        word_count = len(words)
        lower_s = clean_s.lower()

        # Check semicolon (STE Rule 8.1 strictly bans semicolons)
        if ";" in clean_s:
            issues.append({
                "sentence_index": idx,
                "type": "SEMICOLON_BANNED",
                "message": "STE bans the semicolon (Rule 8.1). Split into separate sentences.",
                "snippet": clean_s[:80] + "...",
            })

        # Check sentence length (max 25 for descriptive, 20 for procedural)
        if word_count > 25:
            issues.append({
                "sentence_index": idx,
                "type": "SENTENCE_TOO_LONG",
                "message": f"Sentence {idx} exceeds 25 words ({word_count} words). Shorten or split.",
                "snippet": clean_s[:80] + "..." if len(clean_s) > 80 else clean_s,
            })

        # Check unapproved words
        for unapproved, approved in STE_REPLACEMENTS.items():
            pattern = r"\b" + re.escape(unapproved) + r"\b"
            if re.search(pattern, lower_s):
                issues.append({
                    "sentence_index": idx,
                    "type": "UNAPPROVED_WORD",
                    "message": f"Unapproved word '{unapproved}' found. Replace with '{approved}'.",
                    "snippet": clean_s[:80] + "...",
                })

        # Check soft phrasal verbs (Rule 9.3)
        for phrasal, replacement in PHRASAL_VERBS.items():
            pattern = r"\b" + re.escape(phrasal) + r"\b"
            if re.search(pattern, lower_s):
                issues.append({
                    "sentence_index": idx,
                    "type": "PHRASAL_VERB",
                    "message": f"Soft phrasal verb '{phrasal}' found. Use single plain verb: '{replacement}'.",
                    "snippet": clean_s[:80] + "...",
                })

        # Check nominalizations (Rule 3.7)
        nom_pattern = r"\b(perform|conduct|carry out|carries out|performed|conducted)\s+(?:a|an|the)\s+\w+(?:tion|sion|ment|ance|ence|ysis)\b"
        nom_match = re.search(nom_pattern, lower_s)
        if nom_match:
            issues.append({
                "sentence_index": idx,
                "type": "NOMINALIZATION",
                "message": f"Nominalization '{nom_match.group(0)}' found. Use the direct action verb.",
                "snippet": clean_s[:80] + "...",
            })

        # Check AI filler buzzwords & marketing adjectives
        for buzzword in AI_BUZZWORDS:
            pattern = r"\b" + re.escape(buzzword) + r"\b"
            if re.search(pattern, lower_s):
                issues.append({
                    "sentence_index": idx,
                    "type": "AI_BUZZWORD",
                    "message": f"Marketing adjective / AI buzzword '{buzzword}' found. Delete or replace with plain fact.",
                    "snippet": clean_s[:80] + "...",
                })

        # Check progressive verb form (-ing) flag (heuristic)
        prog_matches = re.findall(r"\b(?:is|are|was|were|been)\s+(\w+ing)\b", lower_s)
        if prog_matches:
            issues.append({
                "sentence_index": idx,
                "type": "PROGRESSIVE_TENSE",
                "message": f"Progressive verb form '{' '.join(prog_matches)}' is not approved. Use simple present or past.",
                "snippet": clean_s[:80] + "...",
            })

        # Check passive voice (heuristic: be verb + past participle ending in -ed)
        passive_matches = re.findall(r"\b(?:is|are|was|were|be|been|being)\s+(\w+ed)\b", lower_s)
        if passive_matches:
            issues.append({
                "sentence_index": idx,
                "type": "PASSIVE_VOICE",
                "message": f"Possible passive voice '{' '.join(passive_matches)}'. Use active voice imperative.",
                "snippet": clean_s[:80] + "...",
            })

    return {
        "total_sentences": len(sentences),
        "total_issues": len(issues),
        "issues": issues,
        "score": max(0, 100 - (len(issues) * 10)),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Convert standard prompts into Karpathy high-bandwidth understanding prompts (ASD-STE100, Diagrams, HTML, 3b1b Video)."
    )
    parser.add_argument("prompt", nargs="?", default="", help="Input prompt, topic, or raw text to transform/lint.")
    parser.add_argument("--tier", choices=["ste100", "80-ste100", "diagram", "html", "video", "all"], default="all", help="Target ladder tier (default: all)")
    parser.add_argument("--tts", choices=["edge-tts", "elevenlabs", "macos-say"], default="edge-tts", help="TTS narration engine for video tier (default: edge-tts)")
    parser.add_argument("--lint", action="store_true", help="Run ASD-STE100 linter on input text instead of prompt compilation")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    # Read from stdin if prompt argument is empty or is '-'
    text = args.prompt
    if not text or text == "-":
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()

    if not text:
        parser.print_help()
        sys.exit(1)

    if args.lint:
        report = lint_text(text)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"=== ASD-STE100 Lint Report (Score: {report['score']}/100) ===")
            print(f"Total Sentences: {report['total_sentences']} | Total Issues: {report['total_issues']}\n")
            if not report["issues"]:
                print("No rule violations found. Text satisfies core STE-100 guidelines.")
            for issue in report["issues"]:
                print(f"[{issue['type']}] Sentence {issue['sentence_index']}: {issue['message']}")
                print(f"  > \"{issue['snippet']}\"\n")
        sys.exit(0 if report["total_issues"] == 0 else 1)

    # Prompt compilation mode
    tier = args.tier
    if tier == "ste100":
        compiled = build_ste100_prompt(text, softened=False)
    elif tier == "80-ste100":
        compiled = build_ste100_prompt(text, softened=True)
    elif tier == "diagram":
        compiled = build_diagram_prompt(text)
    elif tier == "html":
        compiled = build_html_prompt(text)
    elif tier == "video":
        compiled = build_video_prompt(text, tts_engine=args.tts)
    else:
        compiled = build_ladder_prompt(text, tts_engine=args.tts)

    if args.json:
        out = {
            "original_prompt": text,
            "target_tier": tier,
            "tts_engine": args.tts if tier in ["video", "all"] else None,
            "compiled_prompt": compiled,
        }
        print(json.dumps(out, indent=2))
    else:
        print(compiled)


if __name__ == "__main__":
    main()
