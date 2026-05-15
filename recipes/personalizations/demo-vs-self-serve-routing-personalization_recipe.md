---
name: demo-vs-self-serve-routing-personalization
description: |
  Use when a user mentions "demo vs self-serve routing personalization", or asks for related help. Show enterprise visitors a demo CTA, smaller-company visitors a self-serve CTA. Client personalization with firmographic audience targeting (no random split).
arguments: []
intempt:
  id: demo-vs-self-serve-routing-personalization
  version: 1.0.0
  slashCommand: /personalization-recipe
  group: Personalizations
  shortDescription: "Show enterprise visitors a demo CTA, smaller-company visitors a self-serve CTA. Client personalization with firmographic audience targeting (no random split)."
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
  invokesCommands:
    - create_personalization
  procedure:
    - step: 1
      title: "Configure Website Personalization"
      command: create_personalization
      produces: personalization
      bindsAs: personalization
      description: "Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2)."
      prompt: |
        Create a CLIENT PERSONALIZATION on /experiences titled "Demo vs Self-Serve Routing".

        This is a PERSONALIZATION (not an experiment) — different audiences see different content based on targeting rules. There is no random traffic split; instead each variant binds to a specific audience segment. There are no primary/secondary metrics — personalizations measure on existing CRM/CDP metrics rather than hypothesis-bound experiment metrics.

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_personalization

        Variants (each variant binds to a specific audience):
        - Control: standard self-serve CTA, audience = "all" (default; falls through if no other variant matches)
        - Variant B: enterprise demo CTA, audience = "enterprise visitors"
          - Audience definition: company size > 200 employees OR domain matches enterprise patterns (firmographic enrichment via the Accounts object)
        - Variant C: SMB self-serve CTA with social proof, audience = "SMB returning visitors"
          - Audience definition: company size 1-50 employees AND has at least one prior session_start

        Targeting (experience-wide):
        - Pages: page URL is the homepage "/" or marketing landing pages
        - Devices: any (firmographic data is identity-based, not device-based)
        - Audience: specific (each variant has its own audience binding)
        - Display frequency: always

        Metrics (existing CRM/CDP metrics — not hypothesis-bound):
        - form_submitted on demo-request form (per audience)
        - user_created (self-serve signup) (per audience)
        - deal_created (downstream attribution to demo route)

        Schedule: continuous — personalizations are not time-boxed like experiments. Edit the variants when needed; no statistical horizon.

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        Variant: Control (audience = all — fallback)
          HTML target selector: .hero-cta-block (default contents — keep existing)
          Existing self-serve CTA stays as the catch-all.

        Variant: B (audience = enterprise visitors)
          HTML target selector: .hero-cta-block (replace contents)
          Variant DOM:
          <div class="hero-cta-block" data-variant="enterprise" data-audience="enterprise">
            <h2>Enterprise teams move faster with [Product]</h2>
            <p>See how [Brand] adapts to your org's complexity in a 30-min demo.</p>
            <button class="primary-cta" id="demo-cta">Book a Demo</button>
            <p class="secondary-link"><a href="/contact-sales">Talk to sales →</a></p>
          </div>

        Variant: C (audience = SMB returning visitors)
          HTML target selector: .hero-cta-block (replace contents)
          Variant DOM:
          <div class="hero-cta-block" data-variant="smb-returning" data-audience="smb-returning">
            <h2>Welcome back — ready to get started?</h2>
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
        - "Returning visitor" detection uses Users.first_seen_at being older than the current session.
  outputs:
    - { name: personalization, type: personalization, cardinality: single, description: "Website personalization created on /experiences." }
---

# Demo vs Self-Serve Routing Personalization

## Procedure

1. **Configure Website Personalization** [`create_personalization`] — Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2). → produces: personalization

   ```text
   Create a CLIENT PERSONALIZATION on /experiences titled "Demo vs Self-Serve Routing".

   This is a PERSONALIZATION (not an experiment) — different audiences see different content based on targeting rules. There is no random traffic split; instead each variant binds to a specific audience segment. There are no primary/secondary metrics — personalizations measure on existing CRM/CDP metrics rather than hypothesis-bound experiment metrics.

   ═══ PATH 1: Top-level configuration ═══

   Experience type: client_personalization

   Variants (each variant binds to a specific audience):
   - Control: standard self-serve CTA, audience = "all" (default; falls through if no other variant matches)
   - Variant B: enterprise demo CTA, audience = "enterprise visitors"
     - Audience definition: company size > 200 employees OR domain matches enterprise patterns (firmographic enrichment via the Accounts object)
   - Variant C: SMB self-serve CTA with social proof, audience = "SMB returning visitors"
     - Audience definition: company size 1-50 employees AND has at least one prior session_start

   Targeting (experience-wide):
   - Pages: page URL is the homepage "/" or marketing landing pages
   - Devices: any (firmographic data is identity-based, not device-based)
   - Audience: specific (each variant has its own audience binding)
   - Display frequency: always

   Metrics (existing CRM/CDP metrics — not hypothesis-bound):
   - form_submitted on demo-request form (per audience)
   - user_created (self-serve signup) (per audience)
   - deal_created (downstream attribution to demo route)

   Schedule: continuous — personalizations are not time-boxed like experiments. Edit the variants when needed; no statistical horizon.

   ═══ PATH 2: Variant HTML content (Visual Editor) ═══

   Variant: Control (audience = all — fallback)
     HTML target selector: .hero-cta-block (default contents — keep existing)
     Existing self-serve CTA stays as the catch-all.

   Variant: B (audience = enterprise visitors)
     HTML target selector: .hero-cta-block (replace contents)
     Variant DOM:
     <div class="hero-cta-block" data-variant="enterprise" data-audience="enterprise">
       <h2>Enterprise teams move faster with [Product]</h2>
       <p>See how [Brand] adapts to your org's complexity in a 30-min demo.</p>
       <button class="primary-cta" id="demo-cta">Book a Demo</button>
       <p class="secondary-link"><a href="/contact-sales">Talk to sales →</a></p>
     </div>

   Variant: C (audience = SMB returning visitors)
     HTML target selector: .hero-cta-block (replace contents)
     Variant DOM:
     <div class="hero-cta-block" data-variant="smb-returning" data-audience="smb-returning">
       <h2>Welcome back — ready to get started?</h2>
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
   - "Returning visitor" detection uses Users.first_seen_at being older than the current session.
   ```
