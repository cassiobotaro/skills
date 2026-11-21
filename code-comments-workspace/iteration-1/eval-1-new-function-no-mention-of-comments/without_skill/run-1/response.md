I added `unique_slug(title, existing)` to `slugs/slugify.py`. It takes the slug from the existing `slugify`. If that slug is already in `existing`, it tries `-2`, `-3` and so on until it finds one that isn't.

I ran a quick check with the title "A b":
- With an empty set, it returns `a-b`.
- With `{"a-b"}`, it returns `a-b-2`.
- With `{"a-b", "a-b-2"}`, it returns `a-b-3`.

The function doesn't add the new slug to `existing`, so adding it is up to the caller. If the title slugifies to an empty string, the result is `""`, or `-2` if `""` is already taken.
