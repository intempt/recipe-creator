---
frontmatter_id: intent-data-content-personalization
slash_command: /intent-data-content-personalization
description: 'What someone has been reading on your site decides what they see next: two pricing visits brings up the ROI calculator, a security page visit brings up the security case study.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Visitors who have been reading pricing, security, integrations or case-study pages see matching content blocks
    on the homepage and key landing pages, with generic content for everyone else.
  parameters:
  - name: pricing_window
    type: duration
    label: Pricing page lookback window
    default: 7 d
    required: false
  - name: pricing_min_views
    type: number
    label: Minimum pricing page views
    default: 2
    required: false
  - name: security_window
    type: duration
    label: Security/compliance lookback window
    default: 14 d
    required: false
  - name: security_min_views
    type: number
    label: Minimum security/compliance page views
    default: 1
    required: false
  - name: integrations_window
    type: duration
    label: Integrations lookback window
    default: 7 d
    required: false
  - name: integrations_min_views
    type: number
    label: Minimum integrations page views
    default: 2
    required: false
  - name: case_study_window
    type: duration
    label: Case study lookback window
    default: 14 d
    required: false
  - name: case_study_min_views
    type: number
    label: Minimum case study page views
    default: 2
    required: false
  requirements:
  - slot: page_view_event
    kind: event
    meaning: A visitor viewed a page on the website
    properties:
    - name: page_url
      type: string
      meaning: URL of the page viewed
      optional: false
  - slot: content_click_event
    kind: event
    meaning: A visitor clicked a link or button on the website
    properties:
    - name: link_url
      type: string
      meaning: URL of the clicked link
      optional: true
  - slot: demo_request_form_event
    kind: event
    meaning: A visitor submitted a demo-request or contact form
    properties:
    - name: form_name
      type: string
      meaning: Name of the submitted form
      optional: true
  - slot: featured_content_block
    kind: event
    meaning: A featured content block is rendered on the homepage or a key landing page
  - slot: website_destination
    kind: destination
    meaning: The website where the personalized content is shown
    channel: email
  steps:
  - id: s1
    builds: personalization
    uses:
    - page_view_event
    - content_click_event
    - demo_request_form_event
    - featured_content_block
    - website_destination
    - pricing_window
    - pricing_min_views
    - security_window
    - security_min_views
    - integrations_window
    - integrations_min_views
    - case_study_window
    - case_study_min_views
    instruction: 'Create a client personalization titled "Intent-Data Content Personalization" on the experiences area, with
      continuous schedule and display frequency always, targeting any device on the homepage and key landing pages where a
      featured content block renders. This is behavioral personalization: each variant binds to an audience defined by recent
      on-site behavior, not firmographic attributes. Variants in precedence order: (1) Control, fallback audience = all visitors,
      showing generic content blocks with no DOM changes. (2) Variant B, audience = high pricing intent: a visitor who had
      a page view where the page URL contains "/pricing" at least {pricing_min_views} times in the last {pricing_window}.
      Show ROI calculator and pricing-comparison content in the {featured_content_block} target. (3) Variant C, audience =
      security/compliance research: a visitor who had a page view where the page URL contains "/security" or "/compliance"
      at least {security_min_views} time in the last {security_window}, OR clicked a security-whitepaper download link in
      the last {security_window}. Show security case study and compliance content. (4) Variant D, audience = integrations
      research: a visitor who had a page view where the page URL contains "/integrations" at least {integrations_min_views}
      times in the last {integrations_window}. Show integration directory and integrations case studies. (5) Variant E, audience
      = case study readers: a visitor who had a page view where the page URL contains "/case-studies" or "/customers" at least
      {case_study_min_views} times in the last {case_study_window}. Show more case studies and customer logos. Ensure the
      personalization engine evaluates event-history audience rules at render time. Track per variant: click on the personalized
      content block (CTR), and demo-request or contact form submissions per behavioral segment, plus demo-request conversion
      rate per segment.'
---

# Content blocks by browsing behavior

Slash command: /intent-data-content-personalization

## Step 1: Set up the behavior variants

Create a CLIENT PERSONALIZATION on /experiences titled "Intent-Data Content Personalization".
This is BEHAVIORAL personalization: each variant binds to an audience defined by recent on-site behavior, not by firmographic attributes. Different from ABM and industry-vertical personalizations.
═══ PATH 1: Top-level configuration ═══
Experience type: client_personalization
Variants (each binds to a behavioral audience):
- Control (audience = all: fallback): generic content blocks
- Variant B (audience = "high pricing intent"): show ROI calculator and pricing-comparison content
 - Audience: View page where Page URL contains "/pricing": count >= 2 in last 7 days
