from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def associate_role_to_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def associate_service_role_to_account(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_connector_definition(
        self,
        AmznClientToken: str = None,
        InitialVersion: Dict[str, Any] = None,
        Name: str = None,
        tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_connector_definition_version(
        self,
        ConnectorDefinitionId: str,
        AmznClientToken: str = None,
        Connectors: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_core_definition(
        self,
        AmznClientToken: str = None,
        InitialVersion: Dict[str, Any] = None,
        Name: str = None,
        tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_core_definition_version(
        self,
        CoreDefinitionId: str,
        AmznClientToken: str = None,
        Cores: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_deployment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_device_definition(
        self,
        AmznClientToken: str = None,
        InitialVersion: Dict[str, Any] = None,
        Name: str = None,
        tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_device_definition_version(
        self,
        DeviceDefinitionId: str,
        AmznClientToken: str = None,
        Devices: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_function_definition(
        self,
        AmznClientToken: str = None,
        InitialVersion: Dict[str, Any] = None,
        Name: str = None,
        tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_function_definition_version(
        self,
        FunctionDefinitionId: str,
        AmznClientToken: str = None,
        DefaultConfig: Dict[str, Any] = None,
        Functions: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_group(
        self,
        AmznClientToken: str = None,
        InitialVersion: Dict[str, Any] = None,
        Name: str = None,
        tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_group_certificate_authority(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_group_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_logger_definition(
        self,
        AmznClientToken: str = None,
        InitialVersion: Dict[str, Any] = None,
        Name: str = None,
        tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_logger_definition_version(
        self,
        LoggerDefinitionId: str,
        AmznClientToken: str = None,
        Loggers: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_resource_definition(
        self,
        AmznClientToken: str = None,
        InitialVersion: Dict[str, Any] = None,
        Name: str = None,
        tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_resource_definition_version(
        self,
        ResourceDefinitionId: str,
        AmznClientToken: str = None,
        Resources: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_software_update_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_subscription_definition(
        self,
        AmznClientToken: str = None,
        InitialVersion: Dict[str, Any] = None,
        Name: str = None,
        tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_subscription_definition_version(
        self,
        SubscriptionDefinitionId: str,
        AmznClientToken: str = None,
        Subscriptions: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_connector_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_core_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_device_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_function_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_logger_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_resource_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_subscription_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_role_from_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_service_role_from_account(self) -> None:
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
    def get_associated_role(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_bulk_deployment_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_connectivity_info(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_connector_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_connector_definition_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_core_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_core_definition_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_deployment_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_device_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_device_definition_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_function_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_function_definition_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_group_certificate_authority(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_group_certificate_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_group_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_logger_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_logger_definition_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_resource_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_resource_definition_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_service_role_for_account(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_subscription_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_subscription_definition_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_bulk_deployment_detailed_reports(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_bulk_deployments(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_connector_definition_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_connector_definitions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_core_definition_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_core_definitions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_deployments(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_device_definition_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_device_definitions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_function_definition_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_function_definitions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_group_certificate_authorities(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_group_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_logger_definition_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_logger_definitions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_resource_definition_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_resource_definitions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_subscription_definition_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_subscription_definitions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reset_deployments(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_bulk_deployment(
        self,
        ExecutionRoleArn: str,
        InputFileUri: str,
        AmznClientToken: str = None,
        tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def stop_bulk_deployment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, ResourceArn: str, tags: Dict[str, Any] = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_connectivity_info(
        self, ThingName: str, ConnectivityInfo: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_connector_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_core_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_device_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_function_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_group_certificate_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_logger_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_resource_definition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_subscription_definition(self) -> None:
        pass
