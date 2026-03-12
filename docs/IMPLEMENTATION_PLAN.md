# LangCode Implementation Plan

## Critical Rules

⚠️ **MANDATORY WORKFLOW - DO NOT DEVIATE**

1. **Module-by-Module Transfer**: Implement ONE module at a time, in order
2. **Exact Compliance**: Each module must match OpenCode behavior exactly
3. **Self-Review Required**: After completing a module, perform thorough self-review
4. **User Approval Required**: Wait for user approval before proceeding to next module
5. **No Skipping**: Cannot skip ahead or work on multiple modules simultaneously

## Implementation Workflow

For each module:

```
┌─────────────────────────────────────────────────────────┐
│ 1. READ OpenCode source for module                      │
│ 2. IMPLEMENT Python equivalent                          │
│ 3. WRITE unit tests                                     │
│ 4. SELF-REVIEW against OpenCode                         │
│ 5. DOCUMENT completion in this file                     │
│ 6. ⏸️  WAIT for user approval                           │
│ 7. ✅ Proceed to next module only after approval        │
└─────────────────────────────────────────────────────────┘
```

## Self-Review Checklist

After implementing each module, verify:

- [ ] All functions/classes from OpenCode are present
- [ ] Function signatures match (parameters, return types)
- [ ] Behavior is identical (same inputs → same outputs)
- [ ] Error handling matches
- [ ] Edge cases handled identically
- [ ] Constants and defaults match
- [ ] Comments preserved where relevant
- [ ] Tests cover all functionality
- [ ] No additional features added
- [ ] No simplifications made

## Phase 1: Foundation

### Module 1.1: Project Setup - COMPLETED

**OpenCode Reference**: `package.json`, project structure

**Tasks**:
- [x] Initialize uv project
- [x] Create directory structure
- [x] Set up pyproject.toml with dependencies
- [x] Configure ruff (linting/formatting)
- [x] Configure mypy (type checking)
- [x] Set up pytest
- [x] Create .gitignore
- [x] Create README.md

**Files Created**:
- `pyproject.toml` (with all dependencies)
- `src/langcode/__init__.py`
- `src/langcode/__main__.py`
- `.python-version`
- Configuration in `pyproject.toml` (ruff, mypy, pytest sections)
- `.gitignore`
- `README.md`
- Directory structure: cli, server, session, tool, skill, provider, mcp, lsp, storage, config, permission, plugin, project, bus, util, types
- `tests/` directory with conftest.py

**Verification**:
- [x] `uv run python -m langcode` works (outputs version info)
- [x] `uv run pytest` runs (0 tests collected, as expected)
- [x] `uv run ruff check .` passes (All checks passed!)
- [x] `uv run mypy src/` passes (Success: no issues found in 18 source files)

**Self-Review**:
- [x] All required files created
- [x] Dependencies match DEPENDENCIES.md specification
- [x] Directory structure matches DESIGN.md
- [x] Configuration tools (ruff, mypy, pytest) properly configured
- [x] Entry point works correctly
- [x] All verification steps pass
- [x] No additional features added
- [x] Setup follows Python best practices

**Status**: COMPLETED
**Completed**: 2026-03-13
**Approved by user**: AWAITING APPROVAL

---

### Module 1.2: Core Types & Schemas ⏳ NOT STARTED

**OpenCode Reference**: `src/types/`, Zod schemas

**Tasks**:
- [ ] Create Pydantic models for core types
- [ ] Message, Part, Session types
- [ ] Tool parameter schemas
- [ ] Provider types
- [ ] Config types

**Files to Create**:
- `src/langcode/types/__init__.py`
- `src/langcode/types/schemas.py`
- `src/langcode/types/message.py`
- `src/langcode/types/tool.py`
- `src/langcode/types/provider.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/storage/schema.ts`
- `packages/opencode/src/tool/tool.ts`
- `packages/opencode/src/provider/provider.ts`

**Verification**:
- [ ] All Zod schemas have Pydantic equivalents
- [ ] Validation behavior matches
- [ ] JSON serialization works
- [ ] Type hints are correct

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 1.3: Utilities ⏳ NOT STARTED

**OpenCode Reference**: `src/util/`

**Tasks**:
- [ ] Filesystem utilities
- [ ] Logging setup
- [ ] Path handling
- [ ] Glob matching
- [ ] Ripgrep wrapper

**Files to Create**:
- `src/langcode/util/__init__.py`
- `src/langcode/util/filesystem.py`
- `src/langcode/util/log.py`
- `src/langcode/util/glob.py`
- `src/langcode/util/ripgrep.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/util/filesystem.ts`
- `packages/opencode/src/util/log.ts`
- `packages/opencode/src/util/glob.ts`

**Verification**:
- [ ] File operations work identically
- [ ] Glob patterns match same files
- [ ] Ripgrep output format matches
- [ ] Logging format matches

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 2: Storage Layer

### Module 2.1: Database Models ⏳ NOT STARTED

**OpenCode Reference**: `src/storage/schema.ts`

**Tasks**:
- [ ] Create SQLAlchemy models
- [ ] Session, Message, Part tables
- [ ] Todo, Permission tables
- [ ] Relationships and indexes
- [ ] Match Drizzle schema exactly

