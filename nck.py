#!/usr/bin/env python3
"""Unlock-code generator for the Alcatel LINKHUB HH71VM.

Usage:  nck.py <IMEI> [<IMEI> ...]

Derives all seven facility codes from the IMEI alone. No dongle, no database,
no key material.
"""

import hashlib
import sys

# Per-facility constant pair, placed between the three BCD copies of the IMEI.
# "T6" is a seventh facility the vendor GUI never displays; its meaning is unknown.
FACILITIES = (
    ("NCK",   0xC0, 0xCD),
    ("NSCK",  0x52, 0xC7),
    ("SPCK",  0x80, 0x44),
    ("SIM",   0xFD, 0xBE),
    ("C",     0x43, 0x7B),
    ("Other", 0x6D, 0x38),
    ("T6",    0x90, 0x90),
)


def codes(imei):
    """Return [(facility, 10-digit code, 6-digit control value), ...]."""
    digits = "".join(ch for ch in imei if ch.isdigit())
    if len(digits) != 15:
        raise ValueError("IMEI must be 15 digits, got %d" % len(digits))

    bcd = bytes.fromhex("0" + digits)          # 16 nibbles -> 8 bytes

    out = []
    for name, tag1, tag2 in FACILITIES:
        msg = (bcd + bytes((tag1, 0, 0, 0))
             + bcd + bytes((tag2, 0, 0, 0))
             + bcd)                            # 32 bytes
        digest = hashlib.sha1(msg).digest()
        s = "".join(str(((b >> 4) ^ (b & 0x0F)) % 10) for b in digest[:16])
        out.append((name, s[:10], s[10:]))
    return out


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip())
        return 2
    rc = 0
    for imei in argv[1:]:
        print(imei)
        try:
            result = codes(imei)
        except ValueError as exc:
            print("  error: %s" % exc)
            rc = 1
            continue
        for name, code, ctrl in result:
            print("  %-6s %s (%s)" % (name + ":", code, ctrl))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
