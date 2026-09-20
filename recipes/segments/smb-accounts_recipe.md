---
name: smb-accounts
description: |
  Use when a user mentions "smb accounts (under 100 employees)", or asks for related help. Small businesses (under 100 employees): self-serve / low-touch routing.
arguments: []
intempt:
  id: smb-accounts
  version: 1.0.0
  slashCommand: /smb-accounts
  group: Segments
  title: 'Small business accounts'
  shortDescription: 'Companies under 100 employees, the list your self-serve nurture and in-product prompts should run against.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [b2b, saas]
    object: accounts
    complexity: standard
    executionMode: live
    tags: [accounts-segment]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
  procedure:
    - step: 1
      title: 'Build the SMB list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Accounts with fewer than 100 employees.'
      prompt: |
        Create a segment called "SMB Accounts".

        Object: Accounts

        Rules:
        - Attribute: employees < 100

        Description: Small businesses with under 100 employees. Foundation for self-serve / low-touch routing: these accounts go through automated nurture flows, in-product upgrade prompts, and minimal direct sales engagement. The PLG sweet spot.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Small business accounts

Companies under 100 employees, the list your self-serve nurture and in-product prompts should run against.

## What it does

1. **Build the SMB list** (`create_segment`)

   Accounts with fewer than 100 employees.

## What you end up with

- **segment** (segment): Segment created on /segments.
