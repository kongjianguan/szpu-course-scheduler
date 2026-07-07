#!/usr/bin/env python3
import argparse
import os
import sys

from szpu.login import login, login_with_cookies
from szpu.course import get_course_schedule
from szpu.csv_writer import save_csv


def main():
    p = argparse.ArgumentParser(description="SZPU course schedule → CSV")
    p.add_argument("xh", help="student ID")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("-p", "--password", help="password (CAS login)")
    g.add_argument("--cookie", help="cookie string (skip login)")
    p.add_argument("--xn", required=True, help="academic year, e.g. 2025-2026")
    p.add_argument("--xq", type=int, required=True, choices=[1, 2, 3], help="semester: 1/2/3")
    p.add_argument("-o", "--output", help="output CSV path (default: stdout)")
    args = p.parse_args()

    session = login(args.xh, args.password) if args.password else login_with_cookies(args.cookie)
    slots = get_course_schedule(session, args.xh, args.xn, args.xq)

    if not slots:
        print("no schedule data found", file=sys.stderr)
        sys.exit(1)

    if args.output:
        save_csv(slots, args.output)
        print(f"saved: {os.path.abspath(args.output)}")
    else:
        from szpu.csv_writer import to_csv
        print(to_csv(slots), end="")


if __name__ == "__main__":
    main()
