from __future__ import annotations

from datetime import datetime
from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def accept_reserved_node_exchange(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def authorize_cluster_security_group_ingress(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def authorize_snapshot_access(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_delete_cluster_snapshots(self, Identifiers: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def batch_modify_cluster_snapshots(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def cancel_resize(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def copy_cluster_snapshot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_cluster(
        self,
        ClusterIdentifier: str,
        NodeType: str,
        MasterUsername: str,
        MasterUserPassword: str,
        DBName: str = None,
        ClusterType: str = None,
        ClusterSecurityGroups: List[Any] = None,
        VpcSecurityGroupIds: List[Any] = None,
        ClusterSubnetGroupName: str = None,
        AvailabilityZone: str = None,
        PreferredMaintenanceWindow: str = None,
        ClusterParameterGroupName: str = None,
        AutomatedSnapshotRetentionPeriod: int = None,
        ManualSnapshotRetentionPeriod: int = None,
        Port: int = None,
        ClusterVersion: str = None,
        AllowVersionUpgrade: bool = None,
        NumberOfNodes: int = None,
        PubliclyAccessible: bool = None,
        Encrypted: bool = None,
        HsmClientCertificateIdentifier: str = None,
        HsmConfigurationIdentifier: str = None,
        ElasticIp: str = None,
        Tags: List[Any] = None,
        KmsKeyId: str = None,
        EnhancedVpcRouting: bool = None,
        AdditionalInfo: str = None,
        IamRoles: List[Any] = None,
        MaintenanceTrackName: str = None,
        SnapshotScheduleIdentifier: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_cluster_parameter_group(
        self,
        ParameterGroupName: str,
        ParameterGroupFamily: str,
        Description: str,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_cluster_security_group(
        self, ClusterSecurityGroupName: str, Description: str, Tags: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_cluster_snapshot(
        self,
        SnapshotIdentifier: str,
        ClusterIdentifier: str,
        ManualSnapshotRetentionPeriod: int = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_cluster_subnet_group(
        self,
        ClusterSubnetGroupName: str,
        Description: str,
        SubnetIds: List[Any],
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_event_subscription(
        self,
        SubscriptionName: str,
        SnsTopicArn: str,
        SourceType: str = None,
        SourceIds: List[Any] = None,
        EventCategories: List[Any] = None,
        Severity: str = None,
        Enabled: bool = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_hsm_client_certificate(
        self, HsmClientCertificateIdentifier: str, Tags: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_hsm_configuration(
        self,
        HsmConfigurationIdentifier: str,
        Description: str,
        HsmIpAddress: str,
        HsmPartitionName: str,
        HsmPartitionPassword: str,
        HsmServerPublicCertificate: str,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_snapshot_copy_grant(
        self, SnapshotCopyGrantName: str, KmsKeyId: str = None, Tags: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_snapshot_schedule(
        self,
        ScheduleDefinitions: List[Any] = None,
        ScheduleIdentifier: str = None,
        ScheduleDescription: str = None,
        Tags: List[Any] = None,
        DryRun: bool = None,
        NextInvocations: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_tags(self, ResourceName: str, Tags: List[Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_cluster(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_cluster_parameter_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_cluster_security_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_cluster_snapshot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_cluster_subnet_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_event_subscription(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_hsm_client_certificate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_hsm_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_snapshot_copy_grant(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_snapshot_schedule(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_tags(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_account_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_cluster_db_revisions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_cluster_parameter_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_cluster_parameters(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_cluster_security_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_cluster_snapshots(
        self,
        ClusterIdentifier: str = None,
        SnapshotIdentifier: str = None,
        SnapshotType: str = None,
        StartTime: datetime = None,
        EndTime: datetime = None,
        MaxRecords: int = None,
        Marker: str = None,
        OwnerAccount: str = None,
        TagKeys: List[Any] = None,
        TagValues: List[Any] = None,
        ClusterExists: bool = None,
        SortingEntities: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def describe_cluster_subnet_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_cluster_tracks(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_cluster_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_clusters(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_default_cluster_parameters(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_event_categories(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_event_subscriptions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_events(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_hsm_client_certificates(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_hsm_configurations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_logging_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_node_configuration_options(
        self,
        ActionType: str,
        SnapshotIdentifier: str = None,
        OwnerAccount: str = None,
        Filters: List[Any] = None,
        Marker: str = None,
        MaxRecords: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def describe_orderable_cluster_options(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_reserved_node_offerings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_reserved_nodes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_resize(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_snapshot_copy_grants(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_snapshot_schedules(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_storage(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_table_restore_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_tags(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disable_logging(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disable_snapshot_copy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def enable_logging(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def enable_snapshot_copy(self) -> None:
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
    def get_cluster_credentials(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_reserved_node_exchange_offerings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def modify_cluster(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def modify_cluster_db_revision(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def modify_cluster_iam_roles(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def modify_cluster_maintenance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def modify_cluster_parameter_group(
        self, ParameterGroupName: str, Parameters: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def modify_cluster_snapshot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def modify_cluster_snapshot_schedule(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def modify_cluster_subnet_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def modify_event_subscription(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def modify_snapshot_copy_retention_period(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def modify_snapshot_schedule(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def purchase_reserved_node_offering(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reboot_cluster(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reset_cluster_parameter_group(
        self,
        ParameterGroupName: str,
        ResetAllParameters: bool = None,
        Parameters: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def resize_cluster(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def restore_from_cluster_snapshot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def restore_table_from_cluster_snapshot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def revoke_cluster_security_group_ingress(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def revoke_snapshot_access(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def rotate_encryption_key(self) -> None:
        pass
