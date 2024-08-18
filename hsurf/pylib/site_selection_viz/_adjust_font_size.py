from functools import wraps

import matplotlib.pyplot as plt


def adjust_font_size(new_fontsize: float):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Store current font sizes
            original_fontsize = plt.rcParams["font.size"]
            original_legend_fontsize = plt.rcParams["legend.fontsize"]

            # Increase font sizes
            plt.rcParams["font.size"] = new_fontsize
            plt.rcParams["legend.fontsize"] = 10

            try:
                # Run the decorated function
                result = func(*args, **kwargs)
            finally:
                # Restore the original font sizes
                plt.rcParams["font.size"] = original_fontsize
                plt.rcParams["legend.fontsize"] = original_legend_fontsize

            return result

        return wrapper

    return decorator
