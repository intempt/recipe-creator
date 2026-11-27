---
frontmatter_id: cart-recovery
slash_command: /cart-recovery
description: Emails shoppers who left items behind, three times over three days, and emails a weekly digest of the revenue
  that comes back, with a warning when recovery drops.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails shoppers who left items in their cart three times over three days, and emails a weekly recovered-revenue
    digest that warns when recovery drops.
  parameters:
  - name: touch1_delay
    type: duration
    label: Delay before first email
    default: 1 h
    required: false
  - name: touch2_delay
    type: duration
    label: Delay before second email
    default: 24 h
    required: false
  - name: touch3_delay
    type: duration
    label: Delay before third email
    default: 72 h
    required: false
  - name: alert_threshold
    type: number
    label: Recovery rate warning threshold (percent)
    default: 15
    required: false
  - name: final_discount_percent
    type: number
    label: Discount offered in the final email (percent)
    default: 10
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: abandoned_cart_event
    kind: event
    meaning: A customer abandoned a cart without placing an order
    properties:
    - name: cart_id
      type: string
      meaning: Id of the cart
      optional: false
  - slot: order_event
    kind: event
    meaning: A customer completed an order
    properties:
    - name: cart_id
      type: string
      meaning: Id of the cart the order came from
      optional: false
    - name: revenue
      type: number
      meaning: Total value of the order
      optional: false
  - slot: brand_voice
    kind: brand
    meaning: Brand voice and tone guidelines for written emails
  steps:
  - id: s1
    builds: email
    uses:
    - brand_voice
    instruction: Write a gentle cart reminder email in the voice from {brand_voice} for shoppers who left items in their cart
      an hour ago. It shows the items left in the cart and has one button back to the cart (the cart item's own link when
      there is no cart page). No discount.
  - id: s2
    builds: email
    uses:
    - brand_voice
    - order_event
    instruction: Write a second cart email in the voice from {brand_voice} for shoppers who left items in their cart a day
      ago. It shows the items, adds a short line of customer praise taken from the brand's reviews or approved claims (else
      a line on how often the item is ordered, from {order_event} data) and a note that popular items sell out, with one button
      back to the cart (the cart item's own link when there is no cart page). A praise or sell-out line with no source is
      left out and named in the run's notes. Its subject is its own, not the subject of "Write the reminder". No discount.
  - id: s3
    builds: email
    uses:
    - brand_voice
    - final_discount_percent
    instruction: Write a final cart email in the voice from {brand_voice} for shoppers who left items in their cart three
      days ago. It says this is the last reminder, shows the items, and offers {final_discount_percent}% off under a subject
      of its own, not an earlier email's, with one button back to the cart (the cart item's own link when there is no cart
      page).
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - abandoned_cart_event
    - order_event
    - touch1_delay
    - touch2_delay
    - touch3_delay
    dependsOn:
    - s1
    - s2
    - s3
    instruction: Build an automation triggered when a user does {abandoned_cart_event}. It sends the email from "Write the
      reminder" after {touch1_delay}, the email from "Write the social proof email" at {touch2_delay} after the abandonment
      and the email from "Write the final reminder" at {touch3_delay}. It stops as soon as the user does {order_event} with
      the same {order_event.cart_id}. A user already in it does not start it again.
  - id: s5
    builds: automation
    uses:
    - s4
    - abandoned_cart_event
    - order_event
    - alert_threshold
    - digest_recipients
    dependsOn:
    - s4
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the last 7 days
      and writes these figures: carts abandoned by {abandoned_cart_event}; the recovery rate, the share later matched by {order_event}
      with the same {order_event.cart_id}; the revenue recovered, the sum of {order_event.revenue} (the order total) on those
      orders; the median time to recover; recovery by which email from "Send three emails over three days" came last. When
      the recovery rate is below {alert_threshold}%, the email''s first line says so. Then it emails these figures as plain-text
      lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Abandoned cart recovery

Slash command: /cart-recovery

## Step 1: Write the reminder

Write a gentle cart reminder email in the voice from brand voice for shoppers who left items in their cart an hour ago. It shows the items left in the cart and has one button back to the cart (the cart item's own link when there is no cart page). No discount.

## Step 2: Write the social proof email

Write a second cart email in the voice from brand voice for shoppers who left items in their cart a day ago. It shows the items, adds a short line of customer praise taken from the brand's reviews or approved claims (else a line on how often the item is ordered, from order event data) and a note that popular items sell out, with one button back to the cart (the cart item's own link when there is no cart page). A praise or sell-out line with no source is left out and named in the run's notes. Its subject is its own, not the subject of "Write the reminder". No discount.

## Step 3: Write the final reminder

Write a final cart email in the voice from brand voice for shoppers who left items in their cart three days ago. It says this is the last reminder, shows the items, and offers 10% off under a subject of its own, not an earlier email's, with one button back to the cart (the cart item's own link when there is no cart page).

## Step 4: Send three emails over three days

Build an automation triggered when a user does abandoned cart event. It sends the email from "Write the reminder" after 1 h, the email from "Write the social proof email" at 24 h after the abandonment and the email from "Write the final reminder" at 72 h. It stops as soon as the user does order event with the same cart id. A user already in it does not start it again.

## Step 5: Email the weekly recovery digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the last 7 days and writes these figures: carts abandoned by abandoned cart event; the recovery rate, the share later matched by order event with the same cart id; the revenue recovered, the sum of revenue (the order total) on those orders; the median time to recover; recovery by which email from "Send three emails over three days" came last. When the recovery rate is below 15%, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
