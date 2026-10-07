---
author:
  name: Beso
  last_name: Gugushvili
  org_name: intempt-internal-use-only
---
# Pricing Page Follow-Up

## Step 1: Create Pricing Page Visitors Segment

Create a segment called "Visited Pricing Page" for users. Base it on the "page_viewed" event — pick it from the existing event list, do not assume it's there, since it depends on an integration or API being connected. Add one condition group: triggered page_viewed within the last 3 days, where the page_url property contains "pricing".

## Step 2: Generate Follow-Up Banner Image

Generate a friendly, helpful banner image for a follow-up email — clean, modern style, a simple chat bubble or question-mark icon, no sales language, in our brand colors.

## Step 3: Generate Pricing Follow-Up Email

Write a short, helpful email for the "Visited Pricing Page" segment created in Step 1, using the banner image generated in Step 2. Ask if they have questions about pricing, offer a 15-minute call to walk through plans, and close with one clear button to book time. No discount, no pressure — just an offer to help.
