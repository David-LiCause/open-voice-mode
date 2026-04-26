#!/usr/bin/env python3
"""Verify an iCloud Shortcut link is valid and matches expected metadata.

Usage: check_link.py <icloud-shortcut-url> <expected-name>
Exits 0 on pass, 1 on fail.
"""
import json
import sys
import urllib.error
import urllib.request


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: check_link.py <icloud-shortcut-url> <expected-name>", file=sys.stderr)
        return 2

    url, expected_name = sys.argv[1], sys.argv[2]
    record_id = url.rstrip("/").rsplit("/", 1)[-1]
    api = f"https://www.icloud.com/shortcuts/api/records/{record_id}"

    try:
        with urllib.request.urlopen(api, timeout=10) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"FAIL  {expected_name}  HTTP {e.code} from {api}")
        return 1
    except Exception as e:
        print(f"FAIL  {expected_name}  fetch error: {e}")
        return 1

    errors = []
    if data.get("recordType") != "SharedShortcut":
        errors.append(f"recordType={data.get('recordType')!r} (expected 'SharedShortcut')")
    if data.get("deleted"):
        errors.append("shortcut is marked deleted")
    name = data.get("fields", {}).get("name", {}).get("value")
    if name != expected_name:
        errors.append(f"name={name!r} (expected {expected_name!r})")
    sig = data.get("fields", {}).get("signingStatus", {}).get("value")
    if sig is not None and sig != "APPROVED":
        errors.append(f"signingStatus={sig!r} (expected 'APPROVED')")

    if errors:
        print(f"FAIL  {expected_name}")
        for e in errors:
            print(f"      - {e}")
        return 1

    print(f"OK    {expected_name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
