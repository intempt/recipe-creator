---
frontmatter_id: sales-activity-coaching-dashboard
slash_command: /sales-activity-coaching-dashboard
description: Shows sales rep activity volume for calls, emails and meetings alongside the revenue it produced, so managers can identify coaching needs and performance differences.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Gives sales managers one per-rep dashboard of call, email and meeting activity next to revenue, to spot coaching
    needs and performance gaps before weekly 1:1s.
  parameters:
  - name: dashboardTitle
    type: string
    label: Dashboard title
    default: Sales Activity & Coaching
    required: false
  - name: defaultDateRange
    type: duration
    label: Default date range
    default: 30 d
    required: false
  - name: boardVisibility
    type: enum
    label: Dashboard visibility
    default: project
    required: false
    options:
    - project
    - private
  - name: revenuePerCallsCaption
    type: string
    label: Leading-indicator metric name
    default: Team Revenue per 100 Calls
    required: false
  - name: efficiencyAlertRatio
    type: number
    label: Efficiency alert threshold (share of team average)
    default: 0.5
    required: false
  requirements:
  - slot: rep_activity_leaderboard
    kind: segment
    meaning: Per-rep activity volume (calls, outbound emails, meetings, tasks) and revenue from won deals, sourced from the
      rep activity leaderboard insight
  - slot: quota_attainment_by_rep
    kind: segment
    meaning: Per-rep quota attainment against the workspace quota target, sourced from the quota attainment insight
  - slot: win_loss_analysis
    kind: segment
    meaning: Won versus lost deals broken down by lead source, sourced from the win-loss analysis insight
  - slot: deal_velocity_by_stage
    kind: segment
    meaning: Average time deals spend in each pipeline stage, sourced from the deal velocity insight
  - slot: multi_threading_coverage_by_deal
    kind: segment
    meaning: Open deals grouped by number of contacts engaged (single-threaded vs multi-threaded), sourced from the multi-threading
      coverage insight
  - slot: call_completed
    kind: event
    meaning: A customer call was completed by a rep
    properties:
    - name: owner_id
      type: string
      meaning: Rep who owns the call
      optional: false
  - slot: email_sent_outbound
    kind: event
    meaning: A rep sent an outbound email to a customer
    properties:
    - name: owner_id
      type: string
      meaning: Rep who sent the email
      optional: false
    - name: direction
      type: string
      meaning: Email direction, outbound for this recipe
      optional: false
  - slot: meeting_scheduled
    kind: event
    meaning: A rep scheduled a meeting with a prospect or customer
    properties:
    - name: owner_id
      type: string
      meaning: Rep who scheduled the meeting
      optional: false
  - slot: deal_won
    kind: event
    meaning: A deal was marked won
    properties:
    - name: owner_id
      type: string
      meaning: Rep who owns the deal
      optional: false
  steps:
  - id: s1
    builds: dashboard
    uses:
    - dashboardTitle
    - defaultDateRange
    - boardVisibility
    - revenuePerCallsCaption
    - efficiencyAlertRatio
    - rep_activity_leaderboard
    - quota_attainment_by_rep
    - win_loss_analysis
    - deal_velocity_by_stage
    - multi_threading_coverage_by_deal
    - call_completed
    - email_sent_outbound
    - meeting_scheduled
    - deal_won
    instruction: 'Create a 12-column dashboard titled "{dashboardTitle}" for sales managers and frontline coaches, answering
      which reps need coaching and what differentiates top performers. Set the default date range to {defaultDateRange}, no
      exclusion period, visibility {boardVisibility}. Break down all cards by owner_id, with no board filters by default.
      Use 4 rows. Row 1 (height 200 px): four metric cards at 3 width units each: (a) rep_activity_leaderboard as a metric
      titled "Total Calls (Team, 30d)"; (b) rep_activity_leaderboard as a metric titled "Total Meetings Booked"; (c) rep_activity_leaderboard
      as a metric titled "{revenuePerCallsCaption}"; (d) quota_attainment_by_rep as a metric titled "% Reps at ≥100% Attainment".
      Row 2 (height 520 px): one full-width (12 units) table of rep_activity_leaderboard showing per-rep activity and revenue,
      sortable by Top Performers (revenue), Most Active (calls), Most Efficient (revenue per call), and Rising/Falling Stars
      (week-over-week change). Row 3 (height 440 px): two 6-unit bar charts: win_loss_analysis (won vs. lost by source, ICP
      fit signal) and deal_velocity_by_stage (stages that slow deals). Row 4 (height 440 px): two 6-unit cards: multi_threading_coverage_by_deal
      as a stacked bar chart (single-threaded deals), and quota_attainment_by_rep as a bar chart with team-average benchmark.
      Guidance: read before weekly 1:1s; sort the leaderboard by Rising/Falling Stars to spot trend changes and drill into
      reps for coaching topics. Treat revenue per 100 calls below {efficiencyAlertRatio} times the team average as a serious
      efficiency issue, to coach on qualification or talk tracks. Treat row 3 as team-level coaching topics, not 1:1 topics.
      Single-threaded deals should be addressed by advising reps to multi-thread before the proposal stage. Rep identity is
      owner_id across all events.'
