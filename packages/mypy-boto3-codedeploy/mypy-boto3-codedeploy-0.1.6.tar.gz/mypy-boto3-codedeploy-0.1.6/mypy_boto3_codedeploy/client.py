from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def add_tags_to_on_premises_instances(
        self, tags: List[Any], instanceNames: List[Any]
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_get_application_revisions(
        self, applicationName: str, revisions: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def batch_get_applications(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_get_deployment_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_get_deployment_instances(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_get_deployment_targets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_get_deployments(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_get_on_premises_instances(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def continue_deployment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_application(
        self, applicationName: str, computePlatform: str = None, tags: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_deployment(
        self,
        applicationName: str,
        deploymentGroupName: str = None,
        revision: Dict[str, Any] = None,
        deploymentConfigName: str = None,
        description: str = None,
        ignoreApplicationStopFailures: bool = None,
        targetInstances: Dict[str, Any] = None,
        autoRollbackConfiguration: Dict[str, Any] = None,
        updateOutdatedInstancesOnly: bool = None,
        fileExistsBehavior: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_deployment_config(
        self,
        deploymentConfigName: str,
        minimumHealthyHosts: Dict[str, Any] = None,
        trafficRoutingConfig: Dict[str, Any] = None,
        computePlatform: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_deployment_group(
        self,
        applicationName: str,
        deploymentGroupName: str,
        serviceRoleArn: str,
        deploymentConfigName: str = None,
        ec2TagFilters: List[Any] = None,
        onPremisesInstanceTagFilters: List[Any] = None,
        autoScalingGroups: List[Any] = None,
        triggerConfigurations: List[Any] = None,
        alarmConfiguration: Dict[str, Any] = None,
        autoRollbackConfiguration: Dict[str, Any] = None,
        deploymentStyle: Dict[str, Any] = None,
        blueGreenDeploymentConfiguration: Dict[str, Any] = None,
        loadBalancerInfo: Dict[str, Any] = None,
        ec2TagSet: Dict[str, Any] = None,
        ecsServices: List[Any] = None,
        onPremisesTagSet: Dict[str, Any] = None,
        tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_application(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_deployment_config(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_deployment_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_git_hub_account_token(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deregister_on_premises_instance(self) -> None:
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
    def get_application(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_application_revision(
        self, applicationName: str, revision: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_deployment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_deployment_config(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_deployment_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_deployment_instance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_deployment_target(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_on_premises_instance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_application_revisions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_applications(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_deployment_configs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_deployment_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_deployment_instances(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_deployment_targets(
        self,
        deploymentId: str = None,
        nextToken: str = None,
        targetFilters: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_deployments(
        self,
        applicationName: str = None,
        deploymentGroupName: str = None,
        includeOnlyStatuses: List[Any] = None,
        createTimeRange: Dict[str, Any] = None,
        nextToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_git_hub_account_token_names(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_on_premises_instances(
        self,
        registrationStatus: str = None,
        tagFilters: List[Any] = None,
        nextToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_lifecycle_event_hook_execution_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def register_application_revision(
        self, applicationName: str, revision: Dict[str, Any], description: str = None
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def register_on_premises_instance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_tags_from_on_premises_instances(
        self, tags: List[Any], instanceNames: List[Any]
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def skip_wait_time_for_instance_termination(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def stop_deployment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, ResourceArn: str, Tags: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_application(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_deployment_group(
        self,
        applicationName: str,
        currentDeploymentGroupName: str,
        newDeploymentGroupName: str = None,
        deploymentConfigName: str = None,
        ec2TagFilters: List[Any] = None,
        onPremisesInstanceTagFilters: List[Any] = None,
        autoScalingGroups: List[Any] = None,
        serviceRoleArn: str = None,
        triggerConfigurations: List[Any] = None,
        alarmConfiguration: Dict[str, Any] = None,
        autoRollbackConfiguration: Dict[str, Any] = None,
        deploymentStyle: Dict[str, Any] = None,
        blueGreenDeploymentConfiguration: Dict[str, Any] = None,
        loadBalancerInfo: Dict[str, Any] = None,
        ec2TagSet: Dict[str, Any] = None,
        ecsServices: List[Any] = None,
        onPremisesTagSet: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass
