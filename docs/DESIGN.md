# LangCode Python Implementation Design

## Overview

LangCode is a Python clone of OpenCode CLI, maintaining identical functionality while leveraging Python's async/await ecosystem and modern tooling.

## Technology Stack

### Core Framework
- **Python**: 3.11+ (required for modern async features)
- **Agent Framework**: LangChain (for AI orchestration)
- **CLI**: Typer + Rich (command interface + beautiful output)
- **API**: FastAPI + Uvicorn (HTTP server)
- **Storage**: SQLAlchemy (async) + SQLite
- **Package Manager**: uv (fast, modern Python package management)

### Key Libraries
- **Pydantic**: Schema validation (replaces Zod)
- **python-frontmatter**: Markdown parsing (replaces gray-matter)
- **aiofiles**: Async file operations
- **httpx**: Async HTTP client
- **mcp**: Model Context Protocol SDK (official Python SDK)
- **langchain**: AI agent framework
- **langchain-anthropic**: Anthropic provider
- **langchain-openai**: OpenAI provider
- **langchain-google-genai**: Google provider

## Project Structure

```
langcode/
├── pyproject.toml              # uv project config
├── README.md
├── LICENSE
├── .python-version             # 3.11+
│
├── src/
│   └── langcode/
│       ├── __init__.py
│       ├── __main__.py         # Entry point
│       │
│       ├── cli/                # CLI layer
│       │   ├── __init__.py
│       │   ├── app.py          # Typer app
│       │   ├── commands/       # Command implementations
│       │   │   ├── run.py
│       │   │   ├── generate.py
│       │   │   ├── serve.py
│       │   │   ├── login.py
│       │   │   ├── mcp.py
│       │   │   └── ...
│       │   └── output.py       # Rich console output
│       │
│       ├── server/             # HTTP API layer
│       │   ├── __init__.py
│       │   ├── app.py          # FastAPI app
│       │   ├── routes/         # API routes
│       │   │   ├── session.py
│       │   │   ├── project.py
│       │   │   ├── mcp.py
│       │   │   └── ...
│       │   └── websocket.py    # WebSocket support
│       │
│       ├── session/            # Session management
│       │   ├── __init__.py
│       │   ├── manager.py      # Session lifecycle
│       │   ├── message.py      # Message handling
│       │   ├── system.py       # System prompts
│       │   └── prompts/        # Prompt templates
│       │       ├── anthropic.txt
│       │       ├── beast.txt
│       │       ├── gemini.txt
│       │       └── codex_header.txt
│       │
│       ├── tool/               # Tool system
│       │   ├── __init__.py
│       │   ├── base.py         # Tool base class
│       │   ├── registry.py     # Tool registry
│       │   ├── context.py      # Tool execution context
│       │   ├── truncation.py   # Output truncation
│       │   ├── builtin/        # Built-in tools
│       │   │   ├── bash.py
│       │   │   ├── read.py
│       │   │   ├── write.py
│       │   │   ├── edit.py
│       │   │   ├── glob.py
│       │   │   ├── grep.py
│       │   │   ├── websearch.py
│       │   │   ├── webfetch.py
│       │   │   ├── skill.py
│       │   │   ├── task.py
│       │   │   ├── todo.py
│       │   │   └── ...
│       │   └── descriptions/   # Tool description texts
│       │       ├── bash.txt
│       │       ├── read.txt
│       │       └── ...
│       │
│       ├── skill/              # Skill system
│       │   ├── __init__.py
│       │   ├── loader.py       # Skill discovery and loading
│       │   ├── discovery.py    # Remote skill fetching
│       │   └── formatter.py    # Skill formatting
│       │
│       ├── provider/           # AI provider abstraction
│       │   ├── __init__.py
│       │   ├── base.py         # Provider interface
│       │   ├── anthropic.py    # Anthropic/Claude
│       │   ├── openai.py       # OpenAI/GPT
│       │   ├── google.py       # Google/Gemini
│       │   └── factory.py      # Provider factory
│       │
│       ├── mcp/                # MCP integration
│       │   ├── __init__.py
│       │   ├── client.py       # MCP client wrapper
│       │   ├── oauth.py        # OAuth support
│       │   └── converter.py    # Tool format conversion
│       │
│       ├── lsp/                # LSP integration
│       │   ├── __init__.py
│       │   ├── client.py       # LSP client
│       │   └── server.py       # Server spawning
│       │
│       ├── storage/            # Database layer
│       │   ├── __init__.py
│       │   ├── db.py           # Database setup
│       │   ├── models.py       # SQLAlchemy models
│       │   ├── migrations/     # Alembic migrations
│       │   └── schema.py       # Schema definitions
│       │
│       ├── config/             # Configuration system
│       │   ├── __init__.py
│       │   ├── loader.py       # Hierarchical loading
│       │   ├── schema.py       # Config schema
│       │   └── markdown.py     # Markdown config parsing
│       │
│       ├── permission/         # Permission system
│       │   ├── __init__.py
│       │   ├── manager.py      # Permission checking
│       │   └── patterns.py     # Pattern matching
│       │
│       ├── plugin/             # Plugin system
│       │   ├── __init__.py
│       │   ├── loader.py       # Plugin loading
│       │   └── hooks.py        # Hook system
│       │
│       ├── project/            # Project context
│       │   ├── __init__.py
│       │   ├── instance.py     # Instance management
│       │   └── context.py      # Context lifecycle
│       │
│       ├── bus/                # Event bus
│       │   ├── __init__.py
│       │   └── events.py       # Event definitions
│       │
│       ├── util/               # Utilities
│       │   ├── __init__.py
│       │   ├── log.py          # Logging
│       │   ├── filesystem.py   # File operations
│       │   ├── glob.py         # Glob matching
│       │   └── ripgrep.py      # Ripgrep wrapper
│       │
│       └── types/              # Type definitions
│           ├── __init__.py
│           └── schemas.py      # Shared Pydantic models
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
└── docs/                       # Documentation
    ├── ANALYSIS.md
    ├── DESIGN.md
    ├── DECISIONS.md
    └── REFERENCES/
        ├── TOOLS.md
        ├── PROMPTS.md
        └── DEPENDENCIES.md
```

