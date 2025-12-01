# Agent-Aisle-Buddy

Kaggle AI Agent Capstone Group Project

## Introduction

This project demonstrates a multi-agent AI system designed to support complete wedding planning from start to finish. Our primary agent functions as an orchestrator, delegating tasks to specialized sub-agents responsible for individual domains such as logistics, scheduling, food and vendor coordination, photography planning, and vow writing. Each agent focuses on its designated area of expertise, and the orchestrator aggregates their outputs into a unified, comprehensive solution for the user. This project highlights how coordinated AI agents can streamline complex workflows and deliver structured, end-to-end assistance for real-world planning scenarios.

## Diagram of Agent System

![Wedding Agent Diagram](https://github.com/user-attachments/assets/0aa2294b-5601-4720-a32d-805e084a3e7f)



## Problem

Planning a wedding is a complex, multi-layered process that requires coordinating countless details—timelines, budgets, vendors, logistics, aesthetics, photography, vows, and more. Couples often rely on numerous tools and spreadsheets to calculate costs, manage schedules, compare options, and track progress, which can quickly become overwhelming. Professional wedding planners can help, but their services are often expensive and out of reach for many couples.

## Solution

By leveraging AI to organize information, analyze needs, and automate decision-making, planning becomes more accessible, efficient, and less stressful. This allows couples to focus on the meaningful aspects of their day rather than managing the logistics behind it.

## Architecture

**MasterWeddingAgent (root)**

Orchestrates the whole flow.
Knows:
where wedding_state.json lives
where wedding_notes.txt lives
Calls needed agents.
Decides whether to:
run sub-agents sequentially, or
run some of them in parallel and returns a summary of what was generated (for UI / logs).

**Intake_Agent**

ADK Agent focused on turning messy couple input into structured JSON.
Outputs wedding_state JSON (full core state of the wedding).
Writes a short intake summary section into wedding_notes.txt

**Creative_Agent (writing related items)**

Reads wedding_state.json.
Outputs vows drafts, ceremony script outline, speech prompts / email templates.
Appends a “Creative / Writing Output” section to wedding_notes.txt.

**Photography_Agent**

Reads wedding_state.json.
Outputs:
Overview paragraph and detailed recs (coverage, shooters, timing, shot list highlights).
Optionally: structured JSON with package tiers.
Appends “Photography Recommendations” to wedding_notes.txt.

**Catering_Agent**

Reads wedding_state.json.
Outputs menu recommendations, service style (buffet, family-style, plated), timing with respect to ceremony/reception.
Appends “Catering Recommendations” to wedding_notes.txt.

**Budget_Agent**

Reads wedding_state.json.
Also optionally reads outputs from other agents (e.g. photo/catering packages) if you want.
Outputs allocated budget by category, possible “lean / standard / premium” options.
Appends “Budget Breakdown” to wedding_notes.txt.
Optionally:
Writes a small budget.json file for more structured downstream use.

Couple → (raw answers)
→ MasterWeddingAgent
→ IntakeAgent (Gemini via ADK)
→ wedding_state.json (core truth)
→ SubAgents (all read wedding_state.json)
→ each sub-agent outputs text
→ all append to wedding_notes.txt
→ MasterWeddingAgent returns outputs + file paths to your app

## Core Tools

## Conclusion

