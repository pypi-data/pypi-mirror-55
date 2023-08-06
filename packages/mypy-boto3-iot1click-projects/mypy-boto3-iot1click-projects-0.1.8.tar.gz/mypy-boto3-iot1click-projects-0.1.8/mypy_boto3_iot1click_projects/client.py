from __future__ import annotations

from typing import Any
from typing import Dict

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    # pylint: disable=arguments-differ
    def associate_device_with_placement(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_placement(
        self, placementName: str, projectName: str, attributes: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_project(
        self,
        projectName: str,
        description: str = None,
        placementTemplate: Dict[str, Any] = None,
        tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_placement(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_project(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_placement(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_project(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_device_from_placement(self) -> None:
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
    def get_devices_in_placement(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_placements(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_projects(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, resourceArn: str, tags: Dict[str, Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_placement(
        self, placementName: str, projectName: str, attributes: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_project(
        self,
        projectName: str,
        description: str = None,
        placementTemplate: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass
