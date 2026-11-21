I added `unique_slug(title, existing)` to `slugs/slugify.py`. I ran it on three inputs. With nothing taken it returned `a-b`. With `a-b` taken it returned `a-b-2`. With `a-b` and `a-b-2` taken it returned `a-b-3`.

It builds the slug with `slugify(title)`. If that slug is in `existing`, it tries `-2`, `-3` and so on until one is free. It doesn't add the result to `existing`, so you need to do that yourself.

I gave it a docstring in the same style as `slugify`'s. It says `existing` is left unmodified, that the first suffix is `-2`, and it includes one example. I added no other comments.

A title that slugifies to an empty string, such as `"!!!"`, gives `""`. If `""` is already in `existing`, you get `"-2"`. I didn't special-case this because you didn't specify it.
