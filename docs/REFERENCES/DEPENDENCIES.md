# OpenCode Dependencies Mapping

Mapping of npm packages to Python equivalents with rationale for Python implementation.

## Core Framework Dependencies

### AI & Agent Framework

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `ai` (Vercel AI SDK) | `langchain` | Industry-standard Python AI framework with tool calling, streaming, and multi-provider support |
| `@ai-sdk/anthropic` | `langchain-anthropic` | Official Anthropic integration for LangChain |
| `@ai-sdk/openai` | `langchain-openai` | Official OpenAI integration for LangChain |
| `@ai-sdk/google` | `langchain-google-genai` | Official Google integration for LangChain |
| `@ai-sdk/provider` | Built into LangChain | Provider abstraction built into LangChain core |

**Alternative Considered**: Direct API clients (anthropic, openai, google-generativeai)
**Why LangChain**: Unified interface, tool calling abstraction, streaming support, active development

### CLI Framework

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `yargs` | `typer` | Modern, type-hint based CLI framework with excellent DX |
| N/A | `rich` | Beautiful terminal output (colors, tables, progress bars) |
| `@clack/prompts` | `rich.prompt` or `questionary` | Interactive prompts with rich formatting |

**Why Typer**:
- Type-safe with Python type hints
- Automatic help generation
- From creator of FastAPI (consistent ecosystem)
- Better than argparse/click for modern Python

**Why Rich**:
- Beautiful output formatting
- Progress bars, tables, syntax highlighting
- Works well with Typer
- Industry standard for Python CLI apps

### HTTP Server

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `hono` | `fastapi` | Modern async web framework with automatic OpenAPI docs |
| N/A | `uvicorn` | ASGI server for FastAPI |
| `@hono/zod-validator` | Built into FastAPI (Pydantic) | FastAPI uses Pydantic for validation natively |

**Why FastAPI**:
- Async/await native
- Automatic OpenAPI/Swagger docs
- Pydantic integration
- WebSocket support
- Type-safe
- Excellent performance

### Database & ORM

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `drizzle-orm` | `sqlalchemy` (async) | Mature, feature-rich ORM with async support |
| `drizzle-kit` | `alembic` | Database migration tool for SQLAlchemy |
| N/A | `aiosqlite` | Async SQLite driver for SQLAlchemy |

**Why SQLAlchemy 2.0+**:
- Mature and battle-tested
- Full async support in 2.0+
- Type-safe queries
- Excellent migration support (Alembic)
- Direct mapping to Drizzle schema possible

## Schema Validation

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `zod` | `pydantic` v2 | Type-safe schema validation with excellent error messages |
| `zod-to-json-schema` | `pydantic.json_schema` | Built into Pydantic v2 |

**Why Pydantic v2**:
- Native Python type hints
- Fast (Rust core)
- JSON schema generation
- Excellent error messages
- Industry standard for Python
- Used by FastAPI, LangChain, etc.

## File Operations

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `fs/promises` | `aiofiles` | Async file operations |
| `path` | `pathlib.Path` | Object-oriented path handling (stdlib) |
| `glob` | `glob` or `pathlib.Path.glob()` | Pattern matching (stdlib) |
| `@parcel/watcher` | `watchdog` | File system watching |
| `chokidar` | `watchdog` | File system watching (alternative) |

**Why aiofiles**: Async file I/O for non-blocking operations
**Why pathlib**: Modern, cross-platform path handling (stdlib)
**Why watchdog**: Pure Python, cross-platform, actively maintained

## Text Processing

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `gray-matter` | `python-frontmatter` | YAML frontmatter parsing |
| `turndown` | `html2text` or `markdownify` | HTML to Markdown conversion |
| `strip-ansi` | `strip-ansi` (PyPI) | Remove ANSI escape codes |
| `diff` | `difflib` | Unified diff generation (stdlib) |
| `partial-json` | `partial-json-parser` | Parse incomplete JSON |

**Why python-frontmatter**: Direct equivalent, handles YAML/TOML/JSON frontmatter
**Why html2text**: Mature, configurable HTML→Markdown conversion
**Why difflib**: Standard library, no dependencies needed

## Configuration

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `jsonc-parser` | `tomllib` (3.11+) + `json` | TOML for config (Python-native), JSON for compatibility |
| N/A | `tomli-w` | TOML writing (for migration scripts) |
| `xdg-basedir` | `platformdirs` | Cross-platform config directories |

**Why TOML**:
- Python-native format (pyproject.toml)
- Comments supported natively
- More readable than JSON
- Standard library support (Python 3.11+)

**Migration Strategy**: Provide script to convert JSONC → TOML

## Process & Shell

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `child_process` | `asyncio.subprocess` | Async process spawning (stdlib) |
| `bun-pty` | `ptyprocess` or `pexpect` | PTY (pseudo-terminal) support |
| `which` | `shutil.which` | Find executables in PATH (stdlib) |

