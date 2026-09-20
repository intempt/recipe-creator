# Intempt Recipes

Pre-built automations for the [Intempt](https://intempt.com) platform. Each recipe is a
markdown file that Blu, Intempt's agent, executes on your behalf: build a segment, run a
journey, compose a dashboard, generate creative.

**302 recipes** across 12 groups. Anyone can propose one.

```
recipes/
  agents/                1
  content/               4
  creative/             32
  dashboards/           21
  experiments/          24
  journeys/             35
  meetings/              9
  personalizations/      9
  recommendations/       1
  reports/              71
  segments/             47
  workflows/            48
```

## What a recipe is

A recipe is a template, not a script you run yourself. It describes an outcome in
steps, and Blu carries the steps out inside your project using your own access.
Nothing in a recipe can do more than you can.

Recipes in this repository are **global**: identical for every customer, read-only,
and published to a catalog that the Intempt website and console both read.

When you use one, Intempt makes a **copy in your project**. That copy is yours to
edit and it never changes underneath you when the original is updated.

## Anatomy

Every recipe is one `.md` file with YAML frontmatter.

```yaml
---
name: cart-recovery
description: |
  Use when a user mentions "abandoned cart", "cart recovery", or asks for related help.
arguments: []
intempt:
  id: cart-recovery
  title: Abandoned cart recovery
  version: 1.0.0
  slashCommand: /cart-recovery
  group: Journeys
  shortDescription: Emails shoppers who left items behind, three times over three days.
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [ecommerce]
    complexity: advanced
    executionMode: live
    tags: [cart, recovery]
  prerequisites:
    integrations:
      - { value: shopify, severity: blocking }
  procedure:
    - step: 1
      title: Find who abandoned a cart
      command: create_segment
      produces: segment
      bindsAs: cart_abandoners
      description: >
        Shoppers with a cart_abandoned event in the last 30 days who never
        placed an order for that cart.
      prompt: |
        Create a segment called "Cart Abandoners" ...
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "The audience." }
---
Markdown body: the human-readable walkthrough.
```

Two fields do different jobs and are easy to confuse:

| Field | Read by | Written for |
|---|---|---|
| `description` | Blu, to decide when a recipe is relevant | intent matching, not customers |
| `shortDescription` | customers, on the website and in the console | one plain sentence, what they get |

## Writing a good one

The bar is that a customer who has never seen your recipe understands what it does
before they run it.

- **`title`** is a real name. "Abandoned cart recovery", not `cart-recovery`.
- **`shortDescription`** says what the customer gets, in one sentence, under 200
  characters. Never list the objects it builds: "segment, content, journey,
  dashboard" is our vocabulary, not theirs.
- **Step `title`** names the action, not the object type. "Find who abandoned a
  cart", not "Build Segment". Keep it under about 40 characters so it fits a
  canvas node.
- **Step `description`** carries the real rule: the threshold, the timing, the exit
  condition. If it could describe any recipe, it is not specific enough.
- **No em-dashes and no arrow glyphs.** Use a colon, a full stop, or a comma.
- **Declare every integration you mention** under `prerequisites.integrations`, or
  CI will fail the pull request.

## Contributing

1. Fork, branch, add or edit a file under `recipes/<group>/`.
2. Open a pull request **against `staging`**. Not `main`.
3. CI checks prerequisites, id and slash-command uniqueness, and the copy rules.
4. A maintainer reviews. Recipes are executed inside customer projects, so review
   is about safety as much as quality.
5. Merged to `staging`, your recipe is live for internal testing. It reaches
   customers when `staging` is promoted to `main`.

`main` is fast-forward only from `staging`. There are no pull requests to `main`.

## Licence

Source-available, not open source. You may read these, run them on Intempt, and
contribute. You may not redistribute them or use them to build a competing
product. See [LICENSE](./LICENSE).

Contributing grants Intempt a licence to publish your contribution. Partner
revenue share, where it applies, is a separate written agreement.
