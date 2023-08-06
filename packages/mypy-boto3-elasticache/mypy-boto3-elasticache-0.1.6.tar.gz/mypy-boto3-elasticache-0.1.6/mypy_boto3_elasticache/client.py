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
        self, ResourceName: str, Tags: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def authorize_cache_security_group_ingress(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_apply_update_action(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_stop_update_action(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def complete_migration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def copy_snapshot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_cache_cluster(
        self,
        CacheClusterId: str,
        ReplicationGroupId: str = None,
        AZMode: str = None,
        PreferredAvailabilityZone: str = None,
        PreferredAvailabilityZones: List[Any] = None,
        NumCacheNodes: int = None,
        CacheNodeType: str = None,
        Engine: str = None,
        EngineVersion: str = None,
        CacheParameterGroupName: str = None,
        CacheSubnetGroupName: str = None,
        CacheSecurityGroupNames: List[Any] = None,
        SecurityGroupIds: List[Any] = None,
        Tags: List[Any] = None,
        SnapshotArns: List[Any] = None,
        SnapshotName: str = None,
        PreferredMaintenanceWindow: str = None,
        Port: int = None,
        NotificationTopicArn: str = None,
        AutoMinorVersionUpgrade: bool = None,
        SnapshotRetentionLimit: int = None,
        SnapshotWindow: str = None,
        AuthToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_cache_parameter_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_cache_security_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_cache_subnet_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_replication_group(
        self,
        ReplicationGroupId: str,
        ReplicationGroupDescription: str,
        PrimaryClusterId: str = None,
        AutomaticFailoverEnabled: bool = None,
        NumCacheClusters: int = None,
        PreferredCacheClusterAZs: List[Any] = None,
        NumNodeGroups: int = None,
        ReplicasPerNodeGroup: int = None,
        NodeGroupConfiguration: List[Any] = None,
        CacheNodeType: str = None,
        Engine: str = None,
        EngineVersion: str = None,
        CacheParameterGroupName: str = None,
        CacheSubnetGroupName: str = None,
        CacheSecurityGroupNames: List[Any] = None,
        SecurityGroupIds: List[Any] = None,
        Tags: List[Any] = None,
        SnapshotArns: List[Any] = None,
        SnapshotName: str = None,
        PreferredMaintenanceWindow: str = None,
        Port: int = None,
        NotificationTopicArn: str = None,
        AutoMinorVersionUpgrade: bool = None,
        SnapshotRetentionLimit: int = None,
        SnapshotWindow: str = None,
        AuthToken: str = None,
        TransitEncryptionEnabled: bool = None,
        AtRestEncryptionEnabled: bool = None,
        KmsKeyId: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_snapshot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def decrease_replica_count(
        self,
        ReplicationGroupId: str,
        ApplyImmediately: bool,
        NewReplicaCount: int = None,
        ReplicaConfiguration: List[Any] = None,
        ReplicasToRemove: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_cache_cluster(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_cache_parameter_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_cache_security_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_cache_subnet_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_replication_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_snapshot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_cache_clusters(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_cache_engine_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_cache_parameter_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_cache_parameters(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_cache_security_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_cache_subnet_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_engine_default_parameters(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_events(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_replication_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_reserved_cache_nodes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_reserved_cache_nodes_offerings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_service_updates(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_snapshots(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_update_actions(
        self,
        ServiceUpdateName: str = None,
        ReplicationGroupIds: List[Any] = None,
        CacheClusterIds: List[Any] = None,
        Engine: str = None,
        ServiceUpdateStatus: List[Any] = None,
        ServiceUpdateTimeRange: Dict[str, Any] = None,
        UpdateActionStatus: List[Any] = None,
        ShowNodeLevelUpdateStatus: bool = None,
        MaxRecords: int = None,
        Marker: str = None,
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
    def increase_replica_count(
        self,
        ReplicationGroupId: str,
        ApplyImmediately: bool,
        NewReplicaCount: int = None,
        ReplicaConfiguration: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_allowed_node_type_modifications(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def modify_cache_cluster(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def modify_cache_parameter_group(
        self, CacheParameterGroupName: str, ParameterNameValues: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def modify_cache_subnet_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def modify_replication_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def modify_replication_group_shard_configuration(
        self,
        ReplicationGroupId: str,
        NodeGroupCount: int,
        ApplyImmediately: bool,
        ReshardingConfiguration: List[Any] = None,
        NodeGroupsToRemove: List[Any] = None,
        NodeGroupsToRetain: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def purchase_reserved_cache_nodes_offering(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reboot_cache_cluster(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_tags_from_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reset_cache_parameter_group(
        self,
        CacheParameterGroupName: str,
        ResetAllParameters: bool = None,
        ParameterNameValues: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def revoke_cache_security_group_ingress(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_migration(
        self, ReplicationGroupId: str, CustomerNodeEndpointList: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def test_failover(self) -> None:
        pass
