# OpenCode Tools Reference

Complete catalog of all tools with signatures, parameters, and behavior details for Python implementation.

## Tool Interface

### Base Structure

```typescript
Tool.Info<Parameters, Metadata> {
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

### Tool Context

```typescript
Tool.Context {
  sessionID: string
  messageID: string
  agent: string
  abort: AbortSignal
  callID?: string
  extra?: { [key: string]: any }
  messages: MessageV2.WithParts[]
  metadata(input: { title?: string; metadata?: M }): void
  ask(input: PermissionRequest): Promise<void>
}
```

### Tool Result

```typescript
{
  title: string              // Display title (usually relative path or operation)
  metadata: object           // Structured metadata for tracking
  output: string             // Text output for AI
  attachments?: FilePart[]   // Optional file attachments
}
```

## Built-in Tools

### 1. bash

**ID**: `bash`

**Description**: Execute shell commands

**Parameters**:
```typescript
{
  command: string           // The command to execute
  timeout?: number          // Optional timeout in milliseconds (default: 120000)
  workdir?: string          // Working directory (default: Instance.directory)
  description: string       // Clear description of what command does (5-10 words)
}
```

**Behavior**:
- Parses command with tree-sitter-bash
- Extracts file paths and patterns for permission checking
- Spawns shell process (bash/zsh based on system)
- Captures stdout/stderr
- Handles timeout (default 2 minutes, max 10 minutes)
- Returns combined output with exit code

**Metadata**:
```typescript
{
  exitCode: number
  truncated?: boolean
  outputPath?: string
}
```

**Special Features**:
- Tree-sitter parsing for permission extraction
- Detects destructive operations (rm, git reset, etc.)
- Handles background processes
- Process tree cleanup

**Python Notes**:
- Use `asyncio.create_subprocess_exec` for process spawning
- Use `tree-sitter` Python bindings for parsing
- Implement timeout with `asyncio.wait_for`

---

### 2. read

**ID**: `read`

**Description**: Read files or list directory contents

**Parameters**:
```typescript
{
  filePath: string          // Absolute path to file or directory
  offset?: number           // Line number to start reading from (1-indexed)
  limit?: number            // Max lines to read (default: 2000)
}
```

**Behavior**:
- Resolves relative paths to absolute
- Checks if path exists, suggests similar files if not
- For files: reads with line numbers (cat -n format)
- For directories: lists entries with trailing / for dirs
- Truncates long lines (>2000 chars)
- Supports pagination with offset/limit

**Metadata**:
```typescript
{
  filepath: string
  type: "file" | "directory"
  size?: number
  lines?: number
  truncated?: boolean
}
```

**Output Format**:
```
<path>/absolute/path</path>
<type>file</type>
<content>
     1→line 1 content
     2→line 2 content
     ...
