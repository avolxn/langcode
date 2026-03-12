# OpenCode Prompts System Reference

Details on how prompts are stored, loaded, templated, and composed for Python implementation.

## Overview

OpenCode uses model-specific system prompts that are loaded from text files and composed with environment context and skill information.

## Prompt Files

### Location

`src/session/prompt/` directory contains:
- `anthropic.txt` - For Claude models
- `beast.txt` - For OpenAI GPT models (GPT-4, GPT-5, O1, O3)
- `gemini.txt` - For Google Gemini models
- `codex_header.txt` - For Codex/GPT-5 models
- `trinity.txt` - For Trinity models
- `qwen.txt` - For Qwen and other models (Anthropic prompt without todo tool)

### Format

Plain text files with no special formatting. These are the exact instructions given to the AI model.

## Prompt Selection

### Model-Based Selection

```typescript
function provider(model: Provider.Model) {
  if (model.api.id.includes("gpt-5")) return [PROMPT_CODEX]
  if (model.api.id.includes("gpt-") || model.api.id.includes("o1") || model.api.id.includes("o3"))
    return [PROMPT_BEAST]
  if (model.api.id.includes("gemini-")) return [PROMPT_GEMINI]
  if (model.api.id.includes("claude")) return [PROMPT_ANTHROPIC]
  if (model.api.id.toLowerCase().includes("trinity")) return [PROMPT_TRINITY]
  return [PROMPT_ANTHROPIC_WITHOUT_TODO]
}
```

**Python Implementation**:
```python
def select_prompt(model_id: str) -> str:
    """Select prompt template based on model ID"""
    model_lower = model_id.lower()

    if "gpt-5" in model_lower:
        return load_prompt("codex_header.txt")
    if any(x in model_lower for x in ["gpt-", "o1", "o3"]):
        return load_prompt("beast.txt")
    if "gemini-" in model_lower:
        return load_prompt("gemini.txt")
    if "claude" in model_lower:
        return load_prompt("anthropic.txt")
    if "trinity" in model_lower:
        return load_prompt("trinity.txt")

    return load_prompt("qwen.txt")  # Default
```

## Prompt Composition

### System Prompt Structure

The final system prompt is composed of three parts:

1. **Provider-specific instructions** (from prompt file)
2. **Environment context** (dynamic)
3. **Skills information** (dynamic)

### Composition Order

```typescript
const systemPrompt = [
  ...SystemPrompt.provider(model),      // Base instructions
  ...await SystemPrompt.environment(model),  // Environment info
  await SystemPrompt.skills(agent)      // Available skills
].join("\n\n")
```

**Python Implementation**:
```python
async def build_system_prompt(
    model: Model,
    agent: Agent,
    instance: Instance
) -> str:
    """Build complete system prompt"""
    parts = []

    # 1. Provider-specific instructions
    parts.append(select_prompt(model.id))

    # 2. Environment context
    parts.append(await build_environment_context(model, instance))

    # 3. Skills information
    skills_prompt = await build_skills_prompt(agent)
    if skills_prompt:
        parts.append(skills_prompt)

    return "\n\n".join(parts)
```

## Environment Context

### Structure

```xml
You are powered by the model named {model.api.id}. The exact model ID is {model.providerID}/{model.api.id}
Here is some useful information about the environment you are running in:
<env>
  Working directory: {Instance.directory}
  Workspace root folder: {Instance.worktree}
  Is directory a git repo: {yes|no}
  Platform: {process.platform}
  Today's date: {new Date().toDateString()}
</env>
<directories>
  {optional directory tree}
</directories>
```

### Python Implementation

```python
async def build_environment_context(model: Model, instance: Instance) -> str:
    """Build environment context section"""
    project = instance.project

    parts = [
        f"You are powered by the model named {model.api_id}. "
        f"The exact model ID is {model.provider_id}/{model.api_id}",
        "Here is some useful information about the environment you are running in:",
        "<env>",
        f"  Working directory: {instance.directory}",
        f"  Workspace root folder: {instance.worktree}",
        f"  Is directory a git repo: {'yes' if project.vcs == 'git' else 'no'}",
        f"  Platform: {sys.platform}",
        f"  Today's date: {datetime.now().strftime('%a %b %d %Y')}",
        "</env>",
        "<directories>",
        # Optional: directory tree (currently disabled in OpenCode)
        "</directories>",
    ]

    return "\n".join(parts)
```

