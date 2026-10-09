---
name: abm-account-personalization
description: |
  Use when a user mentions "abm account personalization", or asks for related help. Personalize homepage hero (logo, industry-specific messaging) per identified target account. The canonical Mutiny/Demandbase pattern. Requires firmographic enrichment.
arguments: []
intempt:
  id: abm-account-personalization
  version: 1.0.0
  slashCommand: /abm-account-personalization
  group: Personalizations
  title: "Named-account homepage hero"
  shortDescription: "Visitors from your target accounts see a hero built for their industry, with their company name and relevant customer logos. Everyone else sees the standard hero."
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
      title: "Set up the account variants"
      command: create_personalization
      produces: personalization
      bindsAs: personalization
      description: "Enterprise SaaS, financial services and healthcare target accounts each get their own hero, proof points and CTA on the homepage, pricing and demo pages. Visitors you cannot identify fall through to the default. Needs firmographic enrichment to match a visitor to a company."
      prompt: |
        Create a CLIENT PERSONALIZATION on /experiences titled "ABM Account Personalization".

        This is a PERSONALIZATION (audience-driven, no random split). Each variant binds to one or more target-account audiences. The pattern is: identified visitors from named target accounts see a hero customized to their company; unidentified visitors fall through to the default hero.

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_personalization

        Variants (each binds to a target-account audience: adjust audience IDs to your target list):
        - Control (audience = all: fallback): standard homepage hero
        - Variant B (audience = "tier-1 target accounts: enterprise SaaS"): hero customized for enterprise SaaS visitors
          - Audience definition: the account is one of your named target accounts (an explicit account list)
          - OR the account's industry is "Enterprise SaaS" AND the account has more than 1000 employees
        - Variant C (audience = "tier-1 target accounts: financial services"): hero customized for financial-services targets
          - Audience: the account's industry is one of "Banking", "Financial Services", "Insurance" AND the account has more than 500 employees
        - Variant D (audience = "tier-2 target accounts: healthcare"): hero customized for healthcare targets
          - Audience: the account's industry is one of "Healthcare", "Health Tech", "Medical Devices" AND the account has more than 100 employees

        Targeting (experience-wide):
        - Pages: homepage "/" and key conversion pages (/pricing, /demo)
        - Devices: any
        - Audience: specific (per-variant)
        - Display frequency: always

        Metrics (existing CRM/CDP: personalizations don't have hypothesis-bound primary/secondary):
        - Form submitted on demo-request form per audience (B2B's primary outcome)
        - Click on the primary CTA per audience
        - Account-level engagement (View page count per identified company in the targeting window)

        Schedule: continuous

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        Variant: Control (no DOM changes: fallback for non-target traffic)

        Variant: B (Enterprise SaaS targets)
          HTML target selector: .homepage-hero (replace contents)
          Variant DOM:
          <section class="homepage-hero" data-variant="b" data-audience="enterprise-saas">
            <h1>[Account name], scale your data ops without the platform tax</h1>
            <p>The infrastructure platform built for SaaS companies at scale. Trusted by [3-5 named SaaS customers].</p>
            <div class="hero-social-proof">
              <img src="/customers/snowflake-logo.svg" alt="Snowflake" />
              <img src="/customers/databricks-logo.svg" alt="Databricks" />
              <img src="/customers/datadog-logo.svg" alt="Datadog" />
            </div>
            <div class="hero-cta-row">
              <button class="primary-cta" id="hero-cta-demo">Book a demo with [Brand]</button>
              <a href="/case-studies/saas" class="secondary-link">Read SaaS case studies to </a>
            </div>
          </section>

        Variant: C (Financial Services targets)
          HTML target selector: .homepage-hero (replace contents)
          Variant DOM:
          <section class="homepage-hero" data-variant="c" data-audience="financial-services">
            <h1>SOC2 + PCI compliant infrastructure for [Account name]</h1>
            <p>Trusted by leading banks, insurers, and fintechs to handle high-stakes financial data.</p>
            <div class="hero-social-proof">
              <img src="/customers/jpmc-logo.svg" alt="JPMorgan Chase" />
              <img src="/customers/stripe-logo.svg" alt="Stripe" />
              <img src="/customers/plaid-logo.svg" alt="Plaid" />
            </div>
            <div class="hero-compliance-badges">
              <span>SOC2 Type II</span>
              <span>PCI DSS</span>
              <span>ISO 27001</span>
            </div>
            <div class="hero-cta-row">
              <button class="primary-cta" id="hero-cta-demo">Book a demo</button>
              <a href="/case-studies/financial-services" class="secondary-link">Financial services case studies to </a>
            </div>
          </section>

        Variant: D (Healthcare targets)
          Similar structure with HIPAA badges, healthcare customer logos, healthcare-specific copy.

        The Visual Editor allows the user to refine copy, swap customer logos to match the actual account's industry, and inject the account-name placeholder, which is substituted at render time when the visitor is identified.

        Notes:
        - Requires firmographic enrichment: this depends on matching a visitor to a company, via an enrichment provider or IP-based reverse lookup. Without it, all visitors fall through to the Control variant.
        - Make sure the account's industry and company size are populated by your enrichment before launching this personalization.
        - Demandbase's research shows the operational sweet spot is 4-5 distinct account segments. Beyond that, content management overhead exceeds the personalization gains.
        - Mutiny's playbook: tier-1 accounts (top 100 named accounts) get fully custom heroes; tier-2 (industry segments) get vertical-specific heroes; everyone else gets the default. This recipe encodes that pattern.
  outputs:
    - { name: personalization, type: personalization, cardinality: single, description: "Website personalization created on /experiences." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Named-account homepage hero

Visitors from your target accounts see a hero built for their industry, with their company name and relevant customer logos. Everyone else sees the standard hero.

## What it does

1. **Set up the account variants** (`create_personalization`)

   Enterprise SaaS, financial services and healthcare target accounts each get their own hero, proof points and CTA on the homepage, pricing and demo pages. Visitors you cannot identify fall through to the default. Needs firmographic enrichment to match a visitor to a company.

## What you end up with

- **personalization** (personalization): Website personalization created on /experiences.
