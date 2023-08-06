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
    def create_http_namespace(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_private_dns_namespace(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_public_dns_namespace(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_service(
        self,
        Name: str,
        NamespaceId: str = None,
        CreatorRequestId: str = None,
        Description: str = None,
        DnsConfig: Dict[str, Any] = None,
        HealthCheckConfig: Dict[str, Any] = None,
        HealthCheckCustomConfig: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_namespace(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_service(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deregister_instance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def discover_instances(
        self,
        NamespaceName: str,
        ServiceName: str,
        MaxResults: int = None,
        QueryParameters: Dict[str, Any] = None,
        HealthStatus: str = None,
    ) -> Dict[str, Any]:
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
    def get_instance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_instances_health_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_namespace(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_operation(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_service(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_instances(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_namespaces(
        self, NextToken: str = None, MaxResults: int = None, Filters: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_operations(
        self, NextToken: str = None, MaxResults: int = None, Filters: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_services(
        self, NextToken: str = None, MaxResults: int = None, Filters: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def register_instance(
        self,
        ServiceId: str,
        InstanceId: str,
        Attributes: Dict[str, Any],
        CreatorRequestId: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_instance_custom_health_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_service(self, Id: str, Service: Dict[str, Any]) -> Dict[str, Any]:
        pass