**Files to Create**:
- `src/langcode/storage/__init__.py`
- `src/langcode/storage/models.py`
- `src/langcode/storage/schema.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/storage/schema.ts`

**Verification**:
- [ ] Table structure matches Drizzle schema
- [ ] Column types match
- [ ] Indexes match
- [ ] Relationships match
- [ ] Can read OpenCode database

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 2.2: Database Setup & Migrations ⏳ NOT STARTED

**OpenCode Reference**: `src/storage/db.ts`, `src/storage/migrations/`

**Tasks**:
- [ ] Database initialization
- [ ] Connection management
- [ ] Migration system (Alembic)
- [ ] Initial migration matching OpenCode schema

**Files to Create**:
- `src/langcode/storage/db.py`
- `src/langcode/storage/migrations/`
- `alembic.ini`

**OpenCode Files to Reference**:
- `packages/opencode/src/storage/db.ts`
- `packages/opencode/src/storage/migrations/`

**Verification**:
- [ ] Database file location matches
- [ ] Schema matches OpenCode exactly
- [ ] Can migrate from empty database
- [ ] Can read existing OpenCode database

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 3: Configuration System

### Module 3.1: Config Loading ⏳ NOT STARTED

**OpenCode Reference**: `src/config/config.ts`

**Tasks**:
- [ ] Hierarchical config loading (7 levels)
- [ ] TOML/JSON parsing
- [ ] Deep merge logic
- [ ] Environment variable overrides
- [ ] Remote config fetching

**Files to Create**:
- `src/langcode/config/__init__.py`
- `src/langcode/config/loader.py`
- `src/langcode/config/schema.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/config/config.ts`

**Verification**:
- [ ] Config hierarchy matches (7 levels)
- [ ] Merge behavior identical
- [ ] All config options supported
- [ ] Precedence order correct

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 3.2: Config Migration Script ⏳ NOT STARTED

**OpenCode Reference**: JSONC config format

**Tasks**:
- [ ] Create JSONC → TOML migration script
- [ ] Handle all config options
- [ ] Preserve comments where possible
- [ ] Validate converted config

**Files to Create**:
- `scripts/migrate_config.py`
- Documentation in README

**Verification**:
- [ ] Can convert OpenCode config to TOML
- [ ] All options preserved
- [ ] Config loads correctly after migration

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 4: Tool System

### Module 4.1: Tool Base & Context ⏳ NOT STARTED

**OpenCode Reference**: `src/tool/tool.ts`, `src/tool/schema.ts`

**Tasks**:
- [ ] Tool base class (ABC)
- [ ] Tool context class
- [ ] Tool result class
- [ ] Permission request interface
- [ ] Metadata tracking

**Files to Create**:
- `src/langcode/tool/__init__.py`
- `src/langcode/tool/base.py`
- `src/langcode/tool/context.py`
- `src/langcode/tool/result.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/tool/tool.ts`
- `packages/opencode/src/tool/schema.ts`

**Verification**:
- [ ] Tool interface matches OpenCode
- [ ] Context provides all required methods
- [ ] Result format identical
- [ ] Type hints correct

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 4.2: Tool Registry ⏳ NOT STARTED

**OpenCode Reference**: `src/tool/registry.ts`

**Tasks**:
- [ ] Tool registration system
- [ ] Tool discovery (builtin, custom, plugins)
- [ ] Model-specific filtering
- [ ] Tool loading and initialization

**Files to Create**:
- `src/langcode/tool/registry.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/tool/registry.ts`

**Verification**:
- [ ] Discovery paths match OpenCode
- [ ] Loading order correct
- [ ] Filtering logic identical
- [ ] Can load custom tools

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 4.3: Output Truncation ⏳ NOT STARTED

**OpenCode Reference**: `src/tool/truncation.ts`

**Tasks**:
- [ ] Output size limits
- [ ] Truncation logic
- [ ] File writing for large outputs
- [ ] Metadata tracking

**Files to Create**:
- `src/langcode/tool/truncation.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/tool/truncation.ts`

**Verification**:
- [ ] Limits match (2000 lines, 50KB)
- [ ] Truncation behavior identical
- [ ] File paths match format
- [ ] Metadata correct

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 4.4: Tool - bash ⏳ NOT STARTED

**OpenCode Reference**: `src/tool/bash.ts`

**Tasks**:
- [ ] Command execution with asyncio.subprocess
- [ ] Tree-sitter parsing for permissions
- [ ] Timeout handling (default 2min, max 10min)
- [ ] Output capture (stdout/stderr)
- [ ] Exit code handling

**Files to Create**:
- `src/langcode/tool/builtin/__init__.py`
- `src/langcode/tool/builtin/bash.py`
- `src/langcode/tool/descriptions/bash.txt` (copy from OpenCode)

**OpenCode Files to Reference**:
- `packages/opencode/src/tool/bash.ts`
- `packages/opencode/src/tool/bash.txt`

**Verification**:
- [ ] Command execution identical
- [ ] Timeout behavior matches
- [ ] Output format matches
- [ ] Error handling identical
- [ ] Tree-sitter parsing works

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 4.5: Tool - read ⏳ NOT STARTED

**OpenCode Reference**: `src/tool/read.ts`

