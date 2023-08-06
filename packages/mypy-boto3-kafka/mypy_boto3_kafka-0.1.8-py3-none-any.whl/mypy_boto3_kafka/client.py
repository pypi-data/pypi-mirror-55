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
    def create_cluster(
        self,
        BrokerNodeGroupInfo: Dict[str, Any],
        ClusterName: str,
        KafkaVersion: str,
        NumberOfBrokerNodes: int,
        ClientAuthentication: Dict[str, Any] = None,
        ConfigurationInfo: Dict[str, Any] = None,
        EncryptionInfo: Dict[str, Any] = None,
        EnhancedMonitoring: str = None,
        Tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_cluster(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_cluster(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_cluster_operation(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_configuration_revision(self) -> None:
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
    def get_bootstrap_brokers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_cluster_operations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_clusters(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_configuration_revisions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_configurations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_nodes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, ResourceArn: str, Tags: Dict[str, Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_broker_count(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_broker_storage(
        self, ClusterArn: str, CurrentVersion: str, TargetBrokerEBSVolumeInfo: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_cluster_configuration(
        self, ClusterArn: str, ConfigurationInfo: Dict[str, Any], CurrentVersion: str
    ) -> Dict[str, Any]:
        pass
