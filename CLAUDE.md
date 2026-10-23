# lilyshen-site — conventions

- Static site; `python3 build.py` regenerates `public/` from `content/`, `data/papers.yaml`, `data/profile.yaml`, `templates/`, `static/`. Run it after any content edit and check the output line (post / paper / tag counts).
- Numbers in posts come only from the paper's published or posted abstract/text (see `../CLAUDE.md` for the listing-language papers' current facts). Never introduce figures the paper does not state; never reintroduce the retired Paper 2 headline (1.87 SD / $111k).
- Measurement framing: AI discovers the vocabulary; a frozen vocabulary scores every document. Do not claim a live LLM scores each listing.
- Author identity is fixed in `config.yaml` (Lily Shen; no alternate names anywhere on the site). Keep it consistent everywhere; contact email appears only as the written-out form in config.yaml `email_text` (never a mailto link); office in `office`.
- New papers: add to `data/papers.yaml` with a Crossref-verified DOI (`curl -s https://api.crossref.org/works/<doi>`); working papers get `note:` and `ssrn:` when posted.
- Do not `git push` or change `site_url` without Lily's say-so; deploying is outward-facing.
- Profile facts (positions, awards, courses, media, talks, FAQ) live in `data/profile.yaml` and come from the CV; update both when the CV changes. Keep `static/Lily_Shen_CV.pdf` in sync with the application CV.
- Letter-style rules apply to site copy too: no self-praise adjectives, no negative comparisons with Clemson, numbers only from the CV or papers.
