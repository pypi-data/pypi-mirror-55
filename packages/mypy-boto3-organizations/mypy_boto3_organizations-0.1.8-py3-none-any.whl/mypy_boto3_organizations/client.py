from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    # pylint: disable=arguments-differ
    def accept_handshake(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def attach_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def cancel_handshake(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_account(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_gov_cloud_account(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_organization(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_organizational_unit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def decline_handshake(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_organization(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_organizational_unit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_account(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_create_account_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_handshake(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_organization(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_organizational_unit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def detach_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disable_aws_service_access(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disable_policy_type(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def enable_all_features(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def enable_aws_service_access(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def enable_policy_type(self) -> None:
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
    def invite_account_to_organization(
        self, Target: Dict[str, Any], Notes: str = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def leave_organization(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_accounts(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_accounts_for_parent(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_aws_service_access_for_organization(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_children(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_create_account_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_handshakes_for_account(
        self,
        Filter: Dict[str, Any] = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_handshakes_for_organization(
        self,
        Filter: Dict[str, Any] = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_organizational_units_for_parent(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_parents(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_policies(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_policies_for_target(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_roots(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_targets_for_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def move_account(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_account_from_organization(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, ResourceId: str, Tags: List[Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_organizational_unit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_policy(self) -> None:
        pass
