---
description: Sends one honest last email to prospects who never replied, which usually gets a faster yes or no than another follow up would.
author:
  first_name: Somya
  last_name: Nayak
  job_title: Marketing Lead
  avatar: https://cdn.intempt.com/assets/author-profile-pics/somya.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - b2b-saas
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
