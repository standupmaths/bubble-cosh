#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (C) 2020-2021 standupmaths and the bubble-cosh contributors

# The type hints use syntax from Python 3.9+. See also PEP 585 -N
from __future__ import annotations

from math import pi, cosh, sinh
import argparse

inf = float("inf")  # IEEE 754 is cool. -N


def error_get(a: float, b: float, d: float, l: float) -> float:
    """Gets the total error from both endpoints."""
    # I've worked this out from the end conditions
    try:
        x1 = 0
        y1 = d / 2
        e1 = a * cosh((x1 - b) / a) - y1
        x2 = l
        y2 = d / 2
        e2 = a * cosh((x2 - b) / a) - y2
        error = abs(e1) + abs(e2)
        return error
    except Exception:
        return inf


def a_b_finder(
               d: float,
               l: float,
               prec: float = 1e-7,
               starting_step: float = 0.1,
               start_a: float = 1.0,
               start_b: float = 1.0,
               ) -> tuple[float, float]:
    """Finds a and b. All arguments in centimetres."""
    d = float(d)
    l = float(l)
    # takes the diameter of the hoop and distance apart to give a and b
    step = starting_step
    error = inf

    a = start_a
    b = start_b
    # print([a,b])
    while error > prec:
        best_error = error
        new_best_a = a
        new_best_b = b
        while True:
            old_error = best_error
            a_s = (a - step, a, a + step)
            b_s = (b - step, b, b + step)
            for disa in a_s:
                for disb in b_s:
                    dis_error = error_get(disa, disb, d, l)
                    # print("a:{0} b:{1} e:{2}".format(disa,disb,dis_error,best_error))
                    if dis_error < best_error:
                        # print("best")
                        best_error = dis_error
                        new_best_a = disa
                        new_best_b = disb
            if best_error == old_error:  # then there was no improvement
                break
            else:
                a = new_best_a
                b = new_best_b
        error = best_error
        step /= 10.0
        if step < prec:
            # print(error)
            error = 0
        # print("STEP CHANGE: {0}".format(step))
    # print(error)
    # return best_error
    return (a, b)


def total_area(a, b, d, l):
    return pi * (a ** 2) * (sinh(l / a) + (l / a))


def main():
    # This is messy since it's internal behavior. argparse really should have
    # a union operator of some sort. -N
    custom_format = lambda prog: argparse.ArgumentDefaultsHelpFormatter(prog, width=72)

    parser = argparse.ArgumentParser(
        description="""\
        Calculate the parameters of the curve of a bubble between two rings.
        Takes the form y=a*cosh((x-b)/a).""",
        epilog="See <https://youtu.be/31Om4VrSzb8> for more information.",
        formatter_class=custom_format,
    )
    default_d = 1.068
    default_l = 0.6
    parser.add_argument(
        "diameter",
        metavar="d",
        nargs="?",
        type=float,
        default=default_d,
        help="The diameter of the two hoops.",
    )
    parser.add_argument(
        "length",
        metavar="l",
        nargs="?",
        type=float,
        default=default_l,
        help="The length between the two hoops.",
    )
    args = parser.parse_args()
    d = args.diameter
    l = args.length
    a, b = a_b_finder(d, l)
    print("for diameters of {0} and length of {1}".format(d, l))
    print([a, b])

    mid_radius = a * cosh(((l / 2) - b) / a)

    print("Area of {0}".format(total_area(a, b, d, l)))
    print("mid dip of {0}".format((d / 2) - mid_radius))
    print("mid gap of {0}".format(mid_radius * 2))
    """

    # saving out errors only
    # need to change a_b_finder to return best_error
    d = 1.0
    l=0.01
    while l <= d:
        e = a_b_finder(d,l)
        print("{0}\t{1}".format(l,e))
        l += 0.01

    """


if __name__ == "__main__":
    main()
