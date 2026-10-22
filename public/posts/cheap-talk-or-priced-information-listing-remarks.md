# Cheap talk or priced information? What listing remarks do to prices, bargaining, and marketing time

Author: Lily Shen (Yannan Shen), Associate Professor of Finance, Clemson University
Published: 2026-10-19
Canonical URL: https://lilyshen.com/posts/cheap-talk-or-priced-information-listing-remarks/
Site: AI in Real Estate Finance, Lily Shen (https://lilyshen.com/)
License: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)

Summary: Summary of my working paper Cheap Talk or Priced Information? In 63,067 Atlanta MLS transactions, residual listing information is associated with 7.7 percent higher sale prices and 2.5 fewer days on market, adverse disclosure with 17.4 percent lower sale prices, and urgency language with 4.7 percent lower sale prices, showing that remarks carry priced information beyond structured MLS fields.

Papers discussed:
- Shen, L. (2026). Cheap Talk or Priced Information? Listing Language and Housing Transaction Outcomes. Working paper, SSRN, June 2026. https://papers.ssrn.com/abstract=7097938

Economists have a ready null hypothesis for what a seller says about the thing being sold: cheap talk. Statements are costless, unverifiable, and self-interested, so a rational buyer should ignore them. Listing remarks are a natural place to test this, because they are public, written before any bargaining, and attached to transactions whose outcomes we can observe. If remarks are cheap talk, they should not show up in prices.

## Data and method

The sample is 63,067 Atlanta MLS transactions from 2007 to 2017. An LLM scans the corpus and organizes listing language into auditable property and transaction categories, following the [two-step method](/posts/auditable-ai-text-measures-two-step-method/): the model discovers the vocabulary and a frozen vocabulary does the scoring. The main categories are residual information (property content beyond the structured fields), adverse disclosure, urgency pressure, and market stress. All regressions are within search-area-year markets and conditional on a saturated hedonic specification, so the comparison is between similar homes in the same local market and year.

## Results by category

| Category (one standard deviation) | Sale price | List price | Sale-to-list ratio | Days on market |
|---|---|---|---|---|
| Residual information | +7.7% | +7.6% | | 2.5 fewer |
| Adverse disclosure | −17.4% | −16.7% | −0.7% | |
| Urgency pressure | −4.7% | −4.4% | no distinct effect | no distinct effect |

Residual information is priced on both sides of the transaction: it raises the list price and the sale price by about the same amount and shortens marketing time. Adverse disclosure lowers both prices and also lowers the sale-to-list ratio, so disclosed problems are discounted at listing and then discounted again in bargaining. Urgency language lowers the list and sale price but does not produce a distinct bargaining adjustment or a faster sale, which suggests the seller's constraint is priced in up front rather than extracted by buyers.

Market-stress language rises during the housing crisis and is more prevalent where local prices are lower, marketing time is longer, and discounts are larger. That pattern is the starting point for the aggregate analysis in [Soft Information and Price Discovery in Illiquid Asset Markets](/posts/soft-information-price-discovery-illiquid-assets/).

## Robustness

Two concerns deserve attention. First, the text could proxy for unobserved quality that a repeat-sales design would absorb; repeat-sale specifications, and specifications with listing-agent fixed effects, imply more conservative but still economically meaningful price differences. Second, the categories could be relabelings of a handful of frequent words; residual information and adverse disclosure retain pricing content after controlling for LASSO-selected tokens.

## What the results mean

Remarks are not cheap talk. They reveal priced property and transaction information beyond structured MLS fields, and the method identifies the economic categories in which that information appears. For automated valuation models, the implication is that the remarks field carries a component of value that structured inputs cannot recover. For sellers and agents, disclosure is costly in price but is reflected consistently from list to close. For researchers, the design shows how to test a cheap-talk null with text at scale while keeping every measure auditable.

*Status: working paper, posted on SSRN, June 2026. Numbers quoted are from the posted version.*

## Questions this post answers

**Do listing remarks affect the sale price of a house?**

In 63,067 Atlanta MLS transactions from 2007 to 2017, a one-standard-deviation increase in residual listing information is associated with 7.7 percent higher sale prices and 7.6 percent higher list prices, conditional on a saturated hedonic specification and search-area-year fixed effects. Adverse disclosure is associated with 17.4 percent lower sale prices.

**Does urgency language such as motivated seller lower the price?**

Urgency pressure is associated with 4.7 percent lower sale prices and 4.4 percent lower list prices, but not with a distinct sale-to-list adjustment or with shorter marketing time. The discount is set at listing rather than extracted in bargaining.

**How was the listing language classified?**

An LLM scans the corpus and organizes listing language into auditable property and transaction categories; a fixed vocabulary then scores each listing, so every score can be traced to phrases. The categories retain pricing content after LASSO-selected token controls.

## How to cite this post

Shen, L. (2026, October 19). Cheap talk or priced information? What listing remarks do to prices, bargaining, and marketing time. AI in Real Estate Finance. https://lilyshen.com/posts/cheap-talk-or-priced-information-listing-remarks/