**Why asyncio.subprocess**: Native async support, no dependencies
**Why ptyprocess**: Pure Python PTY implementation

## Tree-sitter (Code Parsing)

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `web-tree-sitter` | `tree-sitter` | Python bindings for tree-sitter |
| `tree-sitter-bash` | `tree-sitter-bash` (via tree-sitter) | Bash grammar |

**Why tree-sitter**: Same underlying library, Python bindings available

## MCP (Model Context Protocol)

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `@modelcontextprotocol/sdk` | `mcp` | Official Python MCP SDK |

**Why mcp**: Official Python SDK from Anthropic, feature parity with JS SDK

## LSP (Language Server Protocol)

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `vscode-jsonrpc` | `pygls` | Python language server protocol implementation |
| `vscode-languageserver-types` | Built into `pygls` | LSP types included |

**Why pygls**: Official Python LSP implementation, used by many language servers

## HTTP Client

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `fetch` (built-in) | `httpx` | Modern async HTTP client |

**Why httpx**:
- Async/await support
- HTTP/2 support
- Timeout handling
- Connection pooling
- Similar API to requests

## Utilities

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `ulid` | `python-ulid` | ULID generation |
| `semver` | `packaging.version` | Semantic versioning (stdlib) |
| `mime-types` | `mimetypes` | MIME type detection (stdlib) |
| `minimatch` | `fnmatch` or `wcmatch` | Glob pattern matching |
| `ignore` | `pathspec` | .gitignore-style pattern matching |
| `fuzzysort` | `rapidfuzz` | Fuzzy string matching |
| `open` | `webbrowser` | Open URLs in browser (stdlib) |
| `clipboardy` | `pyperclip` | Clipboard access |

**Why stdlib when possible**: Reduce dependencies, better compatibility

## Ripgrep Integration

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| Direct `rg` calls | `subprocess` + `rg` binary | Call ripgrep binary directly |

**Why subprocess**: Ripgrep is a binary tool, call it directly for best performance

## OAuth & Authentication

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `@openauthjs/openauth` | `authlib` | OAuth 2.0 client/server |
| `google-auth-library` | `google-auth` | Google authentication |
| `@aws-sdk/credential-providers` | `boto3` | AWS credentials |

**Why authlib**: Comprehensive OAuth implementation for Python
**Why google-auth**: Official Google authentication library
**Why boto3**: Official AWS SDK for Python

## Testing

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `bun test` | `pytest` | Industry-standard Python testing framework |
| N/A | `pytest-asyncio` | Async test support for pytest |
| N/A | `pytest-cov` | Coverage reporting |
| N/A | `pytest-mock` | Mocking utilities |

**Why pytest**:
- Most popular Python testing framework
- Excellent async support
- Rich plugin ecosystem
- Better than unittest

## Development Tools

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `typescript` | `mypy` | Static type checking |
| N/A | `ruff` | Fast linter and formatter (replaces flake8, black, isort) |
| N/A | `uv` | Fast package manager and project management |

**Why mypy**: Industry-standard type checker for Python
**Why ruff**: Extremely fast, replaces multiple tools, written in Rust
**Why uv**: Modern, fast package manager (10-100x faster than pip)

## Package Management

| OpenCode (npm) | LangCode (Python) | Rationale |
|----------------|-------------------|-----------|
| `npm` / `bun` | `uv` | Fast, modern Python package manager |
| `package.json` | `pyproject.toml` | Python project configuration (PEP 621) |

**Why uv**:
- 10-100x faster than pip
- Handles virtual environments
- Lock file support
- Compatible with pip/PyPI
- Modern Python tooling

## Not Needed in Python

These OpenCode dependencies are not needed in Python:

| OpenCode Package | Why Not Needed |
|------------------|----------------|
| `@babel/core` | No transpilation needed in Python |
| `@typescript/*` | Python has native type hints |
| `effect` | Use native async/await and context managers |
| `solid-js` | No UI components needed (CLI only) |
| `@opentui/*` | No UI components needed (CLI only) |
| `@zip.js/zip.js` | Use `zipfile` (stdlib) |
| `decimal.js` | Use `decimal.Decimal` (stdlib) |
| `remeda` | Use native Python functions or `itertools` |

## Complete Python Dependencies List

### Core Dependencies

