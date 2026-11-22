# EzraBrand.github.io

Redirects for works that moved to https://openseforim.org.

- `build_redirects.py` writes one redirect page (status 200, meta refresh, canonical) for each old
  `ezrabrand.github.io/<repo>/...` URL, from the sitemap of `../openseforim-site`. Rerun it after a moved work adds pages.
- `404.html` is the fallback for other old paths (JavaScript redirect).