**Tasks**:
- [ ] File reading with line numbers (cat -n format)
- [ ] Directory listing
- [ ] Pagination (offset/limit, default 2000 lines)
- [ ] Line truncation (2000 chars)
- [ ] File suggestions on not found

**Files to Create**:
- `src/langcode/tool/builtin/read.py`
- `src/langcode/tool/descriptions/read.txt` (copy from OpenCode)

**OpenCode Files to Reference**:
- `packages/opencode/src/tool/read.ts`
- `packages/opencode/src/tool/read.txt`

**Verification**:
- [ ] Output format matches exactly (cat -n style)
- [ ] Directory listing identical
- [ ] Pagination works correctly
- [ ] Suggestions match OpenCode

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 4.6: Tool - write ⏳ NOT STARTED

**OpenCode Reference**: `src/tool/write.ts`

**Tasks**:
- [ ] File writing (create/overwrite)
- [ ] Diff generation for permissions
- [ ] LSP diagnostics integration
- [ ] File locking
- [ ] Permission checking

**Files to Create**:
- `src/langcode/tool/builtin/write.py`
- `src/langcode/tool/descriptions/write.txt` (copy from OpenCode)

**OpenCode Files to Reference**:
- `packages/opencode/src/tool/write.ts`
- `packages/opencode/src/tool/write.txt`

**Verification**:
- [ ] Write behavior identical
- [ ] Diff format matches
- [ ] Diagnostics output matches (max 20 per file, 5 files)
- [ ] Locking works correctly

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 4.7: Tool - edit ⏳ NOT STARTED

**OpenCode Reference**: `src/tool/edit.ts`

**Tasks**:
- [ ] Exact string replacement
- [ ] Uniqueness check (fails if multiple matches without replaceAll)
- [ ] replaceAll support
- [ ] Diff generation
- [ ] Error messages with context

**Files to Create**:
- `src/langcode/tool/builtin/edit.py`
- `src/langcode/tool/descriptions/edit.txt` (copy from OpenCode)

**OpenCode Files to Reference**:
- `packages/opencode/src/tool/edit.ts`
- `packages/opencode/src/tool/edit.txt`

**Verification**:
- [ ] Replacement logic identical
- [ ] Error messages match exactly
- [ ] Context display matches
- [ ] Line ending handling correct

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 4.8: Tool - glob ⏳ NOT STARTED

**OpenCode Reference**: `src/tool/glob.ts`

**Tasks**:
- [ ] Pattern matching with ripgrep
- [ ] Result sorting by modification time
- [ ] Result limiting (100 files)
- [ ] Absolute path output

**Files to Create**:
- `src/langcode/tool/builtin/glob.py`
- `src/langcode/tool/descriptions/glob.txt` (copy from OpenCode)

**OpenCode Files to Reference**:
- `packages/opencode/src/tool/glob.ts`
- `packages/opencode/src/tool/glob.txt`

**Verification**:
- [ ] Pattern matching identical
- [ ] Sorting matches OpenCode
- [ ] Limit behavior correct
- [ ] Output format matches

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 4.9: Tool - grep ⏳ NOT STARTED

**OpenCode Reference**: `src/tool/grep.ts`

**Tasks**:
- [ ] Ripgrep integration
- [ ] Regex pattern searching
- [ ] File filtering (include parameter)
- [ ] Output parsing (file:line:content)

**Files to Create**:
- `src/langcode/tool/builtin/grep.py`
- `src/langcode/tool/descriptions/grep.txt` (copy from OpenCode)

**OpenCode Files to Reference**:
- `packages/opencode/src/tool/grep.ts`
- `packages/opencode/src/tool/grep.txt`

**Verification**:
- [ ] Search behavior identical
- [ ] Output format matches
- [ ] Exit code handling correct (0=found, 1=not found, 2=errors)
- [ ] Error handling matches

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 4.10: Tool - websearch ⏳ NOT STARTED

**OpenCode Reference**: `src/tool/websearch.ts`

**Tasks**:
- [ ] Exa API integration
- [ ] Search query handling
- [ ] Result formatting (markdown)
- [ ] Availability check (zen users only)

**Files to Create**:
- `src/langcode/tool/builtin/websearch.py`
- `src/langcode/tool/descriptions/websearch.txt` (copy from OpenCode)

**OpenCode Files to Reference**:
- `packages/opencode/src/tool/websearch.ts`

**Verification**:
- [ ] API calls identical
- [ ] Result format matches
- [ ] Availability logic correct

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 4.11: Tool - webfetch ⏳ NOT STARTED

**OpenCode Reference**: `src/tool/webfetch.ts`

**Tasks**:
- [ ] URL fetching with httpx
- [ ] HTML to Markdown conversion
- [ ] 15-minute cache
- [ ] Redirect handling

**Files to Create**:
- `src/langcode/tool/builtin/webfetch.py`
- `src/langcode/tool/descriptions/webfetch.txt` (copy from OpenCode)

**OpenCode Files to Reference**:
- `packages/opencode/src/tool/webfetch.ts`

**Verification**:
- [ ] Fetch behavior identical
- [ ] Markdown conversion matches
- [ ] Cache works correctly

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 4.12: Tool - skill ⏳ NOT STARTED

**OpenCode Reference**: `src/tool/skill.ts`

