---
frontmatter_id: mrr-movement-decomposition
slash_command: /mrr-movement-decomposition
description: This recipe builds a monthly report that splits recurring revenue change into new, expansion, contraction, churned and reactivation amounts, then sends the results to the people who need to act. It suits finance, revenue and customer success teams at subscription businesses.
author:
  name: Intempt Technologies
  first_name: Intempt
  last_name: Technologies
  org_name: intempt
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
---

# MRR movement waterfall

## Step 1: Break MRR into its five parts

Create an Insights report called "MRR Movement Decomposition".
Compute the five movement categories per month:
New MRR: Sum of Subscription started.amount in the period for users who had no active subscription previously, unit: $
Expansion MRR: From Subscription updated events: for each event, compute (new amount minus prior subscription amount on the same subscription_id). Sum the positive deltas where changed_fields indicates plan upgrade or seat/quantity increase, unit: $
Contraction MRR: Same Subscription updated computation; sum the negative deltas (shown as negative values in the waterfall), unit: $
Churned MRR: Sum of the prior subscription amount for each Subscription canceled event in the period (negative in the waterfall), unit: $
Reactivation MRR: Sum of subscription_resumed.amount where the user previously had a Subscription canceled in the prior 90 days, unit: $
Net New MRR: New plus Expansion plus Contraction (negative) plus Churned (negative) plus Reactivation
Net Revenue Retention: (Starting MRR + Expansion + Reactivation - Contraction - Churn) / Starting MRR times 100, unit: percent
Time granularity: Monthly
Time range: Last 12 months
Compare: Year-over-year
Chart type: Waterfall chart per month (New, Expansion, Reactivation as positive stacks; Contraction, Churn as negative stacks; Net New as the connecting line), with a secondary line showing trailing 12-month Net Revenue Retention
Annotations:
- Flag any month where Net New MRR went negative.
- Flag any month where Churned MRR exceeded New MRR.
- Flag any month where trailing 12-month Net Revenue Retention is below 100 percent.
Taxonomy notes:
- The canonical Intempt taxonomy does not have separate subscription_upgraded, subscription_downgraded, or subscription_reactivated events. The available subscription state-change events are: Subscription started, Subscription updated, Subscription canceled, subscription_paused, subscription_resumed, subscription_expired, subscription_activated.
- Expansion and Contraction are computed from Subscription updated by comparing new versus prior subscription amount. The changed_fields property indicates what changed; plan_items carries the new state.
- Reactivation is computed as subscription_resumed (or subscription_activated) where the same customer_id had a recent Subscription canceled.
- If Subscription updated is sparse in a workspace, the report degrades to New MRR plus Churned MRR only, without the expansion and contraction split.

## Step 2: Route the waterfall to the people who act on it

Create a workflow called "MRR Waterfall Monthly Routing" that runs on the same monthly schedule as "Break MRR into its five parts". When Churned MRR for the month exceeds New MRR, create a task assigned to the retention owner, titled with the calendar month and the words "Churned MRR exceeded New MRR", with the churned accounts' dollar total and a link to the report. When Contraction MRR exceeds Expansion MRR, create a separate task assigned to the account management owner, titled with the calendar month and the words "Contraction outpaced expansion". In both cases, also post the month's full five-part breakdown to the leadership Slack channel. When neither condition is met, post only the five-part breakdown to the leadership Slack channel, with no task created. Use the result of "Break MRR into its five parts".
