# Property descriptions carry priced information that hedonic models miss (Journal of Urban Economics, 2021)

Author: Lily Shen (Yannan Shen), Associate Professor of Finance, Clemson University
Published: 2026-10-19
Canonical URL: https://lilyshen.com/posts/information-value-property-descriptions-machine-learning/
Series: AI in Real Estate Finance. Site: Lily Shen (https://lilyshen.com/)
License: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)

Summary: Summary of Information Value of Property Description: A Machine Learning Approach, with Stephen L. Ross. A machine-learning measure of the soft information in listing text raises sale prices by 15 percent per standard deviation in a hedonic model and 10 percent in a repeat-sales model, and price indices that ignore it overstate prices by 10 to 23 percent and mistime the post-recession stabilization.

Papers discussed:
- Shen, L., & Ross, S. L. (2021). Information Value of Property Description: A Machine Learning Approach. Journal of Urban Economics, 121, 103299. https://doi.org/10.1016/j.jue.2020.103299

Hedonic pricing is the workhorse of housing economics: regress price on a list of measurable characteristics and read off what each one is worth. The trouble is that the list is short and the house is not. Everything that makes a home more or less desirable than its bedroom count implies goes into the residual. This paper, written with Stephen Ross and published in the *Journal of Urban Economics* in 2021, asks how much of that residual can be recovered from the words the listing agent wrote.

## What we measured

The idea is to treat the property description as data. A machine-learning model reads the text of each listing and produces a measure of how unique the property is relative to comparable homes, based on the "soft" content of the description rather than the structured fields. Textual descriptions turn out to contain information that traditional hedonic attributes cannot capture.

## What we found

A one-standard-deviation increase in text-based uniqueness is associated with a 15 percent higher sale price in a hedonic model and a 10 percent higher price in a repeat-sales model. The repeat-sales result matters because it differences out time-invariant property characteristics: the text is not simply proxying for fixed features the hedonic model omitted.

## Why price indices should care

The second contribution is about measurement at the market level. An annual hedonic price index that ignores the text-based measure of unobserved quality overstates real estate prices by between 10 and 23 percent, and it mistimes the stabilization of housing prices following the Great Recession. Similar but smaller effects appear in a repeat-sales index. The mechanism is composition: when the mix of homes coming to market changes over the cycle, an index that cannot see quality attributes the shift to prices.

## Why it matters

For automated valuation models and appraisal, the paper shows that a large, systematic component of value is sitting in a field most models do not read. For index construction, it shows that the omission is not neutral noise but a cyclical bias. And for the research program that followed, it established that listing text could be turned into an economic measure that survives both hedonic and repeat-sales scrutiny. Later work separates [market uniqueness from universal uniqueness](/posts/property-uniqueness-selling-time-and-price/) and organizes the text into [economic categories](/posts/cheap-talk-or-priced-information-listing-remarks/).

The underlying natural-language method was the subject of a Clemson University technology disclosure (2018), and the study was covered by Clemson News in February 2020 under the headline "Clemson study employs AI to decipher 'soft' features of a home's value."

## Questions this post answers

**What does the Shen and Ross (2021) paper find?**

Textual property descriptions contain information that traditional hedonic attributes cannot capture. A one-standard-deviation increase in a property's text-based uniqueness raises its sale price by 15 percent in a hedonic model and 10 percent in a repeat-sales model.

**How do property descriptions affect house price indices?**

An annual hedonic price index that ignores the text-based measure of unobserved quality overstates real estate prices by 10 to 23 percent and mistimes the stabilization of housing prices after the Great Recession. The repeat-sales index shows similar but smaller distortions.

**Where was the paper published?**

Journal of Urban Economics, volume 121, 2021, article 103299, DOI 10.1016/j.jue.2020.103299. Coauthor: Stephen L. Ross, University of Connecticut.

## How to cite this post

Shen, L. (2026, October 19). Property descriptions carry priced information that hedonic models miss (Journal of Urban Economics, 2021). AI in Real Estate Finance. https://lilyshen.com/posts/information-value-property-descriptions-machine-learning/
