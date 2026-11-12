---
frontmatter_id: account-engagement-score-orchestration
slash_command: /account-engagement-score-orchestration
description: Scores each account from 0 to 100 on how its whole team uses the product, then runs a different play for healthy, slipping, declining and inactive accounts.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Scores each account 0-100 on whole-team product use, then sends tier-specific emails, admin dashboard changes,
    and a journey of follow-ups for healthy, slipping, declining and inactive accounts.
  parameters:
  - name: score_refresh
    type: string
    label: Account score refresh cadence
    default: daily
  - name: segment_min_account_age
    type: duration
    label: Minimum account age before scoring applies
    default: 30 d
  - name: green_min_score
    type: number
    label: Green tier minimum score
    default: 75
  - name: yellow_min_score
    type: number
    label: Yellow tier minimum score
    default: 40
  - name: red_min_score
    type: number
    label: Red tier minimum score
    default: 15
  - name: dormant_suppression_window
    type: duration
    label: Sustained dormancy before suppression
    default: 60 d
  - name: yellow_touch2_delay
    type: duration
    label: Yellow touch 2 delay
    default: 7 d
  - name: red_touch2_delay
    type: duration
    label: Red touch 2 delay
    default: 3 d
  - name: dormant_touch2_delay
    type: duration
    label: Dormant touch 2 delay
    default: 14 d
  - name: green_touch_cadence
    type: duration
    label: Green touch 1 cadence
    default: 30 d
  - name: tier_recheck_cadence
    type: duration
    label: Tier re-evaluation cadence
    default: 7 d
  requirements:
  - slot: account_usage_events
    kind: event
    meaning: A user at a customer account performed a product session or feature action
    properties:
    - name: account_id
      type: string
      meaning: Account the user belongs to
      optional: false
    - name: user_id
      type: string
      meaning: User who performed the action
      optional: false
    - name: user_role
      type: string
      meaning: Role of the user at the account
      optional: true
    - name: feature_name
      type: string
      meaning: Product feature used
      optional: true
  - slot: account_record
    kind: attribute
    meaning: A customer account with its seat count, paying status, and creation date
  - slot: account_engagement_score
    kind: attribute
    meaning: A 0-100 engagement score per account with a tier
    creatable: true
    definition: AI-derived account attribute computed daily from active-user ratio, engagement velocity, feature breadth,
      stakeholder distribution, and support ticket sentiment across all users at the account
  - slot: paying_b2b_accounts
    kind: segment
    meaning: Paying B2B accounts that are at least 30 days old and not in an active sales-led save-flow
    creatable: true
    definition: paying B2B accounts older than {segment_min_account_age} and not in an active sales-led save flow, partitioned
      by {account_engagement_score} tier
  - slot: email_channel
    kind: destination
    meaning: Email channel used to send tier emails to account contacts
    channel: email
  - slot: admin_dashboard
    kind: destination
    meaning: In-app admin dashboard where account personalization renders
    channel: email
  - slot: csm_team
    kind: destination
    meaning: Customer success manager task queue for account outreach
    channel: email
  - slot: subscription_events
    kind: event
    meaning: A customer subscription was canceled
    properties:
    - name: account_id
      type: string
      meaning: Account whose subscription changed
      optional: false
  - slot: customer_progress_business_case_journey
    kind: destination
    meaning: Existing journey for customers progressing on a business case, receiving green-tier handoff
    optional: true
    channel: email
  - slot: post_cancel_winback_journey
    kind: destination
    meaning: Existing journey for winning back canceled subscriptions
    optional: true
    channel: email
  - slot: product_engagement_dashboard
    kind: destination
    meaning: Dashboard space for account engagement and retention reporting
    channel: email
  steps:
  - id: s1
    builds: attribute
    uses:
    - account_usage_events
    - account_record
    - account_engagement_score
    - green_min_score
    - yellow_min_score
    - red_min_score
    - score_refresh
    instruction: 'Create the AI-derived attribute {account_engagement_score} on the account object, refreshed {score_refresh}.
      Aggregate across all users at each account: (a) active-user ratio (active users divided by total seats); (b) engagement
      velocity (session and event volume trending up or down at account level); (c) feature breadth (count of distinct features
      used by anyone at the account); (d) stakeholder distribution (engagement from multiple roles versus single-user dependence);
      (e) sentiment signals from support tickets. Output a numeric 0-100 score with tier: green ({green_min_score}-100, healthy
      and growing); yellow ({yellow_min_score}-74, stable but with warning signs); red ({red_min_score}-39, declining quickly);
      dormant (below {red_min_score}, effectively inactive). Read from {account_usage_events.account_id}, {account_usage_events.user_id},
      {account_usage_events.user_role}, {account_usage_events.feature_name} and {account_record}.'
  - id: s2
    builds: segment
    uses:
    - paying_b2b_accounts
    - account_engagement_score
    - segment_min_account_age
    - score_refresh
    - s1
    instruction: Build the segment {paying_b2b_accounts} containing all paying B2B accounts older than {segment_min_account_age}
      that are not in an active sales-led save flow. Partition the segment by the {account_engagement_score} tier and refresh
      it {score_refresh}. Use the result of "Score each account daily".
  - id: s3
    builds: email
    uses:
    - email_channel
    - account_engagement_score
    - paying_b2b_accounts
    - s1
    - s2
    instruction: 'Write one email per tier. GREEN: send to the champion contact, subject ''Your team is in the top 25% of
      [Product] users. Here''s what high-growth accounts do next.'' Include a subtle expansion call to action. YELLOW: send
      to the admin contact, subject ''Noticing a few of your team members aren''t logging in as often. Want help re-engaging
      the team?'' Include a call to action to book a CSM meeting. RED: send to the admin contact and the executive sponsor,
      subject ''Your team''s engagement has shifted. We''d like to understand what''s going on. 15-minute call?'' Include
      a direct CSM offer. DORMANT: send to the champion contact, subject ''It''s been a while. We miss you. Here''s what''s
      new since you last logged in.'' Include a fresh-start onboarding offer. Deliver through {email_channel}. Use the result
      of "Score each account daily" and "Group paying accounts by tier".'
  - id: s4
    builds: personalization
    uses:
    - admin_dashboard
    - account_engagement_score
    - paying_b2b_accounts
    - s1
    - s2
    instruction: 'Configure an in-app personalization on {admin_dashboard} that varies by {account_engagement_score} tier.
      GREEN: show the expansion roadmap and power-feature content for healthy growth. YELLOW: show team-engagement health
      statistics, ''invite team members'' prompts, and use-case templates for slow-adoption rescue. RED: show a direct connect-with-CSM
      button and ''troubleshoot setup'' resources prominently. DORMANT: render no account-engagement personalization. Use
      the result of "Score each account daily" and "Group paying accounts by tier".'
  - id: s5
    builds: automation
    uses:
    - paying_b2b_accounts
    - account_engagement_score
    - tier_recheck_cadence
    - green_touch_cadence
    - yellow_touch2_delay
    - red_touch2_delay
    - dormant_touch2_delay
    - dormant_suppression_window
    - subscription_events
    - customer_progress_business_case_journey
    - post_cancel_winback_journey
    - csm_team
    - email_channel
    - s1
    - s2
    - s3
    - s4
    instruction: 'Build a tiered journey on {paying_b2b_accounts}. Branch on the {account_engagement_score} tier at entry
      and re-evaluate the tier every {tier_recheck_cadence}. GREEN: send the ''Your team is in the top 25%'' email to the
      champion every {green_touch_cadence}, activate the admin personalization, send touch 2 quarterly, then hand off to {customer_progress_business_case_journey}.
      YELLOW: send the reactivation email to the admin on Day 0; on Day {yellow_touch2_delay} create a CSM task to reach out
      if the score has not recovered. RED: send the urgent email on Day 0 and create a CSM task the same day; send touch 2
      on Day {red_touch2_delay}; create an executive-sponsor task if no CSM contact has been made. DORMANT: send the last-chance
      email on Day 0; on Day {dormant_touch2_delay} send the final outreach and warning before suppression. Exit when the
      tier escalates back to green (log retention_win), when {subscription_events} shows a canceled subscription (hand off
      to {post_cancel_winback_journey}), or when dormancy lasts {dormant_suppression_window} or more (suppress). Use the result
      of "Score each account daily", "Group paying accounts by tier", "Write an email per tier" and "Change what the admin
      sees".'
  - id: s6
    builds: dashboard
    uses:
    - product_engagement_dashboard
    - account_engagement_score
    - paying_b2b_accounts
    - s1
    - s2
    - s3
    - s4
    - s5
    instruction: 'Compose an account-engagement dashboard on {product_engagement_dashboard}. Show: tier distribution across
      the book of business (green, yellow, red and dormant proportions); tier-migration trends week over week; the ARR-weighted
      at-risk pile (red plus dormant tier sum); red-tier-to-recovered conversion rate; and per-CSM tier distribution for workload
      balancing. Use the result of "Score each account daily", "Group paying accounts by tier", "Write an email per tier",
      "Change what the admin sees" and "Run the play for each tier".'
