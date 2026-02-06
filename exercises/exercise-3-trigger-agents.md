# Exercise 3: Triggering and Testing Sub-agents

**Duration:** 10-12 minutes
**Goal:** Trigger both sub-agents, observe their behavior, and experience the full review-fix-generate workflow.

---

## Context

You have built the pieces: a skill that defines review standards (Exercise 1) and two sub-agents with scoped permissions (Exercise 2). Now you will put them to work.

In this exercise, you will:
1. Dispatch the `doc-reviewer` to find issues in `update.py`
2. Have the main agent fix the issues
3. Dispatch the `doc-generator` to create documentation
4. Verify the results through the `docgen` CLI

This is the workflow that makes sub-agents valuable: specialized agents handle specialized tasks in their own context window, while the main agent stays focused on development and orchestration.

---

## Step 1: Trigger the doc-reviewer

### 1a. Dispatch the Reviewer

In Claude Code, type the following prompt:

```
Use the doc-reviewer to review the update.py command
```

### 1b. Observe What Happens

Watch the Claude Code interface carefully. You should see:

1. The main agent recognizes this is a task for the `doc-reviewer` sub-agent
2. The sub-agent is dispatched — notice it loads in its own context
3. The `reviewing-documentation` skill is loaded automatically
4. The sub-agent reads `update.py`, then reads the reference files (`display.py`, `constants.py`, `llm.py`, `generate.py`)
5. It checks `update.py` against every item in the conventions checklist
6. It produces a structured report

### 1c. Read the Review Output

The reviewer should find multiple issues in `update.py`. Expect findings like:

| Severity | Description | Location |
|----------|-------------|----------|
| Critical | No type annotations — parameters use bare types without `Annotated` | Function signature |
| Critical | Using `print()` instead of `display` module | Multiple lines |
| Critical | Using magic number exit codes instead of named constants | `raise typer.Exit(1)` |
| Critical | No input validation — file paths not checked before use | Top of function |
| Critical | Inline LLM calls — importing OpenAI directly instead of using `llm` module | Import section and function body |
| Critical | Direct JSON manipulation instead of using `storage` module | File I/O section |
| Warning  | Missing docstring on command function | Function definition |
| Warning  | No error handling / try-except blocks | Entire function |

> **Key Observation:** Notice that the reviewer found all these issues but did NOT attempt to fix any of them. It cannot — it only has Read, Glob, and Grep tools. This is the principle of least privilege in action. The reviewer reports; the developer (or main agent) decides what to fix.

---

## Step 2: Fix the Issues

### 2a. Ask the Main Agent to Fix

Now ask the main agent (not the sub-agent) to fix the issues:

```
Fix the issues found by the reviewer in update.py
```

### 2b. Observe the Fix Process

Watch how the main agent handles this:

1. It reads the review output from the sub-agent
2. It reads `update.py` to understand the current state
3. It reads `generate.py` as the reference for correct patterns
4. It applies fixes one by one:
   - Adds `Annotated` type annotations with help text
   - Replaces `print()` calls with `display.success()`, `display.error()`, etc.
   - Replaces magic exit codes with named constants from `constants.py`
   - Adds input validation at the top of the function
   - Replaces inline OpenAI calls with `llm.generate_documentation()`
   - Replaces direct JSON manipulation with `storage.add_entry()`
   - Adds a docstring
   - Wraps the logic in try-except blocks

### 2c. Verify the Fixes

After the main agent finishes, you can optionally re-run the reviewer to confirm:

```
Use the doc-reviewer to review update.py again
```

The review should now come back clean, or with only minor warnings.

> **Key Observation:** The main agent used its full tool set (Read, Write, Edit) to apply fixes. The reviewer could not have done this on its own. This separation creates a natural checkpoint: review first, then decide what to fix.

---

## Step 3: Trigger the doc-generator

### 3a. Dispatch the Generator

Type the following prompt in Claude Code:

```
Use the doc-generator to generate documentation for storage.py
```

### 3b. Observe What Happens

