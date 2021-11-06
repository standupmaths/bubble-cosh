# SPDX-License-Identifier: MIT
# Copyright (C) 2021 nfitzen

from bubble_cosh import a_b_finder


def test_a_b_finder():
    d = 1.068
    l = 0.5
    # Rounding to 5 digits. That's probably good enough.
    expected_a = 0.46519
    expected_b = 0.25
    a, b = a_b_finder(d, l)
    a = round(a, ndigits=5)
    b = round(b, ndigits=5)
    assert (a, b) == (expected_a, expected_b)


if __name__ == "__main__":
    try:
        import pytest

        pytest.main()
    except ImportError:
        print("You need to install pytest.")
