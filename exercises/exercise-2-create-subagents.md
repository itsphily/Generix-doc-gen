# Exercise 2: Creating Sub-agents with Skills and Tools

**Duration:** 10-12 minutes
**Goal:** Create two sub-agents — `doc-reviewer` and `doc-generator` — each with carefully scoped permissions and attached skills.

---

## Context

Sub-agents are specialized Claude instances that the main agent can dispatch to handle focused tasks. Each sub-agent has:
- A **prompt** defining its role and behavior
- A **set of tools** it is allowed to use (principle of least privilege)
- **Skills** that give it domain-specific knowledge
- Its **own context window**, so it does not consume the main agent's context

The critical design principle here is **least privilege**: each agent gets only the tools it needs, nothing more. A reviewer that can modify code is dangerous. A generator that cannot write files is useless. Getting the tool permissions right is what makes sub-agents safe and effective.

---

## Step 1: Understand the Permission Model

Before creating any agents, understand WHY the tools differ:

| Agent | Purpose | Can Read | Can Write | Can Run Commands |
|-------|---------|----------|-----------|-----------------|
| `doc-reviewer` | Review code quality | Yes | **No** | **No** |
| `doc-generator` | Generate documentation | Yes | Yes | Yes |

**Why the reviewer cannot write:**
- A reviewer's job is to report issues, not fix them
- If the reviewer could modify files, it might silently "fix" things without the developer's knowledge
- Separation of concerns: the main agent decides what to fix based on the review output
- This mirrors real-world code review — reviewers comment, authors fix

**Why the generator needs write access:**
- It must create new markdown files in `docs/`
- It must update the storage index via the `storage` module
- It may need to run shell commands (e.g., `uv run docgen list` to verify results)

---

## Step 2: Create the `doc-reviewer` Agent

### 2a. Open the Agent Creation Interface

1. Open Claude Code in the `docgen` project directory
2. Type `/agents`
3. Select **"Create new agent"**
4. Select **"Project"** (so the agent is stored in `.claude/agents/`)
5. Select **"Manual configuration"**

### 2b. Configure the Agent

Fill in the following fields:

**Name:**
```
doc-reviewer
```

**Prompt** (copy and paste this exactly):
```
You are a code and documentation reviewer ensuring high quality standards.
When invoked, review CLI command files and generated documentation for code quality, convention adherence, input validation, and documentation accuracy.
Output: Issues table with severity, description, suggested fix. Summary with counts. Specific code fixes for critical issues.
```

**Description:**
```
Reviews code and documentation quality. Use when the user asks to review, audit, or check quality.
```

**Tools:** Select ONLY the following three tools, and deselect everything else:
- Read
- Glob
- Grep

**Model:** Inherit from parent

**Color:** Purple

### 2c. Save and Add the Skill

After saving, Claude Code creates the file `.claude/agents/doc-reviewer.md`. Open this file and add the skills section at the bottom:

```yaml
skills:
  - reviewing-documentation
```

This links the skill you created in Exercise 1 to this agent. When the main agent dispatches `doc-reviewer`, it will automatically load the `reviewing-documentation` skill into the sub-agent's context.

> **Hint:** The `skills` section must be at the top level of the agent file's frontmatter, or appended as metadata depending on the format Claude Code uses. Open the file after saving to see its structure and add the skills reference in the correct location.

---

## Step 3: Create the `doc-generator` Agent

### 3a. Open the Agent Creation Interface Again

1. In Claude Code, type `/agents`
2. Select **"Create new agent"**
3. Select **"Project"**
4. Select **"Manual configuration"**

### 3b. Configure the Agent

**Name:**
```
doc-generator
```

**Prompt** (copy and paste this exactly):
```
You are a documentation generator that reads source code and produces comprehensive markdown documentation.
When invoked, read target source files, use llm.py to generate docs, write to docs/ directory, update storage.
Output: What files were documented, where docs were saved, any issues encountered.
```

**Description:**
```
Generates and updates documentation. Use when asked to generate, write, or update docs.
```

**Tools:** Select the following six tools:
- Read
- Write
- Edit
- Bash
- Glob
- Grep

**Model:** Inherit from parent

**Color:** Yellow

### 3c. Save and Add the Skill

After saving, open `.claude/agents/doc-generator.md` and add:

```yaml
skills:
  - generating-documentation
```

> **Note:** The `generating-documentation` skill may not exist yet if it was not part of the pre-built materials. That is fine — the agent will still function, and the skill can be added later. The important thing is that the agent file references it so it will be loaded when the skill becomes available.

---

## Step 4: Verify Both Agents

Check that both agent files exist in the `.claude/agents/` directory:

```bash
ls -la .claude/agents/
```

You should see:
```
doc-reviewer.md
doc-generator.md
```

Open each file and verify:
- The prompt matches what you entered
- The tools list is correct (3 tools for reviewer, 6 for generator)
- The skills reference is present

### Quick Verification Checklist

For `doc-reviewer.md`:
- [ ] Prompt mentions "reviewer" and "quality standards"
- [ ] Only Read, Glob, Grep are listed as tools
- [ ] Skills references `reviewing-documentation`
- [ ] Color is purple

For `doc-generator.md`:
- [ ] Prompt mentions "documentation generator" and "write to docs/"
- [ ] Read, Write, Edit, Bash, Glob, Grep are listed as tools
- [ ] Skills references `generating-documentation`
- [ ] Color is yellow

---

## Step 5: Reload Claude Code

Close and reopen Claude Code so it detects the new agents.

After reopening, type `/agents` to see the list. Both `doc-reviewer` and `doc-generator` should appear.

> **Hint:** If an agent does not appear, check:
> - The file is in `.claude/agents/` (not `.claude/skills/` or another directory)
> - The filename ends in `.md`
> - The file is valid markdown with proper frontmatter

---

## Why This Matters

The separation you just created is a miniature version of how production AI systems are designed:

1. **Least privilege prevents accidents.** The reviewer cannot accidentally overwrite a file. The generator cannot accidentally delete code. Each agent can only do what it is designed to do.

2. **Specialized context is more effective.** Instead of one agent trying to be an expert at everything, each sub-agent loads only the knowledge (skills) it needs. This means less noise in the context window and more focused, accurate results.

3. **The main agent orchestrates.** Your main Claude Code session acts as the "manager" — it decides when to dispatch each sub-agent, reads their output, and takes action. This mirrors how a tech lead delegates code reviews and documentation tasks to specialists.

4. **Skills make agents consistent.** Without the skill, the reviewer would use its general knowledge to review code. With the skill, it checks against YOUR project's specific conventions. This is the difference between a generic review and a useful one.

---

## Success Criteria

You have completed this exercise when:
- [ ] `.claude/agents/doc-reviewer.md` exists with the correct prompt, 3 tools (Read, Glob, Grep), and the `reviewing-documentation` skill
- [ ] `.claude/agents/doc-generator.md` exists with the correct prompt, 6 tools (Read, Write, Edit, Bash, Glob, Grep), and the `generating-documentation` skill
- [ ] Both agents appear when you run `/agents` in Claude Code
- [ ] You can explain why the reviewer has fewer tools than the generator
