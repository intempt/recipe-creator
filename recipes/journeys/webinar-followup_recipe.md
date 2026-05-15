---
name: webinar-followup
description: 'Use when a user mentions "webinar follow-up", "webinar attendee follow-up", "post-webinar cadence", or asks for related help. When a webinar ends, fire branched follow-ups: attendees get the recording + next-step CTA + thank-you, no-shows get the on-demand link + objection-handling content — both feeding into a unified post-webinar conversion dashboard.'
arguments: []
intempt:
  id: webinar-followup
  version: 1.0.0
  slashCommand: /webinar-followup
  group: Journeys
  shortDescription: "'When a webinar ends, fire branched follow-ups: attendees get the recording + next-step CTA + thank-you, no-shows get the on-demand link + objection-handling content — both feeding into a unified post-webinar conversion dashboard.'"
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
      title: Identify Webinar Audience
      command: create_segment
      produces: segment
      bindsAs: segment
      description: Build a segment 'Recent webinar audience - last 14 days' capturing users registered for a webinar that has ended in the last 14 days. Includes both attendees and no-shows; the branching happens inside the journey via the attendance attribute.
      prompt: Build a segment 'Recent webinar audience - last 14 days' capturing users registered for a webinar that has ended in the last 14 days. Includes both attendees and no-shows; the branching happens inside the journey via the attendance attribute.
    - step: 2
      title: Build Attendance AI Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      dependsOn: [segment]
      description: 'Create an AI-derived attribute on the User object called ''last_webinar_attendance''. Computed at webinar_completed from webinar_attended events. Output: object with (a) webinar_id, (b) attended (boolean), (c) attendance_minutes, (d) engagement_score: composite of attendance duration + questions asked + poll responses, (e) topic of interest based on the webinar.'
      prompt: 'Create an AI-derived attribute on the User object called ''last_webinar_attendance''. Computed at webinar_completed from webinar_attended events. Output: object with (a) webinar_id, (b) attended (boolean), (c) attendance_minutes, (d) engagement_score: composite of attendance duration + questions asked + poll responses, (e) topic of interest based on the webinar.'
    - step: 3
      title: Build Branched Content
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment, attribute]
      description: 'Generate two parallel email content paths. Attendees path: touch 1 (within 2 hours) thank-you + recording link + 2-3 key takeaways; touch 2 (3 days later) related content recommendation + book-a-meeting CTA; touch 3 (7 days later, if no engagement) AE outreach with personalized angle based on attendance signals. No-shows path: touch 1 (within 2 hours) ''sorry you missed it'' + on-demand recording link; touch 2 (3 days later) objection-handling content (the most common reason for no-show is competing priorities — content positions on time-saving); touch 3 (7 days later, if engaged) next-webinar invite.'
      prompt: 'Generate two parallel email content paths. Attendees path: touch 1 (within 2 hours) thank-you + recording link + 2-3 key takeaways; touch 2 (3 days later) related content recommendation + book-a-meeting CTA; touch 3 (7 days later, if no engagement) AE outreach with personalized angle based on attendance signals. No-shows path: touch 1 (within 2 hours) ''sorry you missed it'' + on-demand recording link; touch 2 (3 days later) objection-handling content (the most common reason for no-show is competing priorities — content positions on time-saving); touch 3 (7 days later, if engaged) next-webinar invite.'
    - step: 4
      title: Build Branched Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, attribute, asset]
      description: 'Build a branched journey wired to the webinar audience segment. Top-level split on last_webinar_attendance.attended: TRUE → attendee 3-touch path, FALSE → no-show 3-touch path. Both paths feed into the same exit conditions: meeting_scheduled, deal_created, or 14-day max duration. High-engagement attendees (engagement_score >= 70) get fast-tracked to AE-outreach task creation at touch 2 instead of touch 3.'
      prompt: 'Build a branched journey wired to the webinar audience segment. Top-level split on last_webinar_attendance.attended: TRUE → attendee 3-touch path, FALSE → no-show 3-touch path. Both paths feed into the same exit conditions: meeting_scheduled, deal_created, or 14-day max duration. High-engagement attendees (engagement_score >= 70) get fast-tracked to AE-outreach task creation at touch 2 instead of touch 3.'
    - step: 5
      title: Build Webinar Performance Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, attribute, asset, journey]
      description: 'Compose a webinar performance dashboard: registration-to-attendance rate, attendance-minutes distribution, post-webinar email engagement by path (attendee vs no-show), webinar-to-meeting conversion rate, and webinar-to-deal-created conversion rate (90 days). Break down by webinar topic and source channel (email vs paid vs organic). Surface the top 3 webinars by deal conversion (those are good rerun candidates).'
      prompt: 'Compose a webinar performance dashboard: registration-to-attendance rate, attendance-minutes distribution, post-webinar email engagement by path (attendee vs no-show), webinar-to-meeting conversion rate, and webinar-to-deal-created conversion rate (90 days). Break down by webinar topic and source channel (email vs paid vs organic). Surface the top 3 webinars by deal conversion (those are good rerun candidates).'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Webinar Followup

## Procedure

1. **Identify Webinar Audience** [`create_segment`] — Build a segment 'Recent webinar audience - last 14 days' capturing users registered for a webinar that has ended in the last 14 days. Includes both attendees and no-shows; the branching happens inside the journey via the attendance attribute. → produces: segment
2. **Build Attendance AI Attribute** [`create_ai_attribute`] — Create an AI-derived attribute on the User object called 'last_webinar_attendance'. Computed at webinar_completed from webinar_attended events. Output: object with (a) webinar_id, (b) attended (boolean), (c) attendance_minutes, (d) engagement_score: composite of attendance duration + questions asked + poll responses, (e) topic of interest based on the webinar. → produces: attribute
3. **Build Branched Content** [`create_email_content`] — Generate two parallel email content paths. Attendees path: touch 1 (within 2 hours) thank-you + recording link + 2-3 key takeaways; touch 2 (3 days later) related content recommendation + book-a-meeting CTA; touch 3 (7 days later, if no engagement) AE outreach with personalized angle based on attendance signals. No-shows path: touch 1 (within 2 hours) 'sorry you missed it' + on-demand recording link; touch 2 (3 days later) objection-handling content (the most common reason for no-show is competing priorities — content positions on time-saving); touch 3 (7 days later, if engaged) next-webinar invite. → produces: asset
4. **Build Branched Journey** [`create_journey`] — Build a branched journey wired to the webinar audience segment. Top-level split on last_webinar_attendance.attended: TRUE → attendee 3-touch path, FALSE → no-show 3-touch path. Both paths feed into the same exit conditions: meeting_scheduled, deal_created, or 14-day max duration. High-engagement attendees (engagement_score >= 70) get fast-tracked to AE-outreach task creation at touch 2 instead of touch 3. → produces: journey
5. **Build Webinar Performance Dashboard** [`create_dashboard`] — Compose a webinar performance dashboard: registration-to-attendance rate, attendance-minutes distribution, post-webinar email engagement by path (attendee vs no-show), webinar-to-meeting conversion rate, and webinar-to-deal-created conversion rate (90 days). Break down by webinar topic and source channel (email vs paid vs organic). Surface the top 3 webinars by deal conversion (those are good rerun candidates). → produces: dashboard
