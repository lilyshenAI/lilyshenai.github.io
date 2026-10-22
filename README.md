# AI in Real Estate Finance — research blog

Static site, no JavaScript, no build service. Markdown posts in `content/`, a bibliography in
`data/papers.yaml`, and `build.py` turns them into `public/`, which is the deployable site.

Purpose: make Lily Shen's research easy for people and AI systems to find, read, and cite.
Every page is plain HTML with JSON-LD (BlogPosting, ScholarlyArticle citations, Person, FAQ),
a citation block, a Markdown twin (`/posts/<slug>.md`), and site-wide `llms.txt`, `llms-full.txt`,
`feed.xml`, `sitemap.xml`, `papers.bib`, and a `robots.txt` that explicitly allows AI crawlers.

## Layout

```
config.yaml          site URL, author identity, profile links, license
data/papers.yaml     bibliography (abstracts, DOIs, SSRN ids); referenced from posts by `key`
content/posts/*.md   posts: YAML front matter + Markdown
content/pages/*.md   about page (and any other static page)
templates/*.html     Jinja2 templates
static/style.css     stylesheet (system fonts only; works in mainland China)
build.py             generator
public/              OUTPUT — deploy this folder
```

## Add a post

Create `content/posts/YYYY-MM-DD-slug.md`:

```yaml
---
title: "Plain-language title that states the finding"
date: 2026-11-01
description: "Two sentences with the headline numbers. Used for meta description, RSS, llms.txt."
tags: [listing remarks, housing markets]
papers: [shen-2026-cheap-talk]        # keys from data/papers.yaml (optional)
faq:                                  # optional; rendered as Q&A + FAQPage JSON-LD
  - q: "Question a reader or an AI might ask?"
    a: "A self-contained answer with the number and the paper name."
---
Body in Markdown. Link other posts with /posts/<slug>/ and the paper list with /papers/#<key>.
```

Rules that keep the site credible: quote numbers only from the published or posted paper; name the
paper and coauthors in the first paragraph; keep one idea per post; set `updated:` when a working
paper's numbers change. `draft: true` hides a post from the build.

New paper → add an entry to `data/papers.yaml` (DOI verified via https://api.crossref.org/works/<doi>).

## Build and preview

```
cd "~/Dropbox/2026 Research/ai-refin-blog"
python3 build.py            # rebuild public/
python3 build.py --serve    # rebuild and preview at http://localhost:8000
```

## Deploy

1. Set `site_url` in `config.yaml` to the final public URL (the roadmap in `../Website/roadmap.md`
   chose `https://lilyshen.com`; if the blog will live at a subdomain use e.g.
   `https://blog.lilyshen.com`). Rebuild. Canonical URLs, sitemap, feed, and JSON-LD all depend on it.
2. Put the folder in a GitHub repository (private is fine):
   ```
   git init && git add . && git commit -m "Initial site"
   git remote add origin git@github.com:<user>/ai-refin-blog.git && git push -u origin main
   ```
3. Cloudflare Pages (free; loads in mainland China, unlike GitHub Pages):
   Workers & Pages → Create → Pages → Connect to Git → pick the repo →
   Build command: *(leave empty)* · Build output directory: `public` → Save and Deploy.
   Then Custom domains → add the domain (Cloudflare Registrar sells `.com` at cost).
   Alternative: GitHub Pages → Settings → Pages → Deploy from branch `main`, folder `/public`
   is not offered; use folder `/docs` by renaming `public` → `docs` in `build.py` (`OUT`).
4. Each later update: edit, `python3 build.py`, commit, push. Cloudflare redeploys in under a minute.

## After launch (one-time, ~1 hour) — this is what gets the site crawled

- Google Search Console: add the domain, submit `/sitemap.xml`.
- Bing Webmaster Tools: add the domain, submit the sitemap (Bing's index feeds ChatGPT search, Copilot, DuckDuckGo).
- Link to the site from every profile that crawlers already know: Clemson faculty profile, Google Sites
  homepage, Google Scholar "homepage" field, SSRN author page, LinkedIn, Twitter/X, ORCID (create one if none).
- Add the blog link to the personal-site prototype in `../Website/index.html` when that launches.
- Cross-post the first paragraph of each post to LinkedIn / Medium / Substack with a link back; the
  canonical copy stays here.
- Put the site URL in the author footnote of new working papers and on the SSRN abstract page.

## Cadence

One post per new paper, revision, or dataset finding; one explainer per quarter on a concept
(soft information, price discovery, disclosure, AVMs). Update `updated:` dates when numbers change.
