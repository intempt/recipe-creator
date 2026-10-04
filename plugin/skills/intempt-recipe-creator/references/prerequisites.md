# Prerequisites

The idea route and the existing-recipe route need nothing but a conversation. The workspace route
reads your Intempt project, so it needs the CLI and a sign-in. Validating and submitting from the
session use the CLI too.

## 1. Install the Intempt CLI

```
npm install -g @intempt-technologies/cli
intempt --version
```

## 2. Sign in, and say where you are

```
intempt login       # opens a browser once
intempt whoami      # prints your organization and project
```

**Say the organization and project out loud before reading anything.** A recipe built from the
wrong project's segments is a recipe about someone else's data. If it is the wrong one, switch
before going further.

## 3. Preflight the toolchain

```
intempt recipe validate examples/intempt/trial-expiring-nudge/recipe.md; echo "exit=$?"
```

Exit `0` means the toolchain works. Anything else means the problem is your setup, not your recipe,
so fix it here rather than at the last step. The `intempt recipe` commands are new; if your CLI does
not have them yet, update it, or use the Python validator in [VALIDATION.md](validation.md), which
needs Python 3 and PyYAML.

## 4. Install the plugin

| Host | Install |
|---|---|
| **Claude Code** | `/plugin marketplace add intempt/recipe-creator` then `/plugin install intempt-recipe-creator@intempt-recipe-creator` |
| **Codex** | `codex plugin marketplace add intempt/recipe-creator`, then install **intempt-recipe-creator** from Plugins |
| **Cursor** | Add `https://github.com/intempt/recipe-creator` as a plugin marketplace, then install **intempt-recipe-creator** |

## Keeping the plugin current

Nothing updates on its own. The skill checks the published version on every run and switches to it
when it is newer, so most of the time you do not need to do anything. To refresh the install itself
in Claude Code:

```
/plugin marketplace update intempt-recipe-creator
/plugin install intempt-recipe-creator@intempt-recipe-creator
```

If that still installs an old copy, remove both caches and add the marketplace again:

```
rm -rf ~/.claude/plugins/marketplaces/intempt-recipe-creator
rm -rf ~/.claude/plugins/cache/intempt-recipe-creator
```

Read the installed version off disk, not off the announce line:

```
grep -m1 -o 'intempt-recipe-creator/[0-9.]*' ~/.claude/plugins/cache/intempt-recipe-creator/*/*/skills/intempt-recipe-creator/SKILL.md
```
