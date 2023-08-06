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
    def copy_backup_to_region(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_cluster(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_hsm(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_backup(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_cluster(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_hsm(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_backups(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: Dict[str, Any] = None,
        SortAscending: bool = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def describe_clusters(
        self,
        Filters: Dict[str, Any] = None,
        NextToken: str = None,
        MaxResults: int = None,
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
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def initialize_cluster(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def restore_backup(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, ResourceId: str, TagList: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass
