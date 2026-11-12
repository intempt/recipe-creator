---
frontmatter_id: lifecycle-stage-homepage-personalization
slash_command: /lifecycle-stage-homepage-personalization
description: This recipe personalizes an ecommerce homepage based on where each shopper sits in the customer lifecycle, from new and promising to loyal, or at risk of leaving. It is for ecommerce marketers who want to show each group a more relevant message and offer.
author:
  name: Intempt Technologies
  first_name: Intempt
  last_name: Technologies
  org_name: intempt
---

# Homepage by customer lifecycle stage

## Step 1: Set up the three lifecycle heroes

Create a website personalization titled "Lifecycle Stage Homepage Personalization" on the homepage, using the canonical Users.Lifecycle score values: At risk, Needs attention, New customers, Promising, Regulars, Champions.
Variants:
- Control: the standard homepage, shown when Users.Lifecycle score is empty or the session is too new for the score to be computed yet.
- Variant B, "Welcome back": shown when Users.Lifecycle score is Champions or Regulars. The hero greets the returning shopper by name when available, links to their past orders, and surfaces new arrivals.
- Variant C, "We've missed you": shown when Users.Lifecycle score is At risk or Needs attention. The hero offers 15 percent off the next order and surfaces the shopper's previously favorited or most-purchased items.
- Variant D, "First-time browse": shown when Users.Lifecycle score is New customers or Promising. The hero introduces the brand and surfaces items under 50 dollars as an easy first purchase, along with the current week's best sellers.
Targeting: homepage only; any device; the variant shown is fixed for the session once it is determined.
Metrics: the within-session order rate per audience, the average order value per audience, and the primary call-to-action click rate per audience.
Schedule: continuous.

## Step 2: Measure conversion by lifecycle stage

Compose a dashboard titled "Lifecycle Personalization Performance" showing the within-session order rate, average order value, and call-to-action click rate for each of the three variants, compared week over week against the Control. Flag any variant whose order rate falls below the Control's for 2 consecutive weeks. Use the result of "Set up the three lifecycle heroes".

## Step 3: Act on an underperforming win-back offer

Build a workflow that runs monthly, reading the flag from "Measure conversion by lifecycle stage" for Variant C, the At risk and Needs attention audience. When that variant has underperformed the Control for 2 consecutive months, create a task for the lifecycle marketing owner recommending the win-back discount be increased or the offer be redesigned, with the conversion comparison attached. Use the result of "Set up the three lifecycle heroes", "Measure conversion by lifecycle stage".
