# CryptoProphet

## Objetive

Can influencers collectively predict Bitcoin price?

> That's what we wanna find out!

## Methodology

Our hypothesis is that crypto influencers have a predictive (or manipulative) power over Bitcoin price.

So we've extracted a bunch of tweets from over 30 influencers.

We've combined that with data from Yahoo Finance (hourly bitcoin price in comparison to USD).

Then created some features, such as:

1. Bitcoin price in 1, 2, and 12 hours in the future
2. Text embeddings from the tweets (contextual information)
3. Technical Analysis (on going)

After that we've trained simple XGBoost models.

1. Regressor: to predict the exact price of Bitcoin in the given time span
2. Classifier: to predict in which change quantile Bitcoin would be (also within the future time span)

## Results

TBD

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