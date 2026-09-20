---
name: write-recipe
description: Use when writing, editing, or reviewing an Intempt recipe in this repository. Covers the frontmatter schema, the copy rules a recipe is judged on, the validators, and the pull request flow.
---

# Writing an Intempt recipe

A recipe is a template Blu executes inside a customer's project, using **their** access.
It is read by two audiences that want opposite things, and most bad recipes fail because
they were written for only one:

| Audience | Reads | Wants |
|---|---|---|
| A customer deciding whether to run it | `title`, `shortDescription`, step titles and descriptions | plain language, specifics, no jargon |
| Blu, executing it | `description`, `command`, `prompt`, `bindsAs`, `dependsOn` | precision, exact rules, unambiguous bindings |

Write both. Do not let one leak into the other.

## Before you write

Read an existing recipe in the same group. Match its shape rather than inventing one:

```
ls recipes/            # the 12 groups
sed -n '1,60p' recipes/journeys/cart-recovery_recipe.md
```

Check your id does not already exist, and that your slash command is free:

```
grep -rl "id: your-recipe-id" recipes/
grep -rh "slashCommand:" recipes/ | sort | uniq -d
```

## The file

One file, `recipes/<group>/<id>_recipe.md`. The filename stem must equal `intempt.id`.

```yaml
---
name: <id>
description: |
  Use when a user mentions "<phrase>", "<phrase>", or asks for related help.
  <One line on what it does.>
arguments: []
intempt:
  id: <kebab-case, unique across the repo>
  title: <Real name. "Abandoned cart recovery", never the id.>
  version: 1.0.0
  slashCommand: /<unique>
  group: <Journeys | Segments | Reports | Dashboards | Experiments |
          Workflows | Personalizations | Meetings | Creative | Content |
          Agents | Recommendations>
  shortDescription: <One sentence. What the customer gets. Under 200 chars.>
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [<segments | marketing | sales | analytics | design | ...>]
    agent: <segment-architect | journey-builder | data-analyst | ...>
    mode: [<b2b | saas | ecommerce | all>]
    complexity: <quick | standard | advanced>
    executionMode: <oneshot | live | scheduled>
    tags: [<short>, <tags>]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: <shopify>, severity: <blocking | recommended> }
  invokesCommands:
    - <every command your procedure calls>
  procedure:
    - step: 1
      title: <Names the ACTION. Under ~40 chars.>
      command: <create_segment | create_journey | ...>
      produces: <segment | journey | ...>
      bindsAs: <handle later steps refer to>
      dependsOn: [<earlier bindsAs values>]
      description: <Plain language. Carries the real rule.>
      prompt: |
        <The precise instruction Blu executes.>
  outputs:
    - { name: <handle>, type: <type>, cardinality: single, description: "<plain>" }
---
<Markdown body: the human walkthrough.>
```

## The copy rules, which are what review actually checks

**`title`** is a real name a customer would say out loud. Never the id.

**`shortDescription`** says what they get, in one sentence, under 200 characters.

- Bad: `Recover abandoned carts with a 3-touch sequence: segment, content, journey, A/B variants, dashboard, alert workflow.`
- Good: `Emails shoppers who left items behind, three times over three days, and measures how much revenue comes back.`

The bad one lists the objects we build. That is our vocabulary, not the customer's.

**Step `title`** names the action. Under about 40 characters, because the console renders
each step as a canvas node 240px wide.

- Bad: `Build Content`, `Build Journey`, `Configure Segment Rule`
- Good: `Find who abandoned a cart`, `Schedule the sequence`

**Step `description`** carries the concrete rule: the threshold, the window, the exit
condition. The test is whether it could describe a different recipe. If it could, it is
too vague.

- Bad: `Open the segment authoring surface, name the segment, and apply the rule below.`
- Good: `Accounts created in the last 7 days, with 5 or fewer events, lifecycle set to prospect, and no open deal.`

**Never use an em-dash, an en-dash, or an arrow glyph** in any customer-visible field.
Use a colon, a full stop, or a comma. If a sentence needs a parenthetical dash pair, use
parentheses or split it in two.

**Declare every integration you name.** If your text mentions Shopify, HubSpot, Slack or
any other connector, it must appear under `prerequisites.integrations` or CI fails.

## Safety, which is why a human reviews every recipe

Your `prompt` is an instruction executed by an agent inside someone else's project.

- It runs with **the invoking person's own access**, so it can never escalate privilege.
  It can still make that person's credentials do something they did not intend.
- Do not put a URL in a prompt or a step config unless the recipe genuinely needs it.
  Commands that reach the network (`configure_webhook_step`, `configure_web_scrape_step`,
  `configure_slack_step`) get the closest reading in review.
- `invokesCommands` must list every command your procedure actually calls. A mismatch is
  a review failure, not a formatting nit.

## Validate before you push

```
python3 scripts/check_recipe_prerequisites.py
python3 scripts/build_artifacts.py --out /tmp/catalog --check
```

The second one is the copy gate. It fails on an empty or quote-wrapped
`shortDescription`, on an em-dash, en-dash or arrow, and on a duplicate id. It warns on
a `shortDescription` over 200 characters.

## Open the pull request

Against **`staging`**. Never against `main`, which is fast-forward only from staging.

```
git checkout -b feature/<short-name>
git add recipes/<group>/<id>_recipe.md
git commit
gh pr create --base staging
```

Say in the body what the recipe does for a customer and which integrations it needs. If
you are an external contributor, say which company you are contributing on behalf of.

## Red flags in your own draft

| If you wrote | Reconsider |
|---|---|
| a `shortDescription` listing objects built | say what the customer gets instead |
| a step titled `Build <Noun>` | name the action |
| a step description that fits any recipe | put the real rule in it |
| an em-dash | colon, full stop, or comma |
| a URL in a prompt | does the recipe truly need to reach that host |
| `invokesCommands` shorter than the procedure | list every command |
| `title` missing | it renders as a kebab-case id to customers |
