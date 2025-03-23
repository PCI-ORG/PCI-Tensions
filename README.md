# PCI-Tensions
_Last updated on March 23, 2025._

Website: [XXX](XXX)

Authors: [Weifeng Zhong](https://www.weifengzhong.com) and Kaiwei Hsu

---------------------------------------------

PCI Tentions is an open-source method that uses large language models (LLMs) to analyze CCP propaganda and develop early warning signals for a Taiwan Strait crisis—potentially a prelude to an invasion. The methodology is as follows:

1.	Collect the full text of the People’s Daily from the 1994–1996 training period and 2022–2024 test period and label a set of essential metadata for each article, such as publication date, title, content, and page number.
2.	Identify major events that occurred leading up to and during the 1995 Taiwan Strait Crisis (covered by the training period) and recent US-Taiwan diplomatic events in the test period. 
3.	For each newspaper article in the training period, build a set of quantitative indices to measure China-Taiwan relations by prompting an LLM with questions such as how the relationship between China and Taiwan is perceived and how the Chinese government views the Taiwanese government.  Then, aggregate each article-level index to a weekly sum and calculate the four-week moving average of that sum. 
4.	Assess how well the time series of the indices match or even predict the timing of the major events during the 1994–1996 period.
5.	Fine-tune the algorithm by repeating steps 3 and 4. Specifically, improve the indices by revising the LLM prompts to better capture a variety of topics most relevant to China-Taiwan tensions, such as military activities, US engagement, economic relations, culture exchange, and China’s emphasis on reunification and the One China principle. The goal of this step is to optimize the fit of the indices to the timing of the major events.
6.	Assess the model’s performance by deploying the model to People’s Daily articles in the 2022–2024 period, which covers major political events, including Taiwan’s diplomatic activities and China’s military escalations, across the Taiwan Straits. 

Please cite the source of the latest PCI-Tensions by the website: [X].
