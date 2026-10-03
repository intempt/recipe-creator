# Recipe template

Copy this into `recipes/<your-partner-folder>/<your-recipe-id>/recipe.md`, replace every
value, then run `python3 scripts/rebuild_bodies.py` to generate the body.

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

`builds` must be a value from [references/entities.md](./references/entities.md). Use only
the Install now list if you want the recipe runnable on day one.
