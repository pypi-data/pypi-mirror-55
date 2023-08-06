from __future__ import annotations

from datetime import datetime
from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def batch_get_traces(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_sampling_rule(self, SamplingRule: Dict[str, Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_sampling_rule(self) -> None:
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
    def get_encryption_config(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_sampling_rules(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_sampling_statistic_summaries(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_sampling_targets(
        self, SamplingStatisticsDocuments: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_service_graph(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_time_series_service_statistics(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_trace_graph(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_trace_summaries(
        self,
        StartTime: datetime,
        EndTime: datetime,
        TimeRangeType: str = None,
        Sampling: bool = None,
        SamplingStrategy: Dict[str, Any] = None,
        FilterExpression: str = None,
        NextToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def put_encryption_config(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_telemetry_records(
        self,
        TelemetryRecords: List[Any],
        EC2InstanceId: str = None,
        Hostname: str = None,
        ResourceARN: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_trace_segments(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_sampling_rule(
        self, SamplingRuleUpdate: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass
