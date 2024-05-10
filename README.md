# aluminium-prediction

## Overview

This project is generated with [Kedro](https://docs.kedro.org) and Kedro-Viz setup, which was generated using `kedro 0.19.4`.

Take a look at the hints in [readme/Kedro.md](https://github.com/KKobuszewski/aluminium-prediction/blob/main/readme/Kedro.md)
 




<br>
<br>


## Pipelines

### Data aquisition pipeline

This pipeline is located at [/src/aluminium_prediction/pipelines/aquisition](https://github.com/KKobuszewski/aluminium-prediction/tree/main/src/aluminium_prediction/pipelines/aquisition).

Aquisition pipeline collects data scraping them from websites or utilizing certain APIs.

Dataset for aluminium (LME cash) are collected from:

* [www.investing.com/](https://www.investing.com/commodities/aluminum-historical-data)

* [www.westmetall.com](https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Al_cash)

* [metals-api.com](https://metals-api.com/documentation)

* [finance.yahoo.com](https://finance.yahoo.com)