import re
import unicodedata


def slugify(title: str) -> str:
    """Lowercase ASCII slug of `title`; anything that is not a letter or digit becomes '-'.

    slugify("Olá, Mundo!") -> "ola-mundo"
    """
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_title.lower()).strip("-")


def unique_slug(title: str, existing: set[str]) -> str:
    """Slug of `title` that is not in `existing`, appending -2, -3, ... if needed.

    unique_slug("Olá, Mundo!", {"ola-mundo"}) -> "ola-mundo-2"
    """
    base = slugify(title)
    slug = base
    n = 2
    while slug in existing:
        slug = f"{base}-{n}"
        n += 1
    return slug
