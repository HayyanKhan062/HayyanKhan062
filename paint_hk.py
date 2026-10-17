#!/usr/bin/env python3
"""
HK pixel-art painter for the GitHub contribution graph.

PEHLE PARH LO — ye script kya karti hai:
- Ye PAST dates pe EMPTY commits banati hai taake contribution grid pe
  "HK" ka pixel design nazar aaye.
- Ye sirf decorative art hai. Commits khaali hain, koi code change nahi.
- Script APNE PC pe chalani hai, is repo (HayyanKhan062) ke clone ke andar.
- Commits tumhari GitHub wali email se hone chahiye, warna grid pe count nahi honge.

USAGE (Arch Linux terminal):
  1. git clone https://github.com/HayyanKhan062/HayyanKhan062.git
  2. cd HayyanKhan062
  3. git config user.email "hayyan6776@gmail.com"   # GitHub wali email
     git config user.name "HayyanKhan062"
  4. python3 paint_hk.py
  5. git push origin main
"""

import os
import subprocess
import sys
from datetime import date, timedelta

BRANCH = "main"

# "HK" — 7 rows (Sunday..Saturday) x 11 columns
ART = [
    "10001010001",
    "10001010010",
    "10001010100",
    "11111011000",
    "10001010100",
    "10001010010",
    "10001010001",
]


def run(cmd, env=None):
    subprocess.run(cmd, env=env, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    # preview
    print("Design preview (HK):\n")
    for row in ART:
        print("".join("##" if c == "1" else "  " for c in row))
    print()

    # git repo check
    try:
        run(["git", "rev-parse", "--git-dir"])
    except Exception:
        sys.exit("ERROR: ye git repo nahi lag rahi. Pehle repo clone karke uske andar chalao.")

    email = subprocess.run(["git", "config", "user.email"],
                           capture_output=True, text=True).stdout.strip()
    if not email:
        sys.exit("ERROR: git user.email set nahi. Pehle:\n"
                 '  git config user.email "tumhari-github-wali-email"')
    print(f"Commits is email se honge: {email}")
    print("NOTE: ye email tumhare GitHub account se linked honi chahiye,\n"
          "warna commits grid pe count nahi honge.\n")

    # date math: GitHub grid ke columns Sunday se shuru hote hain.
    # Art ka sab se right column pichle mukammal hafte pe rakhein ge.
    today = date.today()
    days_since_sunday = (today.weekday() + 1) % 7
    last_sunday = today - timedelta(days=days_since_sunday)
    n_cols = len(ART[0])
    start_sunday = last_sunday - timedelta(weeks=n_cols - 1)

    targets = []
    for col in range(n_cols):
        for row in range(7):
            if ART[row][col] == "1":
                targets.append(start_sunday + timedelta(weeks=col, days=row))

    print(f"Total {len(targets)} empty commits banenge "
          f"({start_sunday} se {start_sunday + timedelta(weeks=n_cols - 1) + timedelta(days=6)} tak).")
    if os.environ.get("PIXEL_AUTO", "").lower() != "y":
        ok = input("Continue? (y/n): ").strip().lower()
        if ok != "y":
            print("Cancelled.")
            return
    else:
        print("PIXEL_AUTO=y — proceeding non-interactively.")

    for d in targets:
        stamp = d.strftime("%Y-%m-%dT12:00:00")
        env = dict(os.environ)
        env["GIT_AUTHOR_DATE"] = stamp
        env["GIT_COMMITTER_DATE"] = stamp
        run(["git", "commit", "--allow-empty", "-m", f"pixel {d.isoformat()}"],
            env=env)

    print(f"\nHo gaya. Ab push karo:\n  git push origin {BRANCH}")
    print("Push ke baad profile pe HK nazar aayega (kuch minute lag sakte hain).")


if __name__ == "__main__":
    main()