---

# Account engagement scoring and plays

Slash command: /account-engagement-score-orchestration

## Step 1: Score each account daily

Create an AI-derived attribute 'account_engagement_score' on the Account object, refreshed daily. Aggregates ACROSS all users at the account: (a) active-user ratio (active users / total seats); (b) engagement velocity (sessions/events trending up or down at account level); (c) feature breadth (count of features used by anyone at the account); (d) stakeholder distribution (engagement coming from multiple roles vs. single-user dependence); (e) sentiment signals from support tickets. Output: numeric 0-100 with tier: green (75-100 healthy growing) / yellow (40-74 stable but warning signs) / red (15-39 declining quickly) / dormant (<15 effectively inactive). The account-as-unit aggregation is the differentiator: most CDPs score users, this scores the buying entity.

## Step 2: Group paying accounts by tier

Build a segment 'B2B accounts tiered by engagement' capturing all paying B2B accounts, partitioned by account_engagement_score tier. Refreshed daily. Excludes accounts <30 days old (need history) and accounts in active sales-led save-flows (avoid double-orchestration). The journey routes from this segment based on tier. Use the result of "Score each account daily".

## Step 3: Write an email per tier

Generate per-tier email content. GREEN (expansion-leaning content sent to champion: 'Your team is in the top 25% of [Product] users) here's what high-growth accounts do next.' Plus subtle expansion CTA. YELLOW (reactivation content sent to admin: 'Noticing a few of your team members aren't logging in as often) want help re-engaging the team?' With a CSM-meeting CTA. RED (urgent personalized content sent to admin + executive sponsor: 'Your team's engagement has shifted) we'd like to understand what's going on. 15-minute call?' Direct CSM offer. DORMANT (last-chance content sent to champion: 'It's been a while) we miss you. Here's what's new since you last logged in.' With a fresh-start onboarding offer. Use the result of "Score each account daily", "Group paying accounts by tier".

## Step 4: Change what the admin sees

Configure an in-app personalization on the admin dashboard that varies by account tier. Green: shows expansion roadmap + power-features for healthy growth. Yellow: shows team-engagement health stats + 'invite team members' nudges + use-case templates relevant to slow-adoption rescue. Red: shows direct-CSM-connect button + 'troubleshoot setup' resources prominently. Dormant: doesn't render account-engagement personalization (won't help: the user isn't logging in anyway; reach them via email instead). Use the result of "Score each account daily", "Group paying accounts by tier".

## Step 5: Run the play for each tier

Build a tiered journey wired to account-engagement-tiered segment. Branch on account_engagement tier at entry AND re-evaluate weekly. GREEN: Touch 1 monthly (expansion-leaning content to champion. Personalization activates for admin. Touch 2 quarterly) handoff to customer-progress-business-case journey. YELLOW: Touch 1 Day 0 (reactivation content to admin. Touch 2 Day 7) CSM task to reach out if score hasn't recovered. RED: Touch 1 Day 0 (urgent content + CSM task SAME-DAY. Touch 2 Day 3) executive-sponsor task if no CSM contact made. DORMANT: Touch 1 Day 0 (last-chance email. Touch 2 Day 14) final outreach + warning before suppression. Exit on: tier escalation back to green (recovered: log retention_win), Subscription canceled (handoff to post-cancel-winback), or sustained dormancy 60+ days (suppress). Use the result of "Score each account daily", "Group paying accounts by tier", "Write an email per tier", "Change what the admin sees".

## Step 6: See where the book is heading

Compose an account-engagement dashboard: tier distribution across the book of business (green/yellow/red/dormant proportions: the health-of-business snapshot), tier-migration trends week-over-week (which direction are accounts moving), ARR-weighted at-risk pile (red + dormant tier sum), red-tier-to-recovered conversion rate (proof the intervention works), and per-CSM tier distribution (some CSMs handle red-heavy portfolios: informs workload balancing). The strategic NRR view for leadership. Use the result of "Score each account daily", "Group paying accounts by tier", "Write an email per tier", "Change what the admin sees", "Run the play for each tier".
