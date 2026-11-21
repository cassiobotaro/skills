I added `unique_slug(title, existing)` to `slugs/slugify.py`. It returns `slugify(title)` if that slug isn't in `existing`. Otherwise it tries `-2`, `-3` and so on until it finds a free one.

I ran it by hand on three inputs. With an empty set it gave `a-b`. With `{"a-b"}` it gave `a-b-2`. With `{"a-b", "a-b-2"}` it gave `a-b-3`. I didn't add a test file.

The function doesn't modify `existing`, so add the returned slug to the set yourself if you're generating several in a row.

If `title` has no letters or digits, the base slug is empty. The function then returns `""`, or `-2`, `-3` and so on if `""` is already in `existing`.
