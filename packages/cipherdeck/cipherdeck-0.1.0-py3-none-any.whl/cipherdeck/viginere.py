# cipherdeck – utilities for simple text encryption
# Copyright (C) 2019  Jan "Khardix" Staněk <khardix@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""`Vigenère Cipher <https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher>`_"""

import logging
import operator
from itertools import chain
from itertools import cycle
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Iterator
from typing import Optional
from typing import TextIO

import click

from .alphabet import ANY as ALPHABET_MAP
from .alphabet import ENGLISH

#: Character shift operation
ShiftOp = Callable[[int, int], int]

#: Shift operation for traditional encryption
ENCRYPTION_SHIFT: ShiftOp = operator.add
#: Shift operation for traditional decryption
DECRYPTION_SHIFT: ShiftOp = operator.sub

#: Module logger
_LOG = logging.getLogger(__name__)


def transpose(
    shift: ShiftOp, key: str, intext: Iterable[str], *, alphabet: str = ENGLISH
) -> Iterator[str]:
    """Transpose a string using Viginère cipher.

    In Viginère cipher, encryption and decryption are the same character
    substitution made in opposite direction.
    This generator relies on the `shift` parameter
    to decide which direction it should be.
    Traditional encryption uses addition
    and traditional decryption uses subtraction.

    Arguments:
        shift: The operation used for calculating the transformed character.
        key: The key used for calculating the character offsets.
            Non-alphabetic characters in key are ignored (removed).
        intext: The text to be transformed.
            This is expected to be an iterator over single characters.
        alphabet: The alphabet the transformation should use.

    Yields:
        Character of the transformed text.
        Alphabetic characters are transformed,
        non-alphabetic are passed as they were.

    Raises:
        ValueError: Either key or intext contains alphabetic characters
            not present in the specified alphabet.
        ValueError: The iterator did not yield single-character string.
    """

    alphabet = alphabet.lower()
    offset = cycle(alphabet.index(c) for c in key.lower() if c.isalpha())

    for character in intext:
        if len(character) != 1:
            raise ValueError(f"Not a single character: {character}")

        if character.isalpha():
            uppercase = character.isupper()

            index = shift(alphabet.index(character.lower()), next(offset))
            index = index % len(alphabet)

            yield alphabet[index].upper() if uppercase else alphabet[index]

        else:
            yield character


def encrypted(
    key: str, plaintext: Iterable[str], *, alphabet: str = ENGLISH
) -> Iterator[str]:
    """Encrypts `plaintext` using Vigenère cipher with `key`.

    White space in key is ignored/thrown away.
    Non-letter characters are preserved without encryption.

    Yields: Character of encrypted text. See `transpose()` for details.

    Raises: The same errors as `transpose()`.
    """

    return transpose(ENCRYPTION_SHIFT, key, plaintext, alphabet=alphabet)


def decrypted(
    key: str, ciphertext: Iterable[str], *, alphabet: str = ENGLISH
) -> Iterator[str]:
    """Decrypts `ciphertext` using Vigenère cipher with `key`.

    White space in key is ignored/thrown away.
    Non-letter characters are preserved without decryption.

    Yields: Character of decrypted text. See `transpose()` for details.

    Raises: The same errors as `transpose()`.
    """

    return transpose(DECRYPTION_SHIFT, key, ciphertext, alphabet=alphabet)


# CLI interface to this module


def _select_direction(
    _ctx: click.Context, _param: Any, encrypt: Optional[bool]
) -> bool:
    """Warn if used did not explicitly selected a transposition direction."""

    warning = "No direction (encryption or decryption) selected; using encryption."

    if encrypt is None:
        _LOG.warning(warning)
        return True
    else:
        return encrypt


@click.command(name="viginère")
@click.option(
    "-e/-d",
    "--encrypt/--decrypt",
    default=None,
    callback=_select_direction,
    help=(
        "Select encryption or decryption."
        " If omitted, emit a warning and select encryption."
    ),
)
@click.option(
    "-k",
    "--key",
    required=True,
    help="Specify the encryption key phrase. Non-alphabetic characters are ignored.",
)
@click.option(
    "--alphabet",
    "language",
    metavar="LANGUAGE",
    type=click.Choice(ALPHABET_MAP.keys()),
    default="english",
    help="Use alphabet of LANGUAGE for the operation.",
)
@click.option(
    "-i",
    "--input",
    "in_file",
    type=click.File(mode="r"),
    default="-",
    help="Read input from FILE. If omitted or specified as '-', use standard input.",
)
@click.option(
    "-o",
    "--output",
    "out_file",
    type=click.File(mode="w"),
    default="-",
    help="Write output to FILE. If omitted or specified as '-', use standard output.",
)
def cli(
    encrypt: Optional[bool], key: str, language: str, in_file: TextIO, out_file: TextIO
) -> None:
    """Encrypt or decrypt text using the Viginère cipher"""

    shift = ENCRYPTION_SHIFT if encrypt else DECRYPTION_SHIFT
    alphabet = ALPHABET_MAP[language]

    character_iter = chain.from_iterable(iter(line) for line in in_file)
    for character in transpose(shift, key, character_iter, alphabet=alphabet):
        out_file.write(character)  # Let buffering up to underlying implementation


if __name__ == "__main__":
    cli.main(prog_name=".".join((__package__, "viginere")))
