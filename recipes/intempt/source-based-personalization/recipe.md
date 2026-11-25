---
frontmatter_id: source-based-personalization
slash_command: /source-based-personalization
description: Each paid, partner or organic visitor lands on a homepage or landing page whose hero repeats the promise of the
  ad they clicked, with a matching call to action.
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
    type: string
    label: Pages where the hero changes
    default: /, /lp, /landing-*
    required: false
  - name: competitorCampaignKeyword
    type: string
    label: Campaign keyword for competitor search ads
    default: competitor
    required: false
  - name: alternativeCampaignKeyword
    type: string
    label: Campaign keyword for alternative search ads
    default: alternative
    required: false
  - name: enterpriseCampaignKeyword
    type: string
    label: Campaign keyword for enterprise ads
    default: enterprise
    required: false
  - name: smbCampaignKeyword
    type: string
    label: Campaign keyword for small-business ads
    default: smb
    required: false
  - name: partnerSource
    type: string
    label: utm_source value of partner referrals
    default: partner
    required: false
  - name: partnerIncentiveDiscount
    type: string
    label: Offer for partner customers
    default: 20% off your first year
    required: false
  - name: smbFreeTeamLimit
    type: number
    label: Team members on the free plan
    default: 5
    required: false
  - name: competitorName
    type: string
    label: Competitor named in the comparison hero
    required: true
  requirements:
  - slot: ad_click_visit
    kind: event
    meaning: A visitor arrived on the website from a tracked ad or referral click
    properties:
    - name: utm_source
      type: string
      meaning: UTM source of the visit
      optional: false
    - name: utm_medium
      type: string
      meaning: UTM medium of the visit
      optional: false
    - name: utm_campaign
      type: string
      meaning: UTM campaign of the visit
      optional: false
  steps:
  - id: s1
    builds: personalization
    uses:
    - ad_click_visit
    - landingPages
    - competitorCampaignKeyword
    - alternativeCampaignKeyword
    - enterpriseCampaignKeyword
    - smbCampaignKeyword
    - partnerSource
    - partnerIncentiveDiscount
    - smbFreeTeamLimit
    - competitorName
    instruction: 'Create a client-side personalization named "Source-Based Personalization" that replaces the landing page
      hero on {landingPages} with one matched to the ad clicked, all devices, for the session, continuously. Variants by the
      current {ad_click_visit}: (a) {ad_click_visit.utm_source} is google and {ad_click_visit.utm_campaign} contains {competitorCampaignKeyword}
      or {alternativeCampaignKeyword}: a hero comparing the brand with {competitorName} and a "See the comparison" button;
      (b) utm_source is linkedin and utm_campaign contains {enterpriseCampaignKeyword}: an enterprise hero on security and
      trust with a "Book an enterprise demo" button; (c) utm_source is facebook and utm_campaign contains {smbCampaignKeyword}:
      a hero for growing teams saying the free plan covers up to {smbFreeTeamLimit} members with no card, and a "Start free"
      button; (d) utm_source is {partnerSource}: a hero pairing the brand with the partner, the offer {partnerIncentiveDiscount}
      and a partner signup button; (e) utm_source is google and {ad_click_visit.utm_medium} is organic: a welcome hero with
      a free-trial button. Control: the current hero. Track call-to-action clicks and form submissions per variant.'
---

# Landing page matched to the ad

Slash command: /source-based-personalization

## Step 1: Set up the source variants

Create a client-side personalization named "Source-Based Personalization" that replaces the landing page hero on /, /lp, /landing-* with one matched to the ad clicked, all devices, for the session, continuously. Variants by the current ad click visit: (a) utm source is google and utm campaign contains competitor or alternative: a hero comparing the brand with the competitor named in the comparison hero and a "See the comparison" button; (b) utm_source is linkedin and utm_campaign contains enterprise: an enterprise hero on security and trust with a "Book an enterprise demo" button; (c) utm_source is facebook and utm_campaign contains smb: a hero for growing teams saying the free plan covers up to 5 members with no card, and a "Start free" button; (d) utm_source is partner: a hero pairing the brand with the partner, the offer 20% off your first year and a partner signup button; (e) utm_source is google and utm medium is organic: a welcome hero with a free-trial button. Control: the current hero. Track call-to-action clicks and form submissions per variant.
