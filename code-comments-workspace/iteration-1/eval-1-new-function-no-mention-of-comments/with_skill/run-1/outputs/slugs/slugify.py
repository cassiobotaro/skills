import re
import unicodedata


def slugify(title: str) -> str:
    """Lowercase ASCII slug of `title`; anything that is not a letter or digit becomes '-'.

    slugify("Olá, Mundo!") -> "ola-mundo"
    """
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_title.lower()).strip("-")


def unique_slug(title: str, existing: set[str]) -> str:
    """Slug of `title` that is not in `existing`, which is left unmodified.

    A taken slug gets the first free suffix starting at -2; the unsuffixed slug is never "-1".

    unique_slug("Olá, Mundo!", {"ola-mundo", "ola-mundo-2"}) -> "ola-mundo-3"
    """
    base = slugify(title)
    slug = base
    suffix = 2
    while slug in existing:
        slug = f"{base}-{suffix}"
        suffix += 1
    return slug
