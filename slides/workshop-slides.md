# Building AI-Powered Tools with Claude Code Skills & Sub-agents

## Workshop for Generix Development Team

**Duration:** 90 minutes (hands-on)
**Application:** `docgen` -- Documentation Generator CLI

> NARRATION: Welcome to the workshop. Today we're going to build and extend an AI-powered documentation generator. Along the way, you'll learn how to create reusable skills, set up specialized sub-agents, and orchestrate them together. These are patterns you can apply to any project.

---

## What We'll Learn

1. **Structure SKILL.md files** for predictable AI workflows
2. **Create sub-agents** with specific skills and controlled permissions
3. **Trigger, test, and orchestrate** sub-agents together

> NARRATION: By the end of this workshop, you'll have hands-on experience with all three of these. We'll do three guided exercises where you build these yourself. The concepts apply to any project -- not just this demo app.

---

## The Application: `docgen`

**What it does:** CLI that generates documentation for source code using an LLM

**Commands:**

- `docgen generate <file>` -- Generate docs for a source file
- `docgen list` -- Show all documented files
- `docgen check <file>` -- Check if docs are still accurate

**Tech stack:** Python, Typer, Rich, OpenAI SDK, JSON storage

> NARRATION: Our demo app is a documentation generator. You point it at a source file, it reads the code, sends it to an LLM, and produces markdown documentation. It can also list what's been documented and check if docs are still accurate when code changes.

---

## Architecture Overview

```
main.py
  |
  v
commands/__init__.py
  |
  +-- generate.py
  +-- list.py
  +-- check.py
  +-- update.py
  |
  +-- llm.py        (OpenAI SDK)
  +-- storage.py    (JSON persistence)
  +-- display.py    (Rich terminal output)
```

> NARRATION: The architecture follows a clean separation of concerns. The entry point routes to individual command files. Each command uses three shared modules: llm.py for LLM calls, storage.py for persistence, and display.py for terminal output. This is the same pattern you'll see in many CLI applications.

---

## CLAUDE.md: Your Project's Context

**What goes in CLAUDE.md:**

- Tech stack and dependencies
- Architecture map
- Data models and schemas
- Development commands (`run`, `test`, `lint`)
- Rules and conventions

**Key insight:** Always loaded in every conversation -- this is your project's brain.

> NARRATION: CLAUDE.md is a special file that Claude Code reads at the start of every conversation. It gives Claude the context about your project -- the tech stack, the architecture, how data flows, and any rules. Think of it as the documentation that Claude always has in mind. Let me show you ours.

---

## Live Demo: Using the App

```bash
# Generate documentation for a file
docgen generate src/docgen/models.py
# --> creates docs/models.md

# List all documented files
docgen list
# --> shows table of documented files

# Check if docs are still accurate
docgen check src/docgen/models.py
# --> reports accuracy status
```

> NARRATION: Let me show you the app in action. First I'll generate docs for our models file -- watch the LLM call happen. Now let's list what we've documented. And finally, let's check if the docs are still accurate. Each of these commands follows the same pattern: validate input, call LLM if needed, update storage, display results.

---

## What Are Skills?

- **Skills = reusable instruction sets** for specific workflows
- Stored in `.claude/skills/<name>/SKILL.md`
- **Loaded on demand** -- NOT always in context
- Think of them as **"playbooks"** for specific tasks

> NARRATION: Skills are markdown files that define how Claude should handle specific tasks. Unlike CLAUDE.md which is always loaded, skills are loaded on demand -- only when the task matches. This keeps your context clean. You only load the instructions you need, when you need them.

---

## Skills vs CLAUDE.md

| | **CLAUDE.md** | **Skills** |
|---|---|---|
| **Loaded** | Always | On demand |
| **Scope** | Project-wide context | Task-specific workflows |
| **Answers** | "What is this project?" | "How do I do this specific task?" |

> NARRATION: Here's the key distinction. CLAUDE.md answers "what is this project?" -- it's always there. Skills answer "how do I do this specific task?" -- they're loaded only when relevant. If a convention applies to every conversation, put it in CLAUDE.md. If it's a specific workflow, make it a skill.

---

## Anatomy of a SKILL.md File

```
1. Name & Description       --> When to trigger
2. Workflow                  --> Step-by-step instructions
3. Code Examples             --> CORRECT vs WRONG patterns
4. Conventions & Checklist   --> Final validation
```

**Flow:** Trigger --> Workflow --> Validate

> NARRATION: Every skill follows this structure. The description tells Claude when to use it. The workflow gives step-by-step instructions. Code examples show exactly which patterns to follow -- both good and bad examples. And the checklist ensures nothing is missed. Let's look at a real one.

---

## Methodology: Creating a Skill

