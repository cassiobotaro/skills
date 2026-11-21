I added `unique_slug(title, existing)` to `slugs/slugify.py`. It returns `slugify(title)` if that slug isn't in `existing`. Otherwise it tries `-2`, `-3` and so on until it finds a free one. It doesn't modify `existing`, so the caller has to add the returned slug to the set.

I ran three quick checks, and all three gave the expected result:
- `unique_slug("A", {"a", "a-2"})` returns `a-3`.
- `unique_slug("A", set())` returns `a`.
- `unique_slug("!!", {""})` returns `-2`.

A title with no letters or digits slugifies to `""`. If `""` is already taken, the function returns `-2`, a slug with a leading dash. I left that as it is, because the request didn't say what should happen then. If you'd rather reject empty slugs or use a fallback such as `"untitled"`, tell me which.

The docstring follows the style of `slugify`. It records the numeric suffix starting at 2, that `existing` isn't modified, and the empty-slug case. I added no other comments.
