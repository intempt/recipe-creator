---
frontmatter_id: vip-loyalty
slash_command: /vip-loyalty
description: Ranks your best customers into silver, gold and platinum tiers, thanks each tier by email, gives each tier something
  worth having on site, and tests which rewards actually keep them.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
  - travel-hospitality
portable:
  summary: Ranks best customers into silver, gold and platinum tiers, sends tier welcome and tier-up emails, shows tier perks
    on site and tests which reward keeps them buying.
  parameters:
  - name: silver_threshold
    type: number
    label: Orders for silver
    default: 2
    required: false
  - name: gold_threshold
    type: number
    label: Orders for gold
    default: 3
    required: false
  - name: platinum_threshold
    type: number
    label: Orders for platinum
    default: 4
    required: false
  - name: recency_window
    type: duration
    label: Window the orders are counted in
    default: 90 d
    required: false
  - name: tier_up_delay
    type: duration
    label: Wait before the tier-up email
    default: 30 d
    required: false
  requirements:
  - slot: purchase_event
    kind: event
    meaning: A customer completed an order
    properties:
    - name: order_value
      type: number
      meaning: Value of the order
      optional: false
  - slot: email_channel
    kind: destination
    meaning: An email channel to send VIP messages
    channel: email
  - slot: brand_voice
    kind: brand
    meaning: The brand's name and voice for customer messages
    optional: true
  steps:
  - id: s1
    builds: attribute
    uses:
    - purchase_event
    - silver_threshold
    - gold_threshold
    - platinum_threshold
    - recency_window
    instruction: Create a computed user attribute named "vip_tier". Count each user's {purchase_event} events in the last
      {recency_window}. The value is "platinum" when the count is {platinum_threshold} or more, "gold" when it is {gold_threshold}
      or more, "silver" when it is {silver_threshold} or more, and empty otherwise.
  - id: s2
    builds: email
    uses:
    - s1
    - brand_voice
    - silver_threshold
    - gold_threshold
    - platinum_threshold
    - recency_window
    dependsOn:
    - s1
    instruction: 'Write five VIP loyalty emails for users by their vip_tier attribute from "Rank customers by value", in the
      voice of {brand_voice}. Three welcome emails, one per tier: silver (free shipping on every order), gold (free shipping
      and early access to new products), platinum (free shipping, early access and exclusive products). Two tier-up emails:
      for silver users, how many more orders in {recency_window} reach gold ({gold_threshold} in total); for gold users, how
      many more reach platinum ({platinum_threshold} in total). Warm thank-you tone, one call to action to the store. If the
      brand kit has no logo, use the brand name as a plain text header.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - email_channel
    - tier_up_delay
    dependsOn:
    - s1
    - s2
    instruction: Build an automation triggered when a user's vip_tier attribute from "Rank customers by value" changes to
      silver, gold or platinum. It sends the matching tier welcome email from "Write tier welcome and tier-up emails" through
      {email_channel} at once. After {tier_up_delay}, if the user's vip_tier is silver or gold, it sends the matching tier-up
      email from the same step. Each user gets each email at most once.
  - id: s4
    builds: personalization
    uses:
    - s1
    dependsOn:
    - s1
    instruction: 'Create a website personalization for logged-in users by their vip_tier attribute from "Rank customers by
      value". Users with vip_tier silver see a banner "Free shipping on every order". Gold users see the banner plus an "Early
      access" badge on new products. Platinum users see both plus an "Exclusive products" collection link in the site header.
      Users with no vip_tier see the site unchanged. Pages: all store pages; devices: any; display frequency: always; schedule:
      continuous.'
  - id: s5
    builds: experiment
    uses:
    - s1
    - s3
    - purchase_event
    dependsOn:
    - s1
    - s3
    instruction: 'Create an experiment on the tier welcome emails sent by "Thank them, show the next tier" for users with
      a vip_tier from "Rank customers by value". Variant A leads with a 10% discount on the next order, variant B with early
      access to new products, variant C with status perks only (no discount). Split users evenly at random within each tier.
      Primary metric: share of users who did {purchase_event} within 60 days of the email. Secondary metric: share still holding
      their tier after 90 days. Run for 90 days.'
---

# VIP loyalty programme

Slash command: /vip-loyalty

## Step 1: Rank customers by value

Create a computed user attribute named "vip_tier". Count each user's purchase event events in the last 90 d. The value is "platinum" when the count is 4 or more, "gold" when it is 3 or more, "silver" when it is 2 or more, and empty otherwise.

## Step 2: Write tier welcome and tier-up emails

Write five VIP loyalty emails for users by their vip_tier attribute from "Rank customers by value", in the voice of brand voice. Three welcome emails, one per tier: silver (free shipping on every order), gold (free shipping and early access to new products), platinum (free shipping, early access and exclusive products). Two tier-up emails: for silver users, how many more orders in 90 d reach gold (3 in total); for gold users, how many more reach platinum (4 in total). Warm thank-you tone, one call to action to the store. If the brand kit has no logo, use the brand name as a plain text header.

## Step 3: Thank them, show the next tier

Build an automation triggered when a user's vip_tier attribute from "Rank customers by value" changes to silver, gold or platinum. It sends the matching tier welcome email from "Write tier welcome and tier-up emails" through email channel at once. After 30 d, if the user's vip_tier is silver or gold, it sends the matching tier-up email from the same step. Each user gets each email at most once.

## Step 4: Give each tier something

Create a website personalization for logged-in users by their vip_tier attribute from "Rank customers by value". Users with vip_tier silver see a banner "Free shipping on every order". Gold users see the banner plus an "Early access" badge on new products. Platinum users see both plus an "Exclusive products" collection link in the site header. Users with no vip_tier see the site unchanged. Pages: all store pages; devices: any; display frequency: always; schedule: continuous.

## Step 5: Test which reward works

Create an experiment on the tier welcome emails sent by "Thank them, show the next tier" for users with a vip_tier from "Rank customers by value". Variant A leads with a 10% discount on the next order, variant B with early access to new products, variant C with status perks only (no discount). Split users evenly at random within each tier. Primary metric: share of users who did purchase event within 60 days of the email. Secondary metric: share still holding their tier after 90 days. Run for 90 days.
