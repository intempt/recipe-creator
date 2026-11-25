---
frontmatter_id: lifecycle-stage-homepage-personalization
slash_command: /lifecycle-stage-homepage-personalization
description: Loyal shoppers get a welcome back, lapsed ones get a win-back offer, and new shoppers get an introduction in
  the homepage hero, based on the lifecycle stage already on their profile.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: 'Shows each shopper a homepage hero matched to their lifecycle stage: a welcome back for loyal shoppers, a win-back
    offer for lapsed ones, and an introduction for new ones.'
  parameters:
  - name: homepage_path
    type: string
    label: Homepage URL path
    default: /
    required: false
  - name: winback_discount_percent
    type: number
    label: Win-back discount (%)
    default: 15
    required: false
  - name: display_frequency
    type: enum
    label: Display frequency
    default: once_per_session
    required: false
    options:
    - once_per_session
    - always
  requirements:
  - slot: lifecycle_stage_attribute
    kind: attribute
    meaning: The user's lifecycle stage with values At risk, Needs attention, New customers, Promising, Regulars, Champions
  - slot: first_name_attribute
    kind: attribute
    meaning: The user's first name, used to greet them on the homepage
    optional: true
  steps:
  - id: s1
    builds: personalization
    uses:
    - lifecycle_stage_attribute
    - first_name_attribute
    - homepage_path
    - winback_discount_percent
    - display_frequency
    instruction: 'Create a client-side personalization named "Lifecycle Stage Homepage" that replaces the homepage hero on
      {homepage_path} for users on all devices, runs continuously and shows {display_frequency}. Control: the current hero,
      for users whose {lifecycle_stage_attribute} is empty. Variant "Welcome back", for users whose {lifecycle_stage_attribute}
      is Champions or Regulars: heading "Welcome back" followed by their {first_name_attribute} when it is set, a "Shop new
      arrivals" button to /new-arrivals, and a "Picked for you" row of products like their past orders. Variant "We''ve missed
      you", for At risk or Needs attention: heading "We''ve missed you", the line "Here''s {winback_discount_percent}% off
      your next order", a "Claim {winback_discount_percent}% off" button, and a row of products they ordered before. Variant
      "First-time browse", for New customers or Promising: heading "Welcome", a "Shop bestsellers" button to /best-sellers
      and a "Popular this week" row of the most-ordered products. Track hero clicks, orders placed in the same session and
      average order value per variant.'
---

# Homepage by customer lifecycle stage

Slash command: /lifecycle-stage-homepage-personalization

## Step 1: Set up the three lifecycle heroes

Create a client-side personalization named "Lifecycle Stage Homepage" that replaces the homepage hero on / for users on all devices, runs continuously and shows once_per_session. Control: the current hero, for users whose lifecycle stage attribute is empty. Variant "Welcome back", for users whose lifecycle stage attribute is Champions or Regulars: heading "Welcome back" followed by their first name attribute when it is set, a "Shop new arrivals" button to /new-arrivals, and a "Picked for you" row of products like their past orders. Variant "We've missed you", for At risk or Needs attention: heading "We've missed you", the line "Here's 15% off your next order", a "Claim 15% off" button, and a row of products they ordered before. Variant "First-time browse", for New customers or Promising: heading "Welcome", a "Shop bestsellers" button to /best-sellers and a "Popular this week" row of the most-ordered products. Track hero clicks, orders placed in the same session and average order value per variant.
