from __future__ import annotations

from typing import Any
from typing import Dict

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_campaign(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_dataset(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_dataset_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_dataset_import_job(
        self, jobName: str, datasetArn: str, dataSource: Dict[str, Any], roleArn: str
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_event_tracker(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_schema(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_solution(
        self,
        name: str,
        datasetGroupArn: str,
        performHPO: bool = None,
        performAutoML: bool = None,
        recipeArn: str = None,
        eventType: str = None,
        solutionConfig: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_solution_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_campaign(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_dataset(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_dataset_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_event_tracker(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_schema(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_solution(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_algorithm(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_campaign(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_dataset(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_dataset_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_dataset_import_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_event_tracker(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_feature_transformation(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_recipe(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_schema(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_solution(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_solution_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def generate_presigned_url(
        self,
        ClientMethod: str = None,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = None,
        HttpMethod: str = None,
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_solution_metrics(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_campaigns(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_dataset_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_dataset_import_jobs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_datasets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_event_trackers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_recipes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_schemas(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_solution_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_solutions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_campaign(self) -> None:
        pass
