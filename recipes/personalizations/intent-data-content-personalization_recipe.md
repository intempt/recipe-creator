---
name: intent-data-content-personalization
description: |
  Use when a user mentions "intent-data content personalization", or asks for related help. Show different content blocks based on the visitor's recent on-site behavioral signals (viewed pricing 2x to ROI calculator; downloaded security paper to security case study). Behavior-driven, not firmographic.
arguments: []
intempt:
  id: intent-data-content-personalization
  version: 1.0.0
  slashCommand: /intent-data-content-personalization
  group: Personalizations
  title: "Content blocks by browsing behavior"
  shortDescription: "What someone has been reading on your site decides what they see next: two pricing visits brings up the ROI calculator, a security page visit brings up the security case study."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [experiences]
    agent: experiment-strategist
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [personalization, client]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
  invokesCommands:
    - create_personalization
  procedure:
    - step: 1
      title: "Set up the behavior variants"
      command: create_personalization
      produces: personalization
      bindsAs: personalization
      description: "Four behavior triggers: two pricing views in 7 days shows the ROI calculator, a security or compliance view in 14 days shows the security case study, two integrations views shows the integration directory, and two case-study views shows more customer proof."
      prompt: |
        Create a CLIENT PERSONALIZATION on /experiences titled "Intent-Data Content Personalization".

        This is BEHAVIORAL personalization: each variant binds to an audience defined by recent on-site behavior, not by firmographic attributes. Different from ABM and industry-vertical personalizations.

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_personalization

        Variants (each binds to a behavioral audience):
        - Control (audience = all: fallback): generic content blocks
        - Variant B (audience = "high pricing intent"): show ROI calculator and pricing-comparison content
          - Audience: page_viewed where page_url contains "/pricing": count >= 2 in last 7 days
        - Variant C (audience = "security/compliance research"): show security case study and compliance content
          - Audience: page_viewed where page_url contains "/security" OR "/compliance": count >= 1 in last 14 days
          OR click_on on a security-whitepaper download link in last 14 days
        - Variant D (audience = "integrations research"): show integration directory and integrations case studies
          - Audience: page_viewed where page_url contains "/integrations": count >= 2 in last 7 days
        - Variant E (audience = "case study readers"): show more case studies and customer logos
          - Audience: page_viewed where page_url contains "/case-studies" OR "/customers": count >= 2 in last 14 days

        Targeting:
        - Pages: homepage "/" and key landing pages: anywhere a "Featured content" block renders
        - Devices: any
        - Display frequency: always

        Metrics (behavioral personalization):
        - form_submitted on demo-request OR contact form per behavioral segment
        - click_on on the personalized content block (per-variant CTR)
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
        - This recipe uses canonical event-history-based audiences. The platform's personalization engine evaluates audience rules at render time using the visitor's prior page_viewed and click_on event history.
        - Audience evaluation: "page_viewed where page_url contains '/pricing': count >= 2 in last 7 days" requires the platform to query the visitor's event history at render time. Confirm your /experiences personalization engine supports event-history-based audience rules (most modern platforms do; some legacy ones only support attribute-based).
        - The 7-day and 14-day windows are starting points; tune based on your typical buying cycle. B2B SaaS with longer cycles may use 30-day windows.
        - This personalization compounds with ABM and industry-vertical: a visitor from a target account in financial services who has viewed /pricing 3 times sees the most personalized experience: but the variants must be ordered by precedence (per-account beats per-industry beats per-intent beats default).
        - For privacy compliance, ensure your cookie consent banner allows behavioral tracking before evaluating intent-based audiences.
  outputs:
    - { name: personalization, type: personalization, cardinality: single, description: "Website personalization created on /experiences." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Content blocks by browsing behavior

What someone has been reading on your site decides what they see next: two pricing visits brings up the ROI calculator, a security page visit brings up the security case study.

## What it does

1. **Set up the behavior variants** (`create_personalization`)

   Four behavior triggers: two pricing views in 7 days shows the ROI calculator, a security or compliance view in 14 days shows the security case study, two integrations views shows the integration directory, and two case-study views shows more customer proof.

## What you end up with

- **personalization** (personalization): Website personalization created on /experiences.
