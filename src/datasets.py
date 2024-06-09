from typing import Any, Dict, NoReturn

from kedro.io import AbstractDataset
from kedro.io.core import get_filepath_str, DatasetError

class PlotlyHTMLDataset(AbstractDataset):
    def __init__(self, filepath):
        self._filepath = filepath

    def _load(self) -> NoReturn:
        raise DatasetError(f"Loading not supported for '{self.__class__.__name__}'")

    def _save(self, fig) -> None:
        fname = self._filepath
        if not '.html' in fname:
            fname += '.html'
        fig.write_html(fname)

    def _describe(self) -> Dict[str, Any]:
        return { "filepath": self._filepath, }