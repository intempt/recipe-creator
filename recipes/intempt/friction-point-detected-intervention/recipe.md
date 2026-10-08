---
description: Detects friction from behavioral signals, segments those users, and sends email, SMS, push, or Slack follow- ups through a journey. Reply-agent adds 3-way sentiment tags to replies for triage.
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
---

# Friction rescue

Slash command: /friction-point-detected-intervention

## Step 1: Detect where people get stuck

Create an AI-derived attribute 'recent_friction_signal' on the User object, refreshed in real-time. Patterns detected: (a) repeated failed actions on the same UI element (3+ attempts at same form / button within a session); (b) abandoned setup step (started a multi-step flow, didn't complete, didn't return for 24+hrs); (c) error-encountered events without subsequent retry success; (d) help-content visits without subsequent action; (e) rage-click or rapid-back-button patterns. Output: structured object with friction_type, friction_location (where in product), severity (mild / moderate / severe based on time-stuck and repetition), and recommended_intervention.

## Step 2: Group by where they got stuck

Build a segment 'Active friction signal' capturing users with recent_friction_signal in the last 7 days where severity is moderate or severe. Real-time refresh. Excludes users already in active intervention from this journey (no double-poking). Partitions by friction_location so the journey routes contextually. Use the result of "Detect where people get stuck".

## Step 3: Help them inside the app

This step builds a page.
Generate in-app contextual help variants per friction_location. For setup-abandonment: contextual tooltip at the abandoned step with the answer to the common blocker. For repeated-failed-action: floating help bubble with 'Looks like you're stuck: here's what most users do' + GIF or short video. For error-encountered: helpful error explainer rendered where the error appeared. For decision-paralysis (long dwell time on a critical step): comparison guide or recommendation card. Each renders mid-session when the friction is freshest. Tone: helpful colleague, not aggressive sales. Use the result of "Detect where people get stuck", "Group by where they got stuck".

## Step 4: Email the fix if that misses

Generate email fallback content sent if the user doesn't engage with the in-app help OR has left the session before help was shown. Variants per friction_location. Format: subject directly addresses the issue ('Stuck on [specific step]? Here's the fix.'), body is a 60-second tutorial (video link or step-by-step screenshots), with a one-click resume-where-you-left-off deep link. Tone: not generic 'we noticed you got stuck': specific to the exact friction. Use the result of "Detect where people get stuck", "Group by where they got stuck", "Help them inside the app".

## Step 5: Offer to walk them through

Configure an AI agent scenario 'Friction rescue' that engages users with severe friction signal who haven't responded to in-app help OR email. Scenario: agent opens with awareness of the specific friction ('I see you've been working on [step]: happy to help walk through it'), offers to: (a) co-pilot the action with screen-share or step-by-step in chat, (b) escalate to human support if the problem is technical/account-level, (c) flag the friction as a product bug for the engineering queue. Agent NEVER pretends to be human; handoff to human is offered when agent can't resolve in 3 turns. Use the result of "Detect where people get stuck", "Group by where they got stuck".

## Step 6: Escalate if they stay stuck

Build a graduated-escalation journey triggered when recent_friction_signal becomes moderate or severe. Touch 1 (mid-session, immediate): in-app contextual help renders at the friction location. Touch 2 (4 hours later, if user left without resolving): email fallback with tutorial + resume-link. Touch 3 (24 hours later, if friction signal still active OR user hasn't returned): trigger agent scenario or, for severe-tier high-value users, create a CSM task for direct outreach. Exit on: friction_signal resolves (user completed the step (success), user explicitly dismisses help 3 times (respect) don't pester), unsubscribe. Use the result of "Detect where people get stuck", "Group by where they got stuck", "Help them inside the app", "Email the fix if that misses", "Offer to walk them through".

## Step 7: See where the product traps people

Compose a friction intervention dashboard: top 10 friction locations by frequency (a product-team-priority signal: these are the UX bugs the data is telling you about), in-app-help dismiss rate (high = irrelevant help, low = useful), friction-to-resolution rate by intervention touch (which level of escalation actually resolves), severe-tier-to-churn correlation (do users stuck severely actually churn: proves the intervention's necessity), and journey-attributed activation lift (does this play meaningfully move activation rate). The product team gets a free UX-research stream as a side effect. Use the result of "Detect where people get stuck", "Group by where they got stuck", "Help them inside the app", "Email the fix if that misses", "Offer to walk them through", "Escalate if they stay stuck".
