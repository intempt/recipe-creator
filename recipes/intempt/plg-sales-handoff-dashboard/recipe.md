---
frontmatter_id: plg-sales-handoff-dashboard
slash_command: /plg-sales-handoff-dashboard
description: Shows paywall conversion and the free-to-paid funnel so teams can see where free users convert to paid.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
  - media-entertainment
portable:
  summary: Gives sales a morning leaderboard of free users showing strong intent, plus paywall-conversion and free-to-paid
    funnel views showing which features drive upgrades.
  parameters:
  - name: dateRange
    type: enum
    label: Default date range
    default: last_30_days
    required: false
    options:
    - last_7_days
    - last_30_days
    - last_90_days
  - name: exclusionPeriod
    type: enum
    label: Exclude recent period
    default: today
    required: false
    options:
    - today
    - yesterday
    - none
  - name: pqaMinPqls
    type: number
    label: Minimum PQLs for a qualified account (PQA)
    default: 3
    required: false
  - name: trailingWindow
    type: duration
    label: Trailing window for PQL to paid conversion
    default: 7 d
    required: false
  - name: boardVisibility
    type: enum
    label: Dashboard visibility
    default: project
    required: false
    options:
    - project
    - private
  requirements:
  - slot: pql_leaderboard_source
    kind: segment
    meaning: Free users scored as product-qualified leads (PQLs) based on their in-product activity
  - slot: feature_paywall_conversion_source
    kind: event
    meaning: A user viewed the pricing page or was shown a paywall while on a free plan
    properties:
    - name: feature
      type: text
      meaning: Feature that the user was using when the paywall was shown
      optional: false
    - name: page_path
      type: text
      meaning: Page path viewed, filtered to /pricing
      optional: false
  - slot: free_to_paid_funnel_source
    kind: event
    meaning: A user started a subscription after being on a free or trial plan
    properties:
    - name: subscription
      type: text
      meaning: Subscription status of the user, null or trial for free users
      optional: true
  - slot: activated_and_paying_source
    kind: segment
    meaning: Users who completed an activation journey goal and also started a paid subscription
  - slot: account_engagement_source
    kind: attribute
    meaning: The account a user belongs to, used to roll up engagement score for free accounts
  - slot: session_start_event
    kind: event
    meaning: A customer started a session in the product
  - slot: click_event
    kind: event
    meaning: A customer clicked on a tracked element in the product
  - slot: journey_goal_event
    kind: event
    meaning: A customer completed a journey goal
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a paid subscription
  - slot: utm_source_attribute
    kind: attribute
    meaning: The UTM source that brought the user to the product, used as a board breakdown
  steps:
  - id: s1
    builds: dashboard
    uses:
    - pql_leaderboard_source
    - feature_paywall_conversion_source
    - free_to_paid_funnel_source
    - activated_and_paying_source
    - account_engagement_source
    - session_start_event
    - click_event
    - journey_goal_event
    - subscription_started_event
    - utm_source_attribute
    - dateRange
    - exclusionPeriod
    - pqaMinPqls
    - trailingWindow
    - boardVisibility
    instruction: 'Create a 12-column dashboard titled "PLG Sales Handoff" with visibility {boardVisibility}. Answer the question:
      which free users are showing strong intent, and which features are driving them toward paid? Set the default date range
      to {dateRange} and exclude the {exclusionPeriod} period from results, because partial data for that period is unreliable.
      Add a board filter so only users whose subscription is null or trial are included, to scope the board to free and trial
      users. Add a board breakdown by {utm_source_attribute}, applied to cards that support ICP filtering. Lay out four rows.


      Row 1 (height 200 px): four metric cards, each 3 units wide. Card 1 is an insights metric on {pql_leaderboard_source}
      titled "Active PQLs". Card 2 is an insights metric on {pql_leaderboard_source} titled "Active PQAs (≥{pqaMinPqls} PQLs/account)",
      rolling up PQLs at the account level. Card 3 is an insights metric on {pql_leaderboard_source} titled "Trailing-{trailingWindow}
      PQL to Paid Conversion". Card 4 is a funnel metric on {free_to_paid_funnel_source} titled "Trial to Paid Rate".


      Row 2 (height 480 px): one full-width card (12 units). Insights on {pql_leaderboard_source} shown as a sortable table.
      This is the PQL leaderboard that sales reps review every morning.


      Row 3 (height 440 px): two 6-unit cards. Card 1 is an insights chart on {feature_paywall_conversion_source} using a
      scatter visualization, forming a four-quadrant view that shows which features to gate and which to give away. Card 2
      is a funnel chart on {free_to_paid_funnel_source} using funnel steps.


      Row 4 (height 400 px): two 6-unit cards. Card 1 is a funnel chart on {activated_and_paying_source} using funnel steps,
      which reveals the gap between vanity activation and real activation. Card 2 is an insights chart on {account_engagement_source}
      using a line visualization, showing account-level engagement for free accounts.


      Use only the canonical events {session_start_event}, {click_event}, {journey_goal_event}, and {subscription_started_event},
      with the /pricing page filter on paywall views. Roll up PQL and PQA scoring at the account level via the account the
      user belongs to.'
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
- boardBreakdowns: UTM source: pushed down to ICP-filter applicable cards
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
- All source recipes use canonical events: Session start, Click on, Completed a journey goal, View page (filtered to /pricing), Subscription started.
- PQL/PQA scoring uses Users.the account the user belongs to for account-level rollup.
