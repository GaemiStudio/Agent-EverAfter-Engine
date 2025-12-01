# Agent-EverAfter-Engine

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

Our project was built using a modular, agent-based architecture supported by Google’s AI Developer Kit (ADK). Each component of the system was designed to perform a specialized role while contributing to a unified workflow. The key tools and technologies used include:

Google ADK (AI Developer Kit)
Defines, orchestrates, and runs multiple cooperating agents. ADK provided a standardized way to create agents with clear roles, built-in support for state management, tracing, and structured output, and smooth integration of LLM calls inside custom logic.

Gemini Models
Our agents relied on Gemini 2.5 Flash Lite (and Flash where required) to handle:
Natural-language understanding, classification and extraction of relevant details, and generating structured JSON outputs used by other agents in the pipeline.

Python
Python served as the backbone for all implementation, allowing us to build sub-agents with isolated responsibilities, create shared utilities for memory and state tracking, run asynchronous logic where needed (e.g., preparing sessions).

Custom Shared Memory Manager
We implemented our own lightweight memory system to store user input across multiple steps, maintain a persistent wedding-planning state, and append notes and summaries for downstream use.

Modular Sub-Agent Design
We organized the workflow into focused sub-agents (e.g., intake, budget, creative) to keep the system clean, scalable, easy to build out.

## Conclusion

Through this project, we explored how multi-agent coordination, persistent memory, and structured output enforcement can turn a loosely defined problem—planning a wedding—into a reproducible, end-to-end workflow. This experience reinforced the value of clear agent roles, predictable delegation, and thoughtful system design when building reliable AI assistants. With more time, I would extend this architecture into deeper reasoning chains, cost modeling, and real-time external data retrieval, but the current system already demonstrates a strong proof-of-concept for domain-focused multi-agent pipelines. If we were to continue this project, our next build-out would be to refine the instructions for each agent to be even more precise and granular. As is shown in our architecture diagram, we would also explore making a robust memory_manager agent that would use an LLM to intelligently compact, call, and find patterns in the data from interactions. This would then feed in back to the main root agent to further refine and update the structure. We would also need to build a solid database that would keep memory long-term for a more personalized experience in both vector and graph databases.
