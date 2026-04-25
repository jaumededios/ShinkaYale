#!/usr/bin/env python3
import numpy as np


def plot_autocorrelation(extra_data):
    import matplotlib.pyplot as plt

    f_values = np.asarray(extra_data["f_values"], dtype=float)
    c1 = float(extra_data["c1"])
    dx = 0.5 / len(f_values)

    x = np.linspace(-0.25 + 0.5 * dx, 0.25 - 0.5 * dx, len(f_values))
    conv = np.convolve(f_values, f_values, mode="full") * dx
    t = np.linspace(-0.5 + dx, 0.5 - dx, len(conv))

    fig, axes = plt.subplots(2, 1, figsize=(7, 6), sharex=False)

    axes[0].step(x, f_values, where="mid")
    axes[0].set_title(f"Non-negative step function (n={len(f_values)}, C1={c1:.6f})")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("f(x)")
    axes[0].axhline(0.0, color="grey", linewidth=0.5)

    axes[1].plot(t, conv, label="f * f")
    axes[1].axhline(np.max(conv), color="red", linestyle=":", linewidth=1.0, label="max")
    axes[1].set_xlabel("t")
    axes[1].set_ylabel("autoconvolution")
    axes[1].legend()

    fig.tight_layout()
    return [(fig, "autocorrelation")]
