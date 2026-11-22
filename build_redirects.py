"""Write one redirect page for each old ezrabrand.github.io/<repo>/... URL of a work that moved to openseforim.org.

py -3.13 build_redirects.py     (reads openseforim.org's sitemap.xml from the sibling clone ..\\openseforim-site)

GitHub Pages cannot send HTTP 301. A page with status 200, an immediate meta refresh and a canonical link to the
new URL is what search engines treat as a permanent redirect, so old links keep their ranking. 404.html stays as the
fallback for paths that are not listed here.
"""
import html, re, shutil, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
SITEMAP = HERE.parent / "openseforim-site" / "sitemap.xml"
# new slug -> old repo name on ezrabrand.github.io
OLD = {
    "emden": "emden-megillat-sefer",
    "hyman": "hyman-toldot-translation",
    "immanuel": "immanuel-mahberot",
    "meor-einayim": "meor-einayim",
    "bochart": "bochart-hierozoicon",
    "lewysohn": "lewysohn-zoologie",
    "loew": "low-flora",
    "barhebraeus": "barhebraeus-chronography",
    "defus": "defus",
}

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Moved to openseforim.org</title>
<link rel="canonical" href="{u}">
<meta http-equiv="refresh" content="0; url={u}">
<script>location.replace({js} + location.search + location.hash)</script>
</head><body><p>This page moved to <a href="{u}">{u}</a>.</p></body></html>
"""

urls = re.findall(r"<loc>([^<]+)</loc>", SITEMAP.read_text(encoding="utf-8"))
for old in OLD.values():
    shutil.rmtree(HERE / old, ignore_errors=True)
n = 0
for u in urls:
    m = re.match(r"https://openseforim\.org/([^/]+)/(.*)$", u)
    if not m or m.group(1) not in OLD:
        continue
    slug, rest = m.groups()
    out = HERE / OLD[slug] / (rest + "index.html" if rest == "" or rest.endswith("/") else rest)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(PAGE.format(u=html.escape(u), js='"' + u.replace('"', '%22') + '"'), encoding="utf-8")
    n += 1
print(f"{n} redirect pages", flush=True)
