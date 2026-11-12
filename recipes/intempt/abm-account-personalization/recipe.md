---
frontmatter_id: abm-account-personalization
slash_command: /abm-account-personalization
description: Personalize the homepage hero with industry-specific messaging for visitor segments you define. The personalization engine serves the variant, using audience data you supply.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Shows identified visitors from named target accounts a homepage hero tailored to their industry, while other visitors
    see the default hero.
  parameters:
  - name: primary_pages
    type: text
    label: Pages to personalize (homepage and key conversion pages)
    default: /, /pricing, /demo
    required: false
  - name: tier1_employee_min
    type: number
    label: Minimum employee count for tier-1 enterprise SaaS targets
    default: 1000
    required: false
  - name: tier1_fin_employee_min
    type: number
    label: Minimum employee count for tier-1 financial services targets
    default: 500
    required: false
  - name: tier2_health_employee_min
    type: number
    label: Minimum employee count for tier-2 healthcare targets
    default: 100
    required: false
  - name: schedule
    type: enum
    label: Run schedule
    default: continuous
    required: false
    options:
    - continuous
  requirements:
  - slot: visitor_account_identification
    kind: integration
    meaning: A firmographic enrichment source that identifies website visitors to their company account (for example Clearbit,
      Demandbase, 6sense, ZoomInfo or IP-based reverse lookup)
    channel: hubspot
  - slot: account_firmographics
    kind: attribute
    meaning: 'Account firmographic attributes: industry, employee count, account id and account name, populated by enrichment'
  - slot: demo_request_form_submitted
    kind: event
    meaning: A visitor submitted the demo-request form
    properties:
    - name: audience
      type: text
      meaning: The personalization audience the visitor matched
      optional: false
  - slot: primary_cta_clicked
    kind: event
    meaning: A visitor clicked the primary call-to-action button in the homepage hero
    properties:
    - name: audience
      type: text
      meaning: The personalization audience the visitor matched
      optional: false
  - slot: page_viewed
    kind: event
    meaning: A visitor viewed a web page
    properties:
    - name: account_id
      type: text
      meaning: Identified account id of the visitor
      optional: true
  - slot: enterprise_saas_target_list
    kind: segment
    meaning: 'Tier-1 target accounts in enterprise SaaS: an explicit list of named accounts, or accounts in the Enterprise
      SaaS industry with more than the minimum employee count'
  - slot: financial_services_target_list
    kind: segment
    meaning: Tier-1 target accounts in banking, financial services or insurance with more than the minimum employee count
  - slot: healthcare_target_list
    kind: segment
    meaning: Tier-2 target accounts in healthcare, health tech or medical devices with more than the minimum employee count
  steps:
  - id: s1
    builds: experiment
    uses:
    - visitor_account_identification
    - account_firmographics
    - demo_request_form_submitted
    - primary_cta_clicked
    - page_viewed
    - enterprise_saas_target_list
    - financial_services_target_list
    - healthcare_target_list
    - primary_pages
    - tier1_employee_min
    - tier1_fin_employee_min
    - tier2_health_employee_min
    - schedule
    instruction: 'Create a client personalization titled "ABM Account Personalization" on the {primary_pages} pages, with
      display frequency always, any device, and a continuous schedule. Use audience-driven variants with no random traffic
      split. Control is the fallback for all non-target traffic and keeps the standard homepage hero with no DOM changes.
      Variant B targets the audience {enterprise_saas_target_list} (explicit target account list, or Enterprise SaaS industry
      with employee count above {tier1_employee_min}). In Variant B, replace the contents of homepage hero section with an
      enterprise SaaS headline that includes the visitor''s account name, a short infrastructure-platform value line, three
      named SaaS customer logos, and a primary CTA button labeled to book a demo, plus a secondary link to SaaS case studies.
      Variant C targets the audience {financial_services_target_list} (banking, financial services or insurance with employee
      count above {tier1_fin_employee_min}). In Variant C, replace the contents of homepage hero section with a headline that
      includes the account name and compliance focus, a trust line for banks, insurers and fintechs, three financial-services
      customer logos, compliance badges for SOC2 Type II, PCI DSS and ISO 27001, a demo CTA button, and a secondary link to
      financial services case studies. Variant D targets the audience {healthcare_target_list} (healthcare, health tech or
      medical devices with employee count above {tier2_health_employee_min}). In Variant D, use the same structure as Variant
      C with healthcare-specific copy, healthcare customer logos and HIPAA compliance badges. Use the account name placeholder
      in the hero headline so the platform substitutes the identified company name at render time. Track three metrics per
      audience: demo-request form submissions, primary CTA clicks, and page view count per identified account during the targeting
      window.'
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
- Form submitted on demo-request form per audience (B2B's primary outcome)
- Click on on primary CTA per audience
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
The Visual Editor allows the user to refine copy, swap customer logos to match the actual account's industry, and inject the [Account name] placeholder. Use the account's name in the HTML: the platform's personalization engine substitutes the actual account name at render time when the visitor is identified.
Taxonomy notes:
- REQUIRES FIRMOGRAPHIC ENRICHMENT: This recipe depends on visitor-to-account identification, typically via Clearbit, Demandbase, 6sense, ZoomInfo, or IP-based reverse lookup. Without enrichment, all visitors fall through to the Control variant.
- The Accounts object stores firmographic attributes: account_industry, account_employee_count, account_revenue, account_id, etc. Ensure these are populated by your enrichment pipeline before launching this personalization.
- Demandbase's research shows the operational sweet spot is 4-5 distinct account segments. Beyond that, content management overhead exceeds the personalization gains.
- For the [Account name] template substitution, the platform reads from the Users object's company association: typically `Users.company_name` or `Accounts.name` for the matched account.
- Mutiny's playbook: tier-1 accounts (top 100 named accounts) get fully custom heroes; tier-2 (industry segments) get vertical-specific heroes; everyone else gets the default. This recipe encodes that pattern.
