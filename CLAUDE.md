# LangCode: Python Clone of OpenCode

## Mission

Create a Python clone of OpenCode CLI where every function, prompt, tool, and behavior matches the original exactly. No simplifications, no interpretations.

## Source and Target

- Source: ./opencode/ (TypeScript/JavaScript)
- Target: Python 3.11+ with async/await

## Required Technology Stack

- Agent Framework: LangChain
- CLI: Typer + Rich
- API: FastAPI + Uvicorn
- Storage: SQLAlchemy (async) + SQLite
- Package Manager: uv

## Core Principles

### 1. Accuracy First

Reproduce OpenCode behavior exactly before any optimization. When in doubt, match OpenCode precisely.

### 2. Prompts

Copy prompt text word-for-word. Preserve all formatting, whitespace, and structure. Never modify prompt content.

### 3. Tools

Match signatures, outputs, and error handling exactly. Same inputs must produce same outputs.

### 4. Configuration

Use compatible format (TOML instead of JSONC) but provide migration script. All config options must be supported.

### 5. Modularity

Separate core logic from CLI/UI layers for maintainability.

## Implementation Workflow

CRITICAL: This workflow must be followed strictly for every module.

### Step-by-Step Process

For each module in docs/IMPLEMENTATION_PLAN.md:

1. READ the OpenCode source code for that module
2. IMPLEMENT the Python equivalent
3. WRITE unit tests
4. PERFORM self-review using checklist below
5. UPDATE docs/IMPLEMENTATION_PLAN.md with completion status
6. STOP and WAIT for user approval
7. PROCEED to next module only after user approves

### Self-Review Checklist

Before marking a module complete, verify:

- All functions and classes from OpenCode are present
- Function signatures match (parameters, return types)
- Behavior is identical (same inputs produce same outputs)
- Error handling matches
- Edge cases handled identically
- Constants and defaults match
- Relevant comments preserved
- Tests cover all functionality
- No additional features added
- No simplifications made

### Strict Rules

DO NOT work on multiple modules simultaneously
DO NOT skip modules in the sequence
DO NOT proceed to next module without user approval
DO NOT simplify or "improve" OpenCode code
DO NOT add features not present in OpenCode

### Progress Tracking

Before starting work:
- Open docs/IMPLEMENTATION_PLAN.md
- Find current module (first with status NOT STARTED)
- Verify previous module has "Approved by user: YES"
- Only then begin work

After completing module:
- Perform self-review
- Update module status in IMPLEMENTATION_PLAN.md
- Write brief completion report
- STOP and wait for user approval
- Do not start next module

## Tool Usage Guidelines

- Use parallel tool calls for independent operations
- Delegate large research to Explore agent
- Use Plan agent for complex module design
- Keep main context clean, use subagents for deep dives

## Quality Standards

- Run /simplify after each module if needed
- Write tests alongside implementation
- Continuously validate against OpenCode behavior
- Document all architectural decisions in docs/DECISIONS.md

## Communication

- Provide brief updates after each module
- Escalate blockers or uncertainties immediately
- Ask when uncertain, never assume
- Document all deviations in docs/DECISIONS.md with justification

## Why This Workflow Matters

This strict process ensures:
- Exact compliance with OpenCode
- No drift from original behavior
- Quality of each module
- Early problem detection
- Progress transparency
- User control at every step

## Reference Documents

- docs/ANALYSIS.md - OpenCode architecture analysis
- docs/DESIGN.md - Python implementation design
- docs/DECISIONS.md - Architectural decisions
- docs/IMPLEMENTATION_PLAN.md - Detailed module-by-module plan
- docs/REFERENCES/TOOLS.md - Tool catalog
- docs/REFERENCES/PROMPTS.md - Prompt system details
- docs/REFERENCES/DEPENDENCIES.md - npm to Python mapping

## Current Status

Always check docs/IMPLEMENTATION_PLAN.md for current module and approval status before beginning work.
