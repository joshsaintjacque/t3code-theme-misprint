"""Fill source/site_template.html from misprint.json -> index.html (palette rows come straight from the theme)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://joshsaintjacque.github.io/t3code-theme-misprint/"
REPO = "https://github.com/joshsaintjacque/t3code-theme-misprint"
t = json.load(open(os.path.join(HERE, "..", "misprint.json")))
c = t["colors"]
ROWS = [("canvas", "Cream stock", "Chat canvas"), ("sidebar", "Sidebar", "Slightly deeper stock"), ("surface", "Composer paper", "Raised surfaces"),
        ("text", "Overprint ink", "Text: pink x teal, pushed to black"), ("textMuted", "Muted ink", "Secondary text"),
        ("accent", "Fluoro pink", "Ink 1: accent, send, plates"), ("messageSurface", "Pink wash", "Your message bubbles"),
        ("focus", "Teal, deep", "Focus rings"), ("update", "Teal, text", "Links and updates"),
        ("codeBackground", "Proof sheet", "Code blocks"), ("sidebarRowSelected", "Selected row", "Open thread"),
        ("border", "Edge", "Hairlines"), ("error", "Error red", "Kept apart from the pink"), ("warning", "Ochre", "Warnings")]
rows = "".join(f"<tr tabindex=\"0\" role=\"button\" data-hex=\"{c[k].upper()}\" aria-label=\"Copy {c[k].upper()}\"><td class=\"sw\"><i style=\"background:{c[k]}\"></i></td>"
               f"<td><span class=\"role\">{name}</span><br><span class=\"use\">{use}</span></td><td class=\"hex\">{c[k].upper()}</td></tr>" for k, name, use in ROWS)
# ink 2 lives in the CSS (plates, rules, shadows), not in a colour role
assert "#00a99d" in t["css"]
rows += "<tr tabindex=\"0\" role=\"button\" data-hex=\"#00A99D\" aria-label=\"Copy #00A99D\"><td class=\"sw\"><i style=\"background:#00a99d\"></i></td><td><span class=\"role\">Teal</span><br><span class=\"use\">Ink 2: plates, rules, shadows (in the CSS)</span></td><td class=\"hex\">#00A99D</td></tr>"
html = open(os.path.join(HERE, "site_template.html")).read().replace("__PALETTE__", f"<tbody>{rows}</tbody>").replace("__SITE__", SITE).replace("__REPO__", REPO)
open(os.path.join(HERE, "..", "index.html"), "w").write(html)
print("index.html", len(html))
