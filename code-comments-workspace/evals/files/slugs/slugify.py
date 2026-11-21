import re
import unicodedata


def slugify(title: str) -> str:
    """Lowercase ASCII slug of `title`; anything that is not a letter or digit becomes '-'.

    slugify("Olá, Mundo!") -> "ola-mundo"
    """
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_title.lower()).strip("-")
