---
title: "Price discovery in illiquid markets: what listing remarks reveal before transaction indices update"
date: 2026-10-19
order: 5
description: "Summary of my working paper Soft Information and Price Discovery in Illiquid Asset Markets. Using 63,067 Atlanta listings, seller-stress language tracks local market weakness; part of the signal is distressed-sale composition, but the text channels remain jointly significant predictors of next-year local price-index changes after composition is controlled."
tags: [price discovery, illiquid assets, listing remarks, distressed sales, house price index, housing markets]
papers: [shen-2026-soft-information-price-discovery]
faq:
  - q: "Does listing language just measure how many distressed sales there are?"
    a: "Partly. Controlling for the structured distressed-sale share (REO and corporate-owned listings) absorbs most of the seller-stress coefficient in next-year price-index regressions. But the text channels remain jointly significant beyond that share, current conditions, and year effects (F = 7.09, p = 0.003), so the language carries residual soft information as well."
  - q: "Which text channels predict next-year local price changes?"
    a: "Disclosed property-condition risk predicts weaker next-year local price-index changes, and buyer-competition language predicts stronger ones, after controlling for distressed-sale composition."
  - q: "Why is housing a good setting for studying price discovery?"
    a: "Assets are heterogeneous, trade infrequently, and benchmark prices are estimated from transactions that close with delay, while intermediaries describe each asset publicly when it is brought to market. That combination lets us observe information at the listing stage and compare it with benchmarks formed later."
---
How does price discovery work when assets are heterogeneous, trade infrequently, and the benchmark price is estimated from transactions that close with a delay? Equity markets reveal information through continuous trading. Housing does not have that. What it has instead is a public description of every asset at the moment it comes to market, written by an intermediary who knows the property and the local conditions. This paper asks what that description reveals before transaction-based benchmarks update.

## Setting and measurement

The data are 63,067 transaction-level Atlanta MLS listings from 2007 to 2017, a window that spans the housing bust and recovery. Local market conditions are measured from listing-stage language using the [two-step method](/posts/auditable-ai-text-measures-two-step-method/) and aggregated to local-market-year cells.

## The measures behave like market-state signals

Before asking whether the text predicts anything, the paper checks that it tracks what it should. Seller-stress language rises in weak periods, is higher in local markets with lower prices and worse liquidity, and varies across areas within the same aggregate cycle. The last point matters: the text is not just a restatement of the national cycle but contains cross-sectional local information.

## The central result: a decomposition

The question is what listing language reveals before transaction benchmarks update, and the answer has two parts.

**Part of the signal is observable composition.** Some listings are flagged in structured fields as REO (bank-owned) or corporate-owned. Controlling for this distressed-sale share absorbs most of the seller-stress coefficient in regressions of next-year local price-index changes. In other words, a good deal of what the stress language was capturing is simply that more of the listings in a weak market are distressed, which a careful analyst could also see from the structured flags.

**But listing language is not exhausted by composition.** After controlling for the distressed-sale share, current conditions, and year effects, the text channels remain jointly significant predictors of next-year local price-index changes (F = 7.09, p = 0.003). Within that joint result, disclosed property-condition risk predicts weaker next-year changes, and buyer-competition language predicts stronger ones.

The interpretation is that listing remarks aggregate hard distress composition and residual soft information into a single public, real-time signal that appears before delayed transaction benchmarks record local deterioration. Supporting transaction-level tests show that the same remarks are capitalized into individual sale prices, which ties the aggregate finding to the pricing results in [Cheap Talk or Priced Information?](/posts/cheap-talk-or-priced-information-listing-remarks/).

## Caveats

The paper is careful about what the individual coefficients can bear. Once year effects, condition risk, and the distressed share are all included, the seller-stress coefficient on its own is not the headline; the claim rests on the joint test of the text channels and on text as a real-time aggregator of composition. The panel is annual and covers one metropolitan area, so the natural next steps are a higher-frequency panel and a second market. The companion paper [Listing Language and House Price Discovery](/posts/listing-language-house-price-discovery/) takes the second step with more than two million listings across three states.

## Why it matters

For anyone who prices or lends against illiquid assets, the result says that the public description written at listing is informative about where local prices are heading, and that part of that information is not available from structured data. For researchers, it offers a template for separating what text reveals about composition from what it reveals beyond it.

*Status: working paper, 2026. Numbers quoted are from the current draft and will be updated if the paper changes.*
