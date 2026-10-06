#!/usr/bin/env python3
"""
Self-check test suite for karpathy-explainer compiler and STE-100 linter.
Standard library only, assert-based, zero extra test frameworks.
"""

import os
import sys

# Ensure scripts dir is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
import compile_prompt


def test_ste100_prompt_generation():
    topic = "PostgreSQL Write-Ahead Logging"
    p_strict = compile_prompt.build_ste100_prompt(topic, softened=False)
    assert "Strict ASD-STE100" in p_strict
    assert "Procedural sentences <= 20 words" in p_strict
    assert topic in p_strict

    p_soft = compile_prompt.build_ste100_prompt(topic, softened=True)
    assert "80% ASD-STE100" in p_soft
    assert "Retain all technical domain nouns" in p_soft


def test_diagram_prompt_generation():
    topic = "Raft Leader Election"
    p = compile_prompt.build_diagram_prompt(topic)
    assert "Mermaid.js" in p
    assert topic in p
    assert "sequenceDiagram" in p or "flowchart TD" in p


def test_html_prompt_generation():
    topic = "B-Tree Node Splitting"
    p = compile_prompt.build_html_prompt(topic)
    assert "single-file HTML" in p
    assert "Interactive Micro-Simulator" in p
    assert topic in p


def test_video_prompt_generation():
    topic = "Attention Mechanism in Transformers"
    p_edge = compile_prompt.build_video_prompt(topic, tts_engine="edge-tts")
    assert "Manim" in p_edge
    assert "edge-tts" in p_edge

    p_11 = compile_prompt.build_video_prompt(topic, tts_engine="elevenlabs")
    assert "ElevenLabs" in p_11

    p_mac = compile_prompt.build_video_prompt(topic, tts_engine="macos-say")
    assert "say -v" in p_mac


def test_ste100_linter():
    # Dirty sentence with multiple violations:
    # 1. > 25 words
    # 2. Unapproved word 'ensure', 'utilize', 'prior to'
    # 3. AI buzzword 'delve', 'leverage'
    dirty_text = (
        "It is imperative that the operator ensures that the primary database node utilizes modern sharding techniques "
        "prior to commencing operations so we can delve into the architecture and leverage our seamless cutting-edge data pipeline."
    )
    report = compile_prompt.lint_text(dirty_text)
    assert report["total_issues"] > 0
    issue_types = {i["type"] for i in report["issues"]}
    assert "SENTENCE_TOO_LONG" in issue_types
    assert "UNAPPROVED_WORD" in issue_types
    assert "AI_BUZZWORD" in issue_types

    # Test new rules: semicolon, nominalization, phrasal verb
    rule_violation_text = "Spin up the container; then perform an analysis of the log."
    v_report = compile_prompt.lint_text(rule_violation_text)
    v_types = {i["type"] for i in v_report["issues"]}
    assert "SEMICOLON_BANNED" in v_types
    assert "PHRASAL_VERB" in v_types
    assert "NOMINALIZATION" in v_types

    # Clean STE procedural sentence: <=20 words, active, approved words
    clean_text = "Make sure that the hydraulic reservoir is full before you start the operation."
    clean_report = compile_prompt.lint_text(clean_text)
    assert clean_report["total_issues"] == 0
    assert clean_report["score"] == 100


if __name__ == "__main__":
    test_ste100_prompt_generation()
    test_diagram_prompt_generation()
    test_html_prompt_generation()
    test_video_prompt_generation()
    test_ste100_linter()
    print("ALL TESTS PASSED: compile_prompt and STE-100 validator verified successfully.")
