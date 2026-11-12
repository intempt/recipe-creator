---
frontmatter_id: source-based-personalization
slash_command: /source-based-personalization
description: This recipe shows website visitors a homepage or landing page headline that matches the ad, partner link or search that brought them there. It is for growth and web marketers who want each traffic source to feel like a continuation of the click.
author:
  name: Intempt Technologies
  first_name: Intempt
  last_name: Technologies
  org_name: intempt
---

# Landing page matched to the ad

## Step 1: Set up the source variants

Create a website personalization titled "Source-Based Personalization" on the homepage and on landing pages matching "/lp" or "/landing-*". Each variant binds to how the visitor arrived.
Variants:
- Control: a generic hero, shown to direct, organic and unattributed traffic.
- Variant B: shown when Users.UTM source is "google" and Users.UTM campaign contains "competitor" or "alternative". The hero acknowledges the visitor is comparing alternatives and leads with a direct comparison call to action.
- Variant C: shown when Users.UTM source is "linkedin" and Users.UTM campaign contains "enterprise". The hero leads with enterprise-readiness: single sign-on, SOC 2, and dedicated support, with a call to action to book an enterprise demo.
- Variant D: shown when Users.UTM source is "facebook" and Users.UTM campaign contains "smb". The hero leads with ease of getting started for a small team, with a call to action to start a free trial.
- Variant E: shown when the HTTP referrer matches a configured partner domain, or Users.UTM source matches a configured partner identifier. The hero names the partner and states the partner-specific offer configured for that referral, with a call to action to claim it.
- Variant F: shown when Users.UTM source is "google", Users.UTM medium is "organic", and the landing page is the homepage. The hero welcomes a visitor who searched for the product by name directly, with a call to action to start a free trial.
Targeting: homepage and landing pages matching "/lp" or "/landing-*"; any device; the variant that matched at the start of the session persists for the rest of that session.
Metrics: the demo, contact or signup form submission rate per source variant, and the primary call-to-action click rate per source variant.
Schedule: continuous.

## Step 2: Measure conversion by source

Compose a dashboard titled "Source-Based Personalization Performance" showing the form-submission rate and call-to-action click rate for each variant, compared week over week against the Control. Flag any variant whose form-submission rate falls below the Control's for 2 consecutive weeks. Use the result of "Set up the source variants".

## Step 3: Retire underperforming source variants

Build a workflow that runs monthly, reading the flags from "Measure engagement by audience" equivalent flags produced in "Measure conversion by source". When a variant has been flagged as underperforming the Control for 2 consecutive months, create a task for the growth marketing owner recommending that variant be reverted to the Control hero for that source, with the conversion comparison attached. Use the result of "Set up the source variants", "Measure conversion by source".
