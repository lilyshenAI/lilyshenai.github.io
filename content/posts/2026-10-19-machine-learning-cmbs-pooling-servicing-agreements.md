---
title: "Are securitization contracts boilerplate? Machine learning on CMBS pooling and servicing agreements (JFQA, 2024)"
date: 2026-10-19
order: 8
description: "Summary of Information in Financial Contracts: Evidence from Securitization Agreements, with Brent W. Ambrose, Yiqiang Han, and Sanket Korgaonkar. A machine-learning comparison of the pooling and servicing agreements behind commercial mortgage-backed securities shows substantial variation across deals, underwriters, and time, partly explained by collateral, and correlated with later loan and bond performance."
tags: [CMBS, securitization, financial contracts, machine learning, text analysis]
papers: [ambrose-han-korgaonkar-shen-2024-psa]
faq:
  - q: "What is a pooling and servicing agreement?"
    a: "The pooling and servicing agreement (PSA) is the governing contract of a commercial mortgage-backed securities deal. It sets out how the loan pool is held, how the loans are serviced, how cash flows are distributed to bondholders, and what happens when loans become distressed."
  - q: "Are CMBS pooling and servicing agreements all the same?"
    a: "No. Using machine learning to compare the full text of PSAs, the paper documents substantial variation across agreements, both within and across underwriters and over time. Part of that variation reflects differences in loan collateral across deals."
  - q: "Does contract language predict CMBS performance?"
    a: "Differences in PSAs are correlated with ex-post loan and bond performance, which suggests that investors and analysts should examine the entire governing document rather than specific components."
---
Every commercial mortgage-backed securities (CMBS) deal is governed by a pooling and servicing agreement (PSA): a long contract that defines how the pooled loans are held and serviced, how cash is allocated among bond classes, and what the servicer may do when a loan goes bad. The received view among many market participants is that the PSA is boilerplate, copied deal to deal with only the names changed, and therefore not worth reading closely. This paper, with Brent Ambrose, Yiqiang Han, and Sanket Korgaonkar, published in the *Journal of Financial and Quantitative Analysis* in 2024, tests that view by reading the contracts with machines.

## What we did

We introduce a machine-learning comparison of PSAs. Instead of selecting a few clauses by hand, the method compares entire documents to one another and measures how far each agreement departs from the others. This produces a measure of contract variation that can be related to deal characteristics and to outcomes.

## What we found

The PSA is not boilerplate. We document substantial variation across agreements, both within and across underwriters and over time. A part of the variation is explained by differences in loan collateral across deals, which is what one would expect if contracts are tailored to the risks in the pool. The rest is not mechanical.

Most importantly, differences in PSAs are correlated with ex-post loan and bond performance. The contracts carry information about how the deal will fare that is not captured by the standard summary variables investors use.

## Why it matters

The practical lesson is that the whole governing document matters. Analysis that focuses on specific components, or that assumes the agreement is standardized, misses information that is priced in outcomes. For investors, the paper argues for reading the contract; for regulators and rating agencies, it argues for treating contract text as data. Methodologically, it is an early example of the approach I later applied to listing remarks: use machine learning to measure a document at scale, and then ask an economic question about what the measure predicts. The [two-step method](/posts/auditable-ai-text-measures-two-step-method/) I now use with large language models grew out of this work.
