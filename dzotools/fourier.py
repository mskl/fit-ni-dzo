# AUTOGENERATED! DO NOT EDIT! File to edit: 02_fourier.ipynb (unless otherwise specified).

__all__ = ['draw_pair', 'fft_amplitude']

# Cell
import numpy as np
import matplotlib.pyplot as plt

def draw_pair(arr1: np.array, arr2: np.array):
    """Show 2 images side by side"""
    fig, ax = plt.subplots(1, 2, figsize=(10, 10), sharey=True)
    ax[0].imshow(arr1, cmap='gray', vmin=0, vmax=255)
    ax[1].imshow(arr2, cmap='gray', vmin=0, vmax=255)
    plt.tight_layout()
    return fig, ax

# Cell
from numpy.fft import fft2

def fft_amplitude(arr: np.array) -> np.array:
    """Get the amplitude spectrum of the given np array"""
    # Compute the 2-dimensional discrete Fourier Transform
    # Contains complex numbers (x.real, x.imag)
    spectrum = fft2(arr)

    # swap the first quadrant of X with the third, and the second quadrant with the fourth
    mid = (np.asarray(spectrum.shape) / 2).astype(int)
    reconfigured = np.block([
        [spectrum[mid[0]:, mid[1]:], spectrum[mid[0]:, :mid[1]]],
        [spectrum[:mid[0], mid[1]:], spectrum[:mid[0], :mid[1]]]
    ])

    # np.abs gives magnitude of complex number i.e. sqrt(a^2 + b^2)
    return np.abs(reconfigured)