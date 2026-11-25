---
frontmatter_id: returning-vs-new-visitor-personalization
slash_command: /returning-vs-new-visitor-personalization
description: Builds the abandoned-cart segment and shows first-time visitors a value-proposition hero, returning visitors
  with an abandoned cart a cart-resumption hero, and other returning visitors a continue-browsing hero.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows first-time visitors a value-proposition hero, returning visitors with an abandoned cart a cart-resumption
    hero, and other returning visitors a continue-browsing hero.
  parameters:
  - name: cart_window
    type: duration
    label: Abandoned cart lookback
    default: 7 d
    required: false
  - name: display_frequency
    type: enum
    label: Display frequency
    default: once_per_session
    required: false
    options:
    - once_per_session
    - always
  - name: target_pages
    type: string
    label: Pages where the hero changes
    default: / and /category/*
    required: false
  requirements:
  - slot: cart_created_event
    kind: event
    meaning: A customer created a cart
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
  - slot: session_start_event
    kind: event
    meaning: A visitor started a website session
  steps:
  - id: s1
    builds: segment
    uses:
    - cart_created_event
    - placed_order_event
    - cart_window
    instruction: Build a new segment of users named "Returning Visitors with Abandoned Cart". A user is in it when they did
      {cart_created_event} at least once in the last {cart_window} and did not do {placed_order_event} after their most recent
      {cart_created_event}.
  - id: s2
    builds: personalization
    uses:
    - s1
    - session_start_event
    - display_frequency
    - target_pages
    dependsOn:
    - s1
    instruction: 'Create a client-side personalization named "Returning vs New Visitor" that replaces the hero on {target_pages},
      all devices, shown {display_frequency}, running continuously. Check audiences in this order. Variant "Resume your cart",
      for users in the segment from "Find returning visitors with an abandoned cart": heading "Welcome back: your cart''s
      still here", a preview of the items in their cart and a "Resume checkout" button with id hero-cta-resume. Variant "Continue
      browsing", for users who did {session_start_event} before the current session and are not in that segment: heading "Welcome
      back", the line "Pick up where you left off" and a "Recently viewed" row of the last four products they viewed. Variant
      "First visit", for users with no {session_start_event} before the current session: a value-proposition heading, a line
      on free shipping and returns, and a "Shop bestsellers" button with id hero-cta-explore. Control: the current hero for
      everyone else. Track hero clicks and orders placed in the same session per variant.'
---

# New versus returning visitor hero

Slash command: /returning-vs-new-visitor-personalization

## Step 1: Find returning visitors with an abandoned cart

Build a new segment of users named "Returning Visitors with Abandoned Cart". A user is in it when they did cart created event at least once in the last 7 d and did not do placed order event after their most recent cart created event.

## Step 2: Set up the visitor-history heroes

Create a client-side personalization named "Returning vs New Visitor" that replaces the hero on / and /category/*, all devices, shown once_per_session, running continuously. Check audiences in this order. Variant "Resume your cart", for users in the segment from "Find returning visitors with an abandoned cart": heading "Welcome back: your cart's still here", a preview of the items in their cart and a "Resume checkout" button with id hero-cta-resume. Variant "Continue browsing", for users who did session start event before the current session and are not in that segment: heading "Welcome back", the line "Pick up where you left off" and a "Recently viewed" row of the last four products they viewed. Variant "First visit", for users with no session start event before the current session: a value-proposition heading, a line on free shipping and returns, and a "Shop bestsellers" button with id hero-cta-explore. Control: the current hero for everyone else. Track hero clicks and orders placed in the same session per variant.
