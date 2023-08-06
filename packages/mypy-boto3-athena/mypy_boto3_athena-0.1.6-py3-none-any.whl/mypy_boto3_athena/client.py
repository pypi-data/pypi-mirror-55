from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def batch_get_named_query(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_get_query_execution(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_named_query(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_work_group(
        self,
        Name: str,
        Configuration: Dict[str, Any] = None,
        Description: str = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_named_query(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_work_group(self) -> None:
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
    def get_named_query(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_query_execution(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_query_results(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def get_work_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_named_queries(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_query_executions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_work_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_query_execution(
        self,
        QueryString: str,
        ClientRequestToken: str = None,
        QueryExecutionContext: Dict[str, Any] = None,
        ResultConfiguration: Dict[str, Any] = None,
        WorkGroup: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def stop_query_execution(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, ResourceARN: str, Tags: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_work_group(
        self,
        WorkGroup: str,
        Description: str = None,
        ConfigurationUpdates: Dict[str, Any] = None,
        State: str = None,
    ) -> Dict[str, Any]:
        pass
