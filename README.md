# aluminium-prediction

## Overview

This project was partly generated by [Kedro](https://docs.kedro.org) with Kedro-Viz setup, which was generated using `kedro 0.19.4`.

Take a look at the hints in [readme/Kedro.md](https://github.com/KKobuszewski/aluminium-prediction/blob/main/readme/kedro.md)

<br>
<br>

## Project plan

See project diagram [here](https://github.com/KKobuszewski/aluminium-prediction/blob/main/readme/project_plan.darwio.svg).

![](https://github.com/KKobuszewski/aluminium-prediction/blob/main/readme/project_plan.darwio.svg)

<br>
<br>

## Problem statement

We want to predict future values of function $y(t)$ and we assume that it can depend on past values of some other functions $x_1, x_2, \ldots, x_m$ in the past as well as on the past values of $y$ itself.

In discretized form (with constant timestep $\Delta t$) we can write it as mapping:

$$
\lim\limits_{k\to\infty}
\left[\begin{array}{c}
x_{1}(t) \\
x_{1}(t-\Delta t)\\
x_{1}(t-2\Delta t)\\
\vdots\\
x_{1}(t-k\Delta t)\\
x_{2}(t)\\
x_{2}(t-\Delta t)\\
x_{2}(t-2\Delta t)\\
\vdots\\
x_{2}(t-k\Delta t)\\
\vdots\\
\vdots\\
x_{m}(t)\\
x_{m}(t-\Delta t)\\
x_{m}(t-2\Delta t)\\
\vdots\\
x_{m}(t-k\Delta t)\\
y(t)\\
y(t-\Delta t)\\
y(t-2\Delta t)\\
\vdots\\
y(t-k\Delta t)
\end{array}\right]
\qquad\mapsto\qquad
\left[\begin{array}{c}
y(t+\Delta t) \\
y(t+2\Delta t) \\
\vdots \\
y(t+l\Delta t) \\
\end{array}\right]
\qquad\qquad k,l \in \mathbb{Z}_+
$$

This unknown mapping will be approximated using supervised machine learing methods, i. e. neural networks.

See more [here](https://github.com/KKobuszewski/aluminium-prediction/blob/main/readme/problem_statement.md).

<br>
<br>


## Pipelines

### Data aquisition pipeline

This pipeline is located at [/src/aluminium_prediction/pipelines/aquisition](https://github.com/KKobuszewski/aluminium-prediction/tree/main/src/aluminium_prediction/pipelines/aquisition).

Aquisition pipeline collects data scraping them from websites or utilizing certain APIs and resulting dataset contains information about:
* [**aluminium prices**](https://github.com/KKobuszewski/aluminium-prediction/blob/main/readme/aluminium_prices_sources.md),
* [**aluminium production**](https://international-aluminium.org/statistics/primary-aluminium-production/)
* [**indicators of consumption**](https://github.com/KKobuszewski/aluminium-prediction/blob/main/readme/indicators.md#indicators-of-consumption)
* [**indicators of market uncertainity**](https://github.com/KKobuszewski/aluminium-prediction/blob/main/readme/indicators.md#indicators-of-market-uncertainity)
* [**Indicators of trade**](https://github.com/KKobuszewski/aluminium-prediction/blob/main/readme/indicators.md#indicators-of-trade)
* USD/EUR ???  <!--[**USD/EUR ???**]()-->

In order to aim most "interesting" variables the dependencies (information transfer / causal relationships) between different timeseries should be determined -- i. e. using [cross-corelation](https://github.com/KKobuszewski/aluminium-prediction/blob/main/readme/timeseries_analysis.md#cross-correlation) or [transfer entropy](https://github.com/KKobuszewski/aluminium-prediction/blob/main/readme/timeseries_analysis.md#transfer-entropy).

<br>

**This part should also produce raport about current data.**

<br>

### Data preparation & augmentation pipeline

### Model training pipeline

### Inference pipeline

### Model update pipeline

## API

Should return reports as http websites.

Raports should contain current most important price indicators and price predictions.


## Potential issues

1. Too small dataset
    * In [this article](https://medium.com/@mskmay66/transformers-vs-lstm-for-stock-price-time-series-prediction-3a26fcc1a782) LSTMs with ~200.000 parameters and transformers with ~20.000 parameters are trained, while we can use data from 2000-4000 days.
    * Probably more than one variable should be considered (not only aluminium prices). <---- Dimensionality reduction? Autoencoder? PCA? [Granger Causality Test](https://en.wikipedia.org/wiki/Granger_causality)? [**Transfer Entropy**](https://en.wikipedia.org/wiki/Transfer_entropy)?
    * Transformer NN demand less parameters in comparison with LSTM. Some convolution layers can also improve performance (see [here](https://medium.com/@mskmay66/deep-learning-and-stock-time-series-data-ff6a75cfddd9)).
    * As we can have data from different sources (which sligthly differ) we can produce multiple different time series

2. We don't expect data to be stationary in time?
   * Model should not be trained with earlier data to be tested with later data/predict new data
   * How to choose data 'points' for test/valid/train from dataset? Randomly? K-fold? https://stats.stackexchange.com/questions/14099/using-k-fold-cross-validation-for-time-series-model-selection


## Literature

### Transfer of "information" between timeseries

We can aim two issues concernig information/entropy/complexcity of timeseries:

1. How much information is in given timeseries?
2. We want to describe to determine if adding new timeseries to dataset can improve inference performace i. e. if there is information transfer between two series.

Measures for first issuse can be [Approximate Entropy](https://en.wikipedia.org/wiki/Approximate_entropy) (AppEn), [Sample Entropy](https://en.wikipedia.org/wiki/Sample_entropy) (SampEn) or Renyi Entropy. Second issue can be solved using some measures of information transfer, i. e. [Transfer Entropy](https://en.wikipedia.org/wiki/Transfer_entropy),[^1]? 

[^1]: [Cross-entropy](https://en.wikipedia.org/wiki/Cross-entropy) is somehow different, because it is defined on two probability distributions and not timeseries, but in [EntopyHub](https://www.entropyhub.xyz/python/Functions/Cross.html) are some functions for estimation of entropy between two univariate data sequences.

Python implementaion of entropy algorithms is provided by [EntropyHub](https://www.entropyhub.xyz/python/Functions/Base.html)

Usage of AppEn in financial timeseries was described in [S. Pincus, R. E. Kalman, _Irregularity, volatility, risk, and financial market time series_](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC518821/).


[Transfer Entropy](https://en.wikipedia.org/wiki/Transfer_entropy) is most promising approach to measuring transfer of information between timeseries. It was introduced in [T. Schreiber, Phys. Rev. Lett. 85 (2000) 461.](https://arxiv.org/pdf/nlin/0001042) and described in wider context by [P. Jizba, H. Kleinert, M. Shefaat _Rényi's information transfer between financial time series_ (Physica A: Statistical Mechanics and Its Applications. 391 (10): 2971–2989.)](https://arxiv.org/pdf/1106.5913). Python implementaion is provided by [copent](https://pypi.org/project/copent/) package, but olny as an approximation in terms of Coupola entropy (see). Github repository for copent [here](https://github.com/majianthu/pycopent/blob/master/copent/copent.py).


### Neural networks

Example applications of neural networks in financial time series forecasting are available, i. e.:

* https://medium.com/@srmousavi25/how-to-fix-a-common-mistake-in-lstm-time-series-forecasting-4d4d51d9948f

* https://medium.com/@mskmay66/deep-learning-and-stock-time-series-data-ff6a75cfddd9

* https://medium.com/@mskmay66/transformers-vs-lstm-for-stock-price-time-series-prediction-3a26fcc1a782

### Forecating models

[gluonts](https://ts.gluon.ai/stable/index.html), https://ts.gluon.ai/stable/tutorials/advanced_topics/howto_pytorch_lightning.html

https://github.com/thuml/Time-Series-Library/tree/main

[uni2ts/moirai](https://github.com/SalesforceAIResearch/uni2ts/blob/main/example/moirai_forecast_pandas.ipynb), https://huggingface.co/Salesforce/moirai-1.0-R-large

[Time Series Transformer](https://huggingface.co/docs/transformers/model_doc/time_series_transformer#transformers.TimeSeriesTransformerForPrediction) (TST), https://huggingface.co/blog/time-series-transformers

$$
\begin{array}{ccccc}
 & \text{TST} & \text{moirai} & \text{TSlib}\\
\text{static real features} & yes & no & no & \text{data with lower sampling (i.e GDP)}\\
\text{(past) dynamic real features} & no & \text{prediction only} & no & \text{features we don't want to predict}\\
\\
\end{array}
$$

### Information about deployment

https://gitlab.com/inzynier-ai/