**Tasks**:
- [ ] Skill loading by name
- [ ] Skill content return
- [ ] Integration with skill registry

**Files to Create**:
- `src/langcode/tool/builtin/skill.py`
- `src/langcode/tool/descriptions/skill.txt` (copy from OpenCode)

**OpenCode Files to Reference**:
- `packages/opencode/src/tool/skill.ts`

**Verification**:
- [ ] Loading behavior identical
- [ ] Output format matches

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 4.13: Tool - task ⏳ NOT STARTED

**OpenCode Reference**: `src/tool/task.ts`

**Tasks**:
- [ ] Task CRUD operations (create, update, list, get)
- [ ] Dependency tracking (blocks/blockedBy)
- [ ] Status management (pending, in_progress, completed, deleted)
- [ ] Metadata handling

**Files to Create**:
- `src/langcode/tool/builtin/task.py`
- `src/langcode/tool/descriptions/task.txt` (copy from OpenCode)

**OpenCode Files to Reference**:
- `packages/opencode/src/tool/task.ts`

**Verification**:
- [ ] All operations work identically
- [ ] Dependencies tracked correctly
- [ ] Status transitions match

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 4.14: Tool - todo ⏳ NOT STARTED

**OpenCode Reference**: `src/tool/todo.ts`

**Tasks**:
- [ ] Todo creation (write)
- [ ] Todo reading (read)
- [ ] Status management

**Files to Create**:
- `src/langcode/tool/builtin/todo.py`
- `src/langcode/tool/descriptions/todo.txt` (copy from OpenCode)

**OpenCode Files to Reference**:
- `packages/opencode/src/tool/todo.ts`

**Verification**:
- [ ] CRUD operations identical
- [ ] Storage format matches

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 4.15: Tool - question ⏳ NOT STARTED

**OpenCode Reference**: `src/tool/question.ts`

**Tasks**:
- [ ] Question display with Rich
- [ ] Option handling (single/multi-select)
- [ ] Preview support
- [ ] Response collection

**Files to Create**:
- `src/langcode/tool/builtin/question.py`
- `src/langcode/tool/descriptions/question.txt` (copy from OpenCode)

**OpenCode Files to Reference**:
- `packages/opencode/src/tool/question.ts`

**Verification**:
- [ ] UI behavior matches
- [ ] Response format identical
- [ ] Multi-select works correctly

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 5: Skill System

### Module 5.1: Skill Loader ⏳ NOT STARTED

**OpenCode Reference**: `src/skill/skill.ts`

**Tasks**:
- [ ] Skill discovery from multiple locations
- [ ] YAML frontmatter parsing
- [ ] Skill validation
- [ ] Duplicate handling (later overwrites earlier)

**Files to Create**:
- `src/langcode/skill/__init__.py`
- `src/langcode/skill/loader.py`
- `src/langcode/skill/discovery.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/skill/skill.ts`

**Discovery Locations** (in order):
1. `~/.claude/skills/`, `~/.agents/skills/`
2. `.claude/skills/`, `.agents/skills/`
3. `.opencode/skill/`, `.opencode/skills/`
4. Config paths: `config.skills.paths`
5. Remote URLs: `config.skills.urls`

**Verification**:
- [ ] Discovery order matches OpenCode
- [ ] Frontmatter parsing identical
- [ ] Duplicate handling correct
- [ ] Can load from all locations

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 5.2: Skill Formatter ⏳ NOT STARTED

**OpenCode Reference**: `src/skill/skill.ts` (formatting functions)

**Tasks**:
- [ ] Verbose XML format for system prompt
- [ ] Compact markdown format for tool description
- [ ] Skill list formatting

**Files to Create**:
- `src/langcode/skill/formatter.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/skill/skill.ts`

**Verification**:
- [ ] XML format matches exactly
- [ ] Markdown format matches exactly
- [ ] Used in correct contexts

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 6: Provider Layer

### Module 6.1: Provider Base & Factory ⏳ NOT STARTED

**OpenCode Reference**: `src/provider/provider.ts`

**Tasks**:
- [ ] Provider interface/protocol
- [ ] Provider factory
- [ ] Model selection logic
- [ ] Authentication handling

**Files to Create**:
- `src/langcode/provider/__init__.py`
- `src/langcode/provider/base.py`
- `src/langcode/provider/factory.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/provider/provider.ts`

**Verification**:
- [ ] Provider interface matches
- [ ] Factory creates correct providers
- [ ] Model selection identical

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 6.2: Anthropic Provider ⏳ NOT STARTED

**OpenCode Reference**: `@ai-sdk/anthropic` usage

**Tasks**:
- [ ] LangChain Anthropic integration
- [ ] Claude model support
- [ ] Streaming support
- [ ] Tool calling

**Files to Create**:
- `src/langcode/provider/anthropic.py`

**Verification**:
- [ ] API calls identical
- [ ] Streaming works
- [ ] Tool calling matches

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 6.3: OpenAI Provider ⏳ NOT STARTED

**OpenCode Reference**: `@ai-sdk/openai` usage

**Tasks**:
- [ ] LangChain OpenAI integration
- [ ] GPT model support (GPT-4, GPT-5, O1, O3)
- [ ] Streaming support
- [ ] Tool calling

