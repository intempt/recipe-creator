---
frontmatter_id: product-launch-site
slash_command: /product-launch-site
description: Generates a product launch page artifact with hero, feature, call to action, and footer content in your brand styling.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Creates a multi-page product launch microsite with a hero section, feature pages, a call to action and footer,
    styled with your brand, ready to deploy in one click.
  parameters: []
  requirements:
  - slot: brand_tokens
    kind: brand
    meaning: The project's brand styling tokens such as colors, fonts and logo
  steps:
  - id: s1
    builds: page
    uses:
    - brand_tokens
    instruction: 'Create a product launch microsite. Build a multi-page site with: hero section, feature/benefit pages, call-to-action,
      and footer. Apply {brand_tokens} brand tokens. Make it deploy-ready in one click. Output: multi-page microsite.'
---

# Product launch microsite

Slash command: /product-launch-site

## Step 1: Build the launch microsite

Create a product launch microsite.
Build a multi-page site with: hero section, feature/benefit pages, call-to-action, and footer. Apply project brand tokens. Deploy-ready in one click.
Output: multi-page microsite
