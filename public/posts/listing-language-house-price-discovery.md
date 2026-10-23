# Listing language predicts house price growth months before price indices move

Author: Lily Shen, Associate Professor of Finance, Clemson University
Published: 2026-10-19
Canonical URL: https://lilyshen.com/posts/listing-language-house-price-discovery/
Series: AI in Real Estate Finance. Site: Lily Shen (https://lilyshen.com/)
License: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)

Summary: Summary of my working paper Listing Language and House Price Discovery. From 2.03 million MLS listings, AI-assisted measures of demand heat, seller pressure, and asset frictions predict sale prices, marketing time, and six-month county price-index growth, and the design replicates in Georgia, a market never used for estimation.

Papers discussed:
- Shen, L. (2026). Listing Language and House Price Discovery. Working paper.

House price indices are the thermometers of the housing market, and they read late. An index is built from closed transactions, so it can only register a sale after marketing, bargaining, and the possibility of a failed listing have all been resolved. This paper asks whether the text that agents write when a property is listed reveals local conditions earlier, and whether that information is specific enough to be useful.

## Data

The corpus is 2.03 million MLS listings. The primary sample is 0.81 million listings from North and South Carolina on an aligned 2001 to 2019 coverage window. A further 0.83 million Georgia listings are held out entirely and used as an out-of-sample market. Remarks are written at listing and precede closing by a median of 84 days.

## Three typed signals, not one sentiment score

Using the [two-step method](/posts/auditable-ai-text-measures-two-step-method/), an LLM discovers the vocabulary for three economically interpretable categories, and a frozen vocabulary then scores every listing:

- **Demand heat**: language indicating buyer competition and strong demand.
- **Seller pressure**: language indicating urgency or constraint on the seller's side.
- **Asset frictions**: language indicating property-level problems that slow or discount a sale.

Each signal has an economic meaning and a predicted sign, which is what separates this from generic sentiment analysis.

## Listing-level results

In listing-level regressions with county-by-year and listing-agent fixed effects, demand-heat language predicts:

| Outcome | Demand-heat effect |
|---|---|
| Sale price | 1.5 percent higher |
| Days on market | 9.7 fewer |
| Discount from list price | 1.28 percentage points smaller |
| Probability of sale | 4.48 percentage points higher |

Seller-pressure and asset-friction language predict the opposite pattern: lower prices, longer marketing time, larger discounts, and lower sale probabilities. The signs line up with what each category should mean, and the agent fixed effects rule out the explanation that the results merely pick up which agents write enthusiastically.

## County-month results and forecasting

Aggregated to county-months, demand heat predicts 0.58 percentage points higher six-month growth in an MLS hedonic price index within state-month. In a holdout exercise over the 2015 to 2019 expansion, adding the text signal reduces forecast errors by 23 percent. A geographic reassignment test, in which text is reassigned across counties, removes the relation, as it should if the signal is local information rather than a statistical artifact.

## Replication in a market never used for estimation

The same procedure is run on Georgia, a market that entered none of the estimation steps. Demand heat predicts 0.43 percentage points higher six-month price growth there. The replication is the strongest evidence in the paper that what is portable is the measurement procedure, not a word list fitted to one place.

## What the paper does and does not claim

It claims that listing language is typed market information observed months before a transaction-based index can incorporate the corresponding sales, and that this information improves short-horizon forecasts of local price growth. It does not claim that text replaces a price index, or that any single phrase is decisive. The measures are built so that every score can be traced to phrases, and the vocabulary discovery respects the out-of-sample timing rules described in the methods post.

## Who should care

Lenders setting local credit terms, index providers, insurers, investors in single-family rental portfolios, and policymakers watching for local deterioration all currently rely on benchmarks that lag the market by a quarter or more. Listing text is public, high-frequency, and already collected. The paper shows how to read it.

*Status: working paper, 2026. Numbers quoted are from the current draft and will be updated if the paper changes.*

## Questions this post answers

**How far ahead of a house price index does listing language appear?**

In the paper's sample, listing remarks precede closing by a median of 84 days, and a transaction-based index can only incorporate a sale after it closes. Aggregated to county-months, demand-heat language predicts six-month hedonic-index growth.

**What are the three signals measured from listing text?**

Demand heat (language indicating buyer competition and strong demand), seller pressure (language indicating urgency or constraint on the seller side), and asset frictions (language indicating property-level problems that slow or discount a sale).

**Does the result hold outside the estimation sample?**

Yes. The procedure estimated on 0.81 million North and South Carolina listings replicates on 0.83 million Georgia listings never used for estimation: demand heat predicts 0.43 percentage points higher six-month price growth there, versus 0.58 in the primary sample.

## How to cite this post

Shen, L. (2026, October 19). Listing language predicts house price growth months before price indices move. AI in Real Estate Finance. https://lilyshen.com/posts/listing-language-house-price-discovery/