## Skills Formatting

### Verbose Format (for system prompt)

```xml
<available_skills>
  <skill>
    <name>skill-name</name>
    <description>Brief description</description>
    <location>file:///path/to/SKILL.md</location>
  </skill>
  ...
</available_skills>
```

### Compact Format (for tool description)

```markdown
## Available Skills
- **skill-name**: Brief description
- **another-skill**: Another description
```

### Python Implementation

```python
def format_skills(skills: list[Skill], verbose: bool = False) -> str:
    """Format skills for prompt"""
    if not skills:
        return "No skills are currently available."

    if verbose:
        # XML format for system prompt
        lines = ["<available_skills>"]
        for skill in skills:
            lines.extend([
                "  <skill>",
                f"    <name>{skill.name}</name>",
                f"    <description>{skill.description}</description>",
                f"    <location>file://{skill.location}</location>",
                "  </skill>",
            ])
        lines.append("</available_skills>")
        return "\n".join(lines)
    else:
        # Markdown format for tool description
        lines = ["## Available Skills"]
        for skill in skills:
            lines.append(f"- **{skill.name}**: {skill.description}")
        return "\n".join(lines)
```

### Skills Prompt Integration

```python
async def build_skills_prompt(agent: Agent) -> str | None:
    """Build skills section of system prompt"""
    # Check if skill tool is disabled for this agent
    if is_tool_disabled("skill", agent.permissions):
        return None

    # Get available skills (filtered by agent permissions)
    skills = await get_available_skills(agent)

    if not skills:
        return None

    return "\n".join([
        "Skills provide specialized instructions and workflows for specific tasks.",
        "Use the skill tool to load a skill when a task matches its description.",
        format_skills(skills, verbose=True)
    ])
```

## Prompt Loading

### File Loading

```python
from pathlib import Path
from functools import lru_cache

PROMPTS_DIR = Path(__file__).parent / "prompts"

@lru_cache(maxsize=10)
def load_prompt(filename: str) -> str:
    """Load prompt from file with caching"""
    path = PROMPTS_DIR / filename
    return path.read_text(encoding="utf-8").strip()
```

### Dynamic Injection

Prompts are loaded at runtime and can include:
- Model information
- Environment variables
- Current date/time
- Project context
- Available skills

## Prompt Preservation Rules

### Critical Requirements

1. **Exact Copy**: Prompt text must be copied word-for-word from OpenCode
2. **No Modifications**: Do not change wording, formatting, or structure
3. **Preserve Whitespace**: Keep all spacing, indentation, and line breaks
4. **Preserve XML Tags**: Keep all XML structure exactly as-is
5. **Preserve Examples**: Keep all examples and code snippets unchanged

### Verification Process

1. Copy prompt file from OpenCode
2. Compare character-by-character
3. Test with same inputs
4. Verify AI behavior matches

### Example Verification

```python
def verify_prompt_match(opencode_prompt: str, langcode_prompt: str) -> bool:
    """Verify prompts match exactly"""
    # Remove only leading/trailing whitespace
    oc = opencode_prompt.strip()
    lc = langcode_prompt.strip()

    if oc != lc:
        # Show diff
        import difflib
        diff = difflib.unified_diff(
            oc.splitlines(keepends=True),
            lc.splitlines(keepends=True),
            fromfile="opencode",
            tofile="langcode"
        )
        print("".join(diff))
        return False

    return True
```

## Prompt Variables

### Template Variables

Prompts may reference these variables (injected at runtime):

- `${directory}` - Current working directory
- `${maxLines}` - Maximum lines for truncation
- `${maxBytes}` - Maximum bytes for truncation
- `${model.api.id}` - Model identifier
- `${model.providerID}` - Provider identifier
- `${Instance.directory}` - Instance directory
- `${Instance.worktree}` - Workspace root

### Python Implementation

