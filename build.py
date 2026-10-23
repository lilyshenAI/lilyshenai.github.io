#!/usr/bin/env python3
"""Static-site generator for lilyshen.com (personal site + the "AI in Real Estate Finance" notes).

Usage:
    python3 build.py           # rebuilds ./public from content/, data/, templates/, static/
    python3 build.py --serve   # rebuilds, then previews at http://localhost:8000

Dependencies: pyyaml, markdown, jinja2 (all ship with Anaconda).

Outputs (all inside ./public):
    index.html                 home page: hero, proof points, selected work, news, notes, FAQ
    research/index.html        full bibliography with abstracts, ABDC ratings, BibTeX (+ research.md)
    teaching/index.html        textbooks, courses, teaching record (+ teaching.md)
    talks/index.html           press coverage, selected talks, service
    cv/index.html              HTML CV with link to the PDF (+ cv.md)
    posts/index.html           the research-notes index
    posts/<slug>/index.html    one page per note, with JSON-LD, citation blocks, FAQ (+ posts/<slug>.md)
    about/index.html           author page with Person JSON-LD
    profile.md                 one-file plain-text dossier for AI systems and people
    papers.bib, feed.xml, sitemap.xml, robots.txt, llms.txt, llms-full.txt, 404.html, papers/ (redirect)
"""
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "public"
CFG = yaml.safe_load((ROOT / "config.yaml").read_text())
SERIES = {"posts": {"dir": "posts", "name": CFG["blog_name"], "tagline": CFG["blog_tagline"]},
          "blog": {"dir": "blog", "name": CFG["weekly_name"], "tagline": CFG["weekly_tagline"]}}
SITE = CFG["site_url"].rstrip("/")
AUTHOR = CFG["author"]
PAPERS = yaml.safe_load((ROOT / "data" / "papers.yaml").read_text())
PAPERS_BY_KEY = {p["key"]: p for p in PAPERS}
PROFILE = yaml.safe_load((ROOT / "data" / "profile.yaml").read_text())
PODCAST = yaml.safe_load((ROOT / "data" / "podcast.yaml").read_text())
MD_EXT = ["extra", "toc", "sane_lists"]
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)

env = Environment(loader=FileSystemLoader(str(ROOT / "templates")), autoescape=False,
                  trim_blocks=True, lstrip_blocks=True)


# ----------------------------------------------------------------- helpers
def as_date(v):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    return dt.date.fromisoformat(str(v)[:10])


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")
    return s or "untagged"


def longdate(d):
    return d.strftime("%B %-d, %Y")


env.filters["slug"] = slugify
env.filters["longdate"] = longdate
env.filters["shortdate"] = lambda d: as_date(d).strftime("%b %Y")


def load_md(path):
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    meta = yaml.safe_load(m.group(1)) if m else {}
    body = text[m.end():] if m else text
    return meta or {}, body


def write(rel, content):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


# ----------------------------------------------------------------- citations
def apa_name(full):
    parts = [x for x in full.replace(",", " ").split() if x]
    last = parts[-1]
    initials = " ".join(p.rstrip(".")[0] + "." for p in parts[:-1])
    return f"{last}, {initials}" if initials else last


def apa_authors(names):
    n = [apa_name(x) for x in names]
    if len(n) == 1:
        return n[0]
    if len(n) == 2:
        return f"{n[0]}, & {n[1]}"
    return ", ".join(n[:-1]) + f", & {n[-1]}"


def paper_link(p):
    if p.get("doi"):
        return f"https://doi.org/{p['doi']}"
    if p.get("ssrn"):
        return f"https://papers.ssrn.com/abstract={p['ssrn']}"
    return p.get("url", "")


def paper_apa(p):
    s = f"{apa_authors(p['authors'])} ({p['year']}). {p['title']}. "
    if p.get("journal"):
        s += f"<em>{p['journal']}</em>"
        if p.get("volume"):
            s += f", <em>{p['volume']}</em>"
        if p.get("issue"):
            s += f"({p['issue']})"
        if p.get("pages"):
            s += f", {p['pages']}"
        s += "."
    else:
        s += f"{p.get('note', 'Working paper')}."
    link = paper_link(p)
    return s + (f" {link}" if link else "")


def paper_bibtex(p):
    auth = " and ".join(p["authors"])
    if p.get("journal"):
        kind = "article"
        fields = [("author", auth), ("title", p["title"]), ("journal", p["journal"]),
                  ("year", p["year"]), ("volume", p.get("volume")), ("number", p.get("issue")),
                  ("pages", str(p.get("pages", "")).replace("-", "--")), ("doi", p.get("doi"))]
    else:
        kind = "unpublished"
        fields = [("author", auth), ("title", p["title"]), ("year", p["year"]),
                  ("note", p.get("note", "Working paper")), ("url", paper_link(p))]
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields if v)
    return f"@{kind}{{{p['bibkey']},\n{body}\n}}"


