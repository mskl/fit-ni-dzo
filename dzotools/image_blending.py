# AUTOGENERATED! DO NOT EDIT! File to edit: 05_image_blending.ipynb (unless otherwise specified).

__all__ = ['WrappedNdArray', 'laplace_op']

# Cell
class WrappedNdArray:
    """Wraps an ndarray and only returns value if within bounds."""
    def __init__(self, array: np.ndarray):
        self.array = array

    def is_inside(self, location):
        return all([
            0 <= location[0] < self.array.shape[0],
            0 <= location[1] < self.array.shape[1],
        ])

    def __getitem__(self, location):
        if self.is_inside(location):
            return self.array[location]
        return 0

    def __setitem__(self, location, value):
        if self.is_inside(location):
            self.array[location] = value

# Cell
def laplace_op(y: int, x: int, arr: np.array) -> float:
    """Calculate the discrete Laplace operator on arr"""
    return -4 * arr[y, x] + arr[y+1, x] + arr[y-1, x] + arr[y, x+1] + arr[y, x-1]