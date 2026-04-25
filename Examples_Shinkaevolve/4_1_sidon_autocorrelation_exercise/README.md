# 4.1 &mdash; Autocorrelation and Sidon Sets Exercise

This problem is a sibling of [problem 4.2](../4_2_third_autocorrelation_exercise).
The ratio we optimise is the same, but the admissible class of functions
changes — and this one change turns the problem into the continuous
analogue of a classical object in additive combinatorics: the **Sidon
set**. It also turns it into a place where a long-standing folklore
conjecture can be numerically broken.

## Sidon sets ($B_2$ sets)

A finite set $A \subset \mathbb{Z}$ is called a **Sidon set** (or a $B_2$
set) if every pairwise sum $a + b$ with $a, b \in A$ is represented in
**at most one way** up to swapping the summands. Equivalently, the
autoconvolution of the indicator function,

$$
(\mathbf{1}_A * \mathbf{1}_A)(k) \; = \; \#\{(a, b) \in A \times A : a + b = k\},
$$

takes value $\le 2$ everywhere. A classical theorem of Erdős and Turán
(1941) tells us that a Sidon set in $\{1, 2, \dots, N\}$ has size at
most $\sqrt{N} + O(N^{1/4})$. The more general notion of a **$B_2[g]$
set** (every sum represented at most $g$ times) sits at the heart of
additive combinatorics, and bounding the maximum size of such a set
amounts, in the limit, to the continuous problem below.

The *continuous* analogue replaces the indicator function by any
non-negative integrable function supported on an interval of width
$\tfrac{1}{2}$, and asks:

$$
S \; = \; \inf_{\substack{f \ge 0,\ f \not\equiv 0 \\ \mathrm{supp}(f) \subset [-1/4, 1/4]}} \;
\frac{\|f * f\|_\infty}{\bigl(\int f\bigr)^2}.
$$

A small ratio means the mass of $f$ is spread out in a way that avoids
creating a big spike in $f * f$ — exactly the continuous shadow of "all
pairwise sums distinct". Bounds on $S$ give density bounds for
$B_2[g]$ sets, and vice versa; this is the connection studied by
Schinzel & Schmidt, Martin & O'Bryant, Yu, Matolcsi & Vinuesa, and
others.

## A conjecture waiting to be broken

Some papers in the literature conjectured that

$$
S \; \stackrel{?}{=} \; \frac{\pi}{2} \;\approx\; 1.5708,
$$

with the extremal function being the rescaled arcsine-type density
$f(x) = \frac{1}{\pi\sqrt{1/4 - x^2}}$ on $(-\tfrac{1}{4}, \tfrac{1}{4})$
(or an explicit piecewise-constant variant of it). This is a natural
guess: the arcsine density is, up to rescaling, the unique $f$ whose
characteristic function is the Bessel function $J_0$, and such objects
are the "nicest" functions that appear in the Fourier analysis of
$\|f * f\|_\infty$. **That is the conjecture we are trying to break.**

