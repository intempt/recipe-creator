---
frontmatter_id: hero-static-vs-screenshot-test
slash_command: /hero-static-vs-screenshot-test
description: Compares your current hero image against a real product screenshot and a photo of customers or the team. Static images only.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Tests your current landing page hero image against a real product screenshot and a customer or team photo to find
    which image drives more form submissions and sign-ups.
  parameters:
  - name: experiment_title
    type: string
    label: Experiment title
    default: Hero Image Test
    required: false
  - name: test_duration_days
    type: duration
    label: Test duration
    default: 21 d
    required: false
  - name: min_visitors_per_variant
    type: number
    label: Minimum visitors per variant
    default: 1500
    required: false
  - name: control_traffic_pct
    type: number
    label: Control traffic share (%)
    default: 34
    required: false
  - name: variant_b_traffic_pct
    type: number
    label: Product screenshot variant traffic share (%)
    default: 33
    required: false
  - name: variant_c_traffic_pct
    type: number
    label: Customer/team photo variant traffic share (%)
    default: 33
    required: false
  - name: bounce_rate_guardrail_pct
    type: number
    label: Maximum allowed bounce rate increase (%)
    default: 5
    required: false
  - name: mobile_load_time_guardrail_ms
    type: number
    label: Maximum allowed mobile load time increase (ms)
    default: 200
    required: false
  requirements:
  - slot: landing_page_hero
    kind: knowledge
    meaning: The landing pages (homepage and key landing pages) that show a hero image element with the class hero-image
  - slot: demo_form_submitted
    kind: event
    meaning: A visitor submitted a demo, contact, or signup form
  - slot: user_created
    kind: event
    meaning: A new user account was created
    optional: true
  - slot: primary_cta_clicked
    kind: event
    meaning: A visitor clicked the primary call-to-action on a landing page
  - slot: page_bounced
    kind: event
    meaning: A visitor left a landing page without any further interaction
  steps:
  - id: s1
    builds: experiment
    uses:
    - landing_page_hero
    - demo_form_submitted
    - user_created
    - primary_cta_clicked
    - page_bounced
    - experiment_title
    - test_duration_days
    - min_visitors_per_variant
    - control_traffic_pct
    - variant_b_traffic_pct
    - variant_c_traffic_pct
    - bounce_rate_guardrail_pct
    - mobile_load_time_guardrail_ms
    instruction: 'Create a client experiment titled "{experiment_title}" on the homepage and key landing pages. Variants:
      Control ("{control_traffic_pct}%" traffic) keeps the existing hero image with no DOM changes; Variant B ("{variant_b_traffic_pct}%"
      traffic) replaces the {landing_page_hero} hero image element with a clean, authentic static product screenshot of the
      dashboard or core feature; Variant C ("{variant_c_traffic_pct}%" traffic) replaces the same element with an authentic
      photo of real customers or the team using the product. Target all devices and all visitors, with display frequency set
      to always. Primary metric: a goal completed within the experience, where the goal is a {demo_form_submitted} form submission
      or a {user_created} user creation within session of exposure. Secondary metrics: clicks on {primary_cta_clicked}, bounce
      rate from {page_bounced}, time on page, and scroll depth reaching 50%. Guardrails: bounce rate must not increase by
      more than {bounce_rate_guardrail_pct}%, and mobile load time must not increase by more than {mobile_load_time_guardrail_ms}
      ms. Run for {test_duration_days} with at least {min_visitors_per_variant} visitors per variant. Track Largest Contentful
      Paint per variant.'
---

# Landing page hero image test

Slash command: /hero-static-vs-screenshot-test

## Step 1: Set up the hero image test

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
Primary metric: goal_completed_in_experience where experience_id = <this> (goal: Form submitted on demo / contact / signup, OR User created within session of exposure)
Secondary metrics:
- Click on on primary CTA (does the hero image affect CTA click-through?)
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
Taxonomy notes:
- 2026 SaaS research strongly favors authentic visuals over stock illustrations. Real product screenshots often outperform abstract illustrations for product-led teams; real customer photos often outperform for service/enterprise teams.
- Page-speed monitoring is critical: measure Largest Contentful Paint (LCP) per variant. The winning hero image must also load fast.
- A static-image test is the foundation; animated/video heroes (Lottie embeds, MP4 background, etc.) are out of scope for this recipe and can be authored as a future extension once the static winner is determined.
- Mobile-specific image variants are essential: desktop hero images cropped down to mobile usually look poor and convert worse than mobile-designed versions.
