---
description: Goes back to people who cancelled at 30, 60 and 90 days with what has changed, a discount, and a free month, then stops.
author:
  first_name: Somya
  last_name: Nayak
  job_title: Marketing Lead
  avatar: https://cdn.intempt.com/assets/author-profile-pics/somya.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - ecommerce
  - media
---

# Win back after cancellation

Slash command: /post-cancel-winback

## Step 1: Find recent cancellations

Build a segment 'Recently cancelled - last 120 days' capturing users with Subscription canceled in the last 30-120 days AND cancel_reason is NOT 'wrong-fit' or 'company-shutdown' (those won't winback). Excludes users who have already won back (subscribed again) and users who explicitly requested no-marketing in cancel form.

## Step 2: Write three win back emails

Generate 3-touch winback email content. Touch 1 (Day 30 after cancel): 'A lot has changed since you left: here's what's new.' Lead with 2-3 specific product improvements shipped post-cancel, relevant to their stated cancel reason. Touch 2 (Day 60): 'Come back for [N] months at 50% off': winback discount offer. Personalize the call-out with their prior use case if known. Touch 3 (Day 90, final): 'One last invitation' (softer, more emotional appeal) acknowledges you understand they left for a reason, mentions a free 30-day reactivation try (no charge until they confirm) as the final lever. Send-from: their original CSM if known, else success@ address. Use the result of "Find recent cancellations".

## Step 3: Send at 30, 60 and 90 days

Build a 3-touch journey triggered when Subscription canceled fired 30+ days ago. Touch 1: Day 30. Touch 2: Day 60. Touch 3: Day 90. Each touch personalized using the prior account context (cancel reason, plan, last-used features). Exit on: Subscription started (won back: record winback_won event), email_replied (warm handoff to sales), unsubscribe, or 120-day timeout (after which user moves to long-term lapsed nurture, separate motion). Use the result of "Find recent cancellations", "Write three win back emails".

## Step 4: See who comes back

Compose a winback dashboard: post-cancel winback rate (% of cancellers who re-subscribe within 90 days: baseline benchmark is 5-10%), winback rate by touch (which touch is actually driving recoveries), winback rate by original cancel reason (informs which reasons are recoverable vs. final), ARR recovered via winback this quarter, and time-to-winback distribution (most winbacks happen in the first 60 days; users dormant 90+ days rarely return without a major external trigger). Use the result of "Find recent cancellations", "Write three win back emails", "Send at 30, 60 and 90 days".
