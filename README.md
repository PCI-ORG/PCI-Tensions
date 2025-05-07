# PCI-Tensions
_Last updated on May 7, 2025._

Website: [policychangeindex.org/projects/pci-tensions](https://policychangeindex.org/projects/pci-tensions)

Authors: Kaiwei Hsu and [Weifeng Zhong](https://www.weifengzhong.com)

---------------------------------------------

## Introduction

PCI Tentions is an open-source method that uses large language models (LLMs) to analyze CCP propaganda and develop early warning signals for a Taiwan Strait crisis --- potentially a prelude to an invasion. The methodology is as follows:

1. Collect the full text of the _People's Daily_ from the 1994–1996 training period and 2022–2024 test period and label a set of essential metadata for each article, such as publication date, title, content, and page number.
2. Identify major events that occurred leading up to and during the 1995 Taiwan Strait Crisis (covered by the training period) and recent US-Taiwan diplomatic events in the test period.
3. For each newspaper article in the training period, build a set of quantitative indices to measure China-Taiwan relations by prompting an LLM with questions such as how the relationship between China and Taiwan is perceived and how the Chinese government views the Taiwanese government.  Then, aggregate each article-level index to a weekly sum and calculate the four-week moving average of that sum.
4. Assess how well the time series of the indices match or even predict the timing of the major events during the 1994–1996 period.
5. Fine-tune the algorithm by repeating steps 3 and 4. Specifically, improve the indices by revising the LLM prompts to better capture a variety of topics most relevant to China-Taiwan tensions, such as military activities, US engagement, economic relations, culture exchange, and China's emphasis on reunification and the One China principle. The goal of this step is to optimize the fit of the indices to the timing of the major events.
6. Assess the model's performance by deploying the model to _People's Daily_ articles in the 2022–2024 period, which covers major political events, including Taiwan's diplomatic activities and China's military escalations, across the Taiwan Strait.

This repository provides the code to implement steps 2-6 of the PCI-Tensions workflow. Due to copyright considerations, we do not provide the training data. However, the same workflow can be applied to text classification tasks with binary labels and temporal information, such as publication dates. Interested researchers can use their own data for replication.

## Replication Guide

Please follow the following stepes to replicate this study:

1. Prepare the _People's Daily_ data by following the step 1 mentioned in the Introduction. Save the data as `input.csv` (as referenced in `01_Data_processing.py`).
2. Run `01_Data_processing.py` to process the data.
3. Run `02_LLM.py` with an active Open AI key (not included) to execute the LLM-based algorithm.
4. Run `03_Analysis.ipynb` to visualize the results of the model.

## Citing the PCI-Tensions

Please cite the source of the latest PCI-Tensions by the website: https://policychangeindex.org.

For academic work, please cite the following research paper:

- Kaiwei Hsu and Weifeng Zhong. 2025. "Predicting Taiwan Strait Crises Using Propaganda: A New Open-Source Method." [Mercatus Policy Brief](https://www.mercatus.org/research/policy-briefs/predicting-taiwan-strait-crises-using-propaganda-new-open-source-method).

Please stay tune for more research products based on/using this algorithm.
