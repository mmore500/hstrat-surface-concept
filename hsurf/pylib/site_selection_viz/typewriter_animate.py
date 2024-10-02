from matplotlib import animation as mpl_animation
from matplotlib import pyplot as plt
import pandas as pd


from .site_ingest_depth_by_rank_heatmap import site_ingest_depth_by_rank_heatmap


# adapted from https://github.com/agude/agude.github.io/blob/main/files/matplotlib-blitting-supernova/Matplotlib%20Animation%20Blitting%20Example%20-%20Supernova%20Spectra%20Extra.ipynb
def typewriter_animate(
    surface_history_df: pd.DataFrame,
) -> mpl_animation.FuncAnimation:
    fig, ax = plt.subplots(figsize=(12, 7))
    return mpl_animation.FuncAnimation(
        fig=fig,
        func=lambda *args, **kwargs: None,
        frames=lambda *args, **kwargs: range(10),
        init_func=lambda *args, **kwargs: None,
        save_count=10,
        repeat_delay=5000,
    )
