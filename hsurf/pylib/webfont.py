import functools
import tempfile
import urllib.request

from matplotlib.font_manager import FontProperties


@functools.lru_cache
def fetch_ttf(font_url: str) -> str:
    # Download the font data from the URL
    response = urllib.request.urlopen(font_url)
    data = response.read()

    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(
        delete=False, suffix=".ttf", mode="wb"
    )
    temp_file.write(data)
    temp_file.close()

    # Return the path to the temporary file
    return temp_file.name


def make_fontproperties(font_url: str) -> FontProperties:
    return FontProperties(fname=fetch_ttf(font_url))
