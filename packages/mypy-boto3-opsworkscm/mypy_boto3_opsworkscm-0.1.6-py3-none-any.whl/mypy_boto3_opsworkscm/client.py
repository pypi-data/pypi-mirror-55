from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def associate_node(
        self, ServerName: str, NodeName: str, EngineAttributes: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_backup(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_server(
        self,
        ServerName: str,
        InstanceProfileArn: str,
        InstanceType: str,
        ServiceRoleArn: str,
        AssociatePublicIpAddress: bool = None,
        CustomDomain: str = None,
        CustomCertificate: str = None,
        CustomPrivateKey: str = None,
        DisableAutomatedBackup: bool = None,
        Engine: str = None,
        EngineModel: str = None,
        EngineVersion: str = None,
        EngineAttributes: List[Any] = None,
        BackupRetentionCount: int = None,
        KeyPair: str = None,
        PreferredMaintenanceWindow: str = None,
        PreferredBackupWindow: str = None,
        SecurityGroupIds: List[Any] = None,
        SubnetIds: List[Any] = None,
        BackupId: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_backup(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_server(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_account_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_backups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_events(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_node_association_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_servers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_node(
        self, ServerName: str, NodeName: str, EngineAttributes: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def export_server_engine_attribute(
        self,
        ExportAttributeName: str,
        ServerName: str,
        InputAttributes: List[Any] = None,
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
    def restore_server(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_maintenance(
        self, ServerName: str, EngineAttributes: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_server(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_server_engine_attributes(self) -> None:
        pass