**Files to Create**:
- `src/langcode/provider/openai.py`

**Verification**:
- [ ] API calls identical
- [ ] All models supported
- [ ] Tool format correct (apply_patch for non-GPT-4)

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 6.4: Google Provider ⏳ NOT STARTED

**OpenCode Reference**: `@ai-sdk/google` usage

**Tasks**:
- [ ] LangChain Google integration
- [ ] Gemini model support
- [ ] Streaming support
- [ ] Tool calling

**Files to Create**:
- `src/langcode/provider/google.py`

**Verification**:
- [ ] API calls identical
- [ ] Gemini models work
- [ ] Tool calling matches

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 7: Session Management

### Module 7.1: System Prompts ⏳ NOT STARTED

**OpenCode Reference**: `src/session/system.ts`, `src/session/prompt/*.txt`

**Tasks**:
- [ ] Copy all prompt files exactly (anthropic.txt, beast.txt, gemini.txt, etc.)
- [ ] Prompt selection logic
- [ ] Environment context generation
- [ ] Skills prompt integration

**Files to Create**:
- `src/langcode/session/__init__.py`
- `src/langcode/session/system.py`
- `src/langcode/session/prompts/anthropic.txt` (copy)
- `src/langcode/session/prompts/beast.txt` (copy)
- `src/langcode/session/prompts/gemini.txt` (copy)
- `src/langcode/session/prompts/codex_header.txt` (copy)
- `src/langcode/session/prompts/trinity.txt` (copy)
- `src/langcode/session/prompts/qwen.txt` (copy)

**OpenCode Files to Reference**:
- `packages/opencode/src/session/system.ts`
- `packages/opencode/src/session/prompt/*.txt`

**Verification**:
- [ ] All prompt files copied exactly (character-by-character)
- [ ] Selection logic matches
- [ ] Environment context format identical
- [ ] Skills integration correct

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 7.2: Session Manager ⏳ NOT STARTED

**OpenCode Reference**: `src/session/index.ts`

**Tasks**:
- [ ] Session lifecycle management
- [ ] Message storage
- [ ] Part storage
- [ ] Session state tracking

**Files to Create**:
- `src/langcode/session/manager.py`
- `src/langcode/session/message.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/session/index.ts`

**Verification**:
- [ ] Session CRUD operations identical
- [ ] Message hierarchy correct
- [ ] State tracking matches

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 7.3: LangChain Integration ⏳ NOT STARTED

**OpenCode Reference**: AI SDK usage in `src/session/`

**Tasks**:
- [ ] LangChain agent setup
- [ ] Tool integration with LangChain
- [ ] Streaming response handling
- [ ] Message loop

**Files to Create**:
- `src/langcode/session/agent.py`
- `src/langcode/session/executor.py`

**Verification**:
- [ ] Agent behavior matches OpenCode
- [ ] Tool calling works correctly
- [ ] Streaming matches
- [ ] Message format identical

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 8: MCP Integration

### Module 8.1: MCP Client ⏳ NOT STARTED

**OpenCode Reference**: `src/mcp/index.ts`

**Tasks**:
- [ ] MCP SDK integration (Python)
- [ ] Remote server support (HTTP/SSE)
- [ ] Local server support (stdio)
- [ ] Connection management
- [ ] Tool conversion (MCP → LangChain format)

**Files to Create**:
- `src/langcode/mcp/__init__.py`
- `src/langcode/mcp/client.py`
- `src/langcode/mcp/converter.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/mcp/index.ts`

**Verification**:
- [ ] Can connect to MCP servers
- [ ] Tool conversion correct
- [ ] Resource reading works
- [ ] Prompt execution works

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 8.2: MCP OAuth ⏳ NOT STARTED

**OpenCode Reference**: `src/mcp/index.ts` (OAuth handling)

**Tasks**:
- [ ] OAuth flow implementation
- [ ] State management
- [ ] Token storage
- [ ] Browser opening for auth

**Files to Create**:
- `src/langcode/mcp/oauth.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/mcp/index.ts`

**Verification**:
- [ ] OAuth flow matches
- [ ] Token handling correct
- [ ] Browser opening works

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 9: LSP Integration

### Module 9.1: LSP Client ⏳ NOT STARTED

**OpenCode Reference**: `src/lsp/server.ts`

**Tasks**:
- [ ] Language server spawning
- [ ] Root detection
- [ ] Initialization
- [ ] Diagnostics retrieval

**Files to Create**:
- `src/langcode/lsp/__init__.py`
- `src/langcode/lsp/client.py`
- `src/langcode/lsp/server.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/lsp/server.ts`

**Verification**:
- [ ] Server spawning works
- [ ] Diagnostics format matches
- [ ] Root detection identical

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 10: Permission System

### Module 10.1: Permission Manager ⏳ NOT STARTED

**OpenCode Reference**: `src/permission/`

**Tasks**:
- [ ] Permission checking
- [ ] Pattern matching
- [ ] User approval flow
- [ ] Always/never rules

**Files to Create**:
- `src/langcode/permission/__init__.py`
- `src/langcode/permission/manager.py`
- `src/langcode/permission/patterns.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/permission/`

**Verification**:
- [ ] Pattern matching identical
- [ ] Approval flow matches
- [ ] Rules applied correctly

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 11: Project & Instance Management