---

# Rep activity and coaching

Slash command: /sales-activity-coaching-dashboard

## Step 1: Build the rep leaderboard

Create a Dash board (12-column composition canvas) titled "Sales Activity & Coaching".
Persona: Sales Manager or frontline-coach. Question answered: "Which reps need coaching? What patterns differentiate top performers from the rest?"
Distinct from Sales Pipeline (deal-focused, operational) and Sales Forecasting (period commitment). Sales Activity & Coaching is per-rep frontline-management: the dashboard a manager opens when planning weekly 1:1s.
Board-level configuration:
- defaultDateRange: last_30_days
- exclusionPeriod: none
- visibility: project
- boardFilters: none by default; managers typically filter to owner_id IN (their direct reports) at runtime
- boardBreakdowns: owner_id: pushed down throughout
Layout: 4 rows.
Row 1: Activity volume KPIs (heightPx: 200, four metric cards at widthUnits: 3):
- Card 1: Insights metric to source recipe: rep-activity-leaderboard, vizType: metric, titleOverride: "Total Calls (Team, 30d)"
- Card 2: Insights metric to source recipe: rep-activity-leaderboard, vizType: metric, titleOverride: "Total Meetings Booked"
- Card 3: Insights metric to source recipe: rep-activity-leaderboard, vizType: metric, titleOverride: "Team Revenue per 100 Calls"
- Card 4: Insights metric to source recipe: quota-attainment-by-rep, vizType: metric, titleOverride: "% Reps at ≥100% Attainment"
Row 2: The leaderboard (heightPx: 520, full-width single card at widthUnits: 12):
- Card 1: Insights to source recipe: rep-activity-leaderboard, displayMode: table (the sortable per-rep activity + revenue table: the centerpiece coaching artifact). Sort modes: Top Performers (revenue), Most Active (calls), Most Efficient (revenue per call), Rising/Falling Stars (week-over-week change).
Row 3: Win-loss patterns (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: win-loss-analysis, displayMode: chart, vizType: bar (won vs. lost by source: ICP fit signal)
- Card 2: Insights to source recipe: deal-velocity-by-stage, displayMode: chart, vizType: bar (which stages slow deals down: coaching focus areas)
Row 4: Strategic deal hygiene (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: multi-threading-coverage-by-deal, displayMode: chart, vizType: stacked_bar (single-threaded deals are coaching opportunities: Gartner data shows they close at 50% lower rates)
- Card 2: Insights to source recipe: quota-attainment-by-rep, displayMode: chart, vizType: bar (per-rep attainment with team-average benchmark)
Annotations:
- Row 1's "Revenue per 100 Calls" is the Gong-popularized leading-indicator metric. Below team-average × 0.5 indicates serious efficiency issue; coach the rep on qualification or talk tracks.
- Row 2 (the leaderboard, full-width) is the dashboard's centerpiece. Manager workflow: open before weekly 1:1s, sort by "Rising/Falling Stars" to spot trend changes, then drill into specific reps for coaching topics.
- Row 3 shifts from individual to pattern: which deal types/sources lose? Which stages stall? These are team-level coaching topics, not 1:1 topics.
- Row 4 surfaces deal-hygiene issues that compound: single-threaded deals are pure coaching gold (advise the rep to multi-thread before proposal stage). Per-rep attainment with team-average overlay surfaces both the bottom (intervention) and top (replicate) of the distribution.
- Recommended cadence: read this dashboard before weekly 1:1s and Friday team standups. The rising-stars sort changes weekly; the patterns view changes monthly.
Taxonomy notes:
- rep-activity-leaderboard pulls from Call completed, call_logged, Messaged email (direction=outbound), Meeting scheduled, Task completed, Deal won: all canonical events.
- "Rep" identification is unified across events through created_by / assignee_id / owner_id resolving to the same Users object (owner_id is canonical).
- quota-attainment-by-rep depends on workspace-level quota target configuration: see that recipe's notes.
