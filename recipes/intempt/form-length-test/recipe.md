---
description: Compares a 3, 5 and 7 field demo request form, so you can see what each extra field costs you in submissions.
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
---

# Demo form length test

Slash command: /form-length-test

## Step 1: Set up the form length test

Create a CLIENT EXPERIMENT on /experiences titled "Demo Request Form Length".
═══ PATH 1: Top-level configuration ═══
Experience type: client_experiment
Variants:
- Control (34%): 3-field form: name, email, company
- Variant B (33%): 5-field form: adds job title, team size
- Variant C (33%): 7-field form: adds phone, use case description
Targeting:
- Pages: page URL contains "/demo" OR "/contact" OR "/get-started": wherever the demo-request form lives
- Devices: any
- Audience: all visitors who reach the form
- Display frequency: always
Primary metric: goal_completed_in_experience where experience_id = <this> (goal: form_submitted on the demo form within session of exposure)
Secondary metrics:
- form_submitted rate per variant (the headline number: drop-off per added field)
- Per-field abandonment rate (which field do visitors abandon at?)
- Lead quality downstream (SQL rate per variant (does the longer form give better-qualified leads?)) measured at deal_created or opportunity_created within 14 days
Guardrail: SQL rate must not drop more than the inverse of the conversion lift. Example: if Variant A has 25% conversion at 60% SQL rate, and Variant B has 18% conversion at 80% SQL rate, Variant B's net qualified-lead rate is similar: no guardrail violation. Document the tradeoff.
Schedule: 21 days, 500 form views per variant minimum
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (3 fields)
 HTML target selector: .demo-request-form
 Variant DOM:
 <form class="demo-form" id="demo-form" data-variant="control" data-field-count="3">
 <label>Name <input type="text" name="name" required /></label>
 <label>Work email <input type="email" name="email" required /></label>
 <label>Company <input type="text" name="company" required /></label>
 <button type="submit" class="form-submit-cta" id="demo-form-submit">Book a demo</button>
 </form>
Variant: B (5 fields)
 HTML target selector: .demo-request-form
 Variant DOM:
 <form class="demo-form" id="demo-form" data-variant="b" data-field-count="5">
 <label>Name <input type="text" name="name" required /></label>
 <label>Work email <input type="email" name="email" required /></label>
 <label>Company <input type="text" name="company" required /></label>
 <label>Job title <input type="text" name="job_title" required /></label>
 <label>Team size
 <select name="team_size" required>
 <option value="">Select...</option>
 <option value="1-10">1-10</option>
 <option value="11-50">11-50</option>
 <option value="51-200">51-200</option>
 <option value="201-1000">201-1000</option>
 <option value="1000+">1000+</option>
 </select>
 </label>
 <button type="submit" class="form-submit-cta" id="demo-form-submit">Book a demo</button>
 </form>
Variant: C (7 fields)
 HTML target selector: .demo-request-form
 Variant DOM:
 <form class="demo-form" id="demo-form" data-variant="c" data-field-count="7">
 [name, email, company, job title, team size: same as Variant B]
 <label>Phone (optional) <input type="tel" name="phone" /></label>
 <label>What are you hoping to achieve with [Brand]? <textarea name="use_case" rows="3" required></textarea></label>
 <button type="submit" class="form-submit-cta" id="demo-form-submit">Book a demo</button>
 </form>
The Visual Editor allows the user to adjust field labels, helper text, validation messages, and input styling. Ensure the form submission event (submit_on the form_id) fires consistently across all variants for measurement.
Taxonomy notes:
- This recipe assumes the workspace has a configurable demo-request form. The form's underlying handler (Hubspot, Marketo, custom) doesn't matter for the experiment: what changes is the visible field count.
- submit_on with the form's id captures form submissions; goal_completed_in_experience fires when this event occurs after exposure.
- The lead-quality-downstream measurement is the most important secondary signal. A 25% conversion at 50% SQL rate (3-field) vs. 18% at 80% SQL rate (7-field) might yield similar net pipeline. Don't ship the higher-conversion variant blindly without checking lead quality.
- Progressive profiling alternative: instead of adding all fields at once, the form could ask 3 fields first, then ask additional fields after submission. That's a separate test (out of scope for this recipe).
- Mobile note: shorter forms always win on mobile: consider mobile-only variant overrides.
