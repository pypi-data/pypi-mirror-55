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
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_cluster(
        self,
        clusterName: str = None,
        tags: List[Any] = None,
        settings: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_service(
        self,
        serviceName: str,
        cluster: str = None,
        taskDefinition: str = None,
        loadBalancers: List[Any] = None,
        serviceRegistries: List[Any] = None,
        desiredCount: int = None,
        clientToken: str = None,
        launchType: str = None,
        platformVersion: str = None,
        role: str = None,
        deploymentConfiguration: Dict[str, Any] = None,
        placementConstraints: List[Any] = None,
        placementStrategy: List[Any] = None,
        networkConfiguration: Dict[str, Any] = None,
        healthCheckGracePeriodSeconds: int = None,
        schedulingStrategy: str = None,
        deploymentController: Dict[str, Any] = None,
        tags: List[Any] = None,
        enableECSManagedTags: bool = None,
        propagateTags: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_task_set(
        self,
        service: str,
        cluster: str,
        taskDefinition: str,
        externalId: str = None,
        networkConfiguration: Dict[str, Any] = None,
        loadBalancers: List[Any] = None,
        serviceRegistries: List[Any] = None,
        launchType: str = None,
        platformVersion: str = None,
        scale: Dict[str, Any] = None,
        clientToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_account_setting(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_attributes(
        self, attributes: List[Any], cluster: str = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_cluster(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_service(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_task_set(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deregister_container_instance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deregister_task_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_clusters(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_container_instances(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_services(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_task_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_task_sets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_tasks(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def discover_poll_endpoint(self) -> None:
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
    def list_account_settings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_clusters(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_container_instances(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_services(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_task_definition_families(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_task_definitions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tasks(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_account_setting(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_account_setting_default(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_attributes(
        self, attributes: List[Any], cluster: str = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def register_container_instance(
        self,
        cluster: str = None,
        instanceIdentityDocument: str = None,
        instanceIdentityDocumentSignature: str = None,
        totalResources: List[Any] = None,
        versionInfo: Dict[str, Any] = None,
        containerInstanceArn: str = None,
        attributes: List[Any] = None,
        platformDevices: List[Any] = None,
        tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def register_task_definition(
        self,
        family: str,
        containerDefinitions: List[Any],
        taskRoleArn: str = None,
        executionRoleArn: str = None,
        networkMode: str = None,
        volumes: List[Any] = None,
        placementConstraints: List[Any] = None,
        requiresCompatibilities: List[Any] = None,
        cpu: str = None,
        memory: str = None,
        tags: List[Any] = None,
        pidMode: str = None,
        ipcMode: str = None,
        proxyConfiguration: Dict[str, Any] = None,
        inferenceAccelerators: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def run_task(
        self,
        taskDefinition: str,
        cluster: str = None,
        overrides: Dict[str, Any] = None,
        count: int = None,
        startedBy: str = None,
        group: str = None,
        placementConstraints: List[Any] = None,
        placementStrategy: List[Any] = None,
        launchType: str = None,
        platformVersion: str = None,
        networkConfiguration: Dict[str, Any] = None,
        tags: List[Any] = None,
        enableECSManagedTags: bool = None,
        propagateTags: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def start_task(
        self,
        taskDefinition: str,
        containerInstances: List[Any],
        cluster: str = None,
        overrides: Dict[str, Any] = None,
        startedBy: str = None,
        group: str = None,
        networkConfiguration: Dict[str, Any] = None,
        tags: List[Any] = None,
        enableECSManagedTags: bool = None,
        propagateTags: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def stop_task(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def submit_attachment_state_changes(
        self, attachments: List[Any], cluster: str = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def submit_container_state_change(
        self,
        cluster: str = None,
        task: str = None,
        containerName: str = None,
        runtimeId: str = None,
        status: str = None,
        exitCode: int = None,
        reason: str = None,
        networkBindings: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def submit_task_state_change(
        self,
        cluster: str = None,
        task: str = None,
        status: str = None,
        reason: str = None,
        containers: List[Any] = None,
        attachments: List[Any] = None,
        pullStartedAt: datetime = None,
        pullStoppedAt: datetime = None,
        executionStoppedAt: datetime = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, resourceArn: str, tags: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_cluster_settings(
        self, cluster: str, settings: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_container_agent(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_container_instances_state(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_service(
        self,
        service: str,
        cluster: str = None,
        desiredCount: int = None,
        taskDefinition: str = None,
        deploymentConfiguration: Dict[str, Any] = None,
        networkConfiguration: Dict[str, Any] = None,
        platformVersion: str = None,
        forceNewDeployment: bool = None,
        healthCheckGracePeriodSeconds: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_service_primary_task_set(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_task_set(
        self, cluster: str, service: str, taskSet: str, scale: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass
