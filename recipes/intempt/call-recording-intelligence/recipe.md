---
description: Pulls the objections, the talk ratio, the sentiment and the buying signals out of every call recording, files them on the deal, and flags the bad calls.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
---

# Call recording intelligence

Slash command: /call-recording-intelligence

## Step 1: Read every call transcript

Create an AI-derived attribute on the Meeting object called 'call_insights'. Computed at call_recording_available from the transcript. Output: structured object with (a) talk-listen ratio per participant; (b) objections detected (list with quote + timestamp + category: price/timing/competition/feature-gap/authority/trust); (c) sentiment trajectory across call phases (open/discovery/demo/close); (d) buying signals detected (list with quote + timestamp + category); (e) discovery question count; (f) at-risk score (composite: high objections + low buying signals + negative sentiment shifts).

## Step 2: Write the manager alert

Generate Slack alert content for sales managers when a call's at-risk score crosses threshold. Include: rep name, account name, deal value/stage, the 3 highest-severity objections with quoted clips, talk-listen ratio (flag if rep talked >65%), and a deep link to jump to the relevant transcript timestamps. Tone: coach-actionable, not punitive. Use the result of "Read every call transcript".

## Step 3: File it and flag the bad ones

Create a workflow firing on call_recording_available. Step sequence: (1) compute call_insights attribute from the transcript; (2) update the linked Meeting record's notes with the structured insights and link to the deal; (3) if at-risk score crosses threshold (>=70), post the manager alert to Slack #sales-coaching and create a task for the rep's manager to review within 24h; (4) if buying signals are strong and no follow-up exists, create a high-priority next-step task for the rep. Use the result of "Read every call transcript", "Write the manager alert".

## Step 4: Coach from the patterns

Compose a coaching dashboard: talk-listen ratio by rep (rolling 30 days) flagging anyone outside the 40-55% rep-talk healthy range; top 5 objection categories by frequency (network-level + per-rep); discovery question count distribution (flag reps consistently below 5/call); at-risk call count by rep and week; and a leaderboard of calls with the highest buying-signal density (these are good listen-back examples for team training). Use the result of "Read every call transcript", "Write the manager alert", "File it and flag the bad ones".