The `doc-generator` sub-agent will:

1. Load in its own context with the `generating-documentation` skill
2. Read `storage.py` to understand the module's API, functions, and purpose
3. Use the `llm` module to generate comprehensive markdown documentation
4. Write the output to `docs/storage.md`
5. Update the storage index so `docgen list` knows about the new documentation

### 3c. Check the Output

After the generator finishes, verify the documentation was created:

```bash
cat docs/storage.md
```

The documentation should include:
- Module overview and purpose
- Function signatures with parameter descriptions
- Return value documentation
- Usage examples
- Any important notes or caveats

> **Key Observation:** The generator has Write, Edit, and Bash tools because it needs to create files and potentially run commands. The reviewer does not have these tools. Each agent has exactly the permissions its job requires.

---

## Step 4: Verify with the App

Run the `docgen` CLI to confirm everything is registered:

```bash
uv run docgen list
```

You should see `storage.md` (or `storage.py`) listed as a documented module. This confirms the generator not only created the documentation file but also updated the storage index correctly.

> **Hint:** If the entry does not appear, the generator may not have called `storage.add_entry()`. You can ask the main agent to check and fix this.

---

## Step 5 (Bonus): Full Workflow

If you have time remaining, try the complete development-review-document workflow:

### 5a. Create a New Command

Ask the main agent:

```
Add a new "summarize" command to docgen that takes a docs/ directory and produces a summary of all documented modules
```

The main agent will create a new command file (e.g., `summarize.py`), register it with the CLI, and implement the logic.

### 5b. Review the New Command

Dispatch the reviewer:

```
Use the doc-reviewer to review the summarize command
```

Since the main agent wrote the command with awareness of project conventions (it has been reading `generate.py` and the skill throughout this session), the review should come back relatively clean. But there may still be issues — this is normal and valuable.

### 5c. Document the New Command

Dispatch the generator:

```
Use the doc-generator to generate documentation for summarize.py
```

### 5d. Final Verification

```bash
uv run docgen list
```

You should now see the summarize command documented alongside the other modules.

---

## What You Learned

### The Sub-agent Pattern

```
Main Agent (orchestrator)
  |
  |-- dispatches --> doc-reviewer (read-only, reports issues)
  |                    |-- loads skill: reviewing-documentation
  |                    |-- tools: Read, Glob, Grep
  |
  |-- reads review output, applies fixes
  |
  |-- dispatches --> doc-generator (read-write, creates docs)
                       |-- loads skill: generating-documentation
                       |-- tools: Read, Write, Edit, Bash, Glob, Grep
```

### Why This Is Better Than One Agent Doing Everything

1. **Context window efficiency.** Each sub-agent gets its own context window. The main agent's context is not consumed by the detailed review checklist or documentation generation prompts. This matters in long sessions where context space is precious.

2. **Consistency through skills.** The reviewer always checks the same checklist, every time, without forgetting items. A human or a general-purpose agent might skip checks when tired or distracted. The skill makes the review deterministic and exhaustive.

3. **Safety through permissions.** The reviewer physically cannot modify code. This is not a suggestion or a prompt instruction — it literally does not have the Write tool. This is a stronger guarantee than telling an agent "please don't modify files."

4. **Composability.** You can reuse these agents in different workflows. Need to review all commands before a release? Loop the reviewer over every file. Need to regenerate all docs after a refactor? Loop the generator. The agents are building blocks.

5. **Auditability.** Each sub-agent's output is a discrete, readable artifact. You can review what the reviewer found, verify what the generator wrote, and trace every decision. This is much harder when everything happens in one long conversation.

---

## Success Criteria

You have completed this exercise when:
- [ ] You triggered the `doc-reviewer` and received a structured report of issues in `update.py`
- [ ] The main agent fixed the issues based on the review output
- [ ] You triggered the `doc-generator` and `docs/storage.md` was created
- [ ] `uv run docgen list` shows the newly documented module
- [ ] You can explain why sub-agents are more effective than a single agent for specialized tasks
