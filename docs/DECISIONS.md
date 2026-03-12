# Architectural Decisions

This document tracks key architectural decisions made during the LangCode implementation, with rationale and trade-offs.

## Decision Log

### ADR-001: Use LangChain as Agent Framework

**Date**: 2026-03-12

**Status**: Accepted

**Context**:
Need to choose an AI agent framework for Python implementation. Options considered:
1. LangChain
2. Direct API clients (anthropic, openai, google-generativeai)
3. Custom abstraction layer

**Decision**: Use LangChain

**Rationale**:
- Industry-standard Python AI framework
- Built-in tool calling abstraction
- Multi-provider support (Anthropic, OpenAI, Google, etc.)
- Streaming support
- Active development and large community
- Reduces boilerplate code
- Easier to add new providers

**Consequences**:
- Additional dependency
- Must follow LangChain patterns
- Some OpenCode patterns may need adaptation
- Performance overhead (minimal)

**Alternatives Considered**:
- Direct API clients: More control but more boilerplate, harder to maintain
- Custom abstraction: Full control but significant development effort

---

### ADR-002: Use TOML for Configuration Instead of JSONC

**Date**: 2026-03-12

**Status**: Accepted

**Context**:
OpenCode uses JSONC (JSON with comments) for configuration. Python doesn't have native JSONC support.

**Decision**: Use TOML as primary config format, support JSON for compatibility

**Rationale**:
- TOML is Python-native (pyproject.toml standard)
- Native comment support
- More readable than JSON
- Standard library support in Python 3.11+ (tomllib)
- Better for human editing
- Provide migration script from JSONC

**Consequences**:
- Config files not directly compatible with OpenCode
- Need migration script
- Users must convert configs
- Documentation must explain differences

**Migration Strategy**:
- Provide `migrate-config.py` script
- Support both TOML and JSON reading
- Document conversion process
- Preserve all functionality

**Alternatives Considered**:
- YAML: More complex, security issues, not Python-native
- JSON only: No comments, less readable
- Custom JSONC parser: Additional complexity

---

### ADR-003: Use SQLAlchemy Async for Storage

**Date**: 2026-03-12

**Status**: Accepted

**Context**:
OpenCode uses Drizzle ORM with SQLite. Need Python equivalent.

**Decision**: Use SQLAlchemy 2.0+ with async support

**Rationale**:
- Mature, battle-tested ORM
- Full async support in 2.0+
- Type-safe queries
- Excellent migration support (Alembic)
- Can replicate Drizzle schema structure
- Industry standard for Python

**Consequences**:
- Different API than Drizzle
- Must learn SQLAlchemy patterns
- Migration system different (Alembic vs Drizzle Kit)
- Database schema compatible (both use SQLite)

**Alternatives Considered**:
- Tortoise ORM: Less mature, smaller community
- Raw SQL: Too much boilerplate, no type safety
- Peewee: Simpler but less powerful

---

### ADR-004: Use Typer + Rich for CLI

**Date**: 2026-03-12

**Status**: Accepted

**Context**:
OpenCode uses yargs for CLI. Need Python equivalent.

**Decision**: Use Typer for CLI framework, Rich for output formatting

**Rationale**:
- Typer: Modern, type-hint based, excellent DX
- Rich: Beautiful terminal output, progress bars, tables
- Both work well together
- Better than argparse/click for modern Python
- From creator of FastAPI (consistent ecosystem)

**Consequences**:
- Different API than yargs
- Must adapt command structure
- Rich adds color/formatting capabilities
- Better user experience

**Alternatives Considered**:
- Click: Older, less type-safe
- argparse: Verbose, less modern
- Fire: Too magical, less control

---

### ADR-005: Use Context Managers for Lifecycle Management

**Date**: 2026-03-12

**Status**: Accepted

**Context**:
OpenCode uses Effect-style context management. Need Python equivalent.

**Decision**: Use Python context managers (with statement)

**Rationale**:
- Pythonic pattern
- Automatic cleanup with __enter__/__exit__
- Async context managers for async resources
- Well-understood and documented
- Standard library support

**Implementation**:
```python
@asynccontextmanager
async def instance_context(directory: str):
    instance = await Instance.create(directory)
    try:
        yield instance
    finally:
        await instance.dispose()
```

**Consequences**:
- Different pattern than Effect
- Must use `async with` for async resources
- Cleanup guaranteed even on exceptions

**Alternatives Considered**:
- Manual lifecycle: Error-prone, easy to forget cleanup
- Effect port: Unnecessary complexity for Python

---

### ADR-006: Use Pydantic v2 for Schema Validation

**Date**: 2026-03-12

**Status**: Accepted

**Context**:
OpenCode uses Zod for schema validation. Need Python equivalent.

**Decision**: Use Pydantic v2

**Rationale**:
- Direct replacement for Zod
- Type-safe with Python type hints
- Excellent error messages
- JSON schema generation
- Fast (Rust core in v2)
- Used by FastAPI, LangChain
- Industry standard

**Consequences**:
- Different API than Zod
- Must use Python type hints
- Better integration with Python ecosystem

**Alternatives Considered**:
- marshmallow: Older, slower
- attrs + cattrs: More boilerplate
- dataclasses only: No validation

---

### ADR-007: Preserve Prompt Text Exactly

**Date**: 2026-03-12

**Status**: Accepted

**Context**:
System prompts are critical for AI behavior. Any changes could affect output.

**Decision**: Copy prompt files word-for-word from OpenCode, no modifications

