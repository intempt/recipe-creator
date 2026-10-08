---
description: Displays meetings in widgets so teams can review meeting activity in one place.
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
---

# Link meetings to the right deal

Slash command: /meeting-deal-linking-audit

## Step 1: Find meetings with no deal

List all meetings from the last 60 days that have no linked deal. Filter to meetings where the meeting type is revenue-impacting (Discovery, Demo, Proposal, Close, Renewal: exclude internal sync, 1:1, interview). For each unlinked meeting, surface: meeting date, host, attendees (with company), and any open deals on attendees' accounts. The output is the working set for the linking action.

## Step 2: Keep new meetings linked

Create a workflow firing daily that finds new unlinked revenue-impacting meetings (incremental from the audit). For each: (1) compute the most-likely deal match: same account + open stage + attendees overlap with deal contacts; (2) if confidence is high (single clear match), auto-link via link_meeting_to_deal; (3) if confidence is medium (multiple plausible matches or attendees-don't-overlap-deal-contacts), create a task for the meeting host asking them to confirm the right deal; (4) if no plausible match exists (account has no open deals), log to the dashboard for review (likely a new opp that needs a deal record). Use the result of "Find meetings with no deal".

## Step 3: Track linking coverage

Compose a meeting-deal-linking hygiene dashboard: % of revenue-impacting meetings linked to deals (target: 95%+; below 85% means the linking workflow is failing or reps aren't acting on confirmation tasks); count of meetings auto-linked vs. manually-linked vs. unlinked-needing-review; top 5 hosts with most unlinked meetings (coaching signal); recent meetings where 'no plausible deal match' was flagged (likely missing opportunities). Trend over time: falling linking-rate is a leading indicator of pipeline visibility decay. Use the result of "Find meetings with no deal", "Keep new meetings linked".
