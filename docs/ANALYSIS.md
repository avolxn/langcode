# OpenCode Architecture Analysis

## Overview

OpenCode is a production-grade AI coding assistant CLI with a sophisticated multi-layered architecture. It supports multiple AI providers, extensible tools, skills system, MCP integration, and enterprise features.

## High-Level Architecture

### Core Layers

```
┌─────────────────────────────────────────────────────────┐
│                     CLI Layer (yargs)                    │
├─────────────────────────────────────────────────────────┤
│                  Server Layer (Hono HTTP)                │
├─────────────────────────────────────────────────────────┤
│              Session Management (SQLite)                 │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Tool System  │  │ Skill System │  │   Provider   │  │
│  │  (20+ tools) │  │  (Markdown)  │  │ Abstraction  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  MCP Client  │  │  LSP Client  │  │   Plugins    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
├─────────────────────────────────────────────────────────┤
│              Storage (SQLite + Drizzle ORM)              │
├─────────────────────────────────────────────────────────┤
│           Config (Hierarchical JSONC loading)            │
└─────────────────────────────────────────────────────────┘
```

### Cross-Cutting Concerns

- **Bus**: Event pub/sub system for component communication
- **Instance**: Context-based lifecycle management (per-directory caching)
- **Permission**: Fine-grained permission system with pattern matching
- **Project**: Workspace/project context management

## Key Modules and Responsibilities

### 1. CLI Layer (`src/cli/`)

**Entry Point**: `src/index.ts`

**Responsibilities**:
- Command parsing with yargs (25+ commands)
- Global error handling
- Logging initialization
- Database migration on first run
- Command routing

**Key Commands**:
- `run` - Start interactive session
- `generate` - One-shot generation
- `serve` - Start HTTP server
- `login/logout` - Authentication
- `mcp` - MCP server management
- `agent` - Agent management
- `models` - List available models

### 2. Server Layer (`src/server/`)

**Entry Point**: `src/server/server.ts`

**Responsibilities**:
- HTTP API with Hono framework
- WebSocket support for real-time communication
- CORS and authentication middleware
- OpenAPI spec generation

**Routes**:
- `/session` - Session management
- `/project` - Project operations
- `/pty` - Terminal emulation
- `/mcp` - MCP operations
- `/file` - File operations
- `/config` - Configuration
- `/provider` - Provider management
- `/question` - User questions
- `/permission` - Permission management

### 3. Tool System (`src/tool/`)

**Core Interface**: `Tool.Info<Parameters, Metadata>`

**Structure**:
```typescript
Tool.Info {
  id: string
  init(ctx?: InitContext): Promise<{
    description: string
    parameters: Zod schema
    execute(args, ctx): Promise<{
      title: string
      metadata: M
      output: string
      attachments?: FilePart[]
    }>
    formatValidationError?(error): string
  }>
}
```

**Built-in Tools** (20+):
- **File Operations**: read, write, edit, glob, grep
- **Execution**: bash
- **Search**: websearch, codesearch, webfetch
- **Task Management**: task, todo (write/read)
- **Meta**: skill, question, batch, lsp, apply_patch, plan

**Tool Registry** (`src/tool/registry.ts`):
- Loads built-in tools
- Discovers custom tools from `.opencode/tool/` and `.opencode/tools/`
- Loads tools from plugins
- Filters based on model capabilities (e.g., apply_patch vs edit for GPT models)
- Conditional availability (websearch/codesearch for zen users)

**Tool Context**:
- sessionID, messageID, agent name
- abort signal for cancellation
- messages history
- metadata callback
- ask() for permission requests

**Key Features**:
- Automatic parameter validation with Zod
- Output truncation (configurable limits)
- Permission integration
- Plugin hooks for customization

### 4. Skill System (`src/skill/`)

**Structure**: Markdown files with YAML frontmatter

