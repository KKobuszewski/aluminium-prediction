"""
This is a boilerplate pipeline 'aquisition'
generated using Kedro 0.19.3
"""

from kedro.pipeline import Pipeline, pipeline, node
from aluminium_prediction.pipelines.aquisition.nodes import (westmetall_download, investing_download, investing_actualize)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                westmetall_download,
                inputs=None,
                outputs="westmetall_dataset",
                name="westmetall_download_node",
            ),
            node(
                investing_download,
                inputs=None,
                outputs="investing_download",
                name="investing_download_node",
            ),
            node(
                investing_actualize,
                inputs=["investing_dataset","investing_download"],
                outputs="investing_dataset_updated",
                name="investing_actualize_node",
            ),
        ]
    )
