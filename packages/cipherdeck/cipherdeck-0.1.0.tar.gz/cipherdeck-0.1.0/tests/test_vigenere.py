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

"""Viginere cipher tests"""

import pytest

from cipherdeck import alphabet
from cipherdeck import viginere

# Examples from wikipedia
with_english_texts = pytest.mark.parametrize(
    "key,plaintext,ciphertext",
    [
        ("LEMON", "ATTACKATDAWN", "LXFOPVEFRNHR"),
        (
            "abcd",
            "CRYPTO is short for CRYPTOgraphy",
            "CSASTP kv siqut gqu CSASTPiuaqjb",
        ),
    ],
)


@with_english_texts
def test_transpose_encrypts_as_expected(
    key: str, plaintext: str, ciphertext: str
) -> None:
    """Transpose function encrypts text as expected."""

    transposed = viginere.transpose(viginere.ENCRYPTION_SHIFT, key, plaintext)
    assert ciphertext == "".join(transposed)


@with_english_texts
def test_transpose_decrypts_as_expected(
    key: str, plaintext: str, ciphertext: str
) -> None:
    """Transpose function decrypts text as expected."""

    transposed = viginere.transpose(viginere.DECRYPTION_SHIFT, key, ciphertext)
    assert plaintext == "".join(transposed)


def test_transpose_raises_on_unexpected_character() -> None:
    """Transpose raises a ValueError when an unexpected character is encountered."""

    unexpected_in_english = "Ž"
    # expectations check
    assert unexpected_in_english.isalpha()
    assert unexpected_in_english not in alphabet.ENGLISH

    with pytest.raises(ValueError):
        "".join(
            viginere.transpose(viginere.ENCRYPTION_SHIFT, "a", unexpected_in_english)
        )


def test_transpose_raises_on_long_strin() -> None:
    """Transpose raises a ValueError when the intext yields multi-character strings."""

    intext = ["Hello, World"]

    with pytest.raises(ValueError):
        "".join(viginere.transpose(viginere.ENCRYPTION_SHIFT, "a", intext))


@with_english_texts
def test_encrypt_encrypts_as_expected(
    key: str, plaintext: str, ciphertext: str
) -> None:
    """Encrypted function encrypts text as expected."""

    assert ciphertext == "".join(viginere.encrypted(key=key, plaintext=plaintext))


@with_english_texts
def test_decrypt_decrypts_as_expected(
    key: str, plaintext: str, ciphertext: str
) -> None:
    """Decrypted function decrypts text as expected."""

    assert plaintext == "".join(viginere.decrypted(key=key, ciphertext=ciphertext))


@with_english_texts
def test_roundtrip(key: str, plaintext: str, ciphertext: str) -> None:
    """Encryption is inverse to decryption and vice versa."""

    encrypted = viginere.encrypted(key=key, plaintext=plaintext)
    decrypted = list(viginere.decrypted(key=key, ciphertext=encrypted))
    assert plaintext == "".join(decrypted)
