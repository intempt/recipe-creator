---
description: Asks for a review, a referral or a case study just after a customer wins something, and never asks the same person twice inside 90 days.
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
  - finance
  - social
---

# Advocacy asks at the right moment

Slash command: /milestone-driven-advocacy-asks

## Step 1: Spot the goodwill moments

Create an AI-derived attribute 'active_advocacy_moment' on the User/Account object. Detects natural advocacy windows (when goodwill is highest). Inputs: (a) first-value-achieved events (key activation milestone), (b) expansion-completed events (account just upgraded), (c) renewal-closed events (just renewed for another term), (d) high-engagement-streak (consecutive weeks of strong activity), (e) customer-success-milestone (reached usage benchmark, completed initial use case), (f) explicit positive support sentiment, (g) NOT during friction or churn-risk. Output: object with moment_type, moment_strength (high/medium), recommended_ask (review / referral / case-study / speaker-opportunity / roadmap-feedback), and ask_recipient_role (champion / economic-buyer / power-user).

## Step 2: Find who is ready to be asked

Build a segment 'Advocacy-ready' capturing users where active_advocacy_moment is high-strength in the last 7 days AND the user hasn't been asked for an advocacy action in the last 90 days (avoid donor fatigue) AND there's no active friction/churn signal (the timing is genuinely good, not just numerically positive). Partitioned by recommended_ask so the journey routes accordingly. Use the result of "Spot the goodwill moments".

## Step 3: Write one ask per moment

Generate advocacy-ask email variants per recommended_ask. Review ask: 'You just [hit milestone]: would you share your experience publicly? Takes 3 minutes.' Includes one-click links to G2, Capterra, or the relevant review site, pre-filled where the platform allows. Referral ask: 'You're [in top X% of users / just expanded / just renewed]: know anyone who'd benefit from [Product]? Here's your referral code for [reward].' Case-study ask: 'Your team's [specific achievement] is a great story: would you be willing to share it as a customer case study? Our marketing team will do all the writing.' Speaker-opportunity ask: 'We have a [conference / webinar] coming up (would you be interested in speaking?' Roadmap-feedback ask: 'You're using [Product] in such interesting ways) can we get 20 minutes for product roadmap feedback?' Tone: peer-respectful, never transactional. Send-from: named CSM or success lead, never marketing@. Use the result of "Spot the goodwill moments", "Find who is ready to be asked".

## Step 4: Let them volunteer in the app

Configure a recommendation surface 'Advocacy opportunities' that activates for advocacy-ready users in the in-app dashboard. Shows the user 2-3 advocacy actions they could take, each with a clear effort estimate ('3 min', '15 min', '1 hour') and what the user gets in return (recognition, referral reward, speaking visibility). Soft-surface, discoverable not interruptive. Lets the user volunteer rather than only being asked. Use the result of "Spot the goodwill moments", "Find who is ready to be asked".

## Step 5: Ask once, follow up once

Build a journey wired to advocacy-ready segment. Touch 1 (Day 1 after moment detected): advocacy-ask email matched to recommended_ask. Touch 2 (Day 0 of touch 1): activate recommendation surface in-app. Touch 3 (Day 7, ONLY if user engaged with touch 1 OR rec-surface): light follow-up with concrete next step ('You said you'd love to refer someone: here's the link to send them'). Branch: if user submits an advocacy action (review left / referral submitted / case-study agreed / etc), tag the user as 'active advocate' for cross-team awareness AND ensure they're prioritized for future advocacy opportunities. Exit on: action completed (success: log advocacy_event), explicit decline (respect), or 14-day timeout. No badgering. Use the result of "Spot the goodwill moments", "Find who is ready to be asked", "Write one ask per moment", "Let them volunteer in the app".

## Step 6: See which asks get a yes

Compose an advocacy program dashboard: advocacy-moment detection volume per week, ask-to-action conversion rate by ask type (which advocacy asks actually convert: referrals usually beat reviews in volume but reviews beat referrals in long-term value), top advocates (users who have completed 3+ advocacy actions: this is the inner-circle list to nurture specially), and downstream attribution (reviews influencing G2 score, referrals creating new pipeline, case studies appearing in sales decks). Reframes CS work from 'retention cost-center' to 'pipeline contributor'. Use the result of "Spot the goodwill moments", "Find who is ready to be asked", "Write one ask per moment", "Let them volunteer in the app", "Ask once, follow up once".
