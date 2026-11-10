---
frontmatter_id: cart-abandoned-push
slash_command: /cart-abandoned-push
description: Visitors active again this week who first showed up months ago, welcomed back by email with a heads-up to the lifecycle team.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
---

# Long-Tenure Returning Visitors

Slash command: /cart-abandoned-push

## Step 1: Build the long-tenure returning visitor list

Build a segment of users named "Long-Tenure Returning Visitors". A user is in the segment only when all of these are true: triggered "Session start" at least once in the last 7 days; triggered "Session start" at least once between 60 and 90 days ago.

## Step 2: Send a welcome-back email

Generate a designed marketing email for the users in "Long-Tenure Returning Visitors" welcoming them back and pointing to what is new in the product since they last visited regularly. Three sentences, warm tone, no discount language, one button linking to the product. Use the result of "Build the long-tenure returning visitor list".

## Step 3: Notify the lifecycle team

Generate a Slack message to the lifecycle team channel. Say how many users are in "Long-Tenure Returning Visitors" right now, so the team knows a batch of long-time users is active again. Use the result of "Build the long-tenure returning visitor list".
