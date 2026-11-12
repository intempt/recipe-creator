---
frontmatter_id: demo-vs-self-serve-routing-personalization
slash_command: /demo-vs-self-serve-routing-personalization
description: Use the personalization engine to show different CTAs to visitor audiences you define. It does not use firmographic company-size data.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: 'Shows homepage and landing-page visitors a CTA matched to their company: demo booking for enterprise visitors,
    free-trial signup with social proof for returning SMB visitors, and a self-serve CTA for everyone else.'
  parameters:
  - name: experienceTitle
    type: string
    label: Personalization title
    default: Demo vs Self-Serve Routing
    required: false
  - name: enterpriseMinEmployees
    type: number
    label: Enterprise company size threshold (employees, greater than)
    default: 200
    required: false
  - name: smbMaxEmployees
    type: number
    label: SMB company size maximum (employees)
    default: 50
    required: false
  - name: smbMinEmployees
    type: number
    label: SMB company size minimum (employees)
    default: 1
    required: false
  - name: returningVisitorWindow
    type: duration
    label: Returning visitor check (prior session required)
    default: 1 s
    required: false
  requirements:
  - slot: company_size_attribute
    kind: attribute
    meaning: The number of employees at a visitor's company, stored on the account record
  - slot: company_domain_attribute
    kind: attribute
    meaning: The email domain of a visitor's company, used to match enterprise domain patterns
    optional: true
  - slot: session_start_event
    kind: event
    meaning: A visitor started a website session
  - slot: demo_request_form_event
    kind: event
    meaning: A visitor submitted the demo-request form
  - slot: user_created_event
    kind: event
    meaning: A customer created a self-serve user account
  - slot: deal_created_event
    kind: event
    meaning: A sales deal was created in the CRM
    optional: true
  - slot: hero_page_target
    kind: destination
    meaning: Homepage and marketing landing pages where the hero CTA block appears
    optional: true
    channel: email
  steps:
  - id: s1
    builds: personalization
    uses:
    - experienceTitle
    - company_size_attribute
    - company_domain_attribute
    - session_start_event
    - demo_request_form_event
    - user_created_event
    - deal_created_event
    - enterpriseMinEmployees
    - smbMaxEmployees
    - smbMinEmployees
    - returningVisitorWindow
    instruction: 'Create a client personalization titled "{experienceTitle}" on the experiences page. It is a personalization,
      not an experiment: there is no random traffic split, no primary or secondary metrics, and no statistical horizon. Each
      variant delivers to its own audience. Targeting: pages where the URL is the homepage "/" or a marketing landing page;
      devices any; display frequency always; schedule continuous. Measure on existing CRM and CDP metrics per audience: demo-request
      form submitted, self-serve user created, and deal created (downstream attribution to the demo route).'
---

# Demo or self-serve CTA by company size

Slash command: /demo-vs-self-serve-routing-personalization

## Step 1: Set up the two CTA paths

Create a CLIENT PERSONALIZATION on /experiences titled "Demo vs Self-Serve Routing".
This is a PERSONALIZATION (not an experiment): different audiences see different content based on targeting rules. There is no random traffic split; instead each variant binds to a specific audience segment. There are no primary/secondary metrics: personalizations measure on existing CRM/CDP metrics rather than hypothesis-bound experiment metrics.
═══ PATH 1: Top-level configuration ═══
Experience type: client_personalization
Variants (each variant binds to a specific audience):
- Control: standard self-serve CTA, audience = "all" (default; falls through if no other variant matches)
- Variant B: enterprise demo CTA, audience = "enterprise visitors"
 - Audience definition: company size > 200 employees OR domain matches enterprise patterns (firmographic enrichment via the Accounts object)
- Variant C: SMB self-serve CTA with social proof, audience = "SMB returning visitors"
 - Audience definition: company size 1-50 employees AND has at least one prior Session start
Targeting (experience-wide):
- Pages: page URL is the homepage "/" or marketing landing pages
- Devices: any (firmographic data is identity-based, not device-based)
- Audience: specific (each variant has its own audience binding)
- Display frequency: always
Metrics (existing CRM/CDP metrics: not hypothesis-bound):
- Form submitted on demo-request form (per audience)
- User created (self-serve signup) (per audience)
- Deal created (downstream attribution to demo route)
Schedule: continuous: personalizations are not time-boxed like experiments. Edit the variants when needed; no statistical horizon.
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (audience = all: fallback)
 HTML target selector: .hero-cta-block (default contents: keep existing)
 Existing self-serve CTA stays as the catch-all.
Variant: B (audience = enterprise visitors)
 HTML target selector: .hero-cta-block (replace contents)
 Variant DOM:
 <div class="hero-cta-block" data-variant="enterprise" data-audience="enterprise">
 <h2>Enterprise teams move faster with [Product]</h2>
 <p>See how [Brand] adapts to your org's complexity in a 30-min demo.</p>
 <button class="primary-cta" id="demo-cta">Book a Demo</button>
 <p class="secondary-link"><a href="/contact-sales">Talk to sales to </a></p>
 </div>
Variant: C (audience = SMB returning visitors)
 HTML target selector: .hero-cta-block (replace contents)
 Variant DOM:
 <div class="hero-cta-block" data-variant="smb-returning" data-audience="smb-returning">
 <h2>Welcome back: ready to get started?</h2>
 <p>Free for teams up to 5. No credit card required.</p>
 <button class="primary-cta" id="signup-cta">Start Free Trial</button>
 <div class="social-proof">
 <p>Trusted by 12,000+ teams like yours</p>
 </div>
 </div>
The Visual Editor opens for each variant individually so the user can refine copy, social proof selection, and CTA design per audience.
Taxonomy notes:
- Personalizations differ from experiments in that variants don't compete; each one delivers to its own audience segment. The Setup tab hides Primary/Secondary Metrics and replaces the traffic-percentage stepper with an audience picker per variant.
- Firmographic enrichment (company size, domain matching) typically requires an integration like Clearbit or ZoomInfo; the Accounts object is the canonical place to store this data.
- "Returning visitor" detection uses Users.First seen being older than the current session.
