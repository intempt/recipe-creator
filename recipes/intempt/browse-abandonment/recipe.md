---
frontmatter_id: browse-abandonment
slash_command: /browse-abandonment
description: Reminds people who looked at products but never added anything to the cart with two emails showing the items
  they viewed and similar ones, and emails a weekly browse-to-sale digest.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails shoppers who viewed products but never added to cart at 24 and 72 hours with the items they viewed and similar
    picks, plus a weekly browse-to-sale digest.
  parameters:
  - name: browse_window
    type: duration
    label: Browsing window
    default: 7 d
    required: false
  - name: first_reminder_delay
    type: duration
    label: Wait before the first reminder
    default: 24 h
    required: false
  - name: second_reminder_delay
    type: duration
    label: Wait before the second reminder
    default: 72 h
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: product_viewed
    kind: event
    meaning: A customer viewed a product page
    properties:
    - name: product
      type: string
      meaning: The product viewed
      optional: false
  - slot: cart_added
    kind: event
    meaning: A customer added a product to their cart
  - slot: purchase_completed
    kind: event
    meaning: A customer completed a purchase
  - slot: email_channel
    kind: destination
    meaning: An email channel to send reminder emails
    channel: email
  - slot: product_feed
    kind: product_feed
    meaning: A catalog of products with images, categories and links
  steps:
  - id: s1
    builds: segment
    uses:
    - product_viewed
    - cart_added
    - browse_window
    instruction: Build a new segment of users named "Browse Abandoners". A user is in it when they did {product_viewed} in
      the last {browse_window} and did not do {cart_added} in the last {browse_window}.
  - id: s2
    builds: email
    uses:
    - s1
    - product_viewed
    - product_feed
    dependsOn:
    - s1
    instruction: 'Write two browse reminder emails for users in the segment from "Find people who only browsed". Email 1:
      shows the last product they viewed ({product_viewed.product}) with its image, name and a button to its page, plus three
      products from {product_feed} in the same category. Email 2: a shorter nudge with the same viewed product and the three
      best sellers in its category from {product_feed}. Helpful tone, no discount. If the brand kit has no logo, use the brand
      name as a plain text header.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - cart_added
    - purchase_completed
    - email_channel
    - first_reminder_delay
    - second_reminder_delay
    dependsOn:
    - s1
    - s2
    instruction: Build an automation triggered when a user enters the segment from "Find people who only browsed". After {first_reminder_delay}
      it sends email 1 from "Write the browse reminder" through {email_channel}; at {second_reminder_delay} after entering
      it sends email 2. Before each send it checks whether the user did {cart_added} or {purchase_completed} since entering;
      if so it stops for that user. Each user enters at most once in 14 days.
  - id: s4
    builds: automation
    uses:
    - s1
    - s3
    - cart_added
    - purchase_completed
    - digest_recipients
    dependsOn:
    - s1
    - s3
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who entered
      the segment from "Find people who only browsed" in the last 7 days and in the 7 days before, and writes these figures
      for both windows: users entered; open rate and click rate of each email sent by "Send at 24 and 72 hours"; share who
      did {cart_added} within 7 days of entering; share who did {purchase_completed} within 7 days of entering. Then it emails
      these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Browse abandonment follow up

Slash command: /browse-abandonment

## Step 1: Find people who only browsed

Build a new segment of users named "Browse Abandoners". A user is in it when they did product viewed in the last 7 d and did not do cart added in the last 7 d.

## Step 2: Write the browse reminder

Write two browse reminder emails for users in the segment from "Find people who only browsed". Email 1: shows the last product they viewed (product) with its image, name and a button to its page, plus three products from product feed in the same category. Email 2: a shorter nudge with the same viewed product and the three best sellers in its category from product feed. Helpful tone, no discount. If the brand kit has no logo, use the brand name as a plain text header.

## Step 3: Send at 24 and 72 hours

Build an automation triggered when a user enters the segment from "Find people who only browsed". After 24 h it sends email 1 from "Write the browse reminder" through email channel; at 72 h after entering it sends email 2. Before each send it checks whether the user did cart added or purchase completed since entering; if so it stops for that user. Each user enters at most once in 14 days.

## Step 4: Follow browse through to sale

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who entered the segment from "Find people who only browsed" in the last 7 days and in the 7 days before, and writes these figures for both windows: users entered; open rate and click rate of each email sent by "Send at 24 and 72 hours"; share who did cart added within 7 days of entering; share who did purchase completed within 7 days of entering. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
