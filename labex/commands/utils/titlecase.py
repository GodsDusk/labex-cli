"""AP Style title-casing.
"""

import re


LOWER_TITLE = [
    "a",
    "an",
    "and",
    "as",
    "at",
    "but",
    "by",
    "en",
    "for",
    "from",
    "if",
    "in",
    "nor",
    "of",
    "on",
    "or",
    "per",
    "the",
    "to",
    "v",
    "vs",
    "via",
    "with",
]

DO_NOT_TITLE = [
    "JSON",
    "GitHub",
    "IPython"
]


def title_word(chunk):
    """Title-case a given word (or do noting to a non-word chunk)."""
    if chunk.lower() in LOWER_TITLE:
        return chunk.lower()
    if chunk in DO_NOT_TITLE:
        return chunk
    return chunk[0].upper() + chunk[1:].lower()


def titlecase(value):
    words_and_nonword_chunks = re.split(
        r"""
        (                   # capture both words and the chunks between words
            (?:             # split on consecutive:
                \s |        # - whitespace characters
                -  |        # - dashes
                "  |        # - double quotes
                [\[({<]     # - opening brackets and braces
            )+
        )
    """,
        value,
        flags=re.VERBOSE,
    )
    return "".join(
        # upper/lower-casing symbols and whitespace does nothing
        title_word(chunk)
        for chunk in words_and_nonword_chunks
    )