### Module 11.1: Instance Management ⏳ NOT STARTED

**OpenCode Reference**: `src/project/instance.ts`

**Tasks**:
- [ ] Per-directory instance caching
- [ ] Lazy initialization
- [ ] Resource lifecycle management
- [ ] Context-based cleanup

**Files to Create**:
- `src/langcode/project/__init__.py`
- `src/langcode/project/instance.py`
- `src/langcode/project/context.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/project/instance.ts`

**Verification**:
- [ ] Instance caching works
- [ ] Cleanup happens correctly
- [ ] State management matches

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 12: Event Bus

### Module 12.1: Event System ⏳ NOT STARTED

**OpenCode Reference**: `src/bus/`

**Tasks**:
- [ ] Event definition with Pydantic
- [ ] Pub/sub implementation
- [ ] Instance-scoped subscriptions
- [ ] Wildcard support

**Files to Create**:
- `src/langcode/bus/__init__.py`
- `src/langcode/bus/events.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/bus/index.ts`

**Verification**:
- [ ] Event publishing works
- [ ] Subscriptions work
- [ ] Scoping correct

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 13: Plugin System

### Module 13.1: Plugin Loader ⏳ NOT STARTED

**OpenCode Reference**: `src/plugin/`

**Tasks**:
- [ ] Dynamic plugin loading with importlib
- [ ] Hook system
- [ ] Plugin discovery
- [ ] Tool customization hooks

**Files to Create**:
- `src/langcode/plugin/__init__.py`
- `src/langcode/plugin/loader.py`
- `src/langcode/plugin/hooks.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/plugin/`

**Verification**:
- [ ] Can load plugins
- [ ] Hooks work correctly
- [ ] Tool customization works

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 14: CLI Layer

### Module 14.1: CLI App Setup ⏳ NOT STARTED

**OpenCode Reference**: `src/index.ts`, `src/cli/`

**Tasks**:
- [ ] Typer app initialization
- [ ] Rich console setup
- [ ] Global error handling
- [ ] Logging initialization

**Files to Create**:
- `src/langcode/cli/__init__.py`
- `src/langcode/cli/app.py`
- `src/langcode/cli/output.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/index.ts`
- `packages/opencode/src/cli/`

**Verification**:
- [ ] CLI starts correctly
- [ ] Help text matches
- [ ] Error handling works

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 14.2: Command - run ⏳ NOT STARTED

**OpenCode Reference**: `src/cli/` (run command)

**Tasks**:
- [ ] Interactive session loop
- [ ] Message input/output
- [ ] Streaming response display
- [ ] Tool execution display

**Files to Create**:
- `src/langcode/cli/commands/__init__.py`
- `src/langcode/cli/commands/run.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/cli/` (run command implementation)

**Verification**:
- [ ] Session loop works
- [ ] Display matches OpenCode
- [ ] Streaming works
- [ ] Tool output formatted correctly

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 14.3: Command - generate ⏳ NOT STARTED

**OpenCode Reference**: `src/cli/` (generate command)

**Tasks**:
- [ ] One-shot generation
- [ ] Output formatting
- [ ] Exit after completion

**Files to Create**:
- `src/langcode/cli/commands/generate.py`

**Verification**:
- [ ] One-shot mode works
- [ ] Output matches OpenCode

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 14.4: Command - serve ⏳ NOT STARTED

**OpenCode Reference**: `src/cli/` (serve command)

**Tasks**:
- [ ] Start HTTP server
- [ ] Port configuration
- [ ] Server lifecycle

**Files to Create**:
- `src/langcode/cli/commands/serve.py`

**Verification**:
- [ ] Server starts correctly
- [ ] Port handling matches

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 14.5: Command - login/logout ⏳ NOT STARTED

**OpenCode Reference**: `src/cli/` (login/logout commands)

**Tasks**:
- [ ] Authentication flow
- [ ] Token storage
- [ ] Logout cleanup

**Files to Create**:
- `src/langcode/cli/commands/login.py`
- `src/langcode/cli/commands/logout.py`

**Verification**:
- [ ] Auth flow matches
- [ ] Token handling correct

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 14.6: Command - mcp ⏳ NOT STARTED

**OpenCode Reference**: `src/cli/` (mcp command)

**Tasks**:
- [ ] MCP server management
- [ ] List servers
- [ ] Connect/disconnect
- [ ] Status display

**Files to Create**:
- `src/langcode/cli/commands/mcp.py`

**Verification**:
- [ ] MCP commands work
- [ ] Output format matches

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 14.7: Other CLI Commands ⏳ NOT STARTED

**OpenCode Reference**: `src/cli/` (remaining commands)

**Tasks**:
- [ ] models - List available models
- [ ] agent - Agent management
- [ ] config - Config management
- [ ] Other utility commands

**Files to Create**:
- `src/langcode/cli/commands/models.py`
- `src/langcode/cli/commands/agent.py`
- `src/langcode/cli/commands/config.py`

**Verification**:
- [ ] All commands work
- [ ] Output matches OpenCode

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 15: Server Layer (Optional)

### Module 15.1: FastAPI Server ⏳ NOT STARTED

**OpenCode Reference**: `src/server/server.ts`

