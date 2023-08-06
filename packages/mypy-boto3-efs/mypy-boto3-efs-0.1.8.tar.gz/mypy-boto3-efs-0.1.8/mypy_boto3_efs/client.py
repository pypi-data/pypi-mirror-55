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
    def create_file_system(
        self,
        CreationToken: str,
        PerformanceMode: str = None,
        Encrypted: bool = None,
        KmsKeyId: str = None,
        ThroughputMode: str = None,
        ProvisionedThroughputInMibps: float = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_mount_target(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_tags(self, FileSystemId: str, Tags: List[Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_file_system(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_mount_target(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_tags(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_file_systems(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_lifecycle_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_mount_target_security_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_mount_targets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_tags(self) -> None:
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
    def modify_mount_target_security_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_lifecycle_configuration(
        self, FileSystemId: str, LifecyclePolicies: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_file_system(self) -> None:
        pass
