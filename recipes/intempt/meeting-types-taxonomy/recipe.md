---
description: Organizes calls with the notetaker's built in All, My, and Shared views so downstream summaries and reporting pull from the right call set.
author:
  first_name: Sid
  last_name: Chaudhary
  job_title: Founder & CEO
  avatar: https://cdn.intempt.com/assets/author-profile-pics/sid.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
---

# Set up your meeting types

Slash command: /meeting-types-taxonomy

## Step 1: Audit the types you have

List current meeting types in the project. For each existing type, classify: KEEP (clearly defined, distinct purpose, sufficient volume to justify), MERGE (overlaps with another type: e.g. 'product walkthrough' and 'demo' usually merge), RETIRE (dead type, no meetings booked in 90 days), or RENAME (purpose is right but name is unclear).

## Step 2: Create the Discovery type

Create or update the 'Discovery' meeting type. Default duration: 30 min. Booking link visibility: prospects who haven't yet seen a demo. Required outcome on completion: champion identified, pain confirmed, current solution noted, timeline established, budget signal captured. Default notetaker autojoin: ON. Skip creation if a clean equivalent already exists (use the audit output). Use the result of "Audit the types you have".

## Step 3: Create the Demo type

Create or update the 'Demo' meeting type. Default duration: 45 min. Booking link visibility: prospects who have completed discovery (or self-served past the qualifying threshold). Required outcome: features demonstrated logged, technical questions captured, objections logged, next-step proposed. Default notetaker autojoin: ON. Skip if a clean equivalent exists. Use the result of "Audit the types you have", "Create the Discovery type".

## Step 4: Create the Proposal type

Create or update the 'Proposal' meeting type. Default duration: 30 min. Booking link visibility: opportunities at proposal stage. Required outcome: pricing structure confirmed, contract questions captured, decision-maker presence verified, expected close date. Default notetaker autojoin: ON. Use the result of "Audit the types you have", "Create the Demo type".

## Step 5: Create the Renewal type

Create or update the 'Renewal' meeting type. Default duration: 30 min. Booking link visibility: existing customers within 90 days of contract end. Required outcome: usage health confirmed, stakeholder confirmation, expansion/contraction signals, contract terms discussion. Default notetaker autojoin: ON. Use the result of "Audit the types you have", "Create the Proposal type".

## Step 6: Create the Check-in type

Create or update the 'Customer Success Check-in' meeting type. Default duration: 30 min. Booking link visibility: existing customers; reachable from in-app help center. Required outcome: usage patterns discussed, blockers captured, expansion opportunities noted. Default notetaker autojoin: ON. Use the result of "Audit the types you have", "Create the Renewal type".
