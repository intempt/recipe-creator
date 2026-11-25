---
frontmatter_id: demo-vs-self-serve-routing-personalization
slash_command: /demo-vs-self-serve-routing-personalization
description: 'Shows homepage and landing-page visitors a CTA matched to their company size: demo booking for enterprise visitors,
  free-trial signup with social proof for returning small-business visitors, and a self-serve CTA for everyone else.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: 'Shows homepage and landing-page visitors a CTA matched to company size: a demo for enterprise, a free trial for
    returning small businesses, and self-serve for everyone else.'
  parameters:
  - name: experienceTitle
    type: string
    label: Personalization title
    default: Demo vs Self-Serve Routing
    required: false
  - name: enterpriseMinEmployees
    type: number
    label: Employees from which a company counts as enterprise
    default: 200
    required: false
  - name: smbMaxEmployees
    type: number
    label: Employees up to which a company counts as small business
    default: 50
    required: false
  - name: landingPagePaths
    type: string
    label: Landing page paths besides the homepage
    default: /lp/*
    required: false
  requirements:
  - slot: company_size_attribute
    kind: attribute
    meaning: The number of employees at the visitor's company
  - slot: session_start_event
    kind: event
    meaning: A visitor started a website session
  - slot: demo_request_form_event
    kind: event
    meaning: A visitor submitted the demo-request form
  - slot: user_created_event
    kind: event
    meaning: A customer created a self-serve user account
  steps:
  - id: s1
    builds: personalization
    uses:
    - company_size_attribute
    - session_start_event
    - demo_request_form_event
    - user_created_event
    - experienceTitle
    - enterpriseMinEmployees
    - smbMaxEmployees
    - landingPagePaths
    instruction: 'Create a client-side personalization named "{experienceTitle}" that replaces the main hero call to action
      on the homepage and on {landingPagePaths}, all devices, shown always, running continuously. Variant "Enterprise demo",
      for visitors whose {company_size_attribute} is {enterpriseMinEmployees} or more: the button "Book a demo" linking to
      the demo-request form. Variant "Returning small business", for visitors whose {company_size_attribute} is between 1
      and {smbMaxEmployees} and who did {session_start_event} before the current session: the button "Start your free trial"
      with a line of customer proof from similar small teams. Control, for everyone else: the self-serve button "Get started
      free". Track per variant: visitors who did {demo_request_form_event} and visitors who did {user_created_event} in the
      same session.'
---

# Demo or self-serve CTA by company size

Slash command: /demo-vs-self-serve-routing-personalization

## Step 1: Set up the two CTA paths

Create a client-side personalization named "Demo vs Self-Serve Routing" that replaces the main hero call to action on the homepage and on /lp/*, all devices, shown always, running continuously. Variant "Enterprise demo", for visitors whose company size attribute is 200 or more: the button "Book a demo" linking to the demo-request form. Variant "Returning small business", for visitors whose company size attribute is between 1 and 50 and who did session start event before the current session: the button "Start your free trial" with a line of customer proof from similar small teams. Control, for everyone else: the self-serve button "Get started free". Track per variant: visitors who did demo request form event and visitors who did user created event in the same session.
