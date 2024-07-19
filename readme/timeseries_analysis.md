# Analysis of timeseries

## Entropy of timeseries

* https://towardsdatascience.com/time-series-complexity-analysis-using-entropy-ec49a4aaff11

* [cran.r-project.org/RTransferEntropy/vignettes/transfer-entropy.html](https://cran.r-project.org/web/packages/RTransferEntropy/vignettes/transfer-entropy.html)

### Shannon entropy

Shannon entropy (Shannon 1948) states that for a discrete random variable J with probability distribution p(j), where $j \in J$ (the different outcomes the random variable J can take), the average number of bits required to optimally encode independent draws from the distribution of J can be calculated as
$$
H_J = - \sum_{j \in J} p(j) \cdot log \left(p(j)\right).
$$

How to extend it to contionuous random variables



## Mutual dependency between timeseries

We want to find/test simple way to measure impact of preceding data from one timeseries on another.


### Cross-correlation

See 
* https://en.wikipedia.org/wiki/Cross-correlation

<br>

### Transfer entropy

See possible implementations

* C/C++ (/Matlab): [code.google.com/transfer-entropy-toolbox](https://code.google.com/archive/p/transfer-entropy-toolbox/source/default/source)

* Python: [github.com/majianthu/transferentropy](https://github.com/majianthu/transferentropy)

* R: [cran.r-project.org/RTransferEntropy/vignettes/transfer-entropy.html](https://cran.r-project.org/web/packages/RTransferEntropy/vignettes/transfer-entropy.html)



Other useful resources

* https://xuk.ai/blog/copula-entropy.html

* https://proceedings.mlr.press/v180/garg22a/garg22a.pdf

* https://majianthu.github.io/ce1ta.pdf

* https://geoscienceletters.springeropen.com/articles/10.1186/s40562-018-0105-z#Sec24

<br>

### Mutual information