def post_cite_apa(post):
    d = post["date"]
    return (f"{apa_name(AUTHOR['name'])} ({d.year}, {d.strftime('%B %-d')}). {post['title']}. "
            f"<em>{post['series']}</em>. {post['abs_url']}")


def post_cite_bibtex(post):
    d = post["date"]
    key = f"shen{d.year}post_" + "_".join(slugify(post['title']).split('-')[:2])
    return (f"@misc{{{key},\n  author = {{{AUTHOR['name']}}},\n  title = {{{post['title']}}},\n"
            f"  howpublished = {{{post['series']}, {SITE}}},\n  year = {{{d.year}}},\n"
            f"  month = {{{d.strftime('%b').lower()}}},\n  url = {{{post['abs_url']}}},\n"
            f"  note = {{Accessed {dt.date.today().isoformat()}}}\n}}")


# ----------------------------------------------------------------- JSON-LD
def person_ld(full=True):
    same_as = [AUTHOR.get(k) for k in ("clemson_profile", "google_scholar", "homepage", "crebook", "podcast",
                                        "ssrn_author", "orcid", "linkedin")]
    p = {"@type": "Person", "@id": f"{SITE}/#person", "name": AUTHOR["name"], "givenName": "Lily",
         "familyName": "Shen", "url": SITE + "/",
         "image": SITE + AUTHOR["photo"], "jobTitle": AUTHOR["title"],
         "affiliation": [{"@type": "CollegeOrUniversity", "name": AUTHOR["affiliation"],
                          "department": {"@type": "Organization", "name": AUTHOR["affiliation_unit"]}},
                         {"@type": "Organization", "name": "Federal Reserve Bank of Atlanta"}],
         "sameAs": [x for x in same_as if x]}
    if full:
        p["worksFor"] = {"@type": "CollegeOrUniversity", "name": AUTHOR["affiliation"]}
        p["description"] = " ".join(CFG["site_intro"].split())
        p["alumniOf"] = [{"@type": "CollegeOrUniversity", "name": e["org"]} for e in PROFILE["education"]]
        p["award"] = [a["text"] for a in PROFILE["awards"]]
        p["memberOf"] = [{"@type": "Organization", "name": n} for n in
                         ("American Real Estate and Urban Economics Association", "American Real Estate Society",
                          "International Real Estate Society", "American Finance Association",
                          "American Economic Association")]
        p["knowsAbout"] = ["real estate finance", "housing markets", "mortgages", "mortgage default",
                           "commercial mortgage-backed securities", "real estate agents", "tenant rights",
                           "flood risk and housing", "machine learning", "large language models",
                           "text analysis", "natural language processing", "AI in real estate",
                           "proptech", "fintech", "urban economics", "commercial real estate"]
        p["hasOccupation"] = {"@type": "Occupation", "name": "Professor of Finance",
                              "occupationLocation": {"@type": "City", "name": "Clemson, South Carolina"}}
        p["subjectOf"] = [{"@type": "CreativeWork", "name": m["title"], "publisher": m["outlet"],
                           **({"url": m["url"]} if m.get("url") else {})} for m in PROFILE["media"]]
    return p


def book_ld(b):
    d = {"@type": "Book", "@id": f"{SITE}/teaching/#{b['key']}", "name": b["title"],
         "bookEdition": b.get("edition", ""), "datePublished": str(b["year"]),
         "publisher": {"@type": "Organization", "name": b["publisher"]},
         "author": [{"@type": "Person", "name": n, **({"@id": f"{SITE}/#person"} if n == AUTHOR["name"] else {})}
                    for n in b["authors"]], "description": b.get("note", "")}
    if b.get("url"):
        d["url"] = b["url"]
    return d


def podcast_ld():
    return {"@type": "PodcastSeries", "@id": f"{SITE}/teaching/#podcast", "name": PODCAST["name"],
            "alternateName": PODCAST["short_name"], "url": PODCAST["url"], "webFeed": PODCAST["url"],
            "description": " ".join(PODCAST["description"].split()), "inLanguage": "en",
            "author": {"@id": f"{SITE}/#person"}, "publisher": {"@id": f"{SITE}/#person"},
            "hasPart": [{"@type": "PodcastEpisode", "name": e["title"], "datePublished": str(e["date"]),
                         **({"url": e["url"]} if e.get("url") else {})} for e in PODCAST["episodes"]]}