- **Lower bound (rigorous).** A chain of Fourier-analytic arguments
  (Yu; Martin & O'Bryant; Matolcsi & Vinuesa) gives
  $$S \;\ge\; 1.2748.$$
- **Upper bound (constructive).** Matolcsi and Vinuesa, in
  [arXiv:0907.1379](https://arxiv.org/abs/0907.1379), exhibit an
  explicit non-negative $f$ showing $S \le 1.5098$ — and, more
  importantly, disprove the Schinzel–Schmidt conjecture about the
  **shape** of the extremal function. Subsequent refinements have
  pushed the numerical upper bound down to about $S \le 1.5053$.
- **What M–V say.** They write (emphasis ours):

  > *"At this point we do not have any natural conjectures for the
  > exact value of $S$ or any extremal functions where this value could
  > be attained. Upon numerical evidence we are inclined to believe
  > that $S \approx 1.5$, unless there exists some hidden 'magical'
  > number theoretical construction yielding a much smaller value (the
  > possibility of which is by no means excluded)."*

So the conjectured value $S = \pi/2$ is **already known to be false** —
but only barely, and only via a handful of hand-built constructions.
There is still a ~0.22 gap between the best-known upper and lower
bounds. **Our job** is to reproduce the disproof *numerically*, using
Shinka, and then to push past it: find an $f$ whose ratio is not just
below $\pi/2$ but as close to $1.28$ as we can manage. A concrete $f$
with ratio substantially below $1.5$ would be a genuine mathematical
contribution, not just a numerical curiosity.

## The problem, precisely

Find a non-negative step function $f$ on $[-\tfrac{1}{4}, \tfrac{1}{4}]$
that minimises

$$
\frac{\|f * f\|_\infty}{\bigl(\int f\bigr)^2}.
$$

Matolcsi and Vinuesa show (building on Schinzel–Schmidt) that
restricting to step functions does **not** change the infimum, so this
is the right search space. Concretely, we discretise: fix $N$, split
the interval into $N$ bins of width $\delta = \tfrac{1}{2N}$, and
represent $f$ by a vector $(f_1, \dots, f_N) \in \mathbb{R}_{\ge 0}^N$.
The starter uses $N = 400$.

**Scoring.** The evaluator uses the conjectured value $\pi/2$ as the
benchmark and returns

$$
\mathrm{score} \; = \; \frac{\pi/2}{\text{your ratio}}.
$$

So a score of exactly $1$ means you have matched $\pi/2$. A score
strictly above $1$ means you have **disproved the old conjecture
numerically**. The Matolcsi–Vinuesa construction scores about
$\pi/2 / 1.5053 \approx 1.043$; a score approaching $\pi/2 / 1.28
\approx 1.23$ would saturate the current lower bound and essentially
settle the problem.

## Relation to problem 4.2

[Problem 4.2](../4_2_third_autocorrelation_exercise) minimises the same
ratio but **without the sign constraint** on $f$. Allowing $f$ to take
negative values is strictly stronger, because cancellations in $f * f$
can shrink the numerator without shrinking the denominator $\int f$. So
the signed problem has a strictly smaller infimum than this one, and
the two constants are not equal — problem 4.2 lives around $1.28$, this
one around $1.5$. The codes are deliberately parallel: same
discretisation, same entry point, same evaluation pipeline, just with
non-negativity enforced here.

## What you fill in

`initial.py` contains a `search_function()` that returns a vector of
non-negative block values together with its ratio. A simple block-based
search is enough to get started, but the crucial point is that the
returned values must stay non-negative.

In `evaluate.py`, write `validate_output()` so it checks the return
shape, enforces non-negativity, and verifies that the reported ratio
matches the value recomputed from the returned step function. Then fill
in `aggregate_metrics()` so the score reported back to Shinka is the
benchmark ratio.

Write a short prompt in `prompt.txt` describing the mathematical problem,
the output contract, and whatever ideas you want the LLM to try.

The convolution helper and plotting code are already provided.
`plotting.py` visualises the step function and its autoconvolution,
with the maximum of $f * f$ highlighted, once the evaluator is wired up.

## Running it

From this folder, after you fill in `search_function()`, the holes in
`evaluate.py`, and `prompt.txt`:

```bash
python3 initial.py                                           # sanity check
python3 evaluate.py --program_path initial.py --results_dir smoke_test
python3 run_evo.py                                           # launch Shinka
```

## Notes

- **Why the non-negativity matters.** Dropping $f \ge 0$ lets the LLM
  "cheat" by producing sign patterns whose autoconvolutions interfere
  destructively. That is problem 4.2, and it changes the answer.
  Here, every block value must be $\ge 0$, so the LLM has to do honest
  additive-combinatorial work — the same kind of work the Matolcsi–
  Vinuesa construction does.
- **Beating $\pi/2$.** A score of exactly $1.000$ is the old conjecture.
  Any score strictly above $1$ is a numerical disproof. Scores in the
  $1.04$ range reproduce the published state of the art; scores above
  that would be news.
- The plot artifact is saved under `results/plots/`.
