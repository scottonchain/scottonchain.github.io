#!/usr/bin/env python3
"""Read-only checks for the microcredit delivery tree; never build or publish."""
import argparse
import json
from pathlib import Path
from urllib.parse import unquote, urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def check(root, testbed=None):
    root = Path(root).resolve()
    errors = []
    for relative in ("pool/index.html", "listen/index.html", "listen/feed.xml", ".well-known/agent-card.json"):
        if not (root / relative).is_file():
            errors.append("Missing release file: " + relative)
    if errors:
        return errors
    card = json.loads((root / ".well-known/agent-card.json").read_text())
    if card.get("chain", {}).get("chainId") != 84532:
        errors.append("The published card must identify Base Sepolia")
    if testbed:
        source = Path(testbed) / "agent-card.json"
        if (root / ".well-known/agent-card.json").read_bytes() != source.read_bytes():
            errors.append("Published card differs from canonical testbed agent-card.json")
    feed = ET.parse(root / "listen/feed.xml")
    items = feed.findall("./channel/item")
    if not items:
        errors.append("Podcast feed has no published items")
    for item in items:
        enclosure = item.find("enclosure")
        if enclosure is None:
            errors.append("Podcast item has no enclosure")
            continue
        url = urlparse(enclosure.attrib.get("url", ""))
        if url.hostname == "scottonchain.github.io":
            artifact = (root / unquote(url.path).lstrip("/")).resolve()
            if not artifact.is_relative_to(root) or not artifact.is_file():
                errors.append("Missing podcast enclosure: " + url.path)
            elif str(artifact.stat().st_size) != enclosure.attrib.get("length"):
                errors.append("Podcast enclosure length differs: " + url.path)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--testbed", type=Path, help="optional local canonical testbed checkout")
    args = parser.parse_args()
    try:
        errors = check(ROOT, args.testbed)
    except (OSError, ValueError, ET.ParseError) as exc:
        parser.exit(1, f"Delivery check failed: {exc}\n")
    for error in errors:
        print("FAIL:", error)
    if errors:
        return 1
    print("PASS: delivery entrypoints, Base Sepolia card and podcast enclosure bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
