# Submitting a recipe

## Two routes, one review queue

Whichever way you built the recipe, it is submitted the same two ways, and you pick:

| Route | How |
|---|---|
| **The form** | Upload your `recipe.md` at [intempt.com/recipes/submit](https://intempt.com/recipes/submit) |
| **From the session** | `intempt recipe submit <recipe.md>`, which the agent runs for you if you ask |

Both send to the same API, `https://intempt.com/recipes/api/submit`, and reach the same queue. The
agent is required to offer you both. You are never required to use the second.

The public guide is at [intempt.com/recipes/submission-guide](https://intempt.com/recipes/submission-guide).

## Before either route

1. Validate it. See [VALIDATION.md](./VALIDATION.md).
2. **Read it end to end.** You are the last reviewer before it goes out. Nobody runs your recipe as
   part of review: review reads the file, so the runs you did while writing it are the only runs it
   gets before somebody installs it.

## Sending it from the session

```
intempt recipe submit my-handle/my-recipe/recipe.md --name "Your Name" --email you@company.com
```

Without `--yes`, nothing is sent. The command validates the file and prints a preview: the recipe's
id, title, owner, steps, availability and checksum, your creator details, and the consent text. It
also prints a **confirm token**, a random single-use value stored on your machine in
`~/.local/state/intempt-recipe-author/`. The token is not computed from the request, so nothing that
only controls the request can produce one.

To send, run the command the preview prints:

```
intempt recipe submit my-handle/my-recipe/recipe.md --name "Your Name" --email you@company.com \
  --yes <token> --rights-confirmed
```

It refuses if the token is not the one from the latest preview, if the file or your details changed
after the preview, or without `--rights-confirmed`. A refused send means preview again.

The agent never sends without your explicit yes in the conversation, and never builds the request
itself.

## What a submission carries

- The `recipe.md` file, exactly as previewed.
- Your name and work email, so a person can reach you about your recipe. Optionally your company,
  byline, LinkedIn URL and avatar URL.
- Your agreement to the consent text below, and its version.

Your email is never written into the repository.

## What you get back

A **submission id**. The CLI prints it and saves a receipt beside the confirm token. Keep it: it is
how anyone finds your submission.

## What happens next

- **A person reviews it.** Somya Nayak, Marketing lead at Intempt, reviews submissions. The first
  response comes within two business days during early access. A response is not always a verdict;
  a review that needs a conversation starts inside two days.
- **Submitting is not publishing.** Not every submission is published, and overlapping a recipe
  that already exists is not a reason to turn one down.
- **There is no self-service withdrawal.** No command or button pulls a submission back. To withdraw
  one, ask Somya and it is handled by hand.
- **No status notifications yet.** If a review needs changes, that reaches you from a person.
- Questions about what the engine can build go to the Intempt engine team, through Somya.

## Resubmitting

Run the preview again: a confirm token is minted per preview and the send will not take an old one.
If your first submission is still in review, tell Somya you are sending a corrected version, so the
two are not reviewed as separate recipes.

## Where a published recipe lives

```
recipes/<author>/<recipe-id>/recipe.md
```

In the public [intempt/recipe-creator](https://github.com/intempt/recipe-creator) repository. That
folder is written only when a submission is approved. You do not open a pull request and you do not
create the folder; the publisher writes it.

## Consent

Every submission, by either route, agrees to this text, version `intempt-recipes-v1`:

> Intempt may review your recipe and, if it meets the bar, publish it with your attribution in the
> Intempt Collective Marketplace and in the public intempt/recipe-creator repository; may edit it for
> clarity and to run on the Intempt engine while the substance stays yours; your attribution and
> content may persist in git history after removal.

## Licence

The terms that apply to this repository are in [LICENSE](./LICENSE). They are under review as the
repository becomes public. Partner revenue share, where it applies, is a separate written agreement;
see [intempt.com/partner](https://intempt.com/partner#build) and the Intempt Collective Terms.