1. **Identify** the repeatable task
2. **Define** the trigger conditions
3. **Write** step-by-step workflow
4. **Add code examples** with CORRECT / WRONG patterns
5. **Add conventions checklist**
6. **Test** by asking Claude to use it

> NARRATION: This is the methodology you'll follow in Exercise 1. Start by identifying what task you're codifying. Then define when Claude should use this skill. Write the workflow. Add concrete code examples -- Claude does really well when you show it exactly the pattern you want. Add a checklist. And finally, test it. This process works for any skill.

---

## Walk-through: `generating-documentation` Skill

**File:** `.claude/skills/generating-documentation/SKILL.md`

**Highlights:**

- LLM module usage (correct vs wrong)
- Prompt engineering pattern
- Error handling conventions
- Storage update flow
- Checklist of conventions

> NARRATION: Let me open our pre-built skill and walk through it. Notice how specific the code examples are -- we show exactly how to call the LLM module and exactly what NOT to do. We define the prompt engineering pattern. We specify error handling. And we have a checklist at the end. This is the level of detail that makes skills effective.

---

## Exercise 1: Create a Skill

### Create the `reviewing-documentation` skill

**Duration:** 10-12 minutes

- **Template:** `exercises/exercise-1-template-SKILL.md`
- **Good reference:** `generate.py` (follows all conventions)
- **Bad reference:** `update.py` (breaks conventions -- your skill should catch these)

> NARRATION: Now it's your turn. You're going to create a skill for reviewing code quality. I've provided a template with the structure -- you need to fill in the content. Look at generate.py as the gold standard for what good code looks like, and update.py for all the things your skill should catch. Follow the exercise guide step by step.

---

## Why Sub-agents?

**Problem:** Main agent does everything --> fills up context window, gets slow

**Solution:** Delegate to specialized sub-agents

```
Main Agent
  |
  +-- dispatches --> doc-reviewer   --> results back
  +-- dispatches --> doc-generator  --> results back
```

> NARRATION: So far we've been working with the main agent doing everything. But for larger projects, this fills up the context window fast. Sub-agents solve this -- they're specialized workers that run in their own context. The main agent dispatches them, they do their job, and return results. Much more efficient.

---

## Sub-agents: Key Concepts

1. Sub-agents **do NOT inherit** skills from parent
2. You must **explicitly assign** skills
3. You **control which tools** each agent gets
4. Entire SKILL.md is **loaded when agent is dispatched**

> NARRATION: Critical point -- sub-agents don't automatically get the parent's skills. You have to be explicit. Same with tools -- you choose exactly which tools each agent can use. When an agent is dispatched, its assigned skills are fully loaded into its context. This gives you precise control over what each agent can do.

---

## Principle of Least Privilege

| **doc-reviewer** | **doc-generator** |
|---|---|
| Read, Glob, Grep | Read, Write, Edit, Bash, Glob, Grep |
| "Can look, can't touch" | "Can look AND modify" |

**Key insight:** Give each agent only the permissions it needs.

> NARRATION: This is the principle of least privilege applied to AI agents. Our reviewer can only read files -- it reports issues but can't change anything. Our generator can read AND write -- it needs to create documentation files. Neither agent has more power than it needs. This is a good practice for any system, AI or otherwise.

---

## Creating an Agent: `/agents`

**Steps:**

1. `/agents` --> Create new --> Project
2. Choose **Manual configuration**
3. Configure each field:
   - **name** -- Agent identifier
   - **prompt** -- Personality and role
   - **description** -- When to dispatch
   - **tools** -- Allowed capabilities
   - **model** -- Which Claude model
   - **color** -- Terminal display color
   - **skills** -- Assigned SKILL.md files

> NARRATION: Creating an agent is straightforward. Use the /agents command, choose manual configuration so you can see each field. You'll set a name, write a prompt that defines the agent's personality, choose tools, and assign skills. Let me demonstrate the flow.

---

## Agent Prompt vs Skill

| | **Prompt** | **Skill** |
|---|---|---|
| **Purpose** | Agent's personality and role | Specific workflow and conventions |
| **Scope** | Generic, reusable | Detailed, task-specific |
| **Defines** | WHO the agent is | HOW it does tasks |

**Together = Powerful, predictable behavior**

> NARRATION: Think of the prompt as the agent's personality -- it defines WHO the agent is. The skill defines HOW it does specific tasks. The prompt can be generic enough to reuse across projects. The skill provides the project-specific conventions. Together, they give you predictable, high-quality behavior.

---

## Exercise 2: Create Sub-agents

### Create two sub-agents with different permissions

**Duration:** 10-12 minutes

| Agent | Tools | Skill |
|---|---|---|
| `doc-reviewer` | Read, Glob, Grep | `reviewing-documentation` |
| `doc-generator` | Read, Write, Edit, Bash, Glob, Grep | `generating-documentation` |

