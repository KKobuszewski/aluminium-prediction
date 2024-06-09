"""
This is a boilerplate pipeline 'aquisition'
generated using Kedro 0.19.3
"""


from kedro.pipeline import Pipeline, pipeline, node
from aluminium_prediction.pipelines.aquisition.nodes import (westmetall_download, westmetall_actualize, 
                                                             investing_download, investing_actualize,
                                                             visualize_aluminium_datasets, plotly_aluminium_datasets)


"""
poetry run kedro run --from-nodes "investing_download_node"
poetry run kedro run --from-nodes "visualize_aluminium_node"
poetry run kedro run --from-nodes "plotly_aluminium_node"
"""

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                westmetall_download,
                inputs=None,
                outputs="westmetall_download",
                name="westmetall_download_node",
            ),
            node(
                westmetall_actualize,
                inputs=["westmetall_dataset","westmetall_download"],
                outputs="westmetall_dataset_updated",
                name="westmetall_actualize_node",
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
            node(
                visualize_aluminium_datasets,
                inputs=["westmetall_dataset_updated","investing_dataset_updated"],
                outputs="aluminium_LME_plot",
                name="visualize_aluminium_node",
            ),
            node(
                plotly_aluminium_datasets,
                inputs=["westmetall_dataset_updated","investing_dataset_updated","metalsapi_dataset_updated"],
                outputs="datasets_comparison_plot",
                name="plotly_aluminium_node",
                
            )
        ]
    )