**Rationale**:
- AI models are sensitive to prompt wording
- Exact replication ensures identical behavior
- Easier to verify correctness
- Reduces debugging complexity
- Can update when OpenCode updates

**Implementation**:
- Copy .txt files directly
- Verify character-by-character
- Test with same inputs
- Document any necessary deviations

**Consequences**:
- Cannot "improve" prompts
- Must track OpenCode updates
- Prompts may reference TypeScript-specific concepts

---

### ADR-008: Use uv for Package Management

**Date**: 2026-03-12

**Status**: Accepted

**Context**:
Need fast, modern package management for Python. OpenCode uses bun/npm.

**Decision**: Use uv as primary package manager

**Rationale**:
- 10-100x faster than pip
- Modern Python tooling
- Lock file support
- Virtual environment management
- Compatible with pip/PyPI
- Written in Rust (like bun)

**Consequences**:
- Users must install uv
- Provide pip fallback for compatibility
- Different workflow than pip

**Alternatives Considered**:
- pip: Slow, no lock file
- poetry: Slower than uv, more complex
- pipenv: Deprecated, slow

---

### ADR-009: Python 3.11+ Minimum Version

**Date**: 2026-03-12

**Status**: Accepted

**Context**:
Need to choose minimum Python version.

**Decision**: Require Python 3.11+

**Rationale**:
- tomllib in stdlib (TOML parsing)
- Improved async performance
- Better type hints (Self, TypeVarTuple)
- Better error messages
- Still widely available (released Oct 2022)

**Consequences**:
- Cannot support Python 3.10 and earlier
- Most systems have 3.11+ available
- Can use modern Python features

**Alternatives Considered**:
- Python 3.10: Missing tomllib, older async
- Python 3.12: Too new, less adoption
- Python 3.13: Not released yet

---

### ADR-010: Async/Await Throughout

**Date**: 2026-03-12

**Status**: Accepted

**Context**:
OpenCode uses async extensively. Need consistent async strategy.

**Decision**: Use async/await for all I/O operations

**Rationale**:
- Better performance for I/O-bound operations
- Natural fit for AI streaming responses
- Consistent with OpenCode patterns
- Python 3.11+ has mature async support
- Required for FastAPI, LangChain

**Implementation**:
- All file operations: aiofiles
- All HTTP requests: httpx
- All database operations: SQLAlchemy async
- All tool execution: async methods

**Consequences**:
- Must use `await` everywhere
- Cannot mix sync/async easily
- More complex error handling
- Better performance

---

### ADR-011: Tool Base Class Pattern

**Date**: 2026-03-12

**Status**: Accepted

**Context**:
Need consistent tool interface. OpenCode uses Tool.define() pattern.

**Decision**: Use abstract base class for tools

**Rationale**:
- Type-safe tool definition
- Enforces consistent interface
- Easy to test and mock
- Clear inheritance hierarchy
- Pythonic pattern

**Implementation**:
```python
class ToolBase(ABC):
    @property
    @abstractmethod
    def id(self) -> str: ...

    @abstractmethod
    async def execute(self, args: BaseModel, ctx: ToolContext) -> ToolResult: ...
```

**Consequences**:
- Different pattern than Tool.define()
- More boilerplate per tool
- Better type safety
- Easier to understand

**Alternatives Considered**:
- Function-based: Less structure
- Protocol: Less enforcement
- Decorator pattern: More magic

---

### ADR-012: FastAPI for HTTP Server

**Date**: 2026-03-12

**Status**: Accepted

**Context**:
OpenCode uses Hono for HTTP server. Need Python equivalent.

**Decision**: Use FastAPI

**Rationale**:
- Modern async web framework
- Automatic OpenAPI docs
- Pydantic integration
- WebSocket support
- Type-safe
- Excellent performance
- Large community

**Consequences**:
- Different API than Hono
- Must adapt route structure
- Better documentation generation
- More features out of box

**Alternatives Considered**:
- Flask: Sync, older
- Django: Too heavy, not async-first
- Starlette: Lower-level, more boilerplate
- Sanic: Less popular, smaller community

---

## Future Decisions

### To Be Decided

1. **Logging Framework**: structlog vs loguru vs stdlib logging
2. **Testing Strategy**: pytest plugins, coverage targets
3. **Documentation**: Sphinx vs MkDocs vs pdoc
4. **Distribution**: PyPI package vs standalone binary
5. **Performance Optimization**: uvloop, orjson, cython
6. **Plugin System**: Entry points vs dynamic imports
7. **Error Tracking**: Sentry integration?
8. **Metrics**: Prometheus, StatsD?

## Decision Review Process

1. **Proposal**: Document decision with context and alternatives
2. **Discussion**: Review with team/community
3. **Implementation**: Code and test
4. **Validation**: Verify against OpenCode behavior
5. **Documentation**: Update this file
6. **Review**: Revisit after 3 months or when issues arise

## Reversal Process

If a decision needs to be reversed:
1. Document why (new information, better alternative)
2. Update status to "Superseded"
3. Create new ADR with updated decision
4. Link old and new ADRs
5. Plan migration path

## Template for New Decisions

```markdown
### ADR-XXX: [Title]

**Date**: YYYY-MM-DD

**Status**: Proposed | Accepted | Rejected | Superseded

**Context**:
[What is the issue we're trying to solve?]

**Decision**: [What we decided to do]

**Rationale**:
- [Why this decision?]
- [What are the benefits?]

**Consequences**:
- [What are the trade-offs?]
- [What changes as a result?]

**Alternatives Considered**:
- [Option 1]: [Why not?]
- [Option 2]: [Why not?]
```
