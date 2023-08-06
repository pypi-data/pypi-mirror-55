from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def abort_environment_update(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def apply_environment_managed_action(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def check_dns_availability(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def compose_environments(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_application(
        self,
        ApplicationName: str,
        Description: str = None,
        ResourceLifecycleConfig: Dict[str, Any] = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_application_version(
        self,
        ApplicationName: str,
        VersionLabel: str,
        Description: str = None,
        SourceBuildInformation: Dict[str, Any] = None,
        SourceBundle: Dict[str, Any] = None,
        BuildConfiguration: Dict[str, Any] = None,
        AutoCreateApplication: bool = None,
        Process: bool = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_configuration_template(
        self,
        ApplicationName: str,
        TemplateName: str,
        SolutionStackName: str = None,
        PlatformArn: str = None,
        SourceConfiguration: Dict[str, Any] = None,
        EnvironmentId: str = None,
        Description: str = None,
        OptionSettings: List[Any] = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_environment(
        self,
        ApplicationName: str,
        EnvironmentName: str = None,
        GroupName: str = None,
        Description: str = None,
        CNAMEPrefix: str = None,
        Tier: Dict[str, Any] = None,
        Tags: List[Any] = None,
        VersionLabel: str = None,
        TemplateName: str = None,
        SolutionStackName: str = None,
        PlatformArn: str = None,
        OptionSettings: List[Any] = None,
        OptionsToRemove: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_platform_version(
        self,
        PlatformName: str,
        PlatformVersion: str,
        PlatformDefinitionBundle: Dict[str, Any],
        EnvironmentName: str = None,
        OptionSettings: List[Any] = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_storage_location(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_application(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_application_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_configuration_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_environment_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_platform_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_account_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_application_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_applications(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_configuration_options(
        self,
        ApplicationName: str = None,
        TemplateName: str = None,
        EnvironmentName: str = None,
        SolutionStackName: str = None,
        PlatformArn: str = None,
        Options: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def describe_configuration_settings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_environment_health(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_environment_managed_action_history(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_environment_managed_actions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_environment_resources(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_environments(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_events(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_instances_health(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_platform_version(self) -> None:
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
    def list_available_solution_stacks(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_platform_versions(
        self, Filters: List[Any] = None, MaxRecords: int = None, NextToken: str = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def rebuild_environment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def request_environment_info(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def restart_app_server(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def retrieve_environment_info(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def swap_environment_cnames(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def terminate_environment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_application(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_application_resource_lifecycle(
        self, ApplicationName: str, ResourceLifecycleConfig: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_application_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_configuration_template(
        self,
        ApplicationName: str,
        TemplateName: str,
        Description: str = None,
        OptionSettings: List[Any] = None,
        OptionsToRemove: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_environment(
        self,
        ApplicationName: str = None,
        EnvironmentId: str = None,
        EnvironmentName: str = None,
        GroupName: str = None,
        Description: str = None,
        Tier: Dict[str, Any] = None,
        VersionLabel: str = None,
        TemplateName: str = None,
        SolutionStackName: str = None,
        PlatformArn: str = None,
        OptionSettings: List[Any] = None,
        OptionsToRemove: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_tags_for_resource(
        self,
        ResourceArn: str,
        TagsToAdd: List[Any] = None,
        TagsToRemove: List[Any] = None,
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def validate_configuration_settings(
        self,
        ApplicationName: str,
        OptionSettings: List[Any],
        TemplateName: str = None,
        EnvironmentName: str = None,
    ) -> Dict[str, Any]:
        pass
