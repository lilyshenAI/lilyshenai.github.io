---
title: "How to build auditable AI text measures for economic research: a two-step method"
date: 2026-10-19
order: 2
description: "A practical method for using large language models as measurement tools in economics and finance. The model discovers the vocabulary for each economic category across the full corpus; a fixed, published vocabulary then scores every document, so results are reproducible, traceable phrase by phrase, and testable out of sample."
tags: [methods, large language models, text analysis, reproducibility, listing remarks]
papers: [shen-2026-cheap-talk, shen-2026-listing-language-price-discovery]
faq:
  - q: "Should a large language model assign the score to each document directly?"
    a: "Not for the main measure. In the two-step method the model discovers the vocabulary for each economic category, and a frozen, published vocabulary then scores every document deterministically. Live model scoring of a subsample is useful as a validation check, with agreement statistics against the rule-based scores and human readers, but it should not be the number reported in the tables."
  - q: "Why not just write the dictionary by hand?"
    a: "Coverage. Practitioners write in dialect, and a hand-authored list misses most of the phrases that express a category. Having the model read the full corpus and propose phrases, which are then screened and frozen, is more comprehensive while remaining fully auditable."
  - q: "How do you keep an AI-built text measure out of sample?"
    a: "Vocabulary discovery may use only text available before the prediction period. A dictionary can be updated on a rolling or expanding historical window, but text from the test period cannot enter discovery for a test labeled out of sample. Replicating the whole procedure in a second market never used for estimation is the strongest check."
  - q: "What is portable across markets: the word list or the procedure?"
    a: "The procedure. The economic categories, model instructions, discovery protocol, screening rules, validation steps, and index construction stay fixed, while the words and phrases may be rediscovered for each market, period, or dataset so the measure can accommodate local terminology and language change."
---
Economists increasingly want to use large language models (LLMs) to turn text into variables. The obstacle is not capability but credibility. A referee cannot replicate a number if it came from a model that may answer differently tomorrow, and a reader cannot tell what a score means if no one can point to the words that produced it. The method I use in my listing-language papers separates the two jobs an LLM might do and gives only one of them to the model.

## Step 1: the model discovers the vocabulary

Start from economic categories defined before looking at the data. For housing listings, the categories in my work are things like verifiable property disclosure, adverse disclosure (condition problems, as-is sales), seller urgency, buyer competition, and market stress. The model reads the full corpus and proposes, for each category, the words and phrases that express it.

Why use the model rather than a hand-written dictionary? Coverage. Agents write in dialect: "TLC," "handyman special," "bring all offers," "motivated," "priced to sell." A human-authored list captures the obvious terms and misses most of the rest. A model that has read two million remarks finds the long tail. Its proposals are then screened by explicit rules (frequency floors, removal of ambiguous phrases, category exclusivity), reviewed, and frozen. The frozen vocabulary is published with the paper.

## Step 2: a fixed vocabulary scores every document

Scoring is deterministic. Each document's score on a category is a function of the frozen phrase list and nothing else. Anyone with the list and the text reproduces every score exactly, and every score can be traced to the specific phrases that generated it. The LLM does not score listings one at a time, and that is deliberate. Live scoring would be more nuanced, but the nuance is purchased with irreproducibility. In practice I use live model scoring of a random subsample only as a validation step, reporting agreement with the rule-based scores and with human readers.

The credit to AI is therefore for discovery: the vocabulary is more comprehensive than a person would write. The credit for reproducibility goes to the frozen list.

## What is portable: the procedure, not the word list

A natural worry is that a vocabulary built in Atlanta in 2007 to 2017 will not transfer to the Carolinas in 2019 or to Phoenix in 2026. It should not have to. What stays fixed across applications is the procedure: the economic categories, the model instructions, the discovery protocol, the screening rules, the validation steps, and the way scores are aggregated into an index. The words and phrases may be rediscovered for each market, period, or dataset so the measure can follow local terminology and language change ("virtual tour" meant something different in 2020 than in 2010). Comparability lives at the level of the economic category.

## Out-of-sample discipline

If the measure will be used to forecast, vocabulary discovery may use only text available before the prediction period. A dictionary can be updated on a rolling or expanding historical window, but future-period text cannot enter discovery for any test labeled out of sample. The strongest check is to run the entire procedure in a market that was never used to build anything. In [Listing Language and House Price Discovery](/posts/listing-language-house-price-discovery/), the Carolinas are the estimation sample and Georgia is the replication market: demand-heat language predicts 0.43 percentage points higher six-month price growth there, in a market never used for estimation.

## A validation checklist

1. **Face validity.** Scores should move with known market states. Seller-stress language should rise in downturns and be higher where prices are lower and marketing times longer. It does.
2. **Human audit.** A random sample of documents is read by people, and agreement with the rule-based scores is reported.
3. **Model-versus-rules agreement.** The live model scores a subsample; agreement statistics are reported.
4. **Placebo and reassignment tests.** Reassigning text across geographies or periods should destroy the predictive relation.
5. **External replication.** The whole procedure is rerun in a second market.
6. **Alternative text controls.** The categories should retain content after controlling for machine-selected tokens (for example, LASSO-selected words), so that a category is not a relabeling of a few frequent terms. In [Cheap Talk or Priced Information?](/posts/cheap-talk-or-priced-information-listing-remarks/), residual information and adverse disclosure survive this test.

## Why this matters beyond housing

The same two steps apply wherever text carries economic content that structured data does not: loan and servicing agreements, risk-factor sections of filings, analyst reports, consumer complaint narratives, inspection reports. The contracts paper in the *Journal of Financial and Quantitative Analysis* was an early version of this idea with document-similarity methods; the listing-language papers apply it with LLM-discovered vocabularies. The common thread is that the model's job is to help the economist see the text, and the economist's job is to make the measurement reproducible.