```python
def inject_variables(prompt: str, context: dict) -> str:
    """Inject variables into prompt template"""
    import re

    def replace_var(match):
        var_name = match.group(1)
        return str(context.get(var_name, match.group(0)))

    # Replace ${variable} patterns
    return re.sub(r'\$\{([^}]+)\}', replace_var, prompt)
```

## Prompt Updates

### When to Update

Prompts should be updated when:
1. OpenCode releases new prompt versions
2. New features require prompt changes
3. Bug fixes in prompt wording

### Update Process

1. Pull latest OpenCode version
2. Copy prompt files
3. Verify no regressions
4. Test with various models
5. Document changes in DECISIONS.md

## Model-Specific Considerations

### Anthropic (Claude)

- Uses full feature set
- Includes todo tool
- Verbose instructions
- XML-heavy formatting

### OpenAI (GPT)

- Different tool format (apply_patch vs edit)
- Shorter instructions
- Less XML formatting
- Focus on function calling

### Google (Gemini)

- Custom formatting preferences
- Different tool descriptions
- Specific examples

### Default (Qwen, etc.)

- Based on Anthropic prompt
- Excludes todo tool
- Generic instructions

## Testing Prompts

### Unit Tests

```python
def test_prompt_selection():
    """Test correct prompt is selected for each model"""
    assert "claude" in select_prompt("claude-sonnet-4")
    assert "gpt" in select_prompt("gpt-4-turbo")
    assert "gemini" in select_prompt("gemini-pro")

def test_environment_context():
    """Test environment context generation"""
    context = build_environment_context(model, instance)
    assert instance.directory in context
    assert sys.platform in context

def test_skills_formatting():
    """Test skills are formatted correctly"""
    skills = [Skill(name="test", description="Test skill", ...)]

    # Verbose format
    verbose = format_skills(skills, verbose=True)
    assert "<available_skills>" in verbose
    assert "<name>test</name>" in verbose

    # Compact format
    compact = format_skills(skills, verbose=False)
    assert "## Available Skills" in compact
    assert "**test**" in compact
```

### Integration Tests

```python
async def test_full_prompt_composition():
    """Test complete prompt composition"""
    prompt = await build_system_prompt(model, agent, instance)

    # Should contain all sections
    assert "You are powered by" in prompt
    assert "<env>" in prompt
    assert "Working directory:" in prompt

    # Should contain skills if available
    if await get_available_skills(agent):
        assert "<available_skills>" in prompt
```

### Comparison Tests

```python
async def test_prompt_matches_opencode():
    """Compare output with OpenCode"""
    # Run same scenario in both
    oc_prompt = get_opencode_prompt(model, agent)
    lc_prompt = await build_system_prompt(model, agent, instance)

    # Should be identical (after normalizing dynamic parts)
    assert normalize_prompt(oc_prompt) == normalize_prompt(lc_prompt)
```

## Implementation Checklist

- [ ] Copy all prompt files from OpenCode
- [ ] Implement prompt selection logic
- [ ] Implement environment context generation
- [ ] Implement skills formatting (verbose and compact)
- [ ] Implement prompt composition
- [ ] Add variable injection
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Verify against OpenCode output
- [ ] Document any deviations

## Critical Notes

1. **Never modify prompt content** - Copy exactly from OpenCode
2. **Test with all model types** - Each model has different prompts
3. **Preserve XML structure** - AI models are sensitive to formatting
4. **Keep prompts in sync** - Update when OpenCode updates
5. **Document changes** - Track any necessary deviations

## Python-Specific Considerations

### File Encoding

Always use UTF-8 encoding:
```python
path.read_text(encoding="utf-8")
```

### Path Handling

Use pathlib for cross-platform compatibility:
```python
from pathlib import Path
PROMPTS_DIR = Path(__file__).parent / "prompts"
```

### Caching

Cache loaded prompts to avoid repeated file I/O:
```python
from functools import lru_cache

@lru_cache(maxsize=10)
def load_prompt(filename: str) -> str:
    ...
```

### Async Context

Environment and skills sections are async:
```python
async def build_system_prompt(...) -> str:
    parts = [
        select_prompt(model.id),  # Sync
        await build_environment_context(...),  # Async
        await build_skills_prompt(...),  # Async
    ]
    return "\n\n".join(filter(None, parts))
```
