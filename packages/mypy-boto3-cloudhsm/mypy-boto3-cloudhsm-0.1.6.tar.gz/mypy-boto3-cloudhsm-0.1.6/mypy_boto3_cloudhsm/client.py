from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def add_tags_to_resource(
        self, ResourceArn: str, TagList: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_hapg(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_hsm(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_luna_client(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_hapg(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_hsm(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_luna_client(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_hapg(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_hsm(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_luna_client(self) -> None:
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
    def get_config(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_available_zones(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_hapgs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_hsms(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_luna_clients(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def modify_hapg(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def modify_hsm(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def modify_luna_client(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_tags_from_resource(self) -> None:
        pass