## Key Design Decisions

### 1. Async/Await Throughout

**Decision**: Use async/await for all I/O operations

**Rationale**:
- OpenCode uses async patterns extensively
- Python 3.11+ has mature async support
- Better performance for I/O-bound operations
- Natural fit for AI streaming responses

**Implementation**:
```python
# Tool execution
async def execute(self, args: dict, ctx: ToolContext) -> ToolResult:
    async with aiofiles.open(path, 'r') as f:
        content = await f.read()
    return ToolResult(...)

# Session management
async def run_session(session_id: str):
    async with get_db_session() as db:
        messages = await db.query(Message).all()
```

### 2. Pydantic for Schema Validation

**Decision**: Use Pydantic v2 for all schema validation

**Rationale**:
- Direct replacement for Zod
- Type-safe with Python type hints
- Excellent error messages
- JSON schema generation
- Fast validation with Rust core

**Implementation**:
```python
from pydantic import BaseModel, Field

class BashToolParams(BaseModel):
    command: str = Field(description="The command to execute")
    timeout: int | None = Field(None, description="Timeout in milliseconds")
    workdir: str | None = Field(None, description="Working directory")
    description: str = Field(description="Clear description of command")

# Validation
params = BashToolParams.model_validate(args)
```

### 3. Context Managers for Lifecycle

**Decision**: Use Python context managers for resource lifecycle

**Rationale**:
- Replaces Effect-style context in TypeScript
- Automatic cleanup with `__enter__`/`__exit__`
- Async context managers for async resources
- Pythonic and well-understood pattern

**Implementation**:
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def instance_context(directory: str):
    """Per-directory instance with automatic cleanup"""
    instance = await Instance.create(directory)
    try:
        yield instance
    finally:
        await instance.dispose()

# Usage
async with instance_context("/path") as instance:
    tools = await instance.get_tools()
```

### 4. LangChain for AI Orchestration

**Decision**: Use LangChain as the agent framework

**Rationale**:
- Industry-standard Python AI framework
- Built-in tool calling support
- Multiple provider integrations
- Streaming support
- Active development and community

**Implementation**:
```python
from langchain.agents import AgentExecutor
from langchain.tools import BaseTool
from langchain_anthropic import ChatAnthropic

# Create agent
llm = ChatAnthropic(model="claude-sonnet-4")
tools = await registry.get_tools()
agent = AgentExecutor.from_agent_and_tools(
    agent=llm,
    tools=tools,
    verbose=True
)

# Run
result = await agent.ainvoke({"input": user_message})
```

### 5. SQLAlchemy Async for Storage

**Decision**: Use SQLAlchemy 2.0+ with async support

**Rationale**:
- Mature ORM with async support
- Type-safe queries
- Migration support (Alembic)
- Direct mapping to Drizzle schema

**Implementation**:
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_async_engine("sqlite+aiosqlite:///langcode.db")
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True)
    created = Column(DateTime, default=datetime.utcnow)
    # ...
```

### 6. TOML for Configuration

**Decision**: Use TOML instead of JSONC for config files

**Rationale**:
- Python-native format (used by pyproject.toml)
- Supports comments natively
- More readable than JSON
- Standard library support (Python 3.11+)
- Provide migration script from JSONC

