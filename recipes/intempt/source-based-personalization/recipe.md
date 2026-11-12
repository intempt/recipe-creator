---
frontmatter_id: source-based-personalization
slash_command: /source-based-personalization
description: The hero repeats the promise of the ad the visitor clicked, so a competitor search, a LinkedIn enterprise ad and a partner referral each land somewhere that matches.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Each paid, partner or organic visitor lands on a homepage or landing page whose hero repeats the promise of the
    ad they clicked, with a matching call to action.
  parameters:
  - name: landingPages
    type: text
    label: Pages where the personalization runs (homepage and key landing pages)
    default: /, /lp, /landing-*
    required: false
  - name: competitorCampaignKeyword
    type: string
    label: Campaign keyword marking competitor search ads
    default: competitor
    required: false
  - name: alternativeCampaignKeyword
    type: string
    label: Second campaign keyword marking competitor search ads
    default: alternative
    required: false
  - name: enterpriseCampaignKeyword
    type: string
    label: Campaign keyword marking LinkedIn enterprise ads
    default: enterprise
    required: false
  - name: smbCampaignKeyword
    type: string
    label: Campaign keyword marking Facebook SMB ads
    default: smb
    required: false
  - name: partnerIncentiveDiscount
    type: string
    label: Partner referral discount offer
    default: 20% off your first year
    required: false
  - name: smbFreeTeamLimit
    type: number
    label: Team size limit for free SMB plan shown in hero
    default: 5
    required: false
  - name: sessionPersistence
    type: enum
    label: How long source attribution sticks
    default: session
    required: false
    options:
    - session
    - user
  requirements:
  - slot: ad_click_visit
    kind: event
    meaning: A visitor arrived on the website from a tracked ad or referral click
    properties:
    - name: utm_source
      type: string
      meaning: Traffic source named in the link, such as google, linkedin, facebook or partner_xyz
      optional: false
    - name: utm_medium
      type: string
      meaning: Medium named in the link, such as organic or cpc
      optional: true
    - name: utm_campaign
      type: string
      meaning: Campaign name in the link, used to detect competitor, enterprise or SMB messaging
      optional: false
    - name: referrer
      type: string
      meaning: Referring website address
      optional: true
    - name: landing_page
      type: string
      meaning: Page the visitor landed on
      optional: false
  - slot: homepage_hero
    kind: destination
    meaning: The website homepage hero section that can be replaced per visitor source
    channel: email
  - slot: partner_logo_asset
    kind: knowledge
    meaning: Logos of partner companies used on partner referral heroes
    optional: true
  - slot: competitor_name
    kind: knowledge
    meaning: Name of the competitor and the brand's feature and outcome wording used in comparison heroes
  steps:
  - id: s1
    builds: personalization
    instruction: 'Create a client personalization titled "Source-Based Personalization" on the website experiences area that
      runs on {landingPages}. Use a control variant with no DOM changes as the fallback for direct, organic and unattributed
      traffic. Add five source variants, each bound to its audience: (a) competitor search: utm_source is google and utm_campaign
      contains {competitorCampaignKeyword} or {alternativeCampaignKeyword}; hero compares the brand with {competitor_name}
      and invites the visitor to see the comparison. (b) LinkedIn enterprise: utm_source is linkedin and utm_campaign contains
      {enterpriseCampaignKeyword}; hero reads as enterprise-grade without enterprise complexity, notes large-company trust
      and security, and offers a booked enterprise demo. (c) Facebook SMB: utm_source is facebook and utm_campaign contains
      {smbCampaignKeyword}; hero promises a tool built for growing teams, states the free plan covers up to {smbFreeTeamLimit}
      members with no card required, and offers a free trial. (d) Partner referral: referrer contains the partner domain or
      utm_source is partner_xyz; hero pairs the brand with the partner, shows the partner logo from {partner_logo_asset} and
      the offer {partnerIncentiveDiscount} for partner customers, with a partner signup button. (e) Organic branded search:
      utm_source is google, utm_medium is organic and the visitor landed on the homepage; hero welcomes the visitor, acknowledges
      they searched for the brand and offers a free trial. Keep the primary call to action id per variant. Attribution persists
      for the {sessionPersistence} scope. Track form submissions, primary call-to-action clicks and conversion rate per source.
      Run continuously.'
---

# Landing page matched to the ad

Slash command: /source-based-personalization

## Step 1: Set up the source variants

