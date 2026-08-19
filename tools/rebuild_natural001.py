#!/usr/bin/env python3
"""Retired entry point retained to prevent accidental destructive reruns."""


def main() -> int:
    raise SystemExit(
        "tools/rebuild_natural001.py is retired because it overwrote the combined "
        "source ledger and stale outcome metadata. Use "
        "tools/extract_natural001_time_safe.py followed by "
        "tools/finalize_natural_event_metadata.py."
    )


if __name__ == "__main__":
    main()
