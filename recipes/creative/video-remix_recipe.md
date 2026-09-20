---
name: video-remix
description: |
  Use when a user mentions "video remix", "remix video", "video variations", "video references", or asks for branded video variants from reference clips. Four references in, your branded reel out.
arguments: []
intempt:
  id: video-remix
  version: 1.0.0
  slashCommand: /video-remix
  group: Creative
  title: 'Reference-anchored video remix'
  shortDescription: 'Pin up to four video references and get back branded reel variants anchored to them (four by default).'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, remix, reference]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: 'Pin clips and fan out'
      command: generate_video
      produces: video
      bindsAs: video
      description: 'You pin one to four references, which can be a clip, scene, avatar or product. Returns branded reel variants anchored to those clips.'
      prompt: |
        Generate branded video variations from reference pins.

        Inputs:
        - references: 1: 4 video references (clip, scene, avatar, product)
        - fanout: number of variations (default: 4)

        Pipeline: kling v3 i2v multi-ref
        Runner: video-remix (custom)

        Fan out branded reel variants anchored to the reference clips.
  outputs:
    - { name: video, type: video, cardinality: list, description: "Remixed video variations." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Reference-anchored video remix

Pin up to four video references and get back branded reel variants anchored to them (four by default).

## What it does

1. **Pin clips and fan out** (`generate_video`)

   You pin one to four references, which can be a clip, scene, avatar or product. Returns branded reel variants anchored to those clips.

## What you end up with

- **video** (video): Remixed video variations.
