---
frontmatter_id: campaign-performance-leaderboard
slash_command: /campaign-performance-leaderboard
description: This recipe builds a ranked scorecard of your email campaigns by revenue and then reviews it every week, so email marketers can see which sends earn money and which need fixing. It turns weak spots into tasks and shares the winners with the team.
author:
  name: Intempt Technologies
  first_name: Intempt
  last_name: Technologies
  org_name: intempt
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
---

# Campaign performance leaderboard

## Step 1: Rank campaigns by revenue

Create an Insights report called "Campaign Performance Leaderboard".
Series A: Event "Email sent", aggregation: Count grouped by campaign_id, label: "Sends"
Series B: Event "Email opened", aggregation: Count Unique users grouped by campaign_id, label: "Opens"
Series C: Event "Email clicked", aggregation: Count Unique users grouped by campaign_id, label: "Clicks"
Series D: Event "Placed order" where the user previously emitted Email clicked or Email opened with that campaign_id within the attribution window, aggregation: Count Unique users grouped by campaign_id, label: "Conversions"
Series E: Sum of Placed order.total_price for those attributed orders, grouped by campaign_id, unit: $, label: "Attributed Revenue"
Series F: Computed: Series B divided by Series A, times 100, unit: percent, label: "Open Rate"
Series G: Computed: Series C divided by Series A, times 100, unit: percent, label: "Click Rate"
Series H: Computed: Series C divided by Series B, times 100, unit: percent, label: "Click-to-Open Rate"
Series I: Computed: Series D divided by Series A, times 100, unit: percent, label: "Conversion Rate"
Series J: Computed: Series E divided by Series A, unit: $, label: "Revenue per Send"
Attribution window: 7 days
Time range: Last 90 days of campaigns
Breakdown: By campaign_id, each row one campaign
Sort: By Series E (Attributed Revenue) descending by default
Chart type: Sortable table of the top 30 campaigns, with a secondary scatter plot where the X axis is Click Rate, the Y axis is Conversion Rate, and bubble size is Revenue per Send.
Sort modes available: by Attributed Revenue descending, by Revenue per Send descending, by Open Rate descending, by Click-to-Open Rate descending, by Conversion Rate descending.
Annotations:
- Flag campaigns with an open rate above 40 percent but a click-to-open rate below 10 percent, where the subject line worked but the content disappointed.
- Flag campaigns with a click-to-open rate above 20 percent but a conversion rate below 0.5 percent, where the landing page or offer does not match the email.
- Highlight the top 3 campaigns by Revenue per Send, as the templates worth repeating.
- Flag campaigns whose open rate or click-to-open rate is declining against that audience's trailing 4-campaign average, as a sign of subscriber fatigue or list quality erosion.
- Surface cumulative email-attributed revenue against total revenue for the period, for context on whether the email channel is over- or under-invested.
Taxonomy notes:
- Email sent has campaign_id, email, sent_at, subject: campaign_id is the canonical campaign identifier.
- Email opened and Email clicked do not carry campaign_id directly; attribution requires joining via email or masterID against the matching Email sent.
- Attributing Placed order to a campaign requires the sequence: Email clicked with the matching campaign_id, then Placed order within the attribution window. Where the email integration injects UTM campaign into links, Placed order.UTM campaign joined to the email's campaign_id is an alternative.
- This report depends on the workspace's email integration populating campaign_id reliably on Email sent. If campaign_id is sparse, the report degrades to aggregate email performance without the per-campaign breakdown.
- For SMS, substitute messaged_sms, which carries template_id and journey_id, in place of the email events above.

## Step 2: Flag underperforming campaigns before the next send

Create a workflow called "Campaign Leaderboard Weekly Review" that runs weekly, reading "Rank campaigns by revenue" for campaigns sent in the last 7 days. For any campaign with an open rate above 40 percent and a click-to-open rate below 10 percent, create a task for the email marketing owner, titled with the campaign's name and the words "Subject line worked, content didn't". For any campaign with a click-to-open rate above 20 percent and a conversion rate below 0.5 percent, create a separate task, titled with the campaign's name and the words "Landing page mismatch". Post the top 3 campaigns by Revenue per Send to the marketing Slack channel every week regardless of outcome. Use the result of "Rank campaigns by revenue".
