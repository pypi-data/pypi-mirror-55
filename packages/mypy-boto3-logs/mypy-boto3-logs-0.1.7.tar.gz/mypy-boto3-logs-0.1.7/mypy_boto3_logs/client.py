from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def associate_kms_key(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def cancel_export_task(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_export_task(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_log_group(
        self, logGroupName: str, kmsKeyId: str = None, tags: Dict[str, Any] = None
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_log_stream(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_destination(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_log_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_log_stream(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_metric_filter(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_resource_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_retention_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_subscription_filter(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_destinations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_export_tasks(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_log_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_log_streams(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_metric_filters(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_queries(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_resource_policies(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_subscription_filters(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_kms_key(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def filter_log_events(self) -> None:
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
    def get_log_events(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_log_group_fields(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_log_record(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_query_results(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_tags_log_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_destination(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_destination_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_log_events(
        self,
        logGroupName: str,
        logStreamName: str,
        logEvents: List[Any],
        sequenceToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_metric_filter(
        self,
        logGroupName: str,
        filterName: str,
        filterPattern: str,
        metricTransformations: List[Any],
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_resource_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_retention_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_subscription_filter(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_query(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def stop_query(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_log_group(self, logGroupName: str, tags: Dict[str, Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def test_metric_filter(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def untag_log_group(self) -> None:
        pass
