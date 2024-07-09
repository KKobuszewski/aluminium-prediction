

# Sources of aluminium prices

Datasets for **aluminium prices**[^1] are collected from:

* [www.investing.com/](https://www.investing.com/commodities/aluminum-historical-data)

* [www.westmetall.com](https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Al_cash)

* [metals-api.com](https://metals-api.com/documentation)

* [finance.yahoo.com](https://finance.yahoo.com)


[^1]: Probably 1-,2-,3- month contracts can be considered in the future.

<br>

Settlement price and 3-month price on [www.westmetall.com](https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Al_cash) correspond to LME official prices (for offer).

<br>

Price in the table on [www.investing.com/](https://www.investing.com/commodities/aluminum-historical-data) corresponds to LME 3-month closing price.

I'm not sure what's the correspondence between Open/High/Low prices and LME website data... Note that 'High' price can be lower than 'Low' price.


## Comparison of LME prices with westmetall.com

As we can see below, settlement price and 3-month price on [www.westmetall.com](https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Al_cash) correspond to LME official prices (for offer).

![westmetall_vs_lme](https://github.com/KKobuszewski/aluminium-prediction/blob/main/readme/LME_vs_Westmetall.png)

<br>

## Comparison of LME prices with investing.com

![investing_vs_lme](https://github.com/KKobuszewski/aluminium-prediction/blob/main/readme/LME_vs_investing.png)


Images can be added to markdown with HMTL
```
<p align="center">
  <img src="your_relative_path_here" width="350" title="hover text">
  <img src="your_relative_path_here_number_2_large_name" width="350" alt="accessibility text">
</p>
```