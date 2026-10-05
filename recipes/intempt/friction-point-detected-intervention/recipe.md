---
id: friction-point-detected-intervention
title: Friction rescue
slash_command: /friction-point-detected-intervention
group: Journeys
owner: intempt
curator: somya
summary: >-
  Detects friction from behavioral signals, segments those users, and sends email, SMS, push, or Slack follow-
  ups through a journey. Reply-agent adds 3-way sentiment tags to replies for triage.
description: >-
  When behavioral signals detect friction (setup abandoned, repeated failed actions, error encountered, drop-
  off at conversion step), segment the affected users and run a journey that sends email, SMS, push, or Slack.
  Use reply-agent to tag replies as positive, neutral, or negative sentiment. Dashboard tracks the cohort.
version: 2.0.0
classification:
  product:
    - marketing
  agent: journey-builder
  mode:
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - friction-detection
    - in-app-rescue
    - graduated-escalation
prerequisites:
  events:
    - value: session_start
      severity: blocking
    - value: feature_used
      severity: blocking
  integrations:
    - value: slack
      severity: recommended
touches:
  reads:
    - The session_start event in your project
    - The feature_used event in your project
  writes:
    - A new attribute, from step 1 "Detect where people get stuck"
    - A new segment, from step 2 "Group by where they got stuck"
    - A new landing page, from step 3 "Help them inside the app"
    - A new designed email, from step 4 "Email the fix if that misses"
    - A new custom agent, from step 5 "Offer to walk them through"
    - A new journey, from step 6 "Escalate if they stay stuck"
    - A new dashboard, from step 7 "See where the product traps people"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Detect where people get stuck
    summary: >-
      Watched in real time: three or more failed attempts at the same button or form in one session, a
      multi step setup left unfinished for over 24 hours, errors with no successful retry, help pages
      read with nothing done after, and rage clicks or rapid back button use. It records the kind of friction,
      where in the product it happened, how severe it is, and what to do about it.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'recent_friction_signal' on the User object, refreshed in real-time.
      Patterns detected: (a) repeated failed actions on the same UI element (3+ attempts at same form
      / button within a session); (b) abandoned setup step (started a multi-step flow, didn't complete,
      didn't return for 24+hrs); (c) error-encountered events without subsequent retry success; (d) help-content
      visits without subsequent action; (e) rage-click or rapid-back-button patterns. Output: structured
      object with friction_type, friction_location (where in product), severity (mild / moderate / severe
      based on time-stuck and repetition), and recommended_intervention.
  - id: s2
    title: Group by where they got stuck
    summary: >-
      Users with a moderate or severe friction signal in the last 7 days, refreshed live and split by
      where in the product it happened. Anyone this journey is already helping is left out.
    builds: segment
    description: >-
      Build a segment 'Active friction signal' capturing users with recent_friction_signal in the last
      7 days where severity is moderate or severe. Real-time refresh. Excludes users already in active
      intervention from this journey (no double-poking). Partitions by friction_location so the journey
      routes contextually. Use the result of "Detect where people get stuck".
    dependsOn:
      - s1
  - id: s3
    title: Help them inside the app
    summary: >-
      Abandoned setup gets a tooltip at the step they left, carrying the answer to the usual blocker.
      Repeated failures get a help bubble showing what most people do, with a short clip. An error gets
      a plain explanation where it appeared. A long pause on a critical step gets a comparison guide or
      a recommendation. All of it renders mid session, while it is still fresh.
    builds: page
    description: >-
      Generate in-app contextual help variants per friction_location. For setup-abandonment: contextual
      tooltip at the abandoned step with the answer to the common blocker. For repeated-failed-action:
      floating help bubble with 'Looks like you're stuck: here's what most users do' + GIF or short video.
      For error-encountered: helpful error explainer rendered where the error appeared. For decision-paralysis
      (long dwell time on a critical step): comparison guide or recommendation card. Each renders mid-session
      when the friction is freshest. Tone: helpful colleague, not aggressive sales. Use the result of
      "Detect where people get stuck", "Group by where they got stuck".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Email the fix if that misses
    summary: >-
      Sent when the in app help was ignored or the session ended before it could show. The subject names
      the exact step. The body is a 60 second tutorial, by video or screenshots, with a one click link
      back to where they left off.
    builds: email_html
    description: >-
      Generate email fallback content sent if the user doesn't engage with the in-app help OR has left
      the session before help was shown. Variants per friction_location. Format: subject directly addresses
      the issue ('Stuck on [specific step]? Here's the fix.'), body is a 60-second tutorial (video link
      or step-by-step screenshots), with a one-click resume-where-you-left-off deep link. Tone: not generic
      'we noticed you got stuck': specific to the exact friction. Use the result of "Detect where people
      get stuck", "Group by where they got stuck", "Help them inside the app".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Offer to walk them through
    summary: >-
      An AI agent for severe friction that in app help and email both missed. It opens knowing the step
      they are stuck on and offers to walk through it, to escalate to human support for technical or account
      problems, or to file the friction as a bug. It never pretends to be human, and it hands over if
      it cannot resolve things in three turns.
    builds: agent
    description: >-
      Configure an AI agent scenario 'Friction rescue' that engages users with severe friction signal
      who haven't responded to in-app help OR email. Scenario: agent opens with awareness of the specific
      friction ('I see you've been working on [step]: happy to help walk through it'), offers to: (a)
      co-pilot the action with screen-share or step-by-step in chat, (b) escalate to human support if
      the problem is technical/account-level, (c) flag the friction as a product bug for the engineering
      queue. Agent NEVER pretends to be human; handoff to human is offered when agent can't resolve in
      3 turns. Use the result of "Detect where people get stuck", "Group by where they got stuck".
    dependsOn:
      - s1
      - s2
  - id: s6
    title: Escalate if they stay stuck
    summary: >-
      In app help right away, mid session. Four hours later an email with the tutorial and a resume link,
      if they left without finishing. After 24 hours the agent, or a CSM task for high value accounts,
      if the friction is still live. They leave when the step is completed, or after they dismiss the
      help three times.
    builds: journey
    description: >-
      Build a graduated-escalation journey triggered when recent_friction_signal becomes moderate or severe.
      Touch 1 (mid-session, immediate): in-app contextual help renders at the friction location. Touch
      2 (4 hours later, if user left without resolving): email fallback with tutorial + resume-link. Touch
      3 (24 hours later, if friction signal still active OR user hasn't returned): trigger agent scenario
      or, for severe-tier high-value users, create a CSM task for direct outreach. Exit on: friction_signal
      resolves (user completed the step (success), user explicitly dismisses help 3 times (respect) don't
      pester), unsubscribe. Use the result of "Detect where people get stuck", "Group by where they got
      stuck", "Help them inside the app", "Email the fix if that misses", "Offer to walk them through".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
  - id: s7
    title: See where the product traps people
    summary: >-
      The ten places friction happens most, how often the in app help gets dismissed, which level of escalation
      actually resolves it, whether severely stuck users go on to churn, and the activation lift this
      play produces.
    builds: dashboard
    description: >-
      Compose a friction intervention dashboard: top 10 friction locations by frequency (a product-team-priority
      signal: these are the UX bugs the data is telling you about), in-app-help dismiss rate (high = irrelevant
      help, low = useful), friction-to-resolution rate by intervention touch (which level of escalation
      actually resolves), severe-tier-to-churn correlation (do users stuck severely actually churn: proves
      the intervention's necessity), and journey-attributed activation lift (does this play meaningfully
      move activation rate). The product team gets a free UX-research stream as a side effect. Use the
      result of "Detect where people get stuck", "Group by where they got stuck", "Help them inside the
      app", "Email the fix if that misses", "Offer to walk them through", "Escalate if they stay stuck".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
      - s6
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: segment
    producedByStep: s2
    type: segment
    description: Segment produced by this recipe.
  - key: asset
    producedByStep: s4
    type: asset
    description: Asset produced by this recipe.
  - key: agent
    producedByStep: s5
    type: agent
    description: AI Agent Scenario produced by this recipe.
  - key: journey
    producedByStep: s6
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s7
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Friction rescue

Detects friction from behavioral signals, segments those users, and sends email, SMS, push, or Slack follow- ups through a journey. Reply-agent adds 3-way sentiment tags to replies for triage.

## Steps

1. **Detect where people get stuck** (builds attribute)

   Watched in real time: three or more failed attempts at the same button or form in one session, a multi step setup left unfinished for over 24 hours, errors with no successful retry, help pages read with nothing done after, and rage clicks or rapid back button use. It records the kind of friction, where in the product it happened, how severe it is, and what to do about it.

2. **Group by where they got stuck** (builds segment)

   Users with a moderate or severe friction signal in the last 7 days, refreshed live and split by where in the product it happened. Anyone this journey is already helping is left out.

3. **Help them inside the app** (builds page)

   Abandoned setup gets a tooltip at the step they left, carrying the answer to the usual blocker. Repeated failures get a help bubble showing what most people do, with a short clip. An error gets a plain explanation where it appeared. A long pause on a critical step gets a comparison guide or a recommendation. All of it renders mid session, while it is still fresh.

4. **Email the fix if that misses** (builds email_html)

   Sent when the in app help was ignored or the session ended before it could show. The subject names the exact step. The body is a 60 second tutorial, by video or screenshots, with a one click link back to where they left off.

5. **Offer to walk them through** (builds agent)

   An AI agent for severe friction that in app help and email both missed. It opens knowing the step they are stuck on and offers to walk through it, to escalate to human support for technical or account problems, or to file the friction as a bug. It never pretends to be human, and it hands over if it cannot resolve things in three turns.

6. **Escalate if they stay stuck** (builds journey)

   In app help right away, mid session. Four hours later an email with the tutorial and a resume link, if they left without finishing. After 24 hours the agent, or a CSM task for high value accounts, if the friction is still live. They leave when the step is completed, or after they dismiss the help three times.

7. **See where the product traps people** (builds dashboard)

   The ten places friction happens most, how often the in app help gets dismissed, which level of escalation actually resolves it, whether severely stuck users go on to churn, and the activation lift this play produces.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **agent** (agent): AI Agent Scenario produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The session_start event in your project
- The feature_used event in your project

Writes:

- A new attribute, from step 1 "Detect where people get stuck"
- A new segment, from step 2 "Group by where they got stuck"
- A new landing page, from step 3 "Help them inside the app"
- A new designed email, from step 4 "Email the fix if that misses"
- A new custom agent, from step 5 "Offer to walk them through"
- A new journey, from step 6 "Escalate if they stay stuck"
- A new dashboard, from step 7 "See where the product traps people"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build agent, dashboard, journey, page.