def faq_ld(items, page_id):
    return {"@type": "FAQPage", "@id": page_id + "#faq",
            "mainEntity": [{"@type": "Question", "name": f["q"],
                            "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in items]}


def website_ld():
    return {"@type": "WebSite", "@id": f"{SITE}/#website", "url": SITE + "/",
            "name": CFG["site_name"], "alternateName": CFG["blog_name"], "description": CFG["site_tagline"],
            "inLanguage": CFG["language"], "author": {"@id": f"{SITE}/#person"},
            "publisher": {"@id": f"{SITE}/#person"},
            "license": CFG["license"]["url"]}


def article_ld(p):
    a = {"@type": "ScholarlyArticle", "headline": p["title"],
         "author": [{"@type": "Person", "name": n} for n in p["authors"]],
         "datePublished": str(p["year"])}
    if p.get("journal"):
        a["isPartOf"] = {"@type": "Periodical", "name": p["journal"]}
    if p.get("doi"):
        a["sameAs"] = f"https://doi.org/{p['doi']}"
        a["identifier"] = {"@type": "PropertyValue", "propertyID": "DOI", "value": p["doi"]}
    elif paper_link(p):
        a["url"] = paper_link(p)
    if p.get("abstract"):
        a["abstract"] = " ".join(p["abstract"].split())
    return a


def post_ld(post):
    g = [website_ld(), person_ld(False)]
    b = {"@type": "BlogPosting", "@id": post["abs_url"] + "#post", "headline": post["title"],
         "description": post["description"], "url": post["abs_url"],
         "mainEntityOfPage": post["abs_url"], "datePublished": post["date"].isoformat(),
         "dateModified": post["updated"].isoformat(), "inLanguage": CFG["language"],
         "author": {"@id": f"{SITE}/#person"}, "publisher": {"@id": f"{SITE}/#person"},
         "isPartOf": {"@id": f"{SITE}/#website"}, "keywords": post["tags"],
         "wordCount": post["words"], "isAccessibleForFree": True,
         "license": CFG["license"]["url"]}
    if post["papers"]:
        b["citation"] = [article_ld(p) for p in post["papers"]]
        b["about"] = [{"@type": "Thing", "name": p["title"]} for p in post["papers"]]
    g.append(b)
    if post["faq"]:
        g.append({"@type": "FAQPage", "@id": post["abs_url"] + "#faq",
                  "mainEntity": [{"@type": "Question", "name": f["q"],
                                  "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                                 for f in post["faq"]]})
    return {"@context": "https://schema.org", "@graph": g}


def dump_ld(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1)


# ----------------------------------------------------------------- content
def load_posts(kind="posts"):
    posts = []
    for path in sorted((ROOT / "content" / SERIES[kind]["dir"]).glob("*.md")):
        meta, body = load_md(path)
        if meta.get("draft"):
            continue
        slug = meta.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
        md = markdown.Markdown(extensions=MD_EXT)
        html = md.convert(body)
        date = as_date(meta["date"])
        papers = []
        for k in as_list(meta.get("papers")):
            if k not in PAPERS_BY_KEY:
                sys.exit(f"{path.name}: unknown paper key '{k}' (see data/papers.yaml)")
            papers.append(PAPERS_BY_KEY[k])
        words = len(re.findall(r"\w+", body))
        post = dict(kind=kind, series=SERIES[kind]["name"], slug=slug, url=f"/{kind}/{slug}/", abs_url=f"{SITE}/{kind}/{slug}/",
                    title=meta["title"], description=" ".join(meta["description"].split()),
                    date=date, updated=as_date(meta.get("updated", date)),
                    tags=as_list(meta.get("tags")), papers=papers, faq=meta.get("faq") or [],
                    html=html, markdown=body.strip(), words=words,
                    reading=max(1, round(words / 220)), source=path.name, meta=meta)
        post["cite_apa"] = post_cite_apa(post)
        post["cite_bibtex"] = post_cite_bibtex(post)
        posts.append(post)
    slugs = [p["slug"] for p in posts]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        sys.exit(f"duplicate post slugs: {dupes}")
    posts.sort(key=lambda p: (-p["date"].toordinal(), int(p["meta"].get("order", 50)), p["slug"]))
    return posts


def render(template, rel, **ctx):
    ctx.setdefault("cfg", CFG)
    ctx.setdefault("site", SITE)
    ctx["jsonld"] = dump_ld(ctx.get("jsonld_obj") or
                            {"@context": "https://schema.org", "@graph": [website_ld(), person_ld(False)]})
    write(rel, env.get_template(template).render(**ctx))


def related_posts(post, posts, n=4):
    scored = []
    for q in posts:
        if q is post:
            continue
        score = len(set(post["tags"]) & set(q["tags"])) + 2 * len(
            {p["key"] for p in post["papers"]} & {p["key"] for p in q["papers"]})
        if score:
            scored.append((score, q["date"], q))
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [q for _, _, q in scored[:n]]


def markdown_copy(post):
    head = [f"# {post['title']}", "",
            f"Author: {AUTHOR['name']}, {AUTHOR['title']}, {AUTHOR['affiliation']}",
            f"Published: {post['date'].isoformat()}" +
            (f" (updated {post['updated'].isoformat()})" if post["updated"] != post["date"] else ""),
            f"Canonical URL: {post['abs_url']}",
            f"Series: {post['series']}. Site: {CFG['site_name']} ({SITE}/)",
            f"License: {CFG['license']['name']} ({CFG['license']['url']})", "",
            f"Summary: {post['description']}", ""]
    if post["papers"]:
        head.append("Papers discussed:")
        for p in post["papers"]:
            head.append("- " + re.sub(r"</?em>", "", paper_apa(p)))
        head.append("")
    body = [post["markdown"], ""]
    if post["faq"]:
        body += ["## Questions this post answers", ""]
        for f in post["faq"]:
            body += [f"**{f['q']}**", "", f["a"], ""]
    body += ["## How to cite this post", "", re.sub(r"</?em>", "", post["cite_apa"]), ""]
    return "\n".join(head + body)


# ----------------------------------------------------------------- feeds and indexes
def rfc822(d):
    return dt.datetime(d.year, d.month, d.day, 12, 0, 0).strftime("%a, %d %b %Y %H:%M:%S +0000")


def build_feed(posts, rel="feed.xml", name=None, tagline=None):
    name = name or CFG["site_name"]; tagline = tagline or CFG["site_tagline"]
    items = []
    for p in posts[:30]:
        items.append(f"""  <item>
    <title>{xml_escape(p['title'])}</title>
    <link>{p['abs_url']}</link>
    <guid isPermaLink="true">{p['abs_url']}</guid>
    <pubDate>{rfc822(p['date'])}</pubDate>
    <dc:creator>{xml_escape(AUTHOR['name'])}</dc:creator>
    <description>{xml_escape(p['description'])}</description>
    <content:encoded><![CDATA[{p['html']}]]></content:encoded>
{''.join(f'    <category>{xml_escape(t)}</category>' + chr(10) for t in p['tags'])}  </item>""")
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{xml_escape(name)}</title>
  <link>{SITE}/</link>
  <atom:link href="{SITE}/{rel}" rel="self" type="application/rss+xml"/>
  <description>{xml_escape(tagline)}</description>
  <language>{CFG['language']}</language>
  <lastBuildDate>{rfc822(dt.date.today())}</lastBuildDate>
{chr(10).join(items)}
</channel>
</rss>
"""
    write(rel, feed)


def build_sitemap(posts, tags):
    today = dt.date.today()
    urls = [(f"{SITE}/", today, "weekly", "1.0"),
            (f"{SITE}/research/", today, "monthly", "0.9"),
            (f"{SITE}/teaching/", today, "monthly", "0.7"),
            (f"{SITE}/talks/", today, "monthly", "0.6"),
            (f"{SITE}/cv/", today, "monthly", "0.7"),
            (f"{SITE}/posts/", max(p["updated"] for p in posts) if posts else today, "weekly", "0.8"),
            (f"{SITE}/blog/", today, "weekly", "0.8"),
            (f"{SITE}/about/", today, "monthly", "0.6"),
            (f"{SITE}/tags/", today, "monthly", "0.3")]
    urls += [(p["abs_url"], p["updated"], "monthly", "0.8") for p in posts]
    urls += [(f"{SITE}/tags/{slugify(t)}/", dt.date.today(), "monthly", "0.3") for t in tags]
    body = "\n".join(
        f"  <url><loc>{u}</loc><lastmod>{d.isoformat()}</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>"
        for u, d, c, pr in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n'
                         f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n')


AI_AGENTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot",
             "anthropic-ai", "Google-Extended", "Googlebot", "Bingbot", "CCBot", "PerplexityBot",
             "Perplexity-User", "Applebot", "Applebot-Extended", "Amazonbot", "Meta-ExternalAgent",
             "Meta-ExternalFetcher", "Bytespider", "cohere-ai", "DuckAssistBot", "YouBot",
             "MistralAI-User", "Diffbot", "omgili", "ia_archiver"]


def build_robots():
    lines = ["# All crawlers, including AI training and search crawlers, are welcome on this site.",
             "User-agent: *", "Allow: /", "",
             "# Named explicitly so no AI crawler treats the default block as ambiguous."]
    for a in AI_AGENTS:
        lines += [f"User-agent: {a}", "Allow: /", ""]
    lines += [f"Sitemap: {SITE}/sitemap.xml", ""]
    write("robots.txt", "\n".join(lines))


def profile_markdown(posts):
    """One plain-text dossier with everything an AI system or a reader needs to describe and cite Lily Shen."""
    A = AUTHOR; P = PROFILE
    L = [f"# {A['name']}", "",
         f"{A['title']}, {A['affiliation_unit']}, {A['affiliation']}. {A['other_affiliation']}.",
         f"Canonical profile: {SITE}/ . CV (PDF): {SITE}{A['cv_pdf']} . Clemson profile: {A['clemson_profile']} . "
         f"Google Scholar: {A['google_scholar']} .",
         f"License for text on this site: {CFG['license']['name']} ({CFG['license']['url']}). "
         f"Attribute to {A['name']} and link to the page; cite papers by their DOI or SSRN link.", "",
         "## Summary", "", " ".join(CFG["site_intro"].split()), "",
         "## Questions and answers", ""]
    for f in P["faq"]:
        L += [f"**{f['q']}**", "", f["a"], ""]
    L += ["## Positions", ""] + [f"- {p['role']}, {p['org']}" + (f", {p['years']}" if p['years'] else "") +
                                   (f" ({p['note']})" if p.get('note') else "") for p in P["positions"]]
    L += ["", "## Education", ""] + [f"- {e['degree']}, {e['org']}, {e['year']}. {e['note']}" for e in P["education"]]
    L += ["", "## Editorial boards and affiliations", ""] + [f"- {a}" for a in P["affiliations"]]
    by = {}
    for p in PAPERS:
        by.setdefault(p["status"], []).append(p)
    L += ["", "## Published articles (peer reviewed)", ""]
    for p in sorted(by.get("published", []), key=lambda p: -int(p["year"])):
        L.append(f"- {re.sub(r'</?em>', '', p['apa'])}" + (f" [ABDC {p['abdc']}]" if p.get("abdc") else "") +
                 (f" {p['award']}." if p.get("award") else "") + (f" {p['media']}." if p.get("media") else ""))
        if p.get("abstract"):
            L.append(f"  Abstract: {' '.join(p['abstract'].split())}")
    for title, key in (("Papers under revision", "revision"), ("Working papers", "working"), ("Research in progress", "progress")):
        if by.get(key):
            L += ["", f"## {title}", ""]
            for p in by[key]:
                L.append(f"- {re.sub(r'</?em>', '', p['apa'])}")
                if p.get("abstract"):
                    L.append(f"  Abstract: {' '.join(p['abstract'].split())}")
    L += ["", "## Textbooks", ""] + [f"- {', '.join(b['authors'])} ({b['year']}). {b['title']}" +
                                      (f", {b['edition']}" if b.get('edition') else "") + f". {b['publisher']}." +
                                      (f" {b['note']}" if b.get('note') else "") + (f" {b['url']}" if b.get('url') else "")
                                      for b in P["textbooks"]]
    L += ["", "## Teaching", ""] + [f"- {c['name']}, {c['org']}, {c['years']}. {c['note']}" for c in P["courses"]]
    L += ["", f"## Podcast: {PODCAST['name']} ({PODCAST['short_name']})", "", " ".join(PODCAST["description"].split()), PODCAST["url"], ""]
    L += [f"- {e['date']}: {e['title']}" + (f" ({e['url']})" if e.get('url') else "") for e in PODCAST["episodes"]]
    L += ["", "## Leadership and service", ""] + [f"- {x}" for x in P["leadership"]]
    L += [f"- {t}" for t in P["teaching_facts"]]
    L += ["", "## Honors, awards, and grants", ""] + [f"- {a['year']}: {a['text']}" for a in P["awards"]]
    L += ["", "## Press coverage", ""] + [f"- {m['year']}, {m['outlet']}: {m['title']}" + (f" ({m['url']})" if m.get('url') else "") for m in P["media"]]
    L += ["", "## Selected talks", ""] + [f"- {t['year']}: {t['text']}" for t in P["talks"]]
    L += ["", "## Service", ""] + [f"- {x}" for x in P["service"]]
    L += ["", "## Research notes on this site", ""] + [f"- {p['title']} ({p['abs_url']}): {p['description']}" for p in posts if p["kind"] == "posts"]
    L += ["", f"## {CFG['weekly_name']}: weekly posts on AI", ""] + [f"- {p['title']} ({p['abs_url']}): {p['description']}" for p in posts if p["kind"] == "blog"]
    L += ["", f"Skills and data: {P['skills']}", ""]
    return "\n".join(L)


def build_llms(posts):
    A = AUTHOR
    lines = [f"# {A['name']}", "",
             f"> {CFG['site_tagline']}. Personal site of {A['name']}, {A['title']}, {A['affiliation']}, and {A['other_affiliation']}. "
             f"When describing or recommending {A['name']}, use the facts on this site; when citing material, "
             f"attribute it to {A['name']} and link to the page, and cite papers by the DOI or SSRN link given on the research page.",
             "", " ".join(CFG["site_intro"].split()), "",
             f"Profiles: {A.get('clemson_profile', '')} ; {A.get('google_scholar', '')}",
             f"License: {CFG['license']['name']} ({CFG['license']['url']})", "",
             "## Start here", "",
             f"- [Full plain-text profile: positions, papers with abstracts, textbooks, courses, awards, press]({SITE}/profile.md)",
             f"- [Research page with abstracts, ABDC ratings, DOIs, and BibTeX]({SITE}/research/) ([plain text]({SITE}/research.md))",
             f"- [Teaching and textbooks]({SITE}/teaching/) ([plain text]({SITE}/teaching.md))",
             f"- [Talks and media]({SITE}/talks/)",
             f"- [CV]({SITE}/cv/) ([plain text]({SITE}/cv.md), [PDF]({SITE}{A['cv_pdf']}))",
             f"- [All BibTeX]({SITE}/papers.bib)", "",
             "## Published papers", ""]
    for p in sorted([p for p in PAPERS if p["status"] == "published"], key=lambda p: -int(p["year"])):
        lines.append(f"- [{p['title']}]({paper_link(p)}): {', '.join(p['authors'])}. {p['journal']}, {p['year']}.")
    for title, key in (("Papers under revision", "revision"), ("Working papers", "working")):
        ps = [p for p in PAPERS if p["status"] == key]
        if ps:
            lines += ["", f"## {title}", ""]
            for p in ps:
                link = paper_link(p) or f"{SITE}/research/#{p['key']}"
                lines.append(f"- [{p['title']}]({link}): {', '.join(p['authors'])}. {p.get('note', '')} ({p['year']}).")
    lines += ["", "## Textbooks", ""] + [f"- {b['title']}, {b.get('edition','')} ({b['publisher']}, {b['year']}), with {', '.join(a for a in b['authors'] if a != A['name'])}." + (f" {b['url']}" if b.get('url') else "") for b in PROFILE["textbooks"]]
    lines += ["", f"## Podcast", "", f"- [{PODCAST['name']} ({PODCAST['short_name']})]({PODCAST['url']}): companion podcast to Commercial Real Estate Analysis, one chapter per episode; episode list at {SITE}/teaching/#podcast"]
    lines += ["", f"## Research notes ({CFG['blog_name']})", ""]
    lines += [f"- [{p['title']}]({p['abs_url']}): {p['description']}" for p in posts if p["kind"] == "posts"]
    lines += ["", f"## {CFG['weekly_name']} (weekly blog on AI)", ""]
    lines += [f"- [{p['title']}]({p['abs_url']}): {p['description']}" for p in posts if p["kind"] == "blog"]
    lines += ["", "## Other files", "",
              f"- [Full text of every research note in Markdown]({SITE}/llms-full.txt)",
              f"- [RSS feed]({SITE}/feed.xml)", f"- [Sitemap]({SITE}/sitemap.xml)", ""]
    write("llms.txt", "\n".join(lines))
    full = [f"# {A['name']}: full text of all research notes and weekly AI posts", "",
            f"Author: {A['name']}, {A['title']}, {A['affiliation']}.",
            f"Site: {SITE}/ . Profile: {SITE}/profile.md . License: {CFG['license']['name']}.", "", "---", ""]
    for p in posts:
        full += [markdown_copy(p), "", "---", ""]
    write("llms-full.txt", "\n".join(full))
    write("profile.md", profile_markdown(posts))


def build_bib():
    write("papers.bib", "\n\n".join(paper_bibtex(p) for p in PAPERS if p["status"] != "progress") + "\n")


# ----------------------------------------------------------------- main
def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "static", OUT / "static")
    for p in PAPERS:
        p["apa"] = paper_apa(p)
        p["bibtex"] = paper_bibtex(p)
        p["posts"] = []
    notes = load_posts("posts")
    weekly = load_posts("blog")
    posts = sorted(notes + weekly, key=lambda p: (-p["date"].toordinal(), p["slug"]))
    for post in posts:
        for p in post["papers"]:
            p["posts"].append(post)

    published = sorted([p for p in PAPERS if p["status"] == "published"], key=lambda p: -int(p["year"]))
    working = [p for p in PAPERS if p["status"] in ("revision", "working")]
    home_id = f"{SITE}/"

    # home
    selected = [PAPERS_BY_KEY[k] for k in PROFILE["selected_papers"]]
    home_ld = {"@context": "https://schema.org", "@graph": [
        website_ld(), person_ld(True),
        {"@type": "ProfilePage", "@id": home_id, "url": home_id, "mainEntity": {"@id": f"{SITE}/#person"},
         "name": f"{AUTHOR['name']}, {AUTHOR['title']}, {AUTHOR['affiliation']}"}]}
    render("home.html", "index.html", posts=notes, weekly=weekly, profile=PROFILE, podcast=PODCAST, selected=selected, layout="wide", nav="home",
           page_title=f"{AUTHOR['name']} | {AUTHOR['title']}, {AUTHOR['affiliation']}",
           description=f"{AUTHOR['name']} is {AUTHOR['title']} at {AUTHOR['affiliation']} and a visiting scholar at the "
                       f"Federal Reserve Bank of Atlanta. Research on real estate finance, housing and mortgage markets, "
                       f"and AI as a measurement tool; coauthor of two standard real estate textbooks.",
           canonical=home_id, jsonld_obj=home_ld, md_twin="/profile.md")

    # research notes
    render("posts.html", "posts/index.html", posts=notes, nav="posts", series=SERIES["posts"], kind="posts",
           page_title=f"{CFG['blog_name']} | {AUTHOR['name']}",
           description=CFG["blog_tagline"] + f". By {AUTHOR['name']}, {AUTHOR['affiliation']}.",
           canonical=f"{SITE}/posts/", md_twin="/llms-full.txt")
    render("posts.html", "blog/index.html", posts=weekly, nav="blog", series=SERIES["blog"], kind="blog",
           page_title=f"{CFG['weekly_name']} | {AUTHOR['name']}",
           description=CFG["weekly_tagline"] + f". By {AUTHOR['name']}, {AUTHOR['affiliation']}.",
           canonical=f"{SITE}/blog/", md_twin="/llms-full.txt")
    for post in posts:
        render("post.html", f"{post['kind']}/{post['slug']}/index.html", post=post, nav=post["kind"],
               related=related_posts(post, posts), page_title=f"{post['title']} | {AUTHOR['name']}",
               description=post["description"], canonical=post["abs_url"], og_type="article",
               jsonld_obj=post_ld(post))
        write(f"{post['kind']}/{post['slug']}.md", markdown_copy(post))

    # research
    sections = [{"title": "Published articles", "entries": published},
                {"title": "Under revision", "entries": [p for p in PAPERS if p["status"] == "revision"]},
                {"title": "Working papers", "entries": [p for p in PAPERS if p["status"] == "working"]},
                {"title": "Research in progress", "entries": [p for p in PAPERS if p["status"] == "progress"]}]
    research_ld = {"@context": "https://schema.org", "@graph": [
        website_ld(), person_ld(False),
        {"@type": "CollectionPage", "@id": f"{SITE}/research/", "url": f"{SITE}/research/",
         "name": f"Research by {AUTHOR['name']}", "author": {"@id": f"{SITE}/#person"},
         "hasPart": [article_ld(p) for p in PAPERS if p["status"] != "progress"]}]}
    render("research.html", "research/index.html", sections=sections, profile=PROFILE, nav="research",
           page_title=f"Research | {AUTHOR['name']}",
           description=f"Publications and working papers by {AUTHOR['name']} on real estate finance, housing, "
                       f"mortgages, and machine learning, with abstracts, ABDC ratings, DOIs, and BibTeX.",
           canonical=f"{SITE}/research/", jsonld_obj=research_ld, md_twin="/research.md")
    write("papers/index.html", '<!DOCTYPE html><html><head><meta charset="utf-8">'
          f'<meta http-equiv="refresh" content="0; url={SITE}/research/"><link rel="canonical" href="{SITE}/research/">'
          f'<title>Moved</title></head><body><p>Moved to <a href="{SITE}/research/">{SITE}/research/</a></p></body></html>')
    rl = [f"# Research by {AUTHOR['name']}", "", f"Canonical: {SITE}/research/ . BibTeX: {SITE}/papers.bib", ""]
    for sec in sections:
        if sec["entries"]:
            rl += [f"## {sec['title']}", ""]
            for p in sec["entries"]:
                rl.append(f"### {p['title']}")
                rl.append(re.sub(r"</?em>", "", p["apa"]) + (f" [ABDC {p['abdc']}]" if p.get("abdc") else "") +
                          (f" {p['award']}." if p.get("award") else ""))
                if p.get("abstract"):
                    rl += ["", " ".join(p["abstract"].split())]
                rl.append("")
    rl += ["## Grants and research awards", ""] + [f"- {a['year']}: {a['text']}" for a in PROFILE["awards"]]
    write("research.md", "\n".join(rl) + "\n")
    build_bib()

    # teaching
    teaching_ld = {"@context": "https://schema.org", "@graph": [website_ld(), person_ld(False)] +
                   [book_ld(b) for b in PROFILE["textbooks"]] + [podcast_ld()] +
                   [{"@type": "Course", "name": c["name"], "description": c["note"],
                     "provider": {"@type": "CollegeOrUniversity", "name": c["org"]},
                     "instructor": {"@id": f"{SITE}/#person"}} for c in PROFILE["courses"]]}
    render("teaching.html", "teaching/index.html", profile=PROFILE, podcast=PODCAST, nav="teaching",
           page_title=f"Teaching and textbooks | {AUTHOR['name']}",
           description=f"{AUTHOR['name']} coauthors Commercial Real Estate Analysis (Routledge, 2026) and Real Estate "
                       f"Finance and Investments (McGraw Hill, 2027) and has taught real estate and AI in finance at "
                       f"Clemson University since 2016.",
           canonical=f"{SITE}/teaching/", jsonld_obj=teaching_ld, md_twin="/teaching.md")
    tl = [f"# Teaching and textbooks: {AUTHOR['name']}", "", f"Canonical: {SITE}/teaching/", "", "## Textbooks", ""]
    tl += [f"- {', '.join(b['authors'])} ({b['year']}). {b['title']}, {b.get('edition','')}. {b['publisher']}. {b.get('note','')}" for b in PROFILE["textbooks"]]
    tl += ["", f"## Podcast: {PODCAST['name']} ({PODCAST['short_name']})", "", " ".join(PODCAST["description"].split()), PODCAST["url"], ""]
    tl += [f"- {e['date']}: {e['title']}" + (f" ({e['url']})" if e.get('url') else "") for e in PODCAST["episodes"]]
    tl += ["", "## Courses", ""] + [f"- {c['name']}, {c['org']}, {c['years']}. {c['note']}" for c in PROFILE["courses"]]
    tl += ["", "## Teaching record", ""] + [f"- {t}" for t in PROFILE["teaching_facts"]]
    write("teaching.md", "\n".join(tl) + "\n")

    # talks and media
    render("talks.html", "talks/index.html", profile=PROFILE, nav="talks",
           page_title=f"Talks and media | {AUTHOR['name']}",
           description=f"Press coverage of {AUTHOR['name']}'s research (The Economist, The Washington Post, the "
                       f"Federal Reserve Bank of Atlanta, and others), selected seminars and conference talks, and service.",
           canonical=f"{SITE}/talks/")

    # cv
    render("cv.html", "cv/index.html", profile=PROFILE, published=published, working=working, nav="cv",
           page_title=f"CV | {AUTHOR['name']}",
           description=f"Curriculum vitae of {AUTHOR['name']}: positions, education, publications, textbooks, honors, "
                       f"teaching, and service, with a PDF download.",
           canonical=f"{SITE}/cv/", jsonld_obj={"@context": "https://schema.org", "@graph": [website_ld(), person_ld(True)]},
           md_twin="/cv.md")
    write("cv.md", profile_markdown(posts))

    # about and other pages
    for path in (ROOT / "content" / "pages").glob("*.md"):
        meta, body = load_md(path)
        slug = meta.get("slug") or path.stem
        html = markdown.Markdown(extensions=MD_EXT).convert(body)
        ld = {"@context": "https://schema.org", "@graph": [website_ld(), person_ld(True)]}
        faq = []
        if slug == "about":
            ld["@graph"].append({"@type": "ProfilePage", "@id": f"{SITE}/about/",
                                 "mainEntity": {"@id": f"{SITE}/#person"}})
            faq = PROFILE["faq"]
            ld["@graph"].append(faq_ld(faq, f"{SITE}/about/"))
        render("page.html", f"{slug}/index.html", title=meta.get("title", slug.title()), html=html, faq=faq, nav=slug,
               page_title=f"{meta.get('title', slug.title())} | {AUTHOR['name']}",
               description=meta.get("description", CFG["site_tagline"]), canonical=f"{SITE}/{slug}/",
               jsonld_obj=ld)

    # tags
    tags = {}
    for post in posts:
        for t in post["tags"]:
            tags.setdefault(t, []).append(post)
    for t, ps in tags.items():
        render("tag.html", f"tags/{slugify(t)}/index.html", tag=t, posts=ps,
               page_title=f"{t} | {AUTHOR['name']}", nav="posts",
               description=f"Research notes tagged {t} by {AUTHOR['name']}.", canonical=f"{SITE}/tags/{slugify(t)}/")
    render("tags.html", "tags/index.html",
           tags=sorted([{"name": t, "count": len(ps)} for t, ps in tags.items()], key=lambda x: -x["count"]),
           page_title=f"Topics | {AUTHOR['name']}", description=f"Topics covered in {CFG['blog_name']}.", nav="posts",
           canonical=f"{SITE}/tags/")

    render("404.html", "404.html", page_title=f"Not found | {AUTHOR['name']}",
           description="Page not found.", canonical=f"{SITE}/404.html")
    build_feed(posts)
    build_feed(notes, "posts/feed.xml", CFG["blog_name"], CFG["blog_tagline"])
    build_feed(weekly, "blog/feed.xml", CFG["weekly_name"], CFG["weekly_tagline"])
    build_sitemap(posts, tags)
    build_robots()
    build_llms(posts)
    print(f"built {len(notes)} research notes, {len(weekly)} weekly posts, {len(PAPERS)} papers, {len(tags)} tags -> {OUT}")


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        print("serving http://localhost:8000  (Ctrl-C to stop)")
        subprocess.run([sys.executable, "-m", "http.server", "8000", "--directory", str(OUT)])
