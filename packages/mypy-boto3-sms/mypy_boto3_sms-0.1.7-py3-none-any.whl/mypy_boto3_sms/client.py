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
    def create_app(
        self,
        name: str = None,
        description: str = None,
        roleName: str = None,
        clientToken: str = None,
        serverGroups: List[Any] = None,
        tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_replication_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_app(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_app_launch_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_app_replication_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_replication_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_server_catalog(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_connector(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def generate_change_set(self) -> None:
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
    def generate_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_app(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_app_launch_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_app_replication_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_connectors(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_replication_jobs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_replication_runs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_servers(
        self,
        nextToken: str = None,
        maxResults: int = None,
        vmServerAddressList: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def import_server_catalog(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def launch_app(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_apps(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_app_launch_configuration(
        self,
        appId: str = None,
        roleName: str = None,
        serverGroupLaunchConfigurations: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_app_replication_configuration(
        self, appId: str = None, serverGroupReplicationConfigurations: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def start_app_replication(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_on_demand_replication_run(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def stop_app_replication(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def terminate_app(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_app(
        self,
        appId: str = None,
        name: str = None,
        description: str = None,
        roleName: str = None,
        serverGroups: List[Any] = None,
        tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_replication_job(self) -> None:
        pass
