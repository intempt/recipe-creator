---
frontmatter_id: smb-accounts
slash_command: /smb-accounts
description: Companies under 100 employees, the list your self-serve nurture and in-product prompts should run against.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Builds a reusable list of small business accounts with fewer than 100 employees for self-serve nurture and in-product
    prompts to target.
  parameters:
  - name: employee_threshold
    type: number
    label: Maximum employee count (exclusive)
    default: 100
    required: false
  requirements:
  - slot: employee_count
    kind: attribute
    meaning: The number of employees at an account
  steps:
  - id: s1
    builds: segment
    uses:
    - employee_count
    - employee_threshold
    instruction: Build a segment named "SMB Accounts" containing accounts where {employee_count} is less than {employee_threshold}.
---

# Small business accounts

Slash command: /smb-accounts

## Step 1: Build the SMB list

Build a segment of accounts named "SMB Accounts".
An account is in the segment only when all of these are true:
- its employees attribute is less than 100
