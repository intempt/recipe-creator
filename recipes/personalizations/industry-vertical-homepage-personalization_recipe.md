---
name: industry-vertical-homepage-personalization
description: |
  Use when a user mentions "industry vertical homepage personalization", or asks for related help. Show different homepage hero, social proof, and messaging based on the visitor's detected industry (4-5 segments). Demandbase pattern; distinct from per-account ABM.
arguments: []
intempt:
  id: industry-vertical-homepage-personalization
  version: 1.0.0
  slashCommand: /personalization-recipe
  group: Personalizations
  shortDescription: "Show different homepage hero, social proof, and messaging based on the visitor's detected industry (4-5 segments). Demandbase pattern; distinct from per-account ABM."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [experiences]
    agent: experiment-strategist
    mode: [saas, b2b]
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
        Create a CLIENT PERSONALIZATION on /experiences titled "Industry Vertical Homepage".

        This is a PERSONALIZATION at the industry-segment level (broader than per-account ABM, narrower than generic). Each variant binds to one industry vertical. Operational sweet spot: 4-5 verticals.

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_personalization

        Variants (each binds to an industry audience — adjust to your top 4 verticals):
        - Control (audience = all — fallback): generic homepage for visitors without industry identification
        - Variant B (audience = "Technology / SaaS"): Tech/SaaS-specific hero
          - Audience: account_industry IN ("Technology", "SaaS", "Software")
        - Variant C (audience = "Financial Services"): Finance-specific hero
          - Audience: account_industry IN ("Banking", "Financial Services", "Insurance", "Fintech")
        - Variant D (audience = "Healthcare"): Healthcare-specific hero
          - Audience: account_industry IN ("Healthcare", "Health Tech", "Pharmaceuticals", "Medical Devices")
        - Variant E (audience = "Manufacturing / Industrial"): Industrial-specific hero
          - Audience: account_industry IN ("Manufacturing", "Industrial", "Logistics", "Supply Chain")

        Targeting:
        - Pages: homepage "/" and key marketing pages (/solutions, /pricing)
        - Devices: any
        - Display frequency: always

        Metrics:
        - form_submitted on demo-request form per industry segment
        - click_on on primary CTA per segment
        - Demo-request conversion rate per industry (typically the most important downstream metric)

        Schedule: continuous

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        Variant: Control (no DOM changes — fallback)

        Variant: B (Technology / SaaS)
          HTML target selector: .homepage-hero
          Variant DOM:
          <section class="homepage-hero" data-variant="b" data-vertical="technology">
            <h1>The platform that scales with your engineering org</h1>
            <p>From 10 engineers to 10,000. Used by Snowflake, Databricks, and Datadog.</p>
            <div class="hero-stats">
              <div><strong>500+</strong> SaaS companies</div>
              <div><strong>99.99%</strong> uptime</div>
              <div><strong>< 50ms</strong> p99 latency</div>
            </div>
            <button class="primary-cta" id="hero-cta-demo">See it in action</button>
          </section>

        Variant: C (Financial Services)
          Same structure with finance-specific copy:
          <h1>Compliant infrastructure for financial services</h1>
          <p>SOC2, PCI DSS, ISO 27001. Trusted by leading banks and fintechs.</p>
          Plus compliance badges and finance customer logos.

        Variant: D (Healthcare)
          Same structure with healthcare-specific copy:
          <h1>HIPAA-compliant data infrastructure for healthcare</h1>
          <p>BAA-ready. PHI-safe. Trusted by health tech and providers.</p>
          Plus HIPAA badge and healthcare customer logos.

        Variant: E (Manufacturing)
          Same structure with industrial-specific copy:
          <h1>Real-time operations data for manufacturing</h1>
          <p>Connect every machine, line, and warehouse. Built for industrial scale.</p>
          Plus industrial customer logos and IoT-specific imagery.

        The Visual Editor allows the user to swap logos, adjust copy, and select industry-specific stats per vertical. Avoid over-personalizing (vertical-specific case study links are good; vertical-specific pricing is usually too narrow).

        Taxonomy notes:
        - REQUIRES FIRMOGRAPHIC ENRICHMENT: account_industry must be populated via Clearbit, ZoomInfo, IP-reverse lookup, or manual segmentation. Without enrichment, all traffic falls through to Control.
        - This is a broader, more sustainable personalization than per-account ABM. ABM is high-effort per audience (named heroes); industry-vertical is medium-effort and applies to broader traffic.
        - Demandbase's research: 4-5 vertical segments is the operational sweet spot. Going beyond 5 makes content maintenance expensive without proportional return.
        - Don't combine industry-vertical personalization with ABM personalization concurrently on the same page — they'll conflict. Run sequentially or use the experience module's variant-targeting precedence (per-account beats per-industry beats default).
  outputs:
    - { name: personalization, type: personalization, cardinality: single, description: "Website personalization created on /experiences." }
