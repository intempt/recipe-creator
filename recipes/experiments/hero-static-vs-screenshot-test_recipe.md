---
name: hero-static-vs-screenshot-test
description: |
  Use when a user mentions "hero image: static illustration vs. product screenshot vs. customer photo", or asks for related help. Test landing page hero image: abstract illustration vs. real product screenshot vs. customer/team photo. Distinct from product-page-layout (ecom) and onboarding-flow (post-signup).
arguments: []
intempt:
  id: hero-static-vs-screenshot-test
  version: 1.0.0
  slashCommand: /hero-static-vs-screenshot-test
  group: Experiments
  title: 'Landing page hero image test'
  shortDescription: 'Compares your current hero image against a real product screenshot and a photo of customers or the team. Static images only.'
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
      title: 'Set up the hero image test'
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: 'Splits homepage and landing page traffic three ways between the existing hero, a clean screenshot of the product UI, and an authentic photo of real users or the team. The winner is the variant with the most demo, contact or signup submissions in the same session.'
      prompt: |
        Create a CLIENT EXPERIMENT on /experiences titled "Hero Image Test".

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_experiment

        Variants:
        - Control (34%): existing hero image (whatever is currently on the page)
        - Variant B (33%): static product screenshot: a clean, real product UI screenshot showing the dashboard or core feature
        - Variant C (33%): customer/team photo: authentic photo of real users or the team using the product

        (Note: animated variants are out of scope for this recipe. Static images only.)

        Targeting:
        - Pages: homepage "/" and key landing pages
        - Devices: any (note: customer-photo variant should have mobile-cropped versions)
        - Audience: all visitors
        - Display frequency: always

        Primary metric: Completed an experience goal for this experience (goal: Form submitted on demo / contact / signup, OR User created within session of exposure)
        Secondary metrics:
        - Click on the primary CTA (does the hero image affect CTA click-through?)
        - Bounce rate (does the hero image keep visitors engaged?)
        - Time-on-page (proxy for engagement)
        - Scroll-depth-to-50% (does the hero compel visitors to scroll?)

        Guardrail: bounce rate must not increase >5%; mobile load time must not exceed +200ms (image swaps must use optimized formats: WebP, lazy loading)

        Schedule: 21 days, 1,500 visitors per variant minimum

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        Variant: Control (no DOM changes)

        Variant: B (product screenshot)
          HTML target selector: .hero-image (the existing hero image element)
          Replacement HTML:
          <picture class="hero-image hero-image--screenshot" data-variant="b" data-image-type="screenshot">
            <source media="(min-width: 1024px)" srcset="/hero-screenshots/dashboard-desktop.webp" type="image/webp" />
            <source media="(min-width: 768px)" srcset="/hero-screenshots/dashboard-tablet.webp" type="image/webp" />
            <img src="/hero-screenshots/dashboard-mobile.webp"
                 alt="[Brand] dashboard showing [key feature]"
                 loading="eager"
                 width="800"
                 height="500" />
          </picture>

          The screenshot should show a real, recognizable product UI: the dashboard, the main feature in use, or a typical user view. Avoid heavily annotated or marketing-overlaid screenshots; clean and authentic outperforms polished.

        Variant: C (customer/team photo)
          HTML target selector: .hero-image
          Replacement HTML:
          <picture class="hero-image hero-image--photo" data-variant="c" data-image-type="customer-photo">
            <source media="(min-width: 1024px)" srcset="/hero-photos/team-desktop.webp" type="image/webp" />
            <source media="(min-width: 768px)" srcset="/hero-photos/team-tablet.webp" type="image/webp" />
            <img src="/hero-photos/team-mobile.webp"
                 alt="[Customer name] team using [Brand]"
                 loading="eager"
                 width="800"
                 height="500" />
          </picture>

          The photo should be authentic: a real team or customer, not stock photography. If you don't have rights to a real customer photo, use your own team or skip this variant.

        The Visual Editor allows the user to swap actual image assets and adjust alt-text, sizing, and positioning. Critical: ensure all image variants are properly sized and compressed for fast load: image swaps that hurt page speed will lose regardless of design quality.

        2026 SaaS research strongly favors authentic visuals over stock illustrations. Real product screenshots often outperform abstract illustrations for product-led teams; real customer photos often outperform for service/enterprise teams. Monitor page speed by measuring Largest Contentful Paint (LCP) per variant: the winning hero image must also load fast. Animated or video heroes (Lottie embeds, MP4 background, etc.) are out of scope here and can follow as an extension once the static winner is known. Mobile-specific image variants are essential: desktop hero images cropped down to mobile usually look poor and convert worse than mobile-designed versions.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Landing page hero image test

Compares your current hero image against a real product screenshot and a photo of customers or the team. Static images only.

## What it does

1. **Set up the hero image test** (`create_experiment`)

   Splits homepage and landing page traffic three ways between the existing hero, a clean screenshot of the product UI, and an authentic photo of real users or the team. The winner is the variant with the most demo, contact or signup submissions in the same session.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.
