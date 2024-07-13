# Problem statement

## Connection to Volterra series

In more mathimatical language we are assuming that there exists an operator mapping all the past values of $\left[x_1~x_2~\ldots~x_m~y \right]$ to future value of $y$. Probably this operator can be expanded as Volterra (or Wiener) series.

For $y(t)$ dependent on single function $x(t)$ this Volterra series can be written as

$$
\begin{align}
y(t) &=h^{(0)}+\sum _{n=1}^{N}\int _{0}^{T \to \infty}\cdots \int _{0}^{T \to \infty}h^{(n)}(\tau _{1},\dots ,\tau _{n})\prod _{j=1}^{n}x(t-\tau _{j})\,d\tau _{j} = \\
&= h^{(0)} + \int_{\mathbb{R}_+} h^{(1)}(\tau_1)x(t-\tau_1) \, d\tau_1 +
\int_{\mathbb{R}^2_+} h^{(2)}(\tau_1, \tau_2)x(t-\tau_1)x(t-\tau_2) \,
d\tau_1 d\tau_2 + 
\int_{\mathbb{R}^3_+} h^{(3)}(\tau_1, \tau_2,
\tau_3)x(t-\tau_1)x(t-\tau_2)x(t-\tau_3) \, d\tau_1 d\tau_2 d\tau_3 + \ldots
\end{align}
$$

For $y(t)$ dependent on multiple functions $x_1(t),x_2(t), \ldots, x_m(t)$ this Volterra series should be written like following:

$$
\begin{align}
y(t) &= h^{(0)} +
\int_0^T d\tau_1 
\left[
\begin{array}{cccc}
h^{(1)}_1(\tau_1) & h^{(1)}_2(\tau_1) & \ldots & h^{(1)}_m(\tau_1)
\end{array}
\right]
\left[
  \begin{array}{c}
x_1(t-\tau_1)\\
x_2(t-\tau_1)\\
\ldots\\
x_m(t-\tau_1)
\end{array} 
\right] + \\
& + \int_0^T d\tau_1 \int_0^T d\tau_2 
\left[
\begin{array}{cccc}
h_{11}^{(2)}\left(\tau_{1},\tau_{2}\right) & h_{12}^{(2)}\left(\tau_{1},\tau_{2}\right) & \cdots & h_{1m}^{(2)}\left(\tau_{1},\tau_{2}\right)\\
h_{21}^{(2)}\left(\tau_{1},\tau_{2}\right) & h_{22}^{(2)}\left(\tau_{1},\tau_{2}\right) & \cdots & h_{2m}^{(2)}\left(\tau_{1},\tau_{2}\right)\\
\vdots & \vdots & \ddots & \vdots\\
h_{m1}^{(2)}\left(\tau_{1},\tau_{2}\right) & h_{m2}^{(2)}\left(\tau_{1},\tau_{2}\right) & \cdots & h_{mm}^{(2)}\left(\tau_{1},\tau_{2}\right)
\end{array}
\right]
\left[
  \begin{array}{c}
x_1(t-\tau_1)\\
x_2(t-\tau_1)\\
\ldots\\
x_m(t-\tau_1)
\end{array} 
\right]
\left[
\begin{array}{cccc}
x_1(t-\tau_2) & x_2(t-\tau_2) & \ldots & x_m(t-\tau_2)
\end{array}
\right] + \ldots
\end{align}
$$

and probably in vector $\left[\begin{array}{cccc}
x_1(t-\tau) & x_2(t-\tau) & \ldots & x_m(t-\tau)
\end{array}
\right]$ we could include dependence on $y(t-\tau)$.

In Volterra approach all integral kernels $h^{(i)}$ are unknown and have to be estimated from data, which can be more sophisticated than neural network training. Moreover, Volterra series expansion is computationally equivalent to 2-fully connected layer perceptron network (see Wary and Green (1994)[CITATION NEEDED] or [wikipedia](https://en.wikipedia.org/wiki/Volterra_series#Feedforward_network)).

However, some of these integral kernels $h^{(i)}$ as well as some of the functions $x_1(t),x_2(t), \ldots, x_m(t)$ are negligible, thus we want to remove


## Neural network utilization

![Input_vs_output](https://github.com/KKobuszewski/aluminium-prediction/blob/main/readme/Input_vs_output.png)