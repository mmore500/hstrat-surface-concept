from matplotlib.legend_handler import HandlerBase as mpl_HandlerBase
from matplotlib.patches import Rectangle as mpl_Rectangle


class LegendPatchHandler(mpl_HandlerBase):
    def create_artists(
        self,
        legend,
        orig_handle,
        xdescent,
        ydescent,
        width,
        height,
        fontsize,
        trans,
    ):

        return [
            mpl_Rectangle(
                (xdescent, ydescent),
                width,
                height,
                facecolor=orig_handle.get_color(),
                edgecolor="none",
                alpha=0.1,
            ),
        ]
