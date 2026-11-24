---
frontmatter_id: video-reel
slash_command: /video-reel
description: Builds a 5 or 10 second reel of your brand presenter (your brand character) speaking your script for your brand, with its voice and captions.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Creates a short video reel of your brand character presenting your script for your brand, with its voice and captions.
  parameters:
  - name: duration
    type: enum
    label: Reel duration
    default: 5s
    required: false
    options:
    - 5s
    - 10s
  - name: script
    type: text
    label: Script (what the presenter says)
    required: true
  requirements: []
  steps:
  - id: s1
    builds: video
    uses:
    - duration
    - script
    instruction: Generate a short video reel of about {duration} with the brand's presenter character saying {script}.
---

# Short video reel

Slash command: /video-reel

## Step 1: Generate the reel

Generate a short video reel of the brand character (never an uploaded photo of a real person) presenting your script.
Inputs:
- script: what the presenter says
- duration: 5s or 10s
The presenter speaks for the brand (we, our), never as a customer; a customer quote is used only word for word from a real review, with the reviewer's name.
Pipeline: brand character + catalog voice → avatar video, captions
