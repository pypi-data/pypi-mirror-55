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

import pytest

from cipherdeck import alphabet


@pytest.mark.parametrize("name,expected", list(alphabet.ANY.items()))
def test_alphabet_is_accessible_directly(name: str, expected: str) -> None:
    """A named alphabet is also directly accessible as module attribute."""

    assert getattr(alphabet, name.upper()) == expected
