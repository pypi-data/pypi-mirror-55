from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def abort_document_version_upload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def activate_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def add_resource_permissions(
        self,
        ResourceId: str,
        Principals: List[Any],
        AuthenticationToken: str = None,
        NotificationOptions: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_comment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_custom_metadata(
        self,
        ResourceId: str,
        CustomMetadata: Dict[str, Any],
        AuthenticationToken: str = None,
        VersionId: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_folder(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_labels(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_notification_subscription(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_user(
        self,
        Username: str,
        GivenName: str,
        Surname: str,
        Password: str,
        OrganizationId: str = None,
        EmailAddress: str = None,
        TimeZoneId: str = None,
        StorageRule: Dict[str, Any] = None,
        AuthenticationToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def deactivate_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_comment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_custom_metadata(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_document(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_folder(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_folder_contents(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_labels(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_notification_subscription(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_activities(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_comments(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_document_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_folder_contents(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_notification_subscriptions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_resource_permissions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_root_folders(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_users(self) -> None:
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
    def get_current_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_document(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_document_path(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_document_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_folder(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_folder_path(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_resources(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def initiate_document_version_upload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_all_resource_permissions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_resource_permission(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_document(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_document_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_folder(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_user(
        self,
        UserId: str,
        AuthenticationToken: str = None,
        GivenName: str = None,
        Surname: str = None,
        Type: str = None,
        StorageRule: Dict[str, Any] = None,
        TimeZoneId: str = None,
        Locale: str = None,
        GrantPoweruserPrivileges: str = None,
    ) -> Dict[str, Any]:
        pass
