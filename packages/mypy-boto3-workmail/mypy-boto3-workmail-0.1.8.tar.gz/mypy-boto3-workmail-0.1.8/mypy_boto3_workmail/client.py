from __future__ import annotations

from typing import Any
from typing import Dict

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    # pylint: disable=arguments-differ
    def associate_delegate_to_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def associate_member_to_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_alias(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_alias(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_mailbox_permissions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deregister_from_work_mail(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_organization(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_delegate_from_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_member_from_group(self) -> None:
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
    def get_mailbox_details(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_aliases(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_group_members(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_mailbox_permissions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_organizations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_resource_delegates(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_resources(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_users(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_mailbox_permissions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def register_to_work_mail(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reset_password(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_mailbox_quota(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_primary_email_address(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_resource(
        self,
        OrganizationId: str,
        ResourceId: str,
        Name: str = None,
        BookingOptions: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass
