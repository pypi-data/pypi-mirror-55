from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def attach_instances(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def attach_load_balancer_target_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def attach_load_balancers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_delete_scheduled_action(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_put_scheduled_update_group_action(
        self, AutoScalingGroupName: str, ScheduledUpdateGroupActions: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def complete_lifecycle_action(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_auto_scaling_group(
        self,
        AutoScalingGroupName: str,
        MinSize: int,
        MaxSize: int,
        LaunchConfigurationName: str = None,
        LaunchTemplate: Dict[str, Any] = None,
        MixedInstancesPolicy: Dict[str, Any] = None,
        InstanceId: str = None,
        DesiredCapacity: int = None,
        DefaultCooldown: int = None,
        AvailabilityZones: List[Any] = None,
        LoadBalancerNames: List[Any] = None,
        TargetGroupARNs: List[Any] = None,
        HealthCheckType: str = None,
        HealthCheckGracePeriod: int = None,
        PlacementGroup: str = None,
        VPCZoneIdentifier: str = None,
        TerminationPolicies: List[Any] = None,
        NewInstancesProtectedFromScaleIn: bool = None,
        LifecycleHookSpecificationList: List[Any] = None,
        Tags: List[Any] = None,
        ServiceLinkedRoleARN: str = None,
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_launch_configuration(
        self,
        LaunchConfigurationName: str,
        ImageId: str = None,
        KeyName: str = None,
        SecurityGroups: List[Any] = None,
        ClassicLinkVPCId: str = None,
        ClassicLinkVPCSecurityGroups: List[Any] = None,
        UserData: str = None,
        InstanceId: str = None,
        InstanceType: str = None,
        KernelId: str = None,
        RamdiskId: str = None,
        BlockDeviceMappings: List[Any] = None,
        InstanceMonitoring: Dict[str, Any] = None,
        SpotPrice: str = None,
        IamInstanceProfile: str = None,
        EbsOptimized: bool = None,
        AssociatePublicIpAddress: bool = None,
        PlacementTenancy: str = None,
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_or_update_tags(self, Tags: List[Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_auto_scaling_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_launch_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_lifecycle_hook(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_notification_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_scheduled_action(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_tags(self, Tags: List[Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_account_limits(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_adjustment_types(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_auto_scaling_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_auto_scaling_instances(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_auto_scaling_notification_types(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_launch_configurations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_lifecycle_hook_types(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_lifecycle_hooks(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_load_balancer_target_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_load_balancers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_metric_collection_types(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_notification_configurations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_policies(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_scaling_activities(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_scaling_process_types(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_scheduled_actions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_tags(
        self, Filters: List[Any] = None, NextToken: str = None, MaxRecords: int = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def describe_termination_policy_types(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def detach_instances(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def detach_load_balancer_target_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def detach_load_balancers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disable_metrics_collection(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def enable_metrics_collection(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def enter_standby(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def execute_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def exit_standby(self) -> None:
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
    def put_lifecycle_hook(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_notification_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_scaling_policy(
        self,
        AutoScalingGroupName: str,
        PolicyName: str,
        PolicyType: str = None,
        AdjustmentType: str = None,
        MinAdjustmentStep: int = None,
        MinAdjustmentMagnitude: int = None,
        ScalingAdjustment: int = None,
        Cooldown: int = None,
        MetricAggregationType: str = None,
        StepAdjustments: List[Any] = None,
        EstimatedInstanceWarmup: int = None,
        TargetTrackingConfiguration: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_scheduled_update_group_action(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def record_lifecycle_action_heartbeat(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def resume_processes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_desired_capacity(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_instance_health(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_instance_protection(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def suspend_processes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def terminate_instance_in_auto_scaling_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_auto_scaling_group(
        self,
        AutoScalingGroupName: str,
        LaunchConfigurationName: str = None,
        LaunchTemplate: Dict[str, Any] = None,
        MixedInstancesPolicy: Dict[str, Any] = None,
        MinSize: int = None,
        MaxSize: int = None,
        DesiredCapacity: int = None,
        DefaultCooldown: int = None,
        AvailabilityZones: List[Any] = None,
        HealthCheckType: str = None,
        HealthCheckGracePeriod: int = None,
        PlacementGroup: str = None,
        VPCZoneIdentifier: str = None,
        TerminationPolicies: List[Any] = None,
        NewInstancesProtectedFromScaleIn: bool = None,
        ServiceLinkedRoleARN: str = None,
    ) -> None:
        pass