> NARRATION: Time for Exercise 2. You're going to create both sub-agents using the /agents command. Pay close attention to which tools you give each one. The reviewer gets read-only tools. The generator gets read-write tools. Don't forget to add the skills field after creating each agent. Follow the exercise guide.

---

## Triggering Sub-agents

**How to trigger:** Just ask naturally!

```
"Use the doc-reviewer to review update.py"
```

1. Claude dispatches the agent with its skills and tools
2. Agent works in its own context
3. Returns results to main agent

> NARRATION: Triggering a sub-agent is as simple as asking. Say "use the doc-reviewer to review update.py" and Claude dispatches it. The agent runs in its own context window with its assigned skills loaded. When it's done, the results come back to the main agent. Natural language is all you need.

---

## Demo: Reviewing the Bad Command

**Command:** "Use the doc-reviewer to review update.py"

**Expected issues found:**

- No type annotations
- `print()` instead of `display` module
- Wrong exit codes
- No input validation
- Inline LLM calls (not using `llm.py`)
- Direct storage manipulation (not using `storage.py`)
- Missing docstring

> NARRATION: Let me show you the reviewer in action. I'll ask it to review our intentionally bad update.py command. Watch the sub-agent get dispatched... and here's the report. It found all the issues -- no type annotations, using print instead of display, wrong exit codes. This is exactly what our skill told it to check.

---

## Demo: Fixing Based on Review

**Flow:** Main agent reads review output --> applies fixes

**Before / After:**

- `print()` --> `display.info()`, `display.error()`
- No types --> Full type annotations
- `sys.exit(1)` --> `raise typer.Exit(code=1)`
- Inline LLM --> `llm.generate_documentation()`
- Raw JSON --> `storage.save_entry()`

> NARRATION: Now the main agent takes the reviewer's report and fixes each issue. Watch as it adds type annotations, replaces print with display methods, fixes the exit codes, adds validation. The main agent doesn't need the reviewing skill loaded -- it just uses the output.

---

## Demo: Generating Documentation

**Command:** "Use the doc-generator to generate docs for storage.py"

**What happens:**

1. Agent reads `src/docgen/storage.py`
2. Calls LLM via `llm.py` module
3. Writes `docs/storage.md`
4. Updates storage entry
5. Verify: `docgen list` shows new entry

> NARRATION: Now let's use our generator. I'll ask it to document storage.py. The agent reads the file, calls the LLM through our llm.py module, writes the markdown to docs/storage.md, and updates the storage entry. Let me verify with docgen list -- there it is.

---

## Exercise 3: Trigger and Test

### Put your agents to work!

**Duration:** 10-12 minutes

1. Review `update.py` with `doc-reviewer`
2. Fix the issues with the main agent
3. Generate docs with `doc-generator`
4. Verify with `docgen list`

**Bonus:** Add a `summarize` command and run both agents on it

> NARRATION: Final exercise. You're going to trigger both agents yourself. Start by having the reviewer check update.py. Then fix the issues. Then generate documentation for a file. And verify everything works with docgen list. If you finish early, try the bonus -- add a new command and run both agents on it.

---

## What We Built

- A working **CLI app** with LLM integration
- **2 skills:** generating and reviewing documentation
- **2 sub-agents:** generator (read-write) and reviewer (read-only)
- A complete **review --> fix --> generate** workflow

> NARRATION: Let's recap what we built today. A real CLI application that calls an LLM. Two skills that codify our workflows. Two sub-agents with different permissions. And we saw how to orchestrate them -- review code, fix issues, generate documentation. These patterns scale to any project.

---

## Key Takeaways

1. **Skills** = predictable workflows for specific tasks
2. **Sub-agents** = specialized workers with controlled permissions
3. **CLAUDE.md** = project context, always available
4. **Principle of least privilege** applies to AI agents too

> NARRATION: Four things to remember. Skills give you predictable workflows. Sub-agents give you specialized, permission-controlled workers. CLAUDE.md is your project's always-on context. And just like with human access control, give AI agents only the permissions they need. These principles work for any project.

---

## Next Steps

**Create skills for YOUR Generix projects:**

- Deployment skill
- Code review skill
- Testing skill

**Share with your team:**

- Project-level: `.claude/skills/` in your repo
- User-level: `~/.claude/skills/` for personal workflows

**Resources:** Claude Code docs, `/skills` and `/agents` commands

> NARRATION: What's next? Take these patterns back to your own projects. Think about what workflows you repeat -- those are candidates for skills. Share skills with your team through the project .claude folder. Experiment with sub-agents for different roles. The /skills and /agents commands are your starting points. Thank you!
