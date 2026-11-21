import re
import unicodedata


def slugify(title: str) -> str:
    """Lowercase ASCII slug of `title`; anything that is not a letter or digit becomes '-'.

    slugify("Olá, Mundo!") -> "ola-mundo"
    """
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_title.lower()).strip("-")


def unique_slug(title: str, existing: set[str]) -> str:
    """Slug of `title` that is not in `existing`; `existing` is not modified.

    Taken slugs get a numeric suffix starting at 2: with {"a", "a-2"}, "A" -> "a-3".
    A title with no letters or digits has slug "", which is treated like any other.
    """
    base = slugify(title)
    slug = base
    n = 2
    while slug in existing:
        slug = f"{base}-{n}"
        n += 1
    return slug
