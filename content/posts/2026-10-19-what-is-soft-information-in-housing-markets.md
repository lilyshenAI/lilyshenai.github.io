---
title: "What is soft information in housing markets, and how can it be measured?"
date: 2026-10-19
order: 3
description: "Soft information is what a listing says that structured fields cannot: condition, character, seller circumstances, local demand. This explainer defines the term, contrasts it with hard information, and summarizes what my research finds when listing text is measured with machine learning: it is priced, it changes marketing time, and it moves before price indices do."
tags: [soft information, housing markets, listing remarks, explainer, hedonic pricing]
papers: [shen-ross-2021-property-description, shen-springer-2022-odd-one-out, shen-2026-cheap-talk, shen-2026-soft-information-price-discovery]
faq:
  - q: "What is the difference between hard and soft information in real estate?"
    a: "Hard information is quantifiable and verifiable: bedrooms, bathrooms, square footage, lot size, year built, tax records. Soft information requires context or judgment to interpret and is hard to codify: the condition and character of a home, the seller's circumstances, and local demand as described in the listing remarks written by the agent."
  - q: "Is soft information in listing text actually priced?"
    a: "Yes. In Shen and Ross (Journal of Urban Economics, 2021), a one-standard-deviation increase in text-based uniqueness raises sale price by 15 percent in a hedonic model and 10 percent in a repeat-sales model. In the 2026 working paper Cheap Talk or Priced Information?, residual listing information is associated with 7.7 percent higher sale prices and adverse disclosure with 17.4 percent lower sale prices."
  - q: "Why do house price indices need soft information?"
    a: "Because an index that ignores unobserved quality mixes quality changes with price changes. Shen and Ross (2021) find that an annual hedonic index without the text measure overstates prices by 10 to 23 percent and mistimes the post-recession stabilization of housing prices."
  - q: "Is listing language the same as market sentiment?"
    a: "No. Listing language is typed information about specific properties and transactions: disclosure, condition, urgency, competition. It can be aggregated into market signals, but each signal has an economic meaning and can be traced to phrases, which generic sentiment scores cannot."
---
## Hard versus soft information

The banking literature draws the distinction clearly. Hard information is quantifiable, verifiable, and can be transmitted without losing meaning: a credit score, an income figure, a loan-to-value ratio. Soft information requires context and judgment to interpret and is difficult to codify: a loan officer's impression of a borrower, a sense of how a business is run (Stein, 2002; Liberti and Petersen, 2019).

Housing has the same divide. The hard information is in the structured fields of a Multiple Listing Service (MLS) record and in tax rolls: bedrooms, bathrooms, square footage, lot size, year built, sale history. The soft information is in what the listing agent writes: "meticulously maintained," "needs TLC," "sold as-is," "estate sale," "multiple offers received," "bring all offers." For most of the history of the market, this information lived in conversations between agents and buyers. The MLS remarks field turns it into a written, public, time-stamped record, and that record is what machine learning can measure.

## Why soft information is economically interesting

Three reasons.

**It is valued.** Two houses with identical hard characteristics can differ by a great deal in condition, layout, light, and finish. Buyers pay for the difference. A hedonic model that sees only the hard fields attributes that payment to noise or, worse, to the wrong variables.

**It is strategic.** Sellers and their agents choose what to say. Disclosure law makes some adverse statements costly to omit, and the market may discount vague language. So the text is not a neutral description; it is a message in a game, which is why the right null hypothesis is that it is cheap talk.

**It is early.** Remarks are written when a property is brought to market, before bargaining, before closing, and long before a transaction-based price index can incorporate the sale. If the text contains information about local market conditions, it is available months ahead of the benchmarks that lenders and policymakers watch.

## Four ways I have measured it

**Uniqueness relative to neighbors.** In [Shen and Ross (2021)](/posts/information-value-property-descriptions-machine-learning/), a machine-learning model reads property descriptions and measures how unusual each description is relative to nearby listings. A one-standard-deviation increase in this measure raises sale price by 15 percent in a hedonic model and 10 percent in a repeat-sales model. An annual hedonic index that ignores the measure overstates prices by 10 to 23 percent and mistimes the stabilization after the Great Recession.

**Market uniqueness versus universal uniqueness.** In [Shen and Springer (2022)](/posts/property-uniqueness-selling-time-and-price/), we separate being unusual relative to homes on the market at the same time from being unusual relative to the submarket as a whole. A one-standard-deviation increase in market uniqueness raises sale price by 13 percent ($48,490) at the cost of 1.7 extra days on the market; universal uniqueness raises price 11 percent ($41,030) at a 3-day delay.

**Economic categories of listing language.** In [Cheap Talk or Priced Information? (2026)](/posts/cheap-talk-or-priced-information-listing-remarks/), an LLM organizes the language of 63,067 Atlanta listings into auditable categories. Residual information is associated with 7.7 percent higher sale prices and 2.5 fewer days on market; adverse disclosure with 17.4 percent lower sale prices; urgency language with 4.7 percent lower sale prices but no distinct change in marketing time.

**Aggregated market signals.** In [Soft Information and Price Discovery in Illiquid Asset Markets (2026)](/posts/soft-information-price-discovery-illiquid-assets/), the same listings are aggregated to local-market-year cells. Seller-stress language rises in weak periods and in weaker local markets. Much of its predictive power for next-year price-index changes reflects the share of distressed sales, but the text channels remain jointly significant after that composition is controlled (F = 7.09, p = 0.003). A companion paper extends the approach to more than two million listings across the Carolinas and Georgia.

## What soft information is not

It is not sentiment. Generic positive-or-negative scores throw away the economic structure that makes listing text useful: a listing can be enthusiastic and still disclose a foundation problem. It is not a substitute for hard information; the text measures add to hedonic controls rather than replacing them. And it is not free of strategy, which is why the measurement has to be designed so that the categories can be audited phrase by phrase and tested against bargaining outcomes, not only prices.

## Practical implications

Automated valuation models and appraisals that read only structured fields leave a large, systematic component of value unmeasured. Price indices can be improved by controlling for text-based quality. Lenders and index providers can observe local market deterioration in listing language before it appears in closed transactions. And for agents, the remarks field is not decoration: what is said, and what is disclosed, shows up in the sale price.

### References outside my own work

Liberti, J. M., & Petersen, M. A. (2019). Information: Hard and soft. *Review of Corporate Finance Studies*, 8(1), 1–41.
Stein, J. C. (2002). Information production and capital allocation: Decentralized versus hierarchical firms. *Journal of Finance*, 57(5), 1891–1921.