Create a CLIENT PERSONALIZATION on /experiences titled "Source-Based Personalization".
This is the simplest high-impact personalization. Visitors from different sources (Google Ads, LinkedIn Ads, Facebook Ads, organic search, direct, partner referrals) see hero content matched to the source.
═══ PATH 1: Top-level configuration ═══
Experience type: client_personalization
Variants (each binds to a source audience):
- Control (audience = all: fallback): generic hero for direct / organic / unattributed traffic
- Variant B (audience = "Google Ads: competitor terms"): hero matches the competitor-comparison query
 - Audience: UTM source = "google" AND UTM campaign CONTAINS "competitor" or "alternative"
- Variant C (audience = "LinkedIn Ads: enterprise"): hero matches the LinkedIn ad's enterprise messaging
 - Audience: UTM source = "linkedin" AND UTM campaign CONTAINS "enterprise"
- Variant D (audience = "Facebook Ads: SMB"): hero matches the Facebook ad's SMB messaging
 - Audience: UTM source = "facebook" AND UTM campaign CONTAINS "smb"
- Variant E (audience = "Partner referral"): hero matches the partner brand and offers a partner-specific incentive
 - Audience: referrer CONTAINS "partner-domain.com" OR UTM source = "partner_xyz"
- Variant F (audience = "Organic: branded search"): hero matches the brand-search intent
 - Audience: UTM source = "google" AND UTM medium = "organic" AND landing_page contains "/" (homepage)
Targeting:
- Pages: homepage "/" and key landing pages (/lp, /landing-*)
- Devices: any
- Display frequency: always (within session: source attribution sticks for the session)
Metrics:
- Form submitted on demo / contact / signup form per source
- Click on on primary CTA per source
- Conversion rate per source (existing CRM/CDP attribution metric)
Schedule: continuous
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (no DOM changes: fallback for direct/organic/unattributed traffic)
Variant: B (Google Ads: competitor terms)
 HTML target selector: .homepage-hero
 Variant DOM:
 <section class="homepage-hero" data-variant="b" data-source="google-competitor">
 <h1>Looking for an alternative to [Competitor]?</h1>
 <p>Here's why teams switching from [Competitor] choose [Brand]:</p>
 <ul class="comparison-bullets">
 <li>Better [feature 1]: [outcome]</li>
 <li>Faster [feature 2]: [outcome]</li>
 <li>Lower cost at scale: [outcome]</li>
 </ul>
 <button class="primary-cta" id="hero-cta-comparison">See the comparison</button>
 </section>
Variant: C (LinkedIn Ads: enterprise)
 Same structure with enterprise-targeted copy:
 <h1>Enterprise-grade [solution]: without the enterprise complexity</h1>
 <p>Trusted by Fortune 500 teams. SOC2, SAML SSO, dedicated support.</p>
 <button class="primary-cta" id="hero-cta-enterprise-demo">Book an enterprise demo</button>
Variant: D (Facebook Ads: SMB)
 Same structure with SMB-targeted copy:
 <h1>The [solution] built for growing teams</h1>
 <p>Free for teams up to 5. No credit card required.</p>
 <button class="primary-cta" id="hero-cta-smb-signup">Start free trial</button>
Variant: E (Partner referral)
 Same structure with partner co-branding:
 <h1>[Brand] + [Partner]: special offer for [Partner] customers</h1>
 <p>20% off your first year when you join through [Partner].</p>
 <img class="partner-logo" src="/partner-logos/[partner].svg" alt="[Partner]" />
 <button class="primary-cta" id="hero-cta-partner-signup">Claim partner offer</button>
Variant: F (Organic: branded search)
 Same structure with brand-search intent (visitor already knows you):
 <h1>Welcome: get started with [Brand]</h1>
 <p>You searched for us. Here's how to start.</p>
 <button class="primary-cta" id="hero-cta-direct-signup">Start free trial</button>
The Visual Editor allows the user to refine copy, swap images, and adjust CTAs per source segment. Ensure the [Competitor] / [Partner] placeholders are populated correctly per variant.
Taxonomy notes:
- The canonical Users-object UTM attributes are: UTM source, UTM medium, UTM campaign, UTM content, UTM term: all standard. Plus referrer and landing_page.
- These attributes are populated automatically on Session start from URL parameters and HTTP referrer header.
- For source attribution to persist beyond the entry session, the platform stores the first-touch UTM values on the user record (Users.UTM source, etc.). This is the canonical pattern.
- Don't over-segment: 4-6 source segments is the sweet spot. Too many segments to low traffic per variant to unmeasurable.
- Combine with industry-vertical or ABM personalization for compounding effect, but order precedence carefully (per-account beats per-source beats per-industry beats default).
