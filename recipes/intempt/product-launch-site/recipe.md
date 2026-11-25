---
frontmatter_id: product-launch-site
slash_command: /product-launch-site
description: Builds a product launch page with hero, feature, call to action and footer sections in your brand styling.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds a product launch page in your brand styling with a hero, three feature sections, a call to action and a
    footer.
  parameters:
  - name: product_name
    type: string
    label: Name of the product being launched
    required: true
  - name: product_pitch
    type: text
    label: What the product does and its three main features
    required: true
  - name: cta_url
    type: string
    label: Link the call to action button opens
    required: true
  requirements:
  - slot: brand_tokens
    kind: brand
    meaning: The project's brand styling such as colors, fonts and logo
  steps:
  - id: s1
    builds: page
    uses:
    - brand_tokens
    - product_name
    - product_pitch
    - cta_url
    instruction: 'Create a landing page that launches {product_name}, styled with {brand_tokens} colors, fonts and logo. Sections
      in order: a hero with a headline, a one-line sub-headline and a call to action button; three feature sections, one per
      feature, each with a short title, two sentences and an image; a closing call to action section; a footer with the brand
      name and a link to the main site. All copy comes from this description of the product: {product_pitch}. Every call to
      action button links to {cta_url}.'
---

# Product launch microsite

Slash command: /product-launch-site

## Step 1: Build the launch microsite

Create a landing page that launches the name of the product being launched, styled with brand tokens colors, fonts and logo. Sections in order: a hero with a headline, a one-line sub-headline and a call to action button; three feature sections, one per feature, each with a short title, two sentences and an image; a closing call to action section; a footer with the brand name and a link to the main site. All copy comes from this description of the product: the what the product does and its three main features. Every call to action button links to the link the call to action button opens.
