# lilyshen.com — personal site + "AI in Real Estate Finance" research notes

Static site, no JavaScript, no build service. Markdown posts in `content/`, a bibliography in
`data/papers.yaml`, and `build.py` turns them into `public/`, which is the deployable site.

Purpose: present Lily Shen to employers, colleagues, and AI systems, and make her research easy to find,
read, and cite. Pages: home (hero, proof points, selected work, news, FAQ), research (abstracts, ABDC,
DOIs, BibTeX), teaching (textbooks as schema.org Book, courses), talks & media, CV (HTML + PDF), research
notes (the former blog, at /posts/), about. Every page is plain HTML with JSON-LD (Person with sameAs/awards/
knowsAbout, ScholarlyArticle, Book, Course, FAQPage, BlogPosting), and the site ships Markdown twins
(`/profile.md`, `/research.md`, `/teaching.md`, `/cv.md`, `/posts/<slug>.md`), `llms.txt`, `llms-full.txt`,
`feed.xml`, `sitemap.xml`, `papers.bib`, and a `robots.txt` that explicitly allows AI crawlers.

## Layout

```
config.yaml          site URL, author identity, profile links, license, photo, CV path
data/profile.yaml    everything else about Lily: positions, education, textbooks, courses, awards, media, talks, news, FAQ
data/papers.yaml     bibliography (abstracts, DOIs, SSRN ids, ABDC ratings); referenced from posts by `key`
content/posts/*.md   posts: YAML front matter + Markdown
content/pages/*.md   about page (and any other static page)
templates/*.html     Jinja2 templates
static/               style.css, lily-shen.jpg (headshot), Lily_Shen_CV.pdf (replace when the CV changes)
build.py             generator
public/              OUTPUT — deploy this folder
```

## Update the profile

Edit `data/profile.yaml` (news items, awards, courses, talks, media, FAQ) and rebuild. The CV PDF in
`static/` is a copy; replace it when the CV changes. New paper: `data/papers.yaml` (+ add its key to
`selected_papers` in profile.yaml if it should appear on the home page).

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
cd "~/Dropbox/2026 Research/lilyshen-site"
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
   git remote add origin git@github.com:<user>/lilyshen-site.git && git push -u origin main
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


## Deploying (GitHub Pages)

The site lives at https://lilyshen.github.io, served from the GitHub repository `lilyshen/lilyshen.github.io`.
`.github/workflows/pages.yml` rebuilds and deploys on every push to `main`, so the workflow is:
edit content or data, run `python3 build.py` locally to check, commit, `git push`. The `public/` folder is
not committed; Actions regenerates it. Repository setting required once: Settings → Pages → Source = GitHub Actions.
