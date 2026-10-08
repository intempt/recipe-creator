---
description: Personalize the homepage hero with industry-specific messaging for visitor segments you define. The personalization engine serves the variant, using audience data you supply.
author:
  first_name: V
  last_name: Ranadheer
  job_title: Design Engineer
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - media
---

# Named-account homepage hero

Slash command: /abm-account-personalization

## Step 1: Set up the account variants

Create a CLIENT PERSONALIZATION on /experiences titled "ABM Account Personalization".
This is a PERSONALIZATION (audience-driven, no random split). Each variant binds to one or more target-account audiences. The pattern is: identified visitors from named target accounts see a hero customized to their company; unidentified visitors fall through to the default hero.
═══ PATH 1: Top-level configuration ═══
Experience type: client_personalization
Variants (each binds to a target-account audience: adjust audience IDs to your target list):
- Control (audience = all: fallback): standard homepage hero
- Variant B (audience = "tier-1 target accounts: enterprise SaaS"): hero customized for enterprise SaaS visitors
 - Audience definition: account_id IN ("acc-001", "acc-002", ...): the explicit target list
 - OR account_industry = "Enterprise SaaS" AND account_employee_count > 1000
- Variant C (audience = "tier-1 target accounts: financial services"): hero customized for financial-services targets
 - Audience: account_industry IN ("Banking", "Financial Services", "Insurance") AND account_employee_count > 500
- Variant D (audience = "tier-2 target accounts: healthcare"): hero customized for healthcare targets
 - Audience: account_industry IN ("Healthcare", "Health Tech", "Medical Devices") AND account_employee_count > 100
Targeting (experience-wide):
- Pages: homepage "/" and key conversion pages (/pricing, /demo)
- Devices: any
- Audience: specific (per-variant)
- Display frequency: always
Metrics (existing CRM/CDP: personalizations don't have hypothesis-bound primary/secondary):
- form_submitted on demo-request form per audience (B2B's primary outcome)
- click_on on primary CTA per audience
- Account-level engagement (page_viewed count per identified company in the targeting window)
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
The Visual Editor allows the user to refine copy, swap customer logos to match the actual account's industry, and inject the [Account name] placeholder. Use the account's name in the HTML: the platform's personalization engine substitutes the actual account name at render time when the visitor is identified.
Taxonomy notes:
- REQUIRES FIRMOGRAPHIC ENRICHMENT: This recipe depends on visitor-to-account identification, typically via Clearbit, Demandbase, 6sense, ZoomInfo, or IP-based reverse lookup. Without enrichment, all visitors fall through to the Control variant.
- The Accounts object stores firmographic attributes: account_industry, account_employee_count, account_revenue, account_id, etc. Ensure these are populated by your enrichment pipeline before launching this personalization.
- Demandbase's research shows the operational sweet spot is 4-5 distinct account segments. Beyond that, content management overhead exceeds the personalization gains.
- For the [Account name] template substitution, the platform reads from the Users object's company association: typically `Users.company_name` or `Accounts.name` for the matched account.
- Mutiny's playbook: tier-1 accounts (top 100 named accounts) get fully custom heroes; tier-2 (industry segments) get vertical-specific heroes; everyone else gets the default. This recipe encodes that pattern.
