# Existing recipe

For when you already have a `recipe.md` and want it checked and submitted. No sign-in.

## A v2 recipe

It has `steps:` at the top level of its frontmatter.

1. Put it at `<your-handle>/<recipe-id>/recipe.md`. The validator checks that the folder equals the
   `id` and the parent folder equals `owner`.
2. Validate it:

   ```
   intempt recipe validate <your-handle>/<recipe-id>/recipe.md --json
   ```

3. Fix every contract problem. Treat every lint on an Install now recipe as a defect.
4. If it has no `touches` block, add one. See
   [../references/recipe-contract.md](../references/recipe-contract.md).
5. Read it end to end, then submit. See [../SUBMITTING.md](../SUBMITTING.md).

Only the formatting is fixed on this route. The logic is yours, and the agent does not rewrite
your steps to clear a warning without asking.

## A v1 recipe

It has an `intempt:` block with `procedure:` steps. Convert it first:

```
python3 scripts/migrate_v2.py --file old_recipe.md --dst . --owner <your-handle>
```

That writes `<your-handle>/<recipe-id>/recipe.md`. The converter keeps your wording, so the step
descriptions still need the pass in [../WRITING-STEPS.md](../WRITING-STEPS.md), and it does not
write `touches`, which the validator requires. Then continue with the v2 steps above.
