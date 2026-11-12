---
frontmatter_id: breakup-sequence
slash_command: /breakup-sequence
description: Sends one honest last email to prospects who never replied, which usually gets a faster yes or no than another follow up would.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Sends one honest last email to prospects who never replied, giving them an easy yes or no and a way to reconnect
    later, without repeated follow-ups.
  parameters:
  - name: outreach_threshold
    type: number
    label: Minimum outreach attempts (email and call tasks) in the lookback window
    default: 5
    required: false
  - name: lookback_window
    type: duration
    label: Lookback window for outreach attempts
    default: 60 d
    required: false
  - name: topic
    type: string
    label: Topic placeholder used in the email body
    default: '[topic]'
    required: false
  - name: calendar_link
    type: string
    label: Calendar link for reconnecting
    default: '[calendar link]'
    required: false
  - name: email_subject
    type: string
    label: Email subject line
    default: Closing the loop
    required: false
  - name: exit_timeout
    type: duration
    label: Wait before marking lead cold-closed
    default: 14 d
    required: false
  - name: dashboard_period
    type: duration
    label: Reporting window for dashboard metrics
    default: 7 d
    required: false
  requirements:
  - slot: prospect_outreach_event
    kind: event
    meaning: A prospect received an outreach attempt by email or call task
    properties:
    - name: channel
      type: string
      meaning: Outreach channel, email or call
      optional: false
  - slot: prospect_engagement_event
    kind: event
    meaning: A prospect opened an email, replied, or had a meeting scheduled
    properties:
    - name: engagement_type
      type: string
      meaning: Open, reply, or meeting
      optional: false
  - slot: open_deal
    kind: attribute
    meaning: A lead or account has an open deal
  - slot: target_account_list
    kind: segment
    meaning: Accounts on the target-account list
  - slot: cold_silent_segment
    kind: segment
    meaning: Leads who received repeated outreach in the lookback window with no engagement, excluding open deals and target
      accounts
    creatable: true
    definition: leads who received {outreach_threshold}+ outreach attempts (email and call tasks) in the last {lookback_window}
      AND have no opens, no replies, and no meetings, excluding leads with open deals and leads whose accounts are on {target_account_list}
  - slot: email_reply_event
    kind: event
    meaning: A prospect replied to an email
  - slot: meeting_scheduled_event
    kind: event
    meaning: A meeting was scheduled with a prospect
  - slot: unsubscribe_event
    kind: event
    meaning: A prospect unsubscribed from email
  - slot: ae_owner
    kind: attribute
    meaning: The account executive who owns the lead and handles replies
  - slot: cold_closed_status
    kind: attribute
    meaning: Lead status marking a prospect as cold-closed
  steps:
  - id: s1
    builds: segment
    uses:
    - prospect_outreach_event
    - prospect_engagement_event
    - open_deal
    - target_account_list
    - outreach_threshold
    - lookback_window
    instruction: Build the segment '{cold_silent_segment}' of leads who received {outreach_threshold}+ outreach attempts across
      email and call tasks in the last {lookback_window} and have no opens, no replies, and no meetings. Exclude leads with
      an {open_deal} and leads whose accounts are on the {target_account_list}.
  - id: s2
    builds: email
    uses:
    - s1
    - topic
    - calendar_link
    - email_subject
    instruction: 'Write a break-up email with subject ''{email_subject}'' or ''Should I stop reaching out?''. Keep the tone
      direct and honest with no fake urgency and no ''final chance'' framing. Body of 4-5 sentences: ''I''ve reached out a
      few times about {topic}. I might have my timing wrong, or this might not be a priority for you right now. I''ll stop
      reaching out unless I hear back. If circumstances change down the road, here''s an easy way to reconnect: {calendar_link}.''
      Write it for the leads in the cold-silent segment from ''Find prospects who went quiet''.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - email_reply_event
    - meeting_scheduled_event
    - unsubscribe_event
    - exit_timeout
    - ae_owner
    - cold_closed_status
    instruction: 'Build a single-touch journey triggered when a lead enters {cold_silent_segment} from ''Find prospects who
      went quiet''. Send the email from ''Write the closing the loop note'' once. Exit on any of these: {email_reply_event}
      (route the lead to {ae_owner} for human handling as a success), {meeting_scheduled_event} (counts as a major success),
      or {unsubscribe_event} (honor it as a clean outcome). If none of these occur within {exit_timeout}, set the lead''s
      {cold_closed_status} and exit from active outreach. A cold-closed lead may re-enter prospecting only after a new significant
      signal such as a target-account refresh or an intent signal.'
  - id: s4
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - dashboard_period
    - email_reply_event
    - meeting_scheduled_event
    - cold_closed_status
    - ae_owner
    instruction: 'Build a break-up sequence performance dashboard covering the last {dashboard_period}. Show weekly break-up
      email volume from ''Send it once, then stop'', reply rate from {email_reply_event} against sends from ''Write the closing
      the loop note'' (typical range 8-15%), and positive-reply rate: replies that lead to {meeting_scheduled_event} versus
      polite declines. Show cold-closed conversion: the share of leads in {cold_closed_status} who answer ''not now, try again
      later'', tracked as future revival candidates. Show pipeline recovered through the break-up sequence this quarter. Add
      a manager view with rep-by-rep adoption of the break-up tactic, grouped by {ae_owner}. Use the cohort from ''Find prospects
      who went quiet''.'
---

# Breakup email for silent prospects

Slash command: /breakup-sequence

## Step 1: Find prospects who went quiet

Build a segment 'Cold silent prospects' capturing leads who received 5+ outreach attempts (across email and call tasks) in the last 60 days AND have not engaged at all (no opens, no replies, no meetings). Excludes leads with open deals (different motion) and leads whose accounts are on the target-account list (those merit continued outreach with new angles, not breakup).

## Step 2: Write the closing the loop note

Generate break-up email content. Subject: 'Closing the loop' or 'Should I stop reaching out?': direct, no fake urgency. Body: short (4-5 sentences). 'I've reached out a few times about [topic]. I might have my timing wrong, or this might not be a priority for you right now. I'll stop reaching out unless I hear back. If circumstances change down the road, here's an easy way to reconnect: [calendar link].' Tone: honest, no manipulation, no fake 'final chance!' framing. Counter-intuitively often the highest-replying email in a cold sequence because it removes pressure and invites a quick 'yes/no'. Use the result of "Find prospects who went quiet".

## Step 3: Send it once, then stop

Build a 1-touch journey triggered when a lead enters the cold-silent segment. Send the break-up email. Exit on: email_replied (any reply = success, route to AE for human handling), Meeting scheduled (huge success), unsubscribe (honored (and that's a clean outcome too), or 14-day timeout (no response) mark lead as 'cold-closed', exit from active outreach). After timeout, the lead can re-enter prospecting only via a new significant signal (target-account refresh, intent signal, etc). Use the result of "Find prospects who went quiet", "Write the closing the loop note".

## Step 4: See what the last email pulls

Compose a break-up sequence performance dashboard: break-up email volume per week, reply rate (typically 8-15%: surprisingly high for an 'I give up' message), positive-reply rate (replies that lead to meetings vs. polite 'no thanks'), cold-closed conversion (% who say 'not now but try again later': those become future revival candidates), and pipeline recovered via break-up sequence this quarter (the unexpected upside). Manager view: rep-by-rep adoption of the break-up tactic. Use the result of "Find prospects who went quiet", "Write the closing the loop note", "Send it once, then stop".