</content>
```

**Python Notes**:
- Use `aiofiles` for async file reading
- Use `pathlib.Path` for path operations
- Implement line-by-line reading for large files

---

### 3. write

**ID**: `write`

**Description**: Write content to a file (create or overwrite)

**Parameters**:
```typescript
{
  filePath: string          // Absolute path to file
  content: string           // Content to write
}
```

**Behavior**:
- Creates parent directories if needed
- Checks if file exists (requires prior read if exists)
- Generates diff for permission display
- Writes atomically
- Triggers LSP diagnostics after write
- Reports errors in written file and related files

**Metadata**:
```typescript
{
  filepath: string
  exists: boolean
  diagnostics?: object
}
```

**Special Features**:
- LSP integration for error detection
- Shows up to 20 diagnostics per file
- Shows diagnostics from up to 5 related files
- File locking to prevent concurrent edits

**Python Notes**:
- Use `aiofiles` for async writing
- Use `difflib` for diff generation
- Implement file locking with `fcntl` (Unix) or `msvcrt` (Windows)

---

### 4. edit

**ID**: `edit`

**Description**: Edit existing files by replacing text

**Parameters**:
```typescript
{
  filePath: string          // Absolute path to file
  oldString: string         // Text to replace
  newString: string         // Replacement text
  replaceAll?: boolean      // Replace all occurrences (default: false)
}
```

**Behavior**:
- Requires exact string match
- Fails if oldString not found or not unique (unless replaceAll)
- Preserves line endings (detects \n vs \r\n)
- Generates diff for display
- Triggers LSP diagnostics
- File locking to prevent concurrent edits

**Special Cases**:
- `oldString === ""` → append to file
- `newString === ""` → delete oldString
- Multiple matches without `replaceAll` → error with context

**Metadata**:
```typescript
{
  filepath: string
  occurrences: number
  diagnostics?: object
}
```

**Error Handling**:
- Not found: shows surrounding context
- Multiple matches: shows all locations with line numbers
- Ambiguous match: suggests using larger context

**Python Notes**:
- Simple string replacement (no regex)
- Detect line endings with `\r\n` check
- Use `difflib.unified_diff` for diff generation

---

### 5. glob

**ID**: `glob`

**Description**: Find files matching glob patterns

**Parameters**:
```typescript
{
  pattern: string           // Glob pattern (e.g., "**/*.ts", "src/**/*.py")
  path?: string             // Directory to search (default: Instance.directory)
}
```

**Behavior**:
- Uses ripgrep for fast file listing
- Sorts by modification time (newest first)
- Limits to 100 results
- Returns absolute paths

**Metadata**:
```typescript
{
  count: number
  truncated: boolean
}
```

**Output Format**:
```
/absolute/path/to/file1.py
/absolute/path/to/file2.py
...
(Results are truncated: showing first 100 results. Consider using a more specific path or pattern.)
```

**Python Notes**:
- Use `pathlib.Path.glob()` or `glob.glob()` with recursive
- Sort by `os.path.getmtime()`
- Consider using `ripgrep` subprocess for performance

---

### 6. grep

**ID**: `grep`

**Description**: Search file contents with regex patterns

**Parameters**:
```typescript
{
  pattern: string           // Regex pattern to search
  path?: string             // Directory to search (default: Instance.directory)
  include?: string          // File pattern filter (e.g., "*.py", "*.{ts,tsx}")
}
```

**Behavior**:
- Uses ripgrep for fast searching
- Returns file:line:content format
- Truncates long lines (>2000 chars)
- Handles both matches and errors gracefully

**Metadata**:
```typescript
{
  matches: number
  truncated: boolean
}
```

**Output Format**:
```
/path/to/file.py:42:    matching line content
/path/to/file.py:108:   another match
...
```

**Exit Codes**:
- 0: matches found
- 1: no matches
- 2: errors (broken symlinks, etc.) but may have matches

**Python Notes**:
- Use `subprocess` to call `rg` (ripgrep)
- Parse output line by line
- Handle regex escaping properly

---

### 7. websearch

**ID**: `websearch`

**Description**: Search the web using Exa API

**Parameters**:
```typescript
{
  query: string             // Search query
  numResults?: number       // Number of results (default: 10)
  category?: string         // Category filter
}
```

**Availability**: Only for zen users or with `OPENCODE_ENABLE_EXA` flag

**Behavior**:
- Calls Exa search API
- Returns titles, URLs, and snippets
- Formats as markdown

**Metadata**:
```typescript
{
  query: string
  results: number
}
```

**Python Notes**:
- Use `httpx` for async HTTP requests
- Requires Exa API key
- Format output as markdown list

---

### 8. webfetch

**ID**: `webfetch`

**Description**: Fetch and convert web pages to markdown

**Parameters**:
```typescript
{
  url: string               // URL to fetch
}
```

**Behavior**:
- Fetches URL with HTTP client
- Converts HTML to markdown with Turndown
- Returns cleaned markdown content
- Handles redirects
- 15-minute cache

**Metadata**:
```typescript
{
  url: string
  title?: string
  truncated?: boolean
}
```

**Python Notes**:
- Use `httpx` for fetching
- Use `html2text` or `markdownify` for HTML→markdown
- Implement simple cache with `functools.lru_cache`

---

### 9. skill

**ID**: `skill`

**Description**: Load and execute a skill

**Parameters**:
```typescript
{
  name: string              // Skill name to load
}
```

**Behavior**:
- Looks up skill by name
- Returns skill content as markdown
- Skill content becomes part of system prompt

**Metadata**:
```typescript
{
  name: string
  location: string
}
```

**Python Notes**:
- Load from skill registry
- Return raw markdown content
- No special processing needed

---

### 10. task

**ID**: `task`

**Description**: Manage task list (create, update, list, get)

**Parameters**:
```typescript
{
  action: "create" | "update" | "list" | "get"
  taskId?: string           // For update/get
  subject?: string          // For create
  description?: string      // For create
  status?: "pending" | "in_progress" | "completed" | "deleted"
  owner?: string
  metadata?: object
  addBlocks?: string[]      // Task IDs this blocks
  addBlockedBy?: string[]   // Task IDs blocking this
}
```

**Behavior**:
- Manages task list in session
- Supports dependencies (blocks/blockedBy)
- Tracks status transitions
- Stores arbitrary metadata

**Metadata**:
```typescript
{
  action: string
  taskId?: string
  count?: number
}
```

**Python Notes**:
- Store in database (session-scoped)
- Use SQLAlchemy relationships for dependencies
- Validate status transitions

---

### 11. todo (write)

**ID**: `todo_write`

**Description**: Create or update a todo item

**Parameters**:
```typescript
{
  subject: string           // Brief title
  description?: string      // Detailed description
  status?: "pending" | "in_progress" | "completed"
}
```

**Behavior**:
- Creates todo in session
- Returns todo ID
- Persists to database

**Metadata**:
```typescript
{
  todoId: string
  status: string
}
```

**Python Notes**:
- Simple CRUD operation
- Store in database

---

### 12. question

**ID**: `question`

**Description**: Ask user a question with multiple choice options

**Parameters**:
```typescript
{
  questions: Array<{
    question: string
    header: string          // Short label (max 12 chars)
    options: Array<{
      label: string
      description: string
      preview?: string      // Optional preview content
    }>
    multiSelect: boolean
  }>
}
```

**Availability**: Only in app/cli/desktop clients

**Behavior**:
- Displays question to user
- Waits for user response
- Returns selected options

**Metadata**:
```typescript
{
  answers: Record<string, string | string[]>
}
```

**Python Notes**:
- Use Rich for interactive prompts
- Support single and multi-select
- Handle keyboard input

---

### 13. apply_patch

**ID**: `apply_patch`

**Description**: Apply unified diff patch to files

**Parameters**:
```typescript
{
  patch: string             // Unified diff format
}
```

**Availability**: Only for GPT models (not GPT-4)

**Behavior**:
- Parses unified diff
- Applies changes to files
- Handles multiple files in one patch
- Validates patch format

**Metadata**:
```typescript
{
  files: string[]
  changes: number
}
```

**Python Notes**:
- Use `patch` command or implement diff parser
- Validate patch format
- Handle merge conflicts

---

### 14. lsp

**ID**: `lsp`

**Description**: Query language server for code intelligence

**Parameters**:
```typescript
{
  action: "definition" | "references" | "hover" | "diagnostics"
  filePath?: string
  line?: number
  character?: number
}
```

**Availability**: Experimental flag required

**Behavior**:
- Communicates with LSP server
- Returns code intelligence results
- Supports multiple languages

**Metadata**:
```typescript
{
  action: string
  results: number
}
```

**Python Notes**:
- Use `pygls` or `python-lsp-server`
- Implement LSP client protocol
- Handle stdio communication

---

### 15. batch

**ID**: `batch`

**Description**: Execute multiple tool calls in sequence

**Parameters**:
```typescript
{
  tools: Array<{
    tool: string
    args: object
  }>
}
```

**Availability**: Experimental flag required

**Behavior**:
- Executes tools sequentially
- Stops on first error
- Returns combined results

**Metadata**:
```typescript
{
  executed: number
  failed?: number
}
```

**Python Notes**:
- Simple sequential execution
- Collect all results
- Handle errors gracefully

---

### 16. plan_exit

**ID**: `plan_exit`

**Description**: Exit plan mode and request user approval

**Parameters**:
```typescript
{
  allowedPrompts?: Array<{
    tool: string
    prompt: string
  }>
}
```

**Availability**: Only in CLI with plan mode enabled

**Behavior**:
- Signals plan completion
- Requests user approval
- Transitions from plan to execution mode

**Metadata**:
```typescript
{
  approved: boolean
}
```

**Python Notes**:
- State machine for plan/execute modes
- User confirmation prompt

---

## Tool Registry

### Discovery

Tools are discovered from:
1. Built-in tools (hardcoded list)
2. Custom tools in `.opencode/tool/*.{js,ts}`
3. Custom tools in `.opencode/tools/*.{js,ts}`
4. Plugin-provided tools

### Loading Order

1. Load built-in tools
2. Scan config directories for custom tools
3. Load plugins and their tools
4. Apply tool filters based on model capabilities

### Model-Specific Filtering

- **GPT models (not GPT-4)**: Use `apply_patch` instead of `edit`/`write`
- **Zen users**: Enable `websearch` and `codesearch`
- **Experimental flags**: Enable `lsp`, `batch`, `plan_exit`

### Tool Hooks

Plugins can modify tool definitions via `tool.definition` hook:
```typescript
Plugin.trigger("tool.definition", { toolID }, { description, parameters })
```

## Common Patterns

### Permission Flow

1. Tool receives parameters
2. Calls `ctx.ask()` with permission request
3. User approves/denies
4. Tool executes if approved

### Output Truncation

1. Tool returns output
2. Truncation system checks length
3. If too long: writes to file, returns path
4. Metadata includes `truncated: boolean` and `outputPath?: string`

**Limits**:
- MAX_LINES: 2000 lines
- MAX_BYTES: 50 KB

### File Locking

1. Acquire lock before read/write
2. Check file timestamp
3. Perform operation
4. Update timestamp
5. Release lock

### LSP Integration

1. Touch file to notify LSP
2. Wait for diagnostics
3. Format diagnostics for output
4. Include in tool result

### Error Handling

1. Validate parameters with Pydantic
2. Check permissions
3. Execute operation
4. Catch exceptions
5. Return user-friendly error messages

## Implementation Checklist

For each tool:
- [ ] Define Pydantic schema for parameters
- [ ] Implement execute method
- [ ] Add permission checking
- [ ] Handle errors gracefully
- [ ] Add output truncation
- [ ] Write unit tests
- [ ] Document behavior
- [ ] Test against OpenCode output

## Testing Strategy

### Unit Tests
- Test parameter validation
- Test execution logic
- Mock file system operations
- Mock external APIs

### Integration Tests
- Test with real file system
- Test permission flow
- Test error cases
- Compare output with OpenCode

### Validation
- Run same operation in OpenCode and LangCode
- Compare outputs character-by-character
- Verify metadata matches
- Check error messages match