---

# Industry Vertical Homepage Personalization

## Procedure

1. **Configure Website Personalization** [`create_personalization`] — Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2). → produces: personalization

   ```text
   Create a CLIENT PERSONALIZATION on /experiences titled "Industry Vertical Homepage".

   This is a PERSONALIZATION at the industry-segment level (broader than per-account ABM, narrower than generic). Each variant binds to one industry vertical. Operational sweet spot: 4-5 verticals.

   ═══ PATH 1: Top-level configuration ═══

   Experience type: client_personalization

   Variants (each binds to an industry audience — adjust to your top 4 verticals):
   - Control (audience = all — fallback): generic homepage for visitors without industry identification
   - Variant B (audience = "Technology / SaaS"): Tech/SaaS-specific hero
     - Audience: account_industry IN ("Technology", "SaaS", "Software")
   - Variant C (audience = "Financial Services"): Finance-specific hero
     - Audience: account_industry IN ("Banking", "Financial Services", "Insurance", "Fintech")
   - Variant D (audience = "Healthcare"): Healthcare-specific hero
     - Audience: account_industry IN ("Healthcare", "Health Tech", "Pharmaceuticals", "Medical Devices")
   - Variant E (audience = "Manufacturing / Industrial"): Industrial-specific hero
     - Audience: account_industry IN ("Manufacturing", "Industrial", "Logistics", "Supply Chain")

   Targeting:
   - Pages: homepage "/" and key marketing pages (/solutions, /pricing)
   - Devices: any
   - Display frequency: always

   Metrics:
   - form_submitted on demo-request form per industry segment
   - click_on on primary CTA per segment
   - Demo-request conversion rate per industry (typically the most important downstream metric)

   Schedule: continuous

   ═══ PATH 2: Variant HTML content (Visual Editor) ═══

   Variant: Control (no DOM changes — fallback)

   Variant: B (Technology / SaaS)
     HTML target selector: .homepage-hero
     Variant DOM:
     <section class="homepage-hero" data-variant="b" data-vertical="technology">
       <h1>The platform that scales with your engineering org</h1>
       <p>From 10 engineers to 10,000. Used by Snowflake, Databricks, and Datadog.</p>
       <div class="hero-stats">
         <div><strong>500+</strong> SaaS companies</div>
         <div><strong>99.99%</strong> uptime</div>
         <div><strong>< 50ms</strong> p99 latency</div>
       </div>
       <button class="primary-cta" id="hero-cta-demo">See it in action</button>
     </section>

   Variant: C (Financial Services)
     Same structure with finance-specific copy:
     <h1>Compliant infrastructure for financial services</h1>
     <p>SOC2, PCI DSS, ISO 27001. Trusted by leading banks and fintechs.</p>
     Plus compliance badges and finance customer logos.

   Variant: D (Healthcare)
     Same structure with healthcare-specific copy:
     <h1>HIPAA-compliant data infrastructure for healthcare</h1>
     <p>BAA-ready. PHI-safe. Trusted by health tech and providers.</p>
     Plus HIPAA badge and healthcare customer logos.

   Variant: E (Manufacturing)
     Same structure with industrial-specific copy:
     <h1>Real-time operations data for manufacturing</h1>
     <p>Connect every machine, line, and warehouse. Built for industrial scale.</p>
     Plus industrial customer logos and IoT-specific imagery.

   The Visual Editor allows the user to swap logos, adjust copy, and select industry-specific stats per vertical. Avoid over-personalizing (vertical-specific case study links are good; vertical-specific pricing is usually too narrow).

   Taxonomy notes:
   - REQUIRES FIRMOGRAPHIC ENRICHMENT: account_industry must be populated via Clearbit, ZoomInfo, IP-reverse lookup, or manual segmentation. Without enrichment, all traffic falls through to Control.
   - This is a broader, more sustainable personalization than per-account ABM. ABM is high-effort per audience (named heroes); industry-vertical is medium-effort and applies to broader traffic.
   - Demandbase's research: 4-5 vertical segments is the operational sweet spot. Going beyond 5 makes content maintenance expensive without proportional return.
   - Don't combine industry-vertical personalization with ABM personalization concurrently on the same page — they'll conflict. Run sequentially or use the experience module's variant-targeting precedence (per-account beats per-industry beats default).
   ```