**Tasks**:
- [ ] FastAPI app setup
- [ ] CORS middleware
- [ ] Authentication middleware
- [ ] Route registration

**Files to Create**:
- `src/langcode/server/__init__.py`
- `src/langcode/server/app.py`

**OpenCode Files to Reference**:
- `packages/opencode/src/server/server.ts`

**Verification**:
- [ ] Server starts
- [ ] Middleware works
- [ ] Routes accessible

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 15.2: API Routes ⏳ NOT STARTED

**OpenCode Reference**: `src/server/` (route files)

**Tasks**:
- [ ] /session routes
- [ ] /project routes
- [ ] /mcp routes
- [ ] /file routes
- [ ] /config routes

**Files to Create**:
- `src/langcode/server/routes/__init__.py`
- `src/langcode/server/routes/session.py`
- `src/langcode/server/routes/project.py`
- `src/langcode/server/routes/mcp.py`
- `src/langcode/server/routes/file.py`
- `src/langcode/server/routes/config.py`

**Verification**:
- [ ] All routes work
- [ ] Response format matches
- [ ] Error handling correct

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 15.3: WebSocket Support ⏳ NOT STARTED

**OpenCode Reference**: `src/server/` (WebSocket handling)

**Tasks**:
- [ ] WebSocket endpoint
- [ ] Real-time updates
- [ ] Connection management

**Files to Create**:
- `src/langcode/server/websocket.py`

**Verification**:
- [ ] WebSocket works
- [ ] Updates sent correctly

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 16: Testing & Validation

### Module 16.1: Unit Tests - Core ⏳ NOT STARTED

**Tasks**:
- [ ] Test all utility functions
- [ ] Test Pydantic schemas
- [ ] Test database models
- [ ] Test config loading

**Files to Create**:
- `tests/unit/test_utils.py`
- `tests/unit/test_schemas.py`
- `tests/unit/test_storage.py`
- `tests/unit/test_config.py`

**Verification**:
- [ ] All core functionality tested
- [ ] Edge cases covered
- [ ] 80%+ coverage

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 16.2: Unit Tests - Tools ⏳ NOT STARTED

**Tasks**:
- [ ] Test each tool independently
- [ ] Mock file system operations
- [ ] Test parameter validation
- [ ] Test error handling

**Files to Create**:
- `tests/unit/test_tool_bash.py`
- `tests/unit/test_tool_read.py`
- `tests/unit/test_tool_write.py`
- `tests/unit/test_tool_edit.py`
- (one file per tool)

**Verification**:
- [ ] All tools tested
- [ ] Behavior matches OpenCode
- [ ] Error cases covered

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 16.3: Integration Tests ⏳ NOT STARTED

**Tasks**:
- [ ] Test tool execution flow
- [ ] Test session management
- [ ] Test MCP integration
- [ ] Test config hierarchy

**Files to Create**:
- `tests/integration/test_session.py`
- `tests/integration/test_tools.py`
- `tests/integration/test_mcp.py`
- `tests/integration/test_config.py`

**Verification**:
- [ ] End-to-end flows work
- [ ] Integration points tested
- [ ] Real file system operations work

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 16.4: Comparison Tests vs OpenCode ⏳ NOT STARTED

**Tasks**:
- [ ] Run same operations in both OpenCode and LangCode
- [ ] Compare outputs character-by-character
- [ ] Verify behavior matches exactly
- [ ] Document any necessary deviations

**Files to Create**:
- `tests/comparison/test_tool_outputs.py`
- `tests/comparison/test_prompts.py`
- `tests/comparison/test_session.py`

**Verification**:
- [ ] All critical paths tested against OpenCode
- [ ] Outputs match exactly
- [ ] Deviations documented and justified

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 17: Documentation

### Module 17.1: User Documentation ⏳ NOT STARTED

**Tasks**:
- [ ] Installation guide
- [ ] Quick start tutorial
- [ ] Command reference
- [ ] Configuration guide
- [ ] Migration guide from OpenCode

**Files to Create**:
- `README.md`
- `docs/INSTALLATION.md`
- `docs/QUICKSTART.md`
- `docs/COMMANDS.md`
- `docs/CONFIGURATION.md`
- `docs/MIGRATION.md`

**Verification**:
- [ ] All features documented
- [ ] Examples work
- [ ] Clear and comprehensive

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 17.2: Developer Documentation ⏳ NOT STARTED

**Tasks**:
- [ ] Architecture overview
- [ ] API reference
- [ ] Tool development guide
- [ ] Skill development guide
- [ ] Contributing guide

**Files to Create**:
- `docs/ARCHITECTURE.md`
- `docs/API.md`
- `docs/TOOL_DEVELOPMENT.md`
- `docs/SKILL_DEVELOPMENT.md`
- `CONTRIBUTING.md`

**Verification**:
- [ ] Architecture clear
- [ ] APIs documented
- [ ] Extension points explained

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Phase 18: Final Integration & Polish

### Module 18.1: End-to-End Testing ⏳ NOT STARTED

**Tasks**:
- [ ] Test complete workflows
- [ ] Test on Linux, macOS, Windows
- [ ] Test with different Python versions (3.11, 3.12)
- [ ] Performance testing