**Implementation**:
```python
import tomllib  # Python 3.11+

with open("langcode.toml", "rb") as f:
    config = tomllib.load(f)

# Also support JSON for compatibility
import json
with open("langcode.json") as f:
    config = json.load(f)
```

**Migration Script**: Provide `migrate-config.py` to convert OpenCode JSONC → LangCode TOML

### 7. Typer + Rich for CLI

**Decision**: Use Typer for CLI framework and Rich for output

**Rationale**:
- Typer: Modern, type-hint based CLI (from FastAPI author)
- Rich: Beautiful terminal output with colors, tables, progress bars
- Better than argparse/click for modern Python
- Excellent developer experience

**Implementation**:
```python
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def run(
    message: str = typer.Argument(None, help="Initial message"),
    model: str = typer.Option("claude-sonnet-4", help="Model to use"),
):
    """Start an interactive session"""
    console.print(f"[bold green]Starting session with {model}[/bold green]")
    # ...
```

### 8. Tool Base Class Pattern

**Decision**: Use abstract base class for tools

**Rationale**:
- Type-safe tool definition
- Enforces consistent interface
- Easy to test and mock
- Clear inheritance hierarchy

**Implementation**:
```python
from abc import ABC, abstractmethod
from pydantic import BaseModel

class ToolBase(ABC):
    """Base class for all tools"""

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique tool identifier"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description for AI"""
        pass

    @property
    @abstractmethod
    def parameters_schema(self) -> type[BaseModel]:
        """Pydantic model for parameters"""
        pass

    @abstractmethod
    async def execute(self, args: BaseModel, ctx: ToolContext) -> ToolResult:
        """Execute the tool"""
        pass

# Usage
class BashTool(ToolBase):
    id = "bash"
    description = "Execute bash commands"
    parameters_schema = BashToolParams

    async def execute(self, args: BashToolParams, ctx: ToolContext) -> ToolResult:
        # Implementation
        pass
```

### 9. Instance State Caching

**Decision**: Use functools.lru_cache with async support

**Rationale**:
- Replaces Instance.state() pattern from TypeScript
- Per-directory caching
- Automatic cleanup with weak references
- Python-native pattern

**Implementation**:
```python
from functools import lru_cache
from weakref import WeakValueDictionary

class Instance:
    _instances: WeakValueDictionary[str, 'Instance'] = WeakValueDictionary()

    @classmethod
    async def get(cls, directory: str) -> 'Instance':
        """Get or create instance for directory"""
        if directory in cls._instances:
            return cls._instances[directory]

        instance = cls(directory)
        await instance._initialize()
        cls._instances[directory] = instance
        return instance

    async def _initialize(self):
        """Lazy initialization"""
        self.config = await load_config(self.directory)
        self.tools = await load_tools(self.directory)
        self.skills = await load_skills(self.directory)
```

### 10. Event Bus with asyncio

**Decision**: Simple pub/sub with asyncio.Queue

**Rationale**:
- Lightweight, no external dependencies
- Async-native
- Type-safe with Pydantic
- Easy to test

**Implementation**:
```python
from typing import Callable, TypeVar
from pydantic import BaseModel
import asyncio

T = TypeVar('T', bound=BaseModel)

class EventBus:
    def __init__(self):
        self._subscribers: dict[type, list[Callable]] = {}

    def subscribe(self, event_type: type[T], handler: Callable[[T], None]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def publish(self, event: BaseModel):
        event_type = type(event)
        if event_type in self._subscribers:
            await asyncio.gather(*[
                handler(event) for handler in self._subscribers[event_type]
            ])
```

## Handling TypeScript → Python Differences

### 1. Type System

**TypeScript**:
```typescript
interface Tool {
  id: string
  execute(args: any): Promise<Result>
}
```

**Python**:
```python
from typing import Protocol
from pydantic import BaseModel

class Tool(Protocol):
    id: str
    async def execute(self, args: BaseModel) -> Result: ...
```

### 2. Module System

**TypeScript**: ES modules with `import/export`
**Python**: Standard imports with `__init__.py`

**Approach**:
- Use relative imports within package
- Expose public API in `__init__.py`
- Use `__all__` to control exports

### 3. Async/Await

**TypeScript**: Promise-based
**Python**: Native async/await with asyncio

**Key Differences**:
- Python: `async def`, `await`, `async with`, `async for`
- Use `asyncio.gather()` for parallel execution
- Use `asyncio.create_task()` for background tasks

### 4. Error Handling

**TypeScript**: try/catch
**Python**: try/except

**Approach**:
- Define custom exception hierarchy
- Use Pydantic validation errors
- Structured error responses

### 5. JSON Handling

**TypeScript**: Native JSON support
**Python**: `json` module + Pydantic

**Approach**:
- Use Pydantic `.model_dump_json()` for serialization
- Use `.model_validate_json()` for deserialization
- Handle datetime serialization explicitly

