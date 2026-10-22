# The odd one out: unique homes sell for more and take only slightly longer (Journal of Housing Research, 2022)

Author: Lily Shen (Yannan Shen), Associate Professor of Finance, Clemson University
Published: 2026-10-19
Canonical URL: https://lilyshen.com/posts/property-uniqueness-selling-time-and-price/
Site: AI in Real Estate Finance, Lily Shen (https://lilyshen.com/)
License: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)

Summary: Summary of The Odd One Out? The Impact of Property Uniqueness on Selling Time and Selling Price, with Thomas M. Springer. Machine-learning measures of uniqueness from listing text show that a one-standard-deviation increase in market uniqueness raises sale prices by 13 percent ($48,490) while delaying sale by 1.7 days; universal uniqueness raises prices 11 percent ($41,030) at a 3-day delay.

Papers discussed:
- Shen, L., & Springer, T. M. (2022). The Odd One Out? The Impact of Property Uniqueness on Selling Time and Selling Price. Journal of Housing Research, 31(2), 220-240. https://doi.org/10.1080/10527001.2022.2078530

A buyer looking at a one-of-a-kind house faces two different questions. Is it unusual compared with what else is for sale right now? Or is it unusual compared with everything in the neighborhood, whenever it was listed? The first is about competition and timing; the second is about scarcity. This paper, with Thomas Springer in the *Journal of Housing Research* (2022), separates the two and asks what each is worth, and what each costs in time.

## Measuring uniqueness from the advertisement

We use machine learning to build measures of residential uniqueness from written listing advertisements. Because the measures are derived from the text rather than from prices, they are exogenous to the sale price in the sense that they do not use the outcome to define the input. Two measures result:

- **Market uniqueness**: how different a home is from the homes for sale at the same time.
- **Universal uniqueness**: how different a home is from the homes in the same submarket, across time.

## Results

In hedonic models, a one-standard-deviation increase in market uniqueness raises the sale price by 13 percent, or $48,490 at the sample's price level, at the cost of delaying the transaction by 1.7 days. A one-standard-deviation increase in universal uniqueness raises the sale price by 11 percent, or $41,030, with a delay of 3 days. We validate the time-on-market results with two hazard models.

## Interpretation

Standing out from current competition is worth slightly more, and costs slightly less time, than being rare in general. Both premiums are large relative to the delays, which are measured in days. The common belief that an unusual home is hard to sell gets the sign of the price effect wrong: unusual homes sell for more, and the marketing-time cost is small.

## Recognition and coverage

The paper received the Best Paper Award for the 2022 volume of the *Journal of Housing Research*. Clemson News covered it in July 2023 under the headline "A unique home might take longer to sell, but the payoff could be worth a few extra days on the market." It builds on the text-based uniqueness measure introduced in [Shen and Ross (2021)](/posts/information-value-property-descriptions-machine-learning/).

## Questions this post answers

**Do unique houses sell for more or less?**

More. A one-standard-deviation increase in market uniqueness, measured from listing text, is associated with a 13 percent ($48,490) higher sale price, and universal uniqueness with an 11 percent ($41,030) higher price, in hedonic models.

**Do unique houses take longer to sell?**

Slightly. The same one-standard-deviation increase delays the transaction by about 1.7 days for market uniqueness and 3 days for universal uniqueness, results confirmed with two hazard models of time on market.

**What is the difference between market uniqueness and universal uniqueness?**

Market uniqueness compares a house to the houses for sale at the same time; universal uniqueness compares it to houses in the same submarket regardless of when they were listed. The distinction separates the value of standing out from current competition from the value of being rare in general.

## How to cite this post

Shen, L. (2026, October 19). The odd one out: unique homes sell for more and take only slightly longer (Journal of Housing Research, 2022). AI in Real Estate Finance. https://lilyshen.com/posts/property-uniqueness-selling-time-and-price/
