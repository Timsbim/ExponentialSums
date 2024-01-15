# Exponential Sums

I've stumbled uppon the concept of an [exponential sum][expsum_wiki] on John D. Cook's website [Exponentional Sum of the Day][expsum_jdc] (please visit the site). Fascinated by the richness and beauty of the patterns generated by these terms, I had to implement them. The first prototype is in Python (with the external dependency [Matplotlib][matplotlib]). I still intend to do one in Rust.

General idea: for positive integers $`n_1,\, \dots,\, n_k`$ take the sums
```math
    z_m =
    \sum_{n=0}^m
        \exp \left( 2\pi i \left(
            \frac{n}{n_1} + \frac{n^2}{n_2} + \dots + \frac{n^k}{n_k}
        \right) \right)
```
as the vertices of a traverse in $`\mathbb{R}^2`$ ($`\mathbb{C}`$), plot it, and be filled with wonder. The best _general_ choice for the length of the traverse seems to be the lowest common multiplier of $`n_1,\, \dots,\, n_k`$. But there are quite some cases where this is too low.

# Numbers
<img src="Numbers/2_13_31/2-13-31_31-13-2.png" alt="example" width="500"/>

# Days
In the case of a day $`m/d/y`$ the corresponding exponential sum is defined by
```math
    \begin{matrix*}[rcl]
        n_1 & = & m \\
        n_2 & = & d \\
        n_3 & = & y
    \end{matrix*}
```
 (for $`y`$ only the last two digits).

## expsum_days.py

```none
expsum_days.py [-h] [-f START] [-t END] [-s SAVE_TO] [-m | -a]

Generates plots of the lines between the partial sums of

    exp(2πi * (n / month + n**2 / day + n**3 / year))

for n in 0, ..., lcm(month, day, year). For year only the last two digits
are used (year mod 100).

The plots can be static (.png) or animated (.gif). There's also an option
to generate overviews for the given day range in form of six days per
plot.

options:
  -h, --help            show this help message and exit
  -f START, --from START
                        first day (YYYY-MM-DD) of the day range (default is
                        today)
  -t END, --to END      last day (YYYY-MM-DD) of the day range (default is
                        today)
  -s SAVE_TO, --save-to SAVE_TO
                        folder for saving the files (default is cwd)
  -m, --multi           generate overview plots for the given day range (not
                        allowed in comination with animation)
  -a, --animate         generate an animated .gif instead of a plain .png plot

The idea to look at these fascinating images comes from John D. Cook's
exponential sum of the day (https://www.johndcook.com/expsum/). Please
visit his website!
```

## Examples
### Plots

**4/1/2024**|**4/17/2024**|**5/19/2024**
:-:|:-:|:-:
<img src="Days/24/04/4-1-24.png" width="250"/>|<img src="Days/24/04/4-17-24.png" width="250"/>|<img src="Days/24/05/5-19-24.png" width="250"/>

### Animations

**4/1/2024**|**4/17/2024**|**5/19/2024**
:-:|:-:|:-:
<img src="Days/24/04/4-1-24.gif" width="250"/>|<img src="Days/24/04/4-17-24.gif" width="250"/>|<img src="Days/24/05/5-19-24.gif" width="250"/>


 [expsum_wiki]:https://en.wikipedia.org/wiki/Exponential_sum
 [expsum_jdc]:https://www.johndcook.com/expsum/
 [matplotlib]:https://matplotlib.org/stable/
