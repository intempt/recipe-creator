---
name: webinar-followup
description: 'Use when a user mentions "webinar follow-up", "webinar attendee follow-up", "post-webinar cadence", or asks for related help. When a webinar ends, fire branched follow-ups: attendees get the recording + next-step CTA + thank-you, no-shows get the on-demand link + objection-handling content: both feeding into a unified post-webinar conversion dashboard.'
arguments: []
intempt:
  id: webinar-followup
  title: "Webinar follow up"
  version: 1.0.0
  slashCommand: /webinar-followup
  group: Journeys
  shortDescription: "Sends attendees the recording and a next step, sends no shows the on demand link, and shows which webinars actually create deals."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [webinar-followup, event-marketing]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: webinar_completed, severity: blocking }
      - { value: webinar_attended, severity: blocking }
  invokesCommands:
    - create_segment
    - create_ai_attribute
    - create_email_content
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: "Take everyone who registered"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Everyone registered for a webinar that ended in the last 14 days, attendees and no shows alike. The split happens inside the journey."
      prompt: Build a segment 'Recent webinar audience - last 14 days' capturing users registered for a webinar that has ended in the last 14 days. Includes both attendees and no-shows; the branching happens inside the journey via the attendance attribute.
    - step: 2
      title: "Record who actually turned up"
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      dependsOn: [segment]
      description: "Per person: which webinar, whether they attended, how many minutes they watched, an engagement score from that plus questions asked and polls answered, and the topic they came for."
      prompt: 'Create an AI-derived attribute on the User object called ''last_webinar_attendance''. Computed at webinar_completed from webinar_attended events. Output: object with (a) webinar_id, (b) attended (boolean), (c) attendance_minutes, (d) engagement_score: composite of attendance duration + questions asked + poll responses, (e) topic of interest based on the webinar.'
    - step: 3
      title: "Write both follow up paths"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment, attribute]
      description: "Attendees get a thank you with the recording and the key takeaways within two hours, related content and a meeting invitation on day 3, and AE outreach on day 7 if nothing has landed. No shows get the on demand link within two hours, content answering the usual reason for missing it on day 3, and an invitation to the next one on day 7 if they engaged."
      prompt: 'Generate two parallel email content paths. Attendees path: touch 1 (within 2 hours) thank-you + recording link + 2-3 key takeaways; touch 2 (3 days later) related content recommendation + book-a-meeting CTA; touch 3 (7 days later, if no engagement) AE outreach with personalized angle based on attendance signals. No-shows path: touch 1 (within 2 hours) ''sorry you missed it'' + on-demand recording link; touch 2 (3 days later) objection-handling content (the most common reason for no-show is competing priorities: content positions on time-saving); touch 3 (7 days later, if engaged) next-webinar invite.'
    - step: 4
      title: "Split on whether they showed"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, attribute, asset]
      description: "Attendees take one three touch path and no shows the other. Attendees scoring 70 or more on engagement skip ahead to an AE task at the second touch. Both paths end on a booked meeting, a new deal, or after 14 days."
      prompt: 'Build a branched journey wired to the webinar audience segment. Top-level split on last_webinar_attendance.attended: TRUE to attendee 3-touch path, FALSE to no-show 3-touch path. Both paths feed into the same exit conditions: meeting_scheduled, deal_created, or 14-day max duration. High-engagement attendees (engagement_score >= 70) get fast-tracked to AE-outreach task creation at touch 2 instead of touch 3.'
    - step: 5
      title: "See which webinars make deals"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, attribute, asset, journey]
      description: "Registration to attendance, minutes watched, engagement per path, and webinar to meeting and webinar to deal conversion over 90 days, broken out by topic and channel, with the top three for deal conversion called out as rerun candidates."
      prompt: 'Compose a webinar performance dashboard: registration-to-attendance rate, attendance-minutes distribution, post-webinar email engagement by path (attendee vs no-show), webinar-to-meeting conversion rate, and webinar-to-deal-created conversion rate (90 days). Break down by webinar topic and source channel (email vs paid vs organic). Surface the top 3 webinars by deal conversion (those are good rerun candidates).'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Webinar follow up

Sends attendees the recording and a next step, sends no shows the on demand link, and shows which webinars actually create deals.

## Before you run it

- Send the `webinar_completed` event
- Send the `webinar_attended` event

## What it does

1. **Take everyone who registered** (`create_segment`)

   Everyone registered for a webinar that ended in the last 14 days, attendees and no shows alike. The split happens inside the journey.

2. **Record who actually turned up** (`create_ai_attribute`)

   Per person: which webinar, whether they attended, how many minutes they watched, an engagement score from that plus questions asked and polls answered, and the topic they came for.

3. **Write both follow up paths** (`create_email_content`)

   Attendees get a thank you with the recording and the key takeaways within two hours, related content and a meeting invitation on day 3, and AE outreach on day 7 if nothing has landed. No shows get the on demand link within two hours, content answering the usual reason for missing it on day 3, and an invitation to the next one on day 7 if they engaged.

4. **Split on whether they showed** (`create_journey`)

   Attendees take one three touch path and no shows the other. Attendees scoring 70 or more on engagement skip ahead to an AE task at the second touch. Both paths end on a booked meeting, a new deal, or after 14 days.

5. **See which webinars make deals** (`create_dashboard`)

   Registration to attendance, minutes watched, engagement per path, and webinar to meeting and webinar to deal conversion over 90 days, broken out by topic and channel, with the top three for deal conversion called out as rerun candidates.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