```toml
[project]
name = "langcode"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    # AI Framework
    "langchain>=0.1.0",
    "langchain-anthropic>=0.1.0",
    "langchain-openai>=0.1.0",
    "langchain-google-genai>=0.1.0",

    # CLI & Output
    "typer>=0.9.0",
    "rich>=13.0.0",
    "questionary>=2.0.0",

    # Web Server
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "websockets>=12.0",

    # Database
    "sqlalchemy[asyncio]>=2.0.0",
    "aiosqlite>=0.19.0",
    "alembic>=1.13.0",

    # Schema Validation
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",

    # File Operations
    "aiofiles>=23.2.0",
    "watchdog>=4.0.0",

    # Text Processing
    "python-frontmatter>=1.1.0",
    "html2text>=2024.2.26",
    "strip-ansi>=0.1.1",

    # Configuration
    "platformdirs>=4.1.0",
    "tomli-w>=1.0.0",  # For TOML writing

    # HTTP Client
    "httpx>=0.26.0",

    # MCP & LSP
    "mcp>=0.1.0",
    "pygls>=1.3.0",

    # Tree-sitter
    "tree-sitter>=0.21.0",
    "tree-sitter-bash>=0.21.0",

    # OAuth & Auth
    "authlib>=1.3.0",
    "google-auth>=2.27.0",

    # Utilities
    "python-ulid>=2.2.0",
    "pyperclip>=1.8.2",
    "rapidfuzz>=3.6.0",
    "pathspec>=0.12.0",
    "wcmatch>=8.5.0",
    "ptyprocess>=0.7.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
    "mypy>=1.8.0",
    "ruff>=0.1.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
    "mypy>=1.8.0",
    "ruff>=0.1.0",
]
```

## Installation Commands

### Using uv (Recommended)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create project
uv init langcode
cd langcode

# Add dependencies
uv add langchain langchain-anthropic langchain-openai
uv add typer rich fastapi uvicorn
uv add sqlalchemy aiosqlite alembic
uv add pydantic aiofiles httpx

# Add dev dependencies
uv add --dev pytest pytest-asyncio mypy ruff

# Run
uv run python -m langcode
```

### Using pip (Alternative)

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r requirements-dev.txt
```

## Version Pinning Strategy

### Production Dependencies
- Pin major and minor versions: `langchain>=0.1.0,<0.2.0`
- Allow patch updates for security fixes
- Test before upgrading major versions

### Development Dependencies
- Allow more flexibility: `pytest>=7.4.0`
- Keep tooling up to date
- Pin if specific version required

### Lock File
- Use `uv.lock` for reproducible builds
- Commit lock file to repository
- Update regularly with `uv lock --upgrade`

## Migration Notes

### From npm to Python

1. **No transpilation**: Python code runs directly, no build step
2. **Virtual environments**: Use venv or uv for isolation
3. **Import system**: Use relative imports within package
4. **Type hints**: Use native Python type hints, not TypeScript
5. **Async/await**: Native in Python 3.11+, no promises

### Configuration Migration

Provide migration script:
```python
# migrate_config.py
import json
import tomli_w

def migrate_jsonc_to_toml(jsonc_path: str, toml_path: str):
    """Convert OpenCode JSONC to LangCode TOML"""
    # Remove comments, parse JSON
    with open(jsonc_path) as f:
        lines = [l for l in f if not l.strip().startswith('//')]
        config = json.loads(''.join(lines))

    # Write TOML
    with open(toml_path, 'wb') as f:
        tomli_w.dump(config, f)
```

## Compatibility Notes

### Python Version
- **Minimum**: Python 3.11 (for tomllib, improved async, better type hints)
- **Recommended**: Python 3.12 (better performance, improved error messages)
- **Target**: Python 3.11+ for broad compatibility

### Operating Systems
- **Linux**: Full support (primary development platform)
- **macOS**: Full support
- **Windows**: Full support (test thoroughly)

### Architecture
- **x86_64**: Full support
- **ARM64**: Full support (Apple Silicon, ARM servers)

## Performance Considerations

### Fast Dependencies
- `ruff`: Rust-based linter (100x faster than flake8)
- `uv`: Rust-based package manager (10-100x faster than pip)
- `pydantic` v2: Rust core (5-50x faster than v1)
- `httpx`: Fast HTTP client with connection pooling

### Optimization Tips
- Use `uvloop` for faster asyncio (optional)
- Use `orjson` for faster JSON (optional)
- Profile with `py-spy` or `scalene`
- Cache expensive operations

## Security Considerations

### Dependency Scanning
- Use `pip-audit` or `safety` for vulnerability scanning
- Keep dependencies updated
- Review security advisories

### Pinning Strategy
- Pin exact versions in production
- Use lock file for reproducibility
- Test updates in staging first

## Testing Dependencies

All dependencies should be tested for:
1. **Functionality**: Does it work as expected?
2. **Performance**: Is it fast enough?
3. **Compatibility**: Works on all platforms?
4. **Maintenance**: Is it actively maintained?
5. **Documentation**: Is it well documented?

## Implementation Checklist

- [ ] Set up uv project
- [ ] Add core dependencies
- [ ] Add dev dependencies
- [ ] Configure mypy for type checking
- [ ] Configure ruff for linting
- [ ] Set up pytest
- [ ] Create requirements.txt (for pip users)
- [ ] Test on Linux, macOS, Windows
- [ ] Document installation process
- [ ] Create migration scripts