**Discovery Locations** (in order):
1. Global external dirs: `~/.claude/skills/`, `~/.agents/skills/`
2. Project external dirs: `.claude/skills/`, `.agents/skills/`
3. OpenCode dirs: `.opencode/skill/`, `.opencode/skills/`
4. Config paths: `config.skills.paths`
5. Remote URLs: `config.skills.urls`

**Skill Format**:
```markdown
---
name: skill-name
description: Brief description
---

Skill content in markdown...
```

**Loading**:
- Scans for `**/SKILL.md` files
- Parses YAML frontmatter with gray-matter
- Validates name and description
- Warns on duplicates (later overwrites earlier)
- Caches in Instance.state()

**Integration**:
- Formatted as XML in system prompt (verbose mode)
- Loaded via `skill` tool
- Permission-filtered per agent

### 5. Session Management (`src/session/`)

**Storage Schema**:
- **Session**: id, parent, created, updated, archived, summary, share_url, revert
- **Message**: id, sessionID, role, created, updated
- **Part**: id, sessionID, messageID, type, content, metadata
- **Todo**: id, sessionID, subject, description, status, owner, metadata
- **Permission**: id, sessionID, request/response data

**Message Structure**:
- Hierarchical: Session → Message → Parts
- Part types: text, tool_call, tool_result, file
- Parent/child session relationships
- Summary tracking (additions, deletions, files)

**State Management**:
- SQLite persistence with Drizzle ORM
- Async operations
- Transaction support
- Migration system

### 6. Provider Layer (`src/provider/`)

**Abstraction**: Multi-AI provider support via AI SDK

**Supported Providers**:
- Anthropic (Claude)
- OpenAI (GPT, O1, O3)
- Google (Gemini)
- Amazon Bedrock
- Azure OpenAI
- Cerebras, Cohere, DeepInfra, Groq, Mistral, Perplexity, Together AI, xAI
- OpenRouter, AI Gateway
- GitLab AI

**Provider Selection**:
- Model-specific prompt selection
- Capability-based tool filtering
- Authentication management

### 7. MCP Integration (`src/mcp/`)

**MCP Client** (`@modelcontextprotocol/sdk`):
- Remote servers (HTTP/SSE)
- Local servers (stdio)
- OAuth support with state management
- Tool conversion from MCP format to AI SDK format

**Features**:
- Dynamic tool list change notifications
- Resource reading
- Prompt execution with arguments
- Connection status tracking (connected, disabled, failed, needs_auth, needs_client_registration)
- Timeout handling and error recovery
- Process tree cleanup on disconnect
- Browser opening for auth flows

**Configuration**:
```jsonc
{
  "mcp": {
    "servers": {
      "server-name": {
        "type": "remote" | "local",
        "url": "...",  // for remote
        "command": "...",  // for local
        "args": [...],
        "env": {...},
        "oauth": {...}
      }
    }
  }
}
```

### 8. LSP Integration (`src/lsp/`)

**Language Server Protocol**:
- Spawns language servers for multiple languages
- Root detection (nearest package.json, tsconfig.json, etc.)
- Initialization and capability negotiation
- Stdio-based communication
- Used by `lsp` tool for code intelligence

### 9. Configuration System (`src/config/`)

**Hierarchy** (highest to lowest precedence):
1. Managed config (enterprise): `/Library/Application Support/opencode`, `/etc/opencode`
2. Inline config: `OPENCODE_CONFIG_CONTENT` env var
3. .opencode directories: `.opencode/opencode.json{,c}`
4. Project config: `opencode.json{,c}`
5. Custom config: `OPENCODE_CONFIG` env var
6. Global config: `~/.config/opencode/opencode.json{,c}`
7. Remote .well-known/opencode

**Format**: JSONC (JSON with comments)

