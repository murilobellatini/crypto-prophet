# CryptoProphet 🧞💰

## Objetive

Can influencers collectively predict Bitcoin price?

> That's what we wanna find out!

## Overview

Our hypothesis is that crypto influencers have a predictive (or manipulative) power over Bitcoin price.

So we've extracted a bunch of tweets from over 30 influencers.

We've combined that with data from Yahoo Finance (hourly bitcoin price in comparison to USD).

Then created some features, such as:

1. Bitcoin price in 1, 2, and 12 hours in the future
2. Text embeddings from the tweets (contextual information)
3. Technical Analysis (on going)

After that we've trained simple XGBoost models.

1. `Regressor`: to predict the exact price of Bitcoin in the given time span
2. `Classifier`: to predict in which change quantile Bitcoin would be (also within the future time span)

## Results

The experiments below were fully executed.

Surprisingly, the notebook 8h gives the best result WITHOUT considering contextual information. It considers only Technical Analysis indicators. That's might be the case, because this data is less noisy than tweets.

Considering text, the best model is 8d, which predicts the output 3 quantiles (INCREASE, NEUTRAL or DECREASE) within a 12h timeframe. This look the mot promissing to keep up working on the Crypto Prophet based on tweets.

![Results](/img/results.PNG)

## How to run

This repo contains a custom package and exploratory analysis over jupyter notebooks.

Below you can check how to execute the Notebooks.

### Requirements

1. `Python>=3.6`
2. `pipenv` 

### Step-by-step

1. Create environment: `pipenv shell`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch jupyter notebooks: `jupyter notebook`
4. Check notebooks at will

### Extract More Tweets

Scrapping logic is based on Tweets available in influencer's timeline.

1. Access `config.yml`
2. Set parameter `infuencers` with a list of the target influencers' usernames on Twitter
3. Run main.py (with environment activated): `python main.py` 

## Methodology
### Our Data

The datasets we've used are available at the Google Drvie below.

Please as permission to access them (they are private).

https://drive.google.com/drive/folders/1AQH_GH9RjiX6mZzMKwiv-VG6vOz0AKPP

### Notebook's Index

Below an overview of the available Notebooks.

Their objective is described as well.

* `01_check_extracted_tweets.ipynb`: Check extracted tweets for the analysis (amount and influencers)
* `02_develop_crytpo_spotter.ipynb`: Identify mentioned coins on tweets (to use as features afterwards)
* `03_extract_txt_embedding.ipynb`: Clean and extract Text Embeddings from tweets using BERT Transformer.
* `04_extract_btc_price_history.ipynb`: Extract Bitcoin price data from Yahoo Finance API (hourly based :( )
* `05_generate_ta_kpis.ipynb`: Generate Technical Analysis KPI's.
* `06*_create_train_dataset.ipynb`: Preprocess data for training with three variants.
  * `a`: First version - Text Embeddings and other simple features
  * `b`: Technical Analysis - `a` and Technical Analysis KPI's 
  * `c`: Zero Shot Classification - `a` filtering only tweets about Crypto or Bitcoin
* `07*_train_xgboost_regressor.ipynb`: Train and assess results of XGBoost Regression model with two variants
  * `a`: First version - Text Embeddings and other simple features
  * `b`: Technical Analysis - `a` and Technical Analysis KPI's 
* `08*_train_xgboost_quantile_***.ipynb`:Train and assess results of XGBoost Classifier model with 
  * `a`: First version with 5Q2H (5 Quantiles and predictions in 2 hour ahead)
  * `b`: First version with 5Q1H (no tested due to time constraints...)
  * `c`: First version with 3Q2H
  * `d`: First version with 3Q1H
  * `f`: First version with 3Q12H
  * `g`: Zero Shot Classification 3Q2H