### 6. File Operations

**TypeScript**: `fs/promises`
**Python**: `aiofiles`

**Approach**:
```python
import aiofiles

async def read_file(path: str) -> str:
    async with aiofiles.open(path, 'r') as f:
        return await f.read()
```

### 7. Path Handling

**TypeScript**: `path` module
**Python**: `pathlib.Path`

**Approach**:
```python
from pathlib import Path

path = Path("/some/path")
absolute = path.resolve()
relative = path.relative_to(base)
```

### 8. Process Spawning

**TypeScript**: `child_process.spawn`
**Python**: `asyncio.create_subprocess_exec`

**Approach**:
```python
import asyncio

proc = await asyncio.create_subprocess_exec(
    "bash", "-c", command,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE
)
stdout, stderr = await proc.communicate()
```

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
- Project setup with uv
- Core types and schemas
- Storage layer (SQLAlchemy models)
- Config loading system
- Logging and utilities

### Phase 2: Tool System (Week 2-3)
- Tool base class and registry
- Built-in tools (bash, read, write, edit, glob, grep)
- Tool execution context
- Output truncation
- Permission integration

### Phase 3: Session Management (Week 3-4)
- Session lifecycle
- Message handling
- System prompt generation
- Provider abstraction
- LangChain integration

### Phase 4: Skills & MCP (Week 4-5)
- Skill discovery and loading
- Skill formatting
- MCP client integration
- OAuth support
- Tool conversion

### Phase 5: CLI (Week 5-6)
- Typer CLI app
- Command implementations
- Rich output formatting
- Interactive session loop

### Phase 6: Server (Week 6-7)
- FastAPI app
- API routes
- WebSocket support
- Authentication

### Phase 7: Advanced Features (Week 7-8)
- LSP integration
- Plugin system
- Additional tools
- Permission system refinement

### Phase 8: Testing & Polish (Week 8-9)
- Unit tests
- Integration tests
- Documentation
- Migration scripts
- Performance optimization

## Testing Strategy

### Unit Tests
- Test each tool independently
- Mock external dependencies
- Test schema validation
- Test error handling

### Integration Tests
- Test tool execution flow
- Test session management
- Test MCP integration
- Test config loading

### End-to-End Tests
- Test CLI commands
- Test full session flow
- Test with real AI providers (optional)

### Test Framework
```python
import pytest
import pytest_asyncio

@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession)
    async with async_session() as session:
        yield session

@pytest.mark.asyncio
async def test_bash_tool(db_session):
    tool = BashTool()
    ctx = ToolContext(session_id="test", ...)
    result = await tool.execute(
        BashToolParams(command="echo hello", description="Test"),
        ctx
    )
    assert "hello" in result.output
```

## Performance Considerations

### 1. Lazy Loading
- Load tools/skills/config on demand
- Cache per-directory instances
- Use weak references for cleanup

### 2. Async I/O
- Use aiofiles for file operations
- Use httpx for HTTP requests
- Parallel tool execution where possible

### 3. Database
- Use connection pooling
- Batch inserts for messages
- Index frequently queried columns

### 4. Caching
- Cache compiled regexes
- Cache parsed configs
- Cache skill metadata

## Migration from OpenCode

### Config Migration Script

```python
# migrate_config.py
import json
import tomli_w
from pathlib import Path

def migrate_config(jsonc_path: str, toml_path: str):
    """Convert OpenCode JSONC config to LangCode TOML"""
    # Remove comments and parse JSONC
    with open(jsonc_path) as f:
        content = f.read()
    # Simple comment removal (not perfect but works for most cases)
    lines = [line for line in content.split('\n')
             if not line.strip().startswith('//')]
    config = json.loads('\n'.join(lines))

    # Write TOML
    with open(toml_path, 'wb') as f:
        tomli_w.dump(config, f)
```

### Session Migration

OpenCode and LangCode can share the same SQLite database schema, so sessions are compatible.

## Documentation Requirements

### User Documentation
- Installation guide
- Quick start tutorial
- Command reference
- Configuration guide
- Tool development guide
- Skill development guide

### Developer Documentation
- Architecture overview
- API reference
- Contributing guide
- Testing guide

## Success Criteria

1. **Functional Parity**: All OpenCode CLI features work identically
2. **Prompt Accuracy**: System prompts match word-for-word
3. **Tool Compatibility**: All tools produce identical outputs
4. **Config Compatibility**: Can migrate OpenCode configs
5. **Performance**: Comparable or better performance
6. **Code Quality**: Type-safe, well-tested, documented
7. **Maintainability**: Clear architecture, modular design

## Next Steps

After design approval:
1. Set up project structure with uv
2. Implement storage layer
3. Implement tool system
4. Implement session management
5. Implement CLI
6. Test against OpenCode behavior
7. Document and polish
