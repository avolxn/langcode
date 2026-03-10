# LangCode: Python Clone of OpenCode

## Mission
Create a 1:1 functional Python clone of OpenCode CLI. Every feature, prompt, tool, and behavior must match the original exactly. No simplifications, no interpretations.

## Source
- **Path:** `./opencode/` (TypeScript/JavaScript)
- **Target:** Python 3.11+ with async/await

## Tech Stack (Required)
- **Agent Framework:** LangChain + LangGraph
- **CLI:** Typer + Rich
- **API:** FastAPI + Uvicorn (for MCP/LSP)
- **Storage:** SQLAlchemy (async) + SQLite
- **Package Manager:** uv
- **Core Libraries:** anthropic, pydantic, aiofiles, httpx, prompt_toolkit, tree-sitter

## Non-Negotiable Rules
1. **Fidelity First:** Match OpenCode behavior exactly before optimizing
2. **Prompts:** Copy word-for-word, preserve all formatting
3. **Tools:** Identical signatures, outputs, and error handling
4. **Config:** Compatible format or provide migration script
5. **Modular:** Separate core logic from CLI/UI layers

---

## Phase 1: Deep Analysis

**Goal:** Complete understanding of OpenCode architecture, no coding yet.

**Tasks:**
1. Use Explore agent (very thorough) on `./opencode/` to map:
   - Entry points and module structure
   - Tool registration and execution flow
   - Prompt system (storage, templating, composition)
   - State management and memory system
   - MCP/LSP integration
   - Configuration schema

2. Analyze in parallel:
   - All TypeScript files (focus on core modules)
   - package.json dependencies
   - Test structure and coverage
   - Build/deployment scripts

**Deliverables:**
- `docs/MIGRATION_MAP.md` - **CRITICAL:** Complete file-by-file mapping (all 244 TS files):
  - Each TypeScript file → Python module path
  - Purpose and responsibilities of each file
  - Dependencies between files
  - Which files can be skipped (desktop/web UI, etc.)
- `docs/ARCHITECTURE.md` - Python project structure and module organization
- `docs/DEPENDENCIES.md` - npm → Python package mapping with justification
- `docs/PROMPTS.md` - Prompt system documentation (where stored, how loaded, templating)
- `docs/TOOLS.md` - Complete tool catalog with signatures, parameters, behaviors

**Success Criteria:**
- Can explain every OpenCode feature without looking at code
- Clear Python module structure defined
- All dependencies mapped
- Zero ambiguity about what to build

---

## Phase 2: Project Scaffold

**Prerequisites:** Phase 1 approved by user

**Tasks:**
1. Initialize: `uv init langcode && cd langcode && uv python pin 3.11`
2. Configure pyproject.toml (metadata, deps, dev tools, entry points)
3. Create directory structure from ARCHITECTURE.md
4. Setup tooling: ruff, mypy, pytest, .gitignore
5. Create `__init__.py` files with module docstrings

**Deliverables:**
- Working project skeleton
- `uv run langcode --version` executes
- `uv run pytest` discovers tests
- All dependencies installed

---

## Phase 3: Core Implementation

**Process per module:**
1. Read original TypeScript (use parallel reads for related files)
2. Identify all functions, classes, types
3. Implement Python equivalent with type hints
4. Write unit tests (match OpenCode test coverage)
5. Validate behavior against OpenCode

**Priority Order:**
1. Configuration and settings
2. Tool system (registration, execution, validation)
3. Prompt system (loading, templating, composition)
4. Agent core (LangGraph workflow)
5. CLI commands (Typer routes)
6. Storage layer (SQLAlchemy models)
7. MCP/LSP integration
8. Memory system

**Per-Module Checklist:**
- [ ] TypeScript code analyzed
- [ ] Python implementation complete
- [ ] Type hints added (Pydantic where appropriate)
- [ ] Unit tests written and passing
- [ ] Behavior validated against OpenCode
- [ ] Run `/simplify` skill for code review

---

## Phase 4: Integration & Testing

**Tasks:**
1. End-to-end workflow tests
2. CLI command integration tests
3. Tool execution tests (all tools)
4. Prompt rendering tests
5. Performance benchmarking vs OpenCode

**Success Criteria:**
- All OpenCode commands work identically
- All tools produce same outputs
- Prompts render identically
- Config files compatible
- Performance within 20% of OpenCode

---

## Phase 5: Documentation

**Deliverables:**
- README.md (installation, usage, examples)
- MIGRATION.md (deviations, rationale, compatibility notes)
- API docs (if exposing programmatic interface)
- User guide (mirror OpenCode docs)

---

## Execution Guidelines

**Tool Usage:**
- Use parallel tool calls for independent operations
- Delegate large explorations to Explore agent
- Use Plan agent for complex module design
- Keep main context clean, use subagents for deep dives

**Quality:**
- Run `/simplify` after each module
- Write tests alongside implementation
- Validate against OpenCode continuously

**Communication:**
- Brief updates after each module
- Immediate escalation of blockers or ambiguities
- Document architectural decisions in `docs/DECISIONS.md`

**Critical Rules:**
- Don't code until Phase 1 is complete and approved
- Test each module against OpenCode before moving on
- Ask when uncertain, never assume
- Keep migration notes for all deviations

---

## Current Status
**Phase:** Not started
**Next Action:** Await user approval to begin Phase 1