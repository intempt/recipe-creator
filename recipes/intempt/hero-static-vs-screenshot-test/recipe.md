---
description: Compares your current hero image against a real product screenshot and a photo of customers or the team. Static images only.
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
  - ecommerce
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
Primary metric: goal_completed_in_experience where experience_id = <this> (goal: form_submitted on demo / contact / signup, OR user_created within session of exposure)
Secondary metrics:
- click_on on primary CTA (does the hero image affect CTA click-through?)
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