**Structure**:
```jsonc
{
  "providers": {...},  // AI provider configs
  "mcp": {...},  // MCP server definitions
  "plugins": [...],  // Plugin list
  "skills": {
    "paths": [...],
    "urls": [...]
  },
  "permissions": {...},  // Permission ruleset
  "experimental": {...},  // Feature flags
  "instructions": "...",  // Custom system message
  "agents": {...}  // Agent definitions
}
```

**Loading**:
- Deep merge with array concatenation
- Lazy dependency resolution
- JSONC parsing with edit support
- Remote fetching with caching

### 10. Plugin System (`src/plugin/`)

**Plugin Structure**:
- npm packages or local files
- Dynamic loading with importlib
- Hook system for customization

**Hooks**:
- `tool.definition` - Customize tool descriptions/parameters

**Internal Plugins**:
- Anthropic auth
- Copilot auth
- GitLab auth

**Custom Tools**:
- Loaded from `.opencode/tool/*.{js,ts}`
- Loaded from `.opencode/tools/*.{js,ts}`
- Plugin-provided tools

### 11. Permission System (`src/permission/`)

**Fine-Grained Control**:
- Pattern-based matching
- Per-tool permissions
- Per-agent permissions
- Always/never rules
- User approval flow

**Permission Request**:
```typescript
await ctx.ask({
  permission: "read" | "write" | "bash" | ...,
  patterns: ["/path/to/file"],
  always: ["*"],
  metadata: {...}
})
```

### 12. Storage Layer (`src/storage/`)

**Database**: SQLite with Drizzle ORM

**Tables**:
- Account, AccountState, ControlAccount
- Project
- Session, Message, Part, Todo, Permission
- SessionShare
- Workspace

**Features**:
- Async operations
- Migration system
- Transaction support
- Type-safe queries

### 13. Bus System (`src/bus/`)

**Event Pub/Sub**:
- Type-safe event definitions with Zod
- Instance-scoped subscriptions
- Wildcard subscriptions
- Global bus integration

**Event Definition**:
```typescript
BusEvent.define("event.name", z.object({
  prop1: z.string(),
  prop2: z.number()
}))
```

### 14. Instance Management (`src/project/instance.ts`)

**Context-Based Lifecycle**:
- Per-directory instance caching
- Lazy initialization with boot sequence
- Automatic cleanup on disposal
- Provides: directory, worktree, project info

**Pattern**: `Instance.state(async () => { ... })`
- Used for: config, skills, tools, MCP clients, plugins
- Cached per directory
- Disposed on context exit

## Key Design Patterns

### 1. Instance.state() Pattern

Lazy initialization with caching:
```typescript
export const state = Instance.state(async () => {
  // Initialize resources
  return { resource1, resource2 }
})

// Usage
const { resource1 } = await state()
```

### 2. Tool.define() Pattern

Declarative tool definition:
```typescript
export const MyTool = Tool.define("my-tool", {
  description: "...",
  parameters: z.object({...}),
  async execute(args, ctx) {
    // Implementation
    return { title, metadata, output }
  }
})
```

### 3. BusEvent.define() Pattern

Type-safe events:
```typescript
export const MyEvent = BusEvent.define("my.event", z.object({
  data: z.string()
}))

// Publish
Bus.publish(MyEvent, { data: "..." })

// Subscribe
Bus.subscribe(MyEvent, (event) => { ... })
```

### 4. Hierarchical Config Loading

Multiple sources with deep merge:
- Environment variables
- Multiple file locations
- Remote fetching
- Managed config for enterprise

### 5. Context-Based Lifecycle

Effect-style context management:
- Automatic cleanup
- Nested context support
- Resource disposal

### 6. Plugin Hooks

Extensibility points:
- Tool customization
- Custom tool loading
- Provider integration

## Execution Flow

### CLI Session Flow

1. **Startup**:
   - Parse command with yargs
   - Initialize logging
   - Run database migrations
   - Load configuration

2. **Session Creation**:
   - Create or resume session
   - Load project context (Instance)
   - Initialize provider
   - Load tools and skills
   - Connect MCP servers

