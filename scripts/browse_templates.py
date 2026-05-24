#!/usr/bin/env python3
"""Browse beautiful-html-templates by occasion/mood/tone.

Usage:
  python3 browse_templates.py --occasion "tech sharing"
  python3 browse_templates.py --mood energetic
  python3 browse_templates.py --tone minimal
  python3 browse_templates.py --list-categories
  python3 browse_templates.py --all
"""

import json
import os
import sys
from pathlib import Path

# Path to the beautiful-html-templates
TEMPLATES_DIR = Path.home() / ".claude" / "skills" / "ppt-master"
# Fall back to PPT制作 assets
FALLBACK_DIRS = [
    Path("D:/桌面/PPT制作/assets/beautiful-html-templates"),
]

def find_templates_dir():
    """Find the templates directory."""
    for d in [TEMPLATES_DIR / ".." / ".." / ".." / "D:/桌面/PPT制作/assets/beautiful-html-templates",
              Path("D:/桌面/PPT制作/assets/beautiful-html-templates")]:
        resolved = d.resolve()
        if resolved.exists():
            return resolved
    return None

def load_all_templates(templates_dir):
    """Load template.json from each template directory."""
    templates = []
    for item in sorted(templates_dir.iterdir()):
        if item.is_dir():
            json_path = item / "template.json"
            if json_path.exists():
                try:
                    data = json.loads(json_path.read_text(encoding="utf-8"))
                    data["_path"] = str(item)
                    templates.append(data)
                except (json.JSONDecodeError, Exception) as e:
                    print(f"  [warn] {json_path}: {e}", file=sys.stderr)
    return templates

def list_categories(templates):
    """List all unique occasion categories."""
    occasions = set()
    moods = set()
    tones = set()
    for t in templates:
        for o in t.get("occasion", []):
            occasions.add(o)
        for m in t.get("mood", []):
            moods.add(m)
        for to in t.get("tone", []):
            tones.add(to)
    print("=== Occasion Categories ===")
    for o in sorted(occasions):
        print(f"  {o}")
    print(f"\n=== Mood Tags ===")
    for m in sorted(moods):
        print(f"  {m}")
    print(f"\n=== Tone Tags ===")
    for to in sorted(tones):
        print(f"  {to}")

def filter_templates(templates, field, query):
    """Filter templates by a field matching a query (case-insensitive)."""
    q = query.lower()
    results = []
    for t in templates:
        values = [v.lower() for v in t.get(field, [])]
        if any(q in v for v in values):
            results.append(t)
    return results

def display_templates(templates):
    """Display template listing."""
    if not templates:
        print("No matching templates found.")
        return
    print(f"Found {len(templates)} template(s):\n")
    print(f"{'Name':<25} {'Slides':<6} {'Scheme':<8} {'Best For'}")
    print("-" * 75)
    for t in templates:
        name = t.get("name", "?")
        slides = t.get("slide_count", "?")
        scheme = t.get("scheme", "?")
        best = t.get("tagline", "")[:50]
        print(f"{name:<25} {slides:<6} {scheme:<8} {best}")
    print()

def main():
    templates_dir = find_templates_dir()
    if not templates_dir:
        print("Error: beautiful-html-templates directory not found.", file=sys.stderr)
        print("Expected at: D:/桌面/PPT制作/assets/beautiful-html-templates/", file=sys.stderr)
        sys.exit(1)

    templates = load_all_templates(templates_dir)
    if not templates:
        print("Error: no template.json files found.", file=sys.stderr)
        sys.exit(1)

    if "--list-categories" in sys.argv:
        list_categories(templates)
        return

    if "--all" in sys.argv:
        display_templates(templates)
        return

    # Filter by provided flags
    results = templates[:]
    filters = [
        ("--occasion", "occasion"),
        ("--mood", "mood"),
        ("--tone", "tone"),
    ]
    has_filter = False
    for flag, field in filters:
        if flag in sys.argv:
            idx = sys.argv.index(flag) + 1
            if idx < len(sys.argv):
                query = sys.argv[idx]
                results = filter_templates(results, field, query)
                has_filter = True

    if not has_filter:
        print("Usage:")
        print("  browse_templates.py --occasion <query>")
        print("  browse_templates.py --mood <query>")
        print("  browse_templates.py --tone <query>")
        print("  browse_templates.py --list-categories")
        print("  browse_templates.py --all")
        return

    display_templates(results)

if __name__ == "__main__":
    main()
