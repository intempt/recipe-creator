---
name: saas-exit-intent-offer-test
description: |
  Use when a user mentions "saas exit-intent offer test", or asks for related help. Test what to OFFER on exit-intent for SaaS visitors (discount vs. comparison guide vs. content download vs. survey). 5x conversion vs. time-based popup cited.
arguments: []
intempt:
  id: saas-exit-intent-offer-test
  version: 1.0.0
  slashCommand: /saas-exit-intent-offer-test
  group: Experiments
  title: 'Exit-intent offer test'
  shortDescription: 'Compares what to offer a visitor about to leave: a discount, a comparison guide, a content download, a survey, or nothing.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [experiences]
    agent: experiment-strategist
    mode: [saas, b2b]
    complexity: standard
    executionMode: live
    tags: [experiment, client]
    experimentType: a-b
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_experiment
  procedure:
    - step: 1
      title: 'Set up the exit-intent test'
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: 'Splits marketing page traffic five ways, including a no-popup baseline that measures how many people leave anyway. The other four offer a trial extension or first-month discount, a competitor comparison guide, a best-practices report, or a short exit survey. Each variant is scored on the action it asks for, then compared on 7-day return visits and 14-day demo requests.'
      prompt: |
        Create a CLIENT EXPERIMENT on /experiences titled "SaaS Exit-Intent Offer".

        This experiment tests WHAT CONTENT to show in an exit-intent popup on SaaS marketing pages: distinct from cart-abandonment-popup-timing which tests WHEN to show the popup on ecommerce cart pages.

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_experiment

        Variants:
        - Control (20%): no exit-intent popup (baseline: measures intrinsic exit behavior without intervention)
        - Variant B (20%): trial-extension or first-month discount offer ("Stay 30 more days: get 50% off your first month")
        - Variant C (20%): comparison guide download ("Comparing [Brand] vs. [Competitor]? Get our side-by-side guide.")
        - Variant D (20%): content download / lead magnet ("Take our [Industry] Best Practices report with you")
        - Variant E (20%): exit survey ("Quick question: what stopped you from booking a demo today?")

        Targeting:
        - Pages: marketing pages (/pricing, /features, /solutions, key landing pages (NOT /checkout or /signup) exit there is a different problem)
        - Devices: desktop only (exit-intent requires mouse-leave detection; mobile requires different triggers)
        - Audience: visitors who have spent at least 30 seconds on the page (avoid triggering on bounces) AND have not yet converted
        - Display frequency: once per session (don't show twice)

        Primary metric: Completed an experience goal for this experience (goal varies by variant: see secondary metrics)
        Secondary metrics (per variant):
        - Variant B: Form submitted on the discount-claim form: discount-redemption rate
        - Variant C: Click on the comparison-guide download: guide-download rate
        - Variant D: Form submitted with email captured: lead-capture rate
        - Variant E: Form submitted on the exit survey: survey-completion rate
        - Cross-variant: 7-day return visit rate, 14-day demo-request conversion rate (which offer brings the highest-quality leads back?)

        Guardrail: bounce rate must not increase >5%; popup-dismiss rate must not exceed 80% (high dismissal = annoyance signal)

        Schedule: 21 days, 1,000 exit-intents triggered per variant minimum (note: only ~20-30% of visitors trigger exit-intent)

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        Variant: Control (no DOM changes: no popup)

        Variant: B (trial-extension / first-month discount)
          HTML target selector: body (append modal triggered on exit-intent)
          Variant DOM:
          <div class="exit-intent-modal" data-variant="b" data-offer="discount" hidden>
            <div class="modal-content">
              <button class="modal-close" id="exit-modal-dismiss" aria-label="Close">×</button>
              <h2>Wait: before you go</h2>
              <p>Get <strong>50% off your first month</strong> when you start a trial today.</p>
              <form class="discount-claim-form" id="exit-discount-form">
                <input type="email" name="email" placeholder="your@email.com" required />
                <button type="submit" class="modal-cta" id="exit-modal-cta">Claim 50% off</button>
              </form>
              <p class="modal-disclaimer">Discount code emailed instantly. No credit card required.</p>
            </div>
          </div>

        Variant: C (comparison guide download)
          HTML target selector: body
          Variant DOM:
          <div class="exit-intent-modal" data-variant="c" data-offer="comparison-guide" hidden>
            <div class="modal-content">
              <button class="modal-close" id="exit-modal-dismiss">×</button>
              <h2>Comparing options? Take our guide with you.</h2>
              <p>The 12-page comparison: <strong>[Brand] vs. [Competitor]</strong>. Honest, side-by-side.</p>
              <img src="/lead-magnets/comparison-guide-cover.webp" alt="Comparison guide cover" class="guide-thumbnail" />
              <form class="guide-download-form" id="exit-guide-form">
                <input type="email" name="email" placeholder="Work email" required />
                <button type="submit" class="modal-cta" id="exit-modal-cta">Email me the guide</button>
              </form>
            </div>
          </div>

        Variant: D (industry best-practices report)
          HTML target selector: body
          Variant DOM:
          <div class="exit-intent-modal" data-variant="d" data-offer="content-download" hidden>
            <div class="modal-content">
              <button class="modal-close" id="exit-modal-dismiss">×</button>
              <h2>Take our [Industry] best-practices report with you</h2>
              <p>30+ pages of insights from leading [Industry] teams. Free.</p>
              <img src="/lead-magnets/industry-report-cover.webp" alt="Industry report cover" class="report-thumbnail" />
              <form class="report-download-form" id="exit-report-form">
                <input type="email" name="email" placeholder="Work email" required />
                <input type="text" name="company" placeholder="Company" required />
                <button type="submit" class="modal-cta" id="exit-modal-cta">Send me the report</button>
              </form>
            </div>
          </div>

        Variant: E (exit survey)
          HTML target selector: body
          Variant DOM:
          <div class="exit-intent-modal exit-intent-modal--survey" data-variant="e" data-offer="survey" hidden>
            <div class="modal-content">
              <button class="modal-close" id="exit-modal-dismiss">×</button>
              <h2>Quick question: got 10 seconds?</h2>
              <p>What stopped you from booking a demo today?</p>
              <form class="exit-survey-form" id="exit-survey-form">
                <label><input type="radio" name="reason" value="too-expensive" /> Pricing was unclear or too high</label>
                <label><input type="radio" name="reason" value="not-relevant" /> Product didn't match what I need</label>
                <label><input type="radio" name="reason" value="researching" /> Just researching: not ready yet</label>
                <label><input type="radio" name="reason" value="missing-feature" /> Missing a key feature for me</label>
                <label><input type="radio" name="reason" value="other" /> Other</label>
                <input type="email" name="email" placeholder="Email (optional: for follow-up)" />
                <button type="submit" class="modal-cta" id="exit-modal-cta">Submit</button>
              </form>
            </div>
          </div>

          Trigger logic for all variants: attach mouseleave listener to document.documentElement; when mouse exits the top of the viewport AND the user has been on the page for >30 seconds AND hasn't converted, show the popup. Lightweight JS the user refines in the Visual Editor.

        This recipe is desktop-only because exit-intent needs mouse-leave detection. Mobile needs a different trigger, typically scroll-up direction on long pages, so use a separate mobile recipe if you need it.
        The 30-second engagement gate matters: without it the popup triggers on bouncers, where exit-intent isn't really intent at all.
        Treat the exit survey responses as research input for future page-content tests, not just a conversion variant.
        The discount variant often has the highest immediate conversion but may bring lower-quality leads, so judge it on the 14-day downstream demo-request rate.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Exit-intent offer test

Compares what to offer a visitor about to leave: a discount, a comparison guide, a content download, a survey, or nothing.

## What it does

1. **Set up the exit-intent test** (`create_experiment`)

   Splits marketing page traffic five ways, including a no-popup baseline that measures how many people leave anyway. The other four offer a trial extension or first-month discount, a competitor comparison guide, a best-practices report, or a short exit survey. Each variant is scored on the action it asks for, then compared on 7-day return visits and 14-day demo requests.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.