**Verification**:
- [ ] Works on all platforms
- [ ] Performance acceptable
- [ ] No critical bugs

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 18.2: Code Quality & Linting ⏳ NOT STARTED

**Tasks**:
- [ ] Run ruff on entire codebase
- [ ] Run mypy type checking
- [ ] Fix all linting issues
- [ ] Ensure consistent code style

**Verification**:
- [ ] `ruff check .` passes
- [ ] `mypy src/` passes
- [ ] No warnings

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

### Module 18.3: Package & Distribution ⏳ NOT STARTED

**Tasks**:
- [ ] Finalize pyproject.toml
- [ ] Create distribution package
- [ ] Test installation from package
- [ ] Prepare for PyPI (optional)

**Verification**:
- [ ] Package installs correctly
- [ ] All dependencies included
- [ ] Entry points work

**Status**: ⏳ Awaiting start
**Completed**: -
**Approved by user**: ❌

---

## Progress Tracking

### Overall Progress

**Total Modules**: 60+
**Completed**: 0
**In Progress**: 0
**Not Started**: 60+

**Completion**: 0%

### Phase Completion

- [ ] Phase 1: Foundation (3 modules)
- [ ] Phase 2: Storage Layer (2 modules)
- [ ] Phase 3: Configuration System (2 modules)
- [ ] Phase 4: Tool System (15 modules)
- [ ] Phase 5: Skill System (2 modules)
- [ ] Phase 6: Provider Layer (4 modules)
- [ ] Phase 7: Session Management (3 modules)
- [ ] Phase 8: MCP Integration (2 modules)
- [ ] Phase 9: LSP Integration (1 module)
- [ ] Phase 10: Permission System (1 module)
- [ ] Phase 11: Project & Instance Management (1 module)
- [ ] Phase 12: Event Bus (1 module)
- [ ] Phase 13: Plugin System (1 module)
- [ ] Phase 14: CLI Layer (7 modules)
- [ ] Phase 15: Server Layer (3 modules) - Optional
- [ ] Phase 16: Testing & Validation (4 modules)
- [ ] Phase 17: Documentation (2 modules)
- [ ] Phase 18: Final Integration & Polish (3 modules)

### Current Status

**Current Phase**: Phase 1 - Foundation
**Current Module**: Module 1.1 - Project Setup
**Status**: ⏳ NOT STARTED
**Awaiting**: User approval to begin

---

## Critical Reminders

### Before Starting Each Module

1. ✅ Read OpenCode source code for the module
2. ✅ Understand exact behavior
3. ✅ Note all edge cases
4. ✅ Check for constants and defaults

### During Implementation

1. ✅ Copy prompts/descriptions exactly
2. ✅ Match function signatures
3. ✅ Preserve error messages
4. ✅ Write tests alongside code

### After Completing Each Module

1. ✅ Run self-review checklist
2. ✅ Compare with OpenCode behavior
3. ✅ Run tests
4. ✅ Update this document
5. ⏸️ **STOP and wait for user approval**
6. ❌ **DO NOT proceed to next module without approval**

---

## Self-Review Template

After completing each module, fill this out:

```markdown
## Module X.Y Self-Review

**Module**: [Name]
**Completed**: [Date]

### Checklist
- [ ] All functions/classes present
- [ ] Signatures match OpenCode
- [ ] Behavior identical (tested)
- [ ] Error handling matches
- [ ] Edge cases handled
- [ ] Constants/defaults match
- [ ] Tests written and passing
- [ ] No extra features added
- [ ] No simplifications made
- [ ] Documentation updated

### Comparison with OpenCode
[Describe how you verified behavior matches]

### Deviations (if any)
[List any necessary deviations with justification]

### Test Results
[Paste test output]

### Ready for Review
✅ Yes / ❌ No

**Awaiting user approval to proceed to Module X.Y+1**
```

---

## Notes

### Workflow Discipline

This plan enforces strict discipline to ensure exact compliance with OpenCode:

1. **Sequential**: Modules must be completed in order
2. **Complete**: Each module must be fully finished before moving on
3. **Verified**: Self-review is mandatory
4. **Approved**: User approval is required before proceeding
5. **Documented**: Progress must be tracked in this file

### Why This Approach?

- **Prevents drift**: Ensures we don't deviate from OpenCode
- **Maintains quality**: Each module is thoroughly reviewed
- **Enables tracking**: Clear progress visibility
- **Reduces rework**: Catch issues early before building on top
- **Ensures compliance**: User validates each step

### Estimated Timeline

- **Phase 1-3 (Foundation)**: 1-2 weeks
- **Phase 4 (Tools)**: 2-3 weeks
- **Phase 5-13 (Core Systems)**: 3-4 weeks
- **Phase 14-15 (CLI/Server)**: 2-3 weeks
- **Phase 16-18 (Testing/Docs)**: 2-3 weeks

**Total**: 10-15 weeks for complete implementation

### Success Criteria

The implementation is complete when:

1. ✅ All modules implemented and approved
2. ✅ All tests passing
3. ✅ Behavior matches OpenCode exactly
4. ✅ Documentation complete
5. ✅ Code quality checks pass
6. ✅ Works on all platforms
7. ✅ User acceptance testing passed

---

## Next Steps

**Ready to begin Module 1.1: Project Setup**

Awaiting user approval to start implementation.

