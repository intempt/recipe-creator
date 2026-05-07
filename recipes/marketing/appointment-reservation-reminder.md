---
name: Appointment Reservation Reminder
description: Multi-touch reminder for booked appointments, reservations, or service bookings — reduces no-shows with 48hr,
  24hr, and day-of confirmations. Works for retail services, beauty, dining, healthcare.
intempt:
  id: appointment-reservation-reminder
  version: 1.0.0
  slashCommand: /appointment-reservation-reminder
  shortDescription: Multi-touch reminder for booked appointments, reservations, or service bookings — reduces no-shows with
    48hr, 24hr, and day-of confirmations. Works for retail services, beauty, dining, healthcare.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: journey-builder
    mode:
    - ecommerce
    complexity: standard
    executionMode: live
    tags:
    - appointment
    - appointments-and-bookings
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: build-content
    describe: 'Generate alert email and SMS content templates for: back-in-stock, price-drop, birthday gift, and wishlist-on-sale.
      (Tailored for: Appointment / reservation reminder.)'
    produces: content
  - id: build-journey
    describe: 'Build event-triggered journeys firing on product_back_in_stock, product_price_decreased, and user_birthday
      events. (Tailored for: Appointment / reservation reminder.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking alert send volume, click-through rate, and conversion rate by alert type. (Tailored
      for: Appointment / reservation reminder.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: calendly
      severity: blocking
---

# Appointment Reservation Reminder

Multi-touch reminder for booked appointments, reservations, or service bookings — reduces no-shows with 48hr, 24hr, and day-of confirmations. Works for retail services, beauty, dining, healthcare.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate alert email and SMS content templates for: back-in-stock, price-drop, birthday gift, and wishlist-on-sale. (Tailored for: Appointment / reservation reminder.)
2. Build event-triggered journeys firing on product_back_in_stock, product_price_decreased, and user_birthday events. (Tailored for: Appointment / reservation reminder.)
3. Compose a dashboard tracking alert send volume, click-through rate, and conversion rate by alert type. (Tailored for: Appointment / reservation reminder.)

## Prerequisites

- Integration: **calendly** (blocking)