- Variant C (audience = "security/compliance research"): show security case study and compliance content
 - Audience: View page where Page URL contains "/security" OR "/compliance": count >= 1 in last 14 days
 OR Click on on a security-whitepaper download link in last 14 days
- Variant D (audience = "integrations research"): show integration directory and integrations case studies
 - Audience: View page where Page URL contains "/integrations": count >= 2 in last 7 days
- Variant E (audience = "case study readers"): show more case studies and customer logos
 - Audience: View page where Page URL contains "/case-studies" OR "/customers": count >= 2 in last 14 days
Targeting:
- Pages: homepage "/" and key landing pages: anywhere a "Featured content" block renders
- Devices: any
- Display frequency: always
Metrics (behavioral personalization):
- Form submitted on demo-request OR contact form per behavioral segment
- Click on on the personalized content block (per-variant CTR)
- Demo-request conversion rate per segment (the downstream signal that intent-matched content drives conversions)
Schedule: continuous
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (no DOM changes: fallback for visitors without strong intent signals)
Variant: B (high pricing intent: show ROI calculator)
 HTML target selector: .featured-content-block (the homepage block where featured content lives)
 Variant DOM:
 <section class="featured-content" data-variant="b" data-intent="pricing">
 <h2>Calculate your ROI with [Brand]</h2>
 <p>Based on what you've been reading, here's how teams like yours quantify the impact:</p>
 <div class="roi-calculator-embed">
 <!-- Lightweight embedded calculator: team size + tool spend to estimated savings -->
 <label>Your team size: <input type="number" id="roi-team-size" value="50" /></label>
 <label>Current tool spend ($/year): <input type="number" id="roi-current-spend" value="120000" /></label>
 <div class="roi-result">
 Estimated savings: <strong id="roi-savings">$48,000/year</strong>
 </div>
 </div>
 <a href="/pricing" class="content-cta" id="content-cta-pricing">See pricing to </a>
 </section>
Variant: C (security research: show security case study)
 HTML target selector: .featured-content-block
 Variant DOM:
 <section class="featured-content" data-variant="c" data-intent="security">
 <h2>How [Customer] passed their SOC2 audit with [Brand]</h2>
 <p>SOC2 Type II certified. PCI DSS Level 1. ISO 27001. Built for security teams.</p>
 <div class="case-study-card">
 <img src="/case-studies/customer-security.jpg" alt="Customer security case study" />
 <h3>Read the case study</h3>
 <p>How [Customer] reduced compliance overhead by 60%</p>
 </div>
 <a href="/security" class="content-cta" id="content-cta-security">Explore security to </a>
 </section>
Variant: D (integrations research: show integration directory)
 HTML target selector: .featured-content-block
 Variant DOM:
 <section class="featured-content" data-variant="d" data-intent="integrations">
 <h2>200+ pre-built integrations</h2>
 <p>Connect [Brand] to your existing stack: Salesforce, Slack, Snowflake, GitHub, and more.</p>
 <div class="integration-logo-grid">
 <img src="/logos/salesforce.svg" alt="Salesforce" />
 <img src="/logos/slack.svg" alt="Slack" />
 <img src="/logos/snowflake.svg" alt="Snowflake" />
 <img src="/logos/github.svg" alt="GitHub" />
 <img src="/logos/aws.svg" alt="AWS" />
 </div>
 <a href="/integrations" class="content-cta" id="content-cta-integrations">Browse integrations to </a>
 </section>
Variant: E (case-study readers: show more case studies)
 HTML target selector: .featured-content-block
 Variant DOM showing more customer stories.
The Visual Editor allows the user to refine copy, embed actual ROI-calculator widgets, and select case studies that match the visitor's likely industry.
Taxonomy notes:
- This recipe uses canonical event-history-based audiences. The platform's personalization engine evaluates audience rules at render time using the visitor's prior View page and Click on event history.
- Audience evaluation: "View page where Page URL contains '/pricing': count >= 2 in last 7 days" requires the platform to query the visitor's event history at render time. Confirm your /experiences personalization engine supports event-history-based audience rules (most modern platforms do; some legacy ones only support attribute-based).
- The 7-day and 14-day windows are starting points; tune based on your typical buying cycle. B2B SaaS with longer cycles may use 30-day windows.
- This personalization compounds with ABM and industry-vertical: a visitor from a target account in financial services who has viewed /pricing 3 times sees the most personalized experience: but the variants must be ordered by precedence (per-account beats per-industry beats per-intent beats default).
- For privacy compliance, ensure your cookie consent banner allows behavioral tracking before evaluating intent-based audiences.
