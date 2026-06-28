#!/usr/bin/env python3
"""
The Hunt — Name Rater: share-link / file decoder.

Turns anything a voter sends back into readable JSON:
  - a "Send my ratings" link   (https://.../#r=G.xxxx  or file:///...#r=...)
  - a bare code                (G.xxxx  or  U.xxxx)
  - a downloaded .json file     (the backup, merged, or summary exports — already plain JSON)

Usage:
  python3 decode.py "<link, code, or path>"
  python3 decode.py            # then paste the link/code and press Enter

For Claude/Cowork: run this on any link the user pastes, then fold the
events into each name's `leans` in ../names.json (keyed by person, by id).
The link payload format is documented in README.md ("Payload format").
"""
import sys, re, base64, gzip, json, os

def decode(raw: str):
    raw = raw.strip().strip('"').strip("'")
    # 1) a path to an already-plain-JSON file (backup / merged / summary)
    if os.path.exists(raw):
        with open(raw, "r", encoding="utf-8") as f:
            return json.load(f)
    # 2) pull the code out of a link (#r=... or ?r=... or &r=...)
    m = re.search(r"[#?&]r=([^\s&]+)", raw)
    code = m.group(1) if m else raw
    # 3) split the "G." / "U." prefix
    if "." not in code:
        raise ValueError("Not a recognisable code, link, or file path.")
    mode, data = code.split(".", 1)
    # 4) base64url -> bytes (restore padding the app stripped)
    b = base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))
    # 5) gunzip if it was compressed
    if mode == "G":
        b = gzip.decompress(b)
    elif mode != "U":
        raise ValueError(f"Unknown payload prefix '{mode}.' (expected 'G.' or 'U.')")
    return json.loads(b.decode("utf-8"))

def main():
    raw = sys.argv[1] if len(sys.argv) > 1 else input("Paste link / code / file path:\n").strip()
    obj = decode(raw)
    print(json.dumps(obj, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
