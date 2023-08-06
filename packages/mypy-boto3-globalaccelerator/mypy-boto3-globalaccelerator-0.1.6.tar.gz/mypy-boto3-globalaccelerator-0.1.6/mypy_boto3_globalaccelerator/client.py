from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_accelerator(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_endpoint_group(
        self,
        ListenerArn: str,
        EndpointGroupRegion: str,
        IdempotencyToken: str,
        EndpointConfigurations: List[Any] = None,
        TrafficDialPercentage: float = None,
        HealthCheckPort: int = None,
        HealthCheckProtocol: str = None,
        HealthCheckPath: str = None,
        HealthCheckIntervalSeconds: int = None,
        ThresholdCount: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_listener(
        self,
        AcceleratorArn: str,
        PortRanges: List[Any],
        Protocol: str,
        IdempotencyToken: str,
        ClientAffinity: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_accelerator(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_endpoint_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_listener(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_accelerator(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_accelerator_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_endpoint_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_listener(self) -> None:
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
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_accelerators(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_endpoint_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_listeners(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_accelerator(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_accelerator_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_endpoint_group(
        self,
        EndpointGroupArn: str,
        EndpointConfigurations: List[Any] = None,
        TrafficDialPercentage: float = None,
        HealthCheckPort: int = None,
        HealthCheckProtocol: str = None,
        HealthCheckPath: str = None,
        HealthCheckIntervalSeconds: int = None,
        ThresholdCount: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_listener(
        self,
        ListenerArn: str,
        PortRanges: List[Any] = None,
        Protocol: str = None,
        ClientAffinity: str = None,
    ) -> Dict[str, Any]:
        pass
