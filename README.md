# Exponential Sums

Calculation and drawing of John D. Cook's [Exponentional Sum of the Day](https://www.johndcook.com/expsum/). Please visit his website!

General idea: Look at the sums $`z_m`$
```math
    z_m =
    \sum_{n=0}^m
        \exp \left( 2\pi i \left(
            \frac{n}{n_1} + \frac{n^2}{n_2} + \dots + \frac{n^k}{n_k}
        \right) \right)
```
for positive integers $`n_1, \dots, n_k`$.

In the case of a day $`m/d/y`$ ($`y`$ only the last two digits): $`n_1 = m`$, $`n_2 = d`$ and $`n_3 = y`$ (ie. $`k = 3`$).

## Examples: 

### Plots
#### 4/1/2024
![example](Days/24/04/4-1-24.png)
#### 4/17/2024
![example](Days/24/04/4-17-24.png)
#### 5/19/2024
![example](Days/24/05/5-19-24.png)

### Animations
#### 4/1/2024
![example](Days/24/04/4-1-24.gif)
#### 4/17/2024
![example](Days/24/04/4-17-24.gif)
#### 5/19/2024
![example](Days/24/05/5-19-24.gif)
