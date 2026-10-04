# Messaging: SMS, push and Slack

| `builds` | What it makes | Install now |
|---|---|---|
| `sms` | an SMS text message | yes |
| `push` | a push notification | yes |
| `slack` | a Slack message | yes |

## What the builders make

The message content, saved in the installer's project. Like an email, building it is not sending
it: delivery on a trigger or a schedule is a journey or a workflow, both Coming soon
([../../NO-ENTITY-EXISTS.md](../no-entity-exists.md)). A recipe whose next step posts the message
somewhere is waiting on that builder, and its `builds` says so.

## A good description names

- who or what it is about, by an earlier step's title when it uses one, with `dependsOn`;
- the length limit: characters for SMS, a title and a body line for push;
- what it must contain, field by field;
- the tone;
- for Slack, what the message is for, not where it goes: the channel is the installer's.

## Good, from `recipes/intempt/`

No recipe in this repository is Install now with a messaging step yet. This Slack step is lint-clean.
`demo-request-fast-path` step 2 (Coming soon):

```
Generate Slack alert content for the #demo-requests channel. Include: requester name, account name,
employee count, industry, deal-size estimate (if available), prior touch history (last engagement,
ICP fit score), and a direct link to the user record. Tone: terse, scannable: this is a triage card,
not a marketing message. Use the result of "Find recent demo requests".
```

It names every field and the tone. What it gets wrong is `#demo-requests`: a channel that exists in
one workspace. Make the channel an `inputs` row and say "the channel chosen for this run".

No recipe in this repository builds `push`.

## Bad, from `recipes/intempt/`

`booking-confirmation-flow` step 2 (Coming soon), the only `sms` step. The lint reports a bracket
placeholder:

```
Generate a 2-hour-before SMS reminder. Format: under 160 chars. Include meeting time, conferencing
link (shortened), and a reply-RESCHEDULE option. Example: 'Reminder: your call with [Host Name]
starts in 2 hours. Join: [link]. Reply RESCHEDULE to move it.' Only fires if user has SMS opt-in.
```

`[Host Name]` and `[link]` point at nothing, and "only fires if user has SMS opt-in" describes a
send condition, which is a journey's job, not the message's.

## What belongs in `inputs`

- the Slack channel;
- a short link domain or a sender id, when the recipe should not choose one;
- the phone number or app the installer sends from, if the copy has to name it.

## Common lint failures

| Lint | Seen as | Fix |
|---|---|---|
| bracket placeholder | `[Host Name]`; a lowercase `[link]` is not caught and is just as vague | write the value, or make it an `inputs` row |
| over 1200 chars | one step writing every variant of an alert | one message per step |

A send condition ("only when", "at 2am", "after they opt in") inside a message step is a sign the
recipe needs a journey or a workflow step after it.
