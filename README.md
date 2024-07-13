# aluminium-prediction

## Overview

This project was partly generated by [Kedro](https://docs.kedro.org) with Kedro-Viz setup, which was generated using `kedro 0.19.4`.

Take a look at the hints in [readme/Kedro.md](https://github.com/KKobuszewski/aluminium-prediction/blob/main/readme/kedro.md)

<br>
<br>

## Problem statement

We want to predict future values of function $y(t)$ that can depend on past values of some other functions $x_1, x_2, \ldots, x_m$ in the past as well as on the past values of $y$ itself.

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
y(t+\Delta t) \\ y(t+2\Delta t) \\ \vdots \\ y(t+l\Delta t) 
\end{array}\right]
$$

This unknown mapping will be approximated using supervised machine learing methods, i. e. neural networks.
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


## Neural networks

https://medium.com/@srmousavi25/how-to-fix-a-common-mistake-in-lstm-time-series-forecasting-4d4d51d9948f


