---
description: Shows paywall conversion and the free-to-paid funnel so teams can see where free users convert to paid.
author:
  first_name: Sid
  last_name: Chaudhary
  job_title: Founder & CEO
  avatar: https://cdn.intempt.com/assets/author-profile-pics/sid.png
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - media
---

# Free users worth calling

Slash command: /plg-sales-handoff-dashboard

## Step 1: Build the PQL leaderboard

Create a Dash board (12-column composition canvas) titled "PLG Sales Handoff".
Persona: PLG Sales Lead, Hybrid GTM operator, or PLG-aware AE. Question answered: "Which free users are showing strong intent, and which features are driving them toward paid?"
This dashboard pairs the canonical PLG sales handoff signals (PQL leaderboard, paywall conversion) with the funnel and account-level views that surface the highest-intent users for sales outreach.
Board-level configuration:
- defaultDateRange: last_30_days
- exclusionPeriod: today (PQL signals are fast-moving; today's data is partial)
- visibility: project
- boardFilters: subscription is null OR subscription is trial (default-pinned to scope to free/trial users only)
- boardBreakdowns: utm_source: pushed down to ICP-filter applicable cards
Layout: 4 rows.
Row 1: Handoff KPIs (heightPx: 200, four metric cards at widthUnits: 3):
- Card 1: Insights metric to source recipe: pql-leaderboard, vizType: metric, titleOverride: "Active PQLs"
- Card 2: Insights metric to source recipe: pql-leaderboard, vizType: metric, titleOverride: "Active PQAs (≥3 PQLs/account)"
- Card 3: Insights metric to source recipe: pql-leaderboard, vizType: metric, titleOverride: "Trailing-7d PQL to Paid Conversion"
- Card 4: Funnel metric to source recipe: free-paid-conversion-funnel, vizType: metric, titleOverride: "Trial to Paid Rate"
Row 2: The leaderboard (heightPx: 480, full-width single card at widthUnits: 12):
- Card 1: Insights to source recipe: pql-leaderboard, displayMode: table (the sortable PQL leaderboard: the canonical sales-handoff artifact)
Row 3: Paywall and feature intelligence (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: feature-paywall-conversion, displayMode: chart, vizType: scatter (the four-quadrant scatter)
- Card 2: Funnel to source recipe: free-paid-conversion-funnel, displayMode: chart, vizType: funnel_steps
Row 4: Activated-and-paying view (heightPx: 400, two cards at widthUnits: 6):
- Card 1: Funnel to source recipe: compound-funnel-activated-and-paying, displayMode: chart, vizType: funnel_steps
- Card 2: Insights to source recipe: account-engagement-score-trend, displayMode: chart, vizType: line (account-level engagement on free accounts)
Annotations:
- Row 1's KPIs are filtered views of the pql-leaderboard recipe (PQL count, PQA count via account-roll-up, trailing conversion).
- Row 2 (the PQL leaderboard, full-width) is what sales reps look at every morning.
- Row 3 Card 1 (paywall conversion scatter) tells the product team which features to gate vs. give away.
- Row 4 Card 1 (Activated AND Paying) reveals the gap between vanity activation and real activation.
Taxonomy notes:
- All source recipes use canonical events: session_start, click_on, goal_completed_in_journey, page_viewed (filtered to /pricing), subscription_created.
- PQL/PQA scoring uses Users.primary_account_id for account-level rollup.
