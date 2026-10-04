# Recipe template

Copy this into `<your-handle>/<your-recipe-id>/recipe.md` in your working directory, or run
`intempt recipe new <your-recipe-id> --owner <your-handle>`. Replace every value. The body under
the frontmatter is generated: `intempt recipe new` writes it, and in this repository
`python3 scripts/rebuild_bodies.py` regenerates it.

```yaml
---
id: your-recipe-id
title: A name a customer would say out loud
slash_command: /your-recipe-id
group: Segments
owner: your-partner-folder
summary: >-
  What the customer gets, in one sentence, under 200 characters.
description: >-
  What the whole recipe is for and when Blu should offer it.
version: 1.0.0
classification:
  product:
    - segments
  mode:
    - saas
  complexity: quick
  tags:
    - your-tag
inputs:
  - input: Something only the installer has
    what_the_installer_supplies: What they give, in plain words
    if_missing: What happens without it, for example the step waits until one is chosen
does_not_claim:
  - Anything the recipe does not prove, for example where a threshold came from.
touches:
  reads:
    - The events and attributes the steps name, in plain words
  writes:
    - A new segment, from step 1 "An action, under 40 characters"
    - A new designed email, from step 2 "The next action"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: An action, under 40 characters
    summary: >-
      The concrete rule, in words a customer reads on the Marketplace.
    builds: segment
    description: >-
      Build a segment of users who ... Name the event or attribute exactly as it exists in
      the project, and write out every value.
  - id: s2
    title: The next action
    summary: >-
      What this step produces, for the customer.
    builds: email_html
    description: >-
      Write a designed email for the users in "An action, under 40 characters". Say the
      tone, the length and the call to action.
    dependsOn:
      - s1
outputs:
  - key: your_segment
    producedByStep: s1
    type: segment
  - key: your_email
    producedByStep: s2
    type: email_html
---
```

`touches` is required. `inputs` and `does_not_claim` are optional; leave them out rather than fill
them with nothing. All three render into the body as "What this recipe touches", "Declared inputs"
and "What this recipe does not claim".

`builds` must be a value from [references/entities.md](./references/entities.md). Use only
the Install now list if you want the recipe runnable on day one.
