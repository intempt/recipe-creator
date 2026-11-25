---
frontmatter_id: return-rate-by-category
slash_command: /return-rate-by-category
description: Emails a weekly digest of which product categories get returned most and which have worsened against the prior
  period, with flagged jumps and top-5 lists.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails a weekly digest of return rates by product category, the top categories by return volume and by rate, and
    categories whose rate jumped.
  parameters:
  - name: time_window
    type: duration
    label: Window analyzed
    default: 90 d
    required: false
  - name: comparison_window
    type: duration
    label: Earlier window it is compared with
    default: 90 d
    required: false
  - name: jump_threshold_pp
    type: number
    label: Rise in return rate that gets flagged (percentage points)
    default: 5
    required: false
  - name: top_n
    type: number
    label: Categories in each top list
    default: 5
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: order_fulfilled_event
    kind: event
    meaning: A customer's order was fulfilled
    properties:
    - name: order_id
      type: string
      meaning: Identifier of the fulfilled order
      optional: false
  - slot: return_requested_event
    kind: event
    meaning: A customer requested a return of an order
    properties:
    - name: order_id
      type: string
      meaning: Order the return belongs to
      optional: false
    - name: items
      type: text
      meaning: Items included in the return
      optional: false
  - slot: products_catalog
    kind: product_feed
    meaning: Product catalog containing each product's category
    properties:
    - name: category
      type: string
      meaning: Product category
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - order_fulfilled_event
    - return_requested_event
    - products_catalog
    - time_window
    - comparison_window
    - jump_threshold_pp
    - top_n
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes {order_fulfilled_event}
      and {return_requested_event} in the last {time_window}, resolving each return''s {return_requested_event.items} to a
      {products_catalog.category} (or else through its order by {return_requested_event.order_id}), and writes these figures
      per category: returns, fulfilled orders and the return rate (returns divided by fulfilled orders), next to the rate
      for the {comparison_window} before; the top {top_n} categories by return count; the top {top_n} categories by return
      rate. When a category''s return rate rose by more than {jump_threshold_pp} percentage points, the email''s first line
      names it. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else
      is sent.'
---

# Return rate by category

Slash command: /return-rate-by-category

## Step 1: Email the weekly returns digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes order fulfilled event and return requested event in the last 90 d, resolving each return's items to a category (or else through its order by order id), and writes these figures per category: returns, fulfilled orders and the return rate (returns divided by fulfilled orders), next to the rate for the 90 d before; the top 5 categories by return count; the top 5 categories by return rate. When a category's return rate rose by more than 5 percentage points, the email's first line names it. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