3. **Message Loop**:
   - User input
   - Build system prompt (provider + environment + skills)
   - Call AI provider with tools
   - Execute tool calls
   - Handle permissions
   - Store messages/parts
   - Display response

4. **Tool Execution**:
   - Validate parameters (Zod)
   - Check permissions
   - Execute tool logic
   - Truncate output if needed
   - Return result with metadata

5. **Cleanup**:
   - Dispose Instance resources
   - Close MCP connections
   - Close database connections

### Server Flow

1. **Startup**:
   - Initialize Hono app
   - Register middleware (CORS, auth, logging)
   - Register routes
   - Start WebSocket server
   - Listen on port

2. **Request Handling**:
   - Route to handler
   - Validate request
   - Execute operation
   - Return response

3. **WebSocket**:
   - Real-time session updates
   - Tool execution progress
   - Error notifications

## What to Skip for Python CLI

### Not Needed

**Desktop/Web UI**:
- `packages/app/` - Next.js web app
- `packages/desktop/` - Tauri desktop app
- `packages/desktop-electron/` - Electron app
- `packages/ui/` - React component library
- `packages/web/` - Web frontend
- `packages/storybook/` - Component documentation

**IDE Extensions**:
- `sdks/vscode/` - VS Code extension
- `packages/extensions/zed/` - Zed extension

**Enterprise/Infrastructure**:
- `packages/console/` - Admin console
- `packages/enterprise/` - Enterprise features
- `infra/` - SST infrastructure
- `packages/containers/` - Docker containers
- `github/` - GitHub Actions

### Keep for Python Clone

**Core Functionality**:
- Tool system (definitions, registry, execution)
- Skill system (discovery, loading, formatting)
- MCP client integration
- Config loading hierarchy
- Session/message storage schema
- Provider abstraction
- Permission system
- Plugin system basics
- CLI commands
- Server API (optional, but useful)

## Critical Implementation Notes

### TypeScript → Python Mappings

1. **Zod → Pydantic**: Schema validation
2. **yargs → Typer**: CLI framework
3. **Hono → FastAPI**: HTTP framework
4. **Drizzle → SQLAlchemy**: ORM
5. **gray-matter → python-frontmatter**: Markdown parsing
6. **Effect → asyncio**: Async/context management
7. **JSONC → TOML/YAML**: Config format

### Key Files to Reference

- `src/tool/tool.ts` - Tool interface
- `src/tool/registry.ts` - Tool loading
- `src/skill/skill.ts` - Skill loading
- `src/mcp/index.ts` - MCP integration
- `src/storage/db.ts` - Database setup
- `src/config/config.ts` - Config loading
- `src/session/index.ts` - Session management
- `src/session/system.ts` - System prompts
- `src/provider/provider.ts` - Provider abstraction

### Important Behaviors to Preserve

1. **Tool Execution**: Validation → Permission → Execute → Truncate
2. **Skill Discovery**: Multiple locations with precedence
3. **Config Loading**: Hierarchical with deep merge
4. **MCP Integration**: OAuth, reconnection, tool conversion
5. **Permission Flow**: Pattern matching, user approval
6. **Instance Lifecycle**: Per-directory caching, lazy init, cleanup
7. **Output Truncation**: Configurable limits, metadata tracking
8. **Error Handling**: Structured errors, user-friendly messages

## Architecture Quality

OpenCode demonstrates production-grade architecture:

- **Modularity**: Clear separation of concerns
- **Extensibility**: Plugin system, custom tools, skills
- **Robustness**: Error handling, permissions, validation
- **Performance**: Caching, lazy loading, async operations
- **Enterprise-Ready**: Managed config, OAuth, fine-grained permissions
- **Developer Experience**: Type safety, clear interfaces, good defaults

The Python clone should maintain these architectural qualities while adapting to Python idioms and async/await conventions.
