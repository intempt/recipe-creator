---
description: Creates a Salesforce lead the moment product usage says someone is ready, so a signal the product saw becomes a record a rep can work.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - b2b-saas
  - ecommerce
---

# Product qualified signal to a Salesforce lead

Slash command: /salesforce-pql-to-lead

## Step 1: Agree the qualifying signal

Create a segment describing the product-qualified signal (the usage threshold, the feature reached, the seats added) rather than encoding it inside the workflow. The definition is the thing sales and product will argue about, so it needs to live somewhere both can see it.

## Step 2: Upsert the lead, never double

Create a workflow enrolling members of the segment and creating a Salesforce lead for each. Use upsert with an external ID rather than create, because a create without a match key is a duplicate generator and the rep pays for it. Map only fields Intempt owns (the score, the signal, the source) and leave Salesforce-owned fields alone. Failure policy is skip-and-record so one rejected lead does not stop the rest. Use the result of "Agree the qualifying signal".
