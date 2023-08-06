from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def accept_shared_directory(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def add_ip_routes(
        self,
        DirectoryId: str,
        IpRoutes: List[Any],
        UpdateSecurityGroupForDirectoryControllers: bool = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def add_tags_to_resource(self, ResourceId: str, Tags: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def cancel_schema_extension(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def connect_directory(
        self,
        Name: str,
        Password: str,
        Size: str,
        ConnectSettings: Dict[str, Any],
        ShortName: str = None,
        Description: str = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_alias(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_computer(
        self,
        DirectoryId: str,
        ComputerName: str,
        Password: str,
        OrganizationalUnitDistinguishedName: str = None,
        ComputerAttributes: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_conditional_forwarder(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_directory(
        self,
        Name: str,
        Password: str,
        Size: str,
        ShortName: str = None,
        Description: str = None,
        VpcSettings: Dict[str, Any] = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_log_subscription(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_microsoft_ad(
        self,
        Name: str,
        Password: str,
        VpcSettings: Dict[str, Any],
        ShortName: str = None,
        Description: str = None,
        Edition: str = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_snapshot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_trust(
        self,
        DirectoryId: str,
        RemoteDomainName: str,
        TrustPassword: str,
        TrustDirection: str,
        TrustType: str = None,
        ConditionalForwarderIpAddrs: List[Any] = None,
        SelectiveAuth: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_conditional_forwarder(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_directory(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_log_subscription(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_snapshot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_trust(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deregister_event_topic(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_conditional_forwarders(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_directories(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_domain_controllers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_event_topics(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_shared_directories(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_snapshots(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_trusts(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disable_radius(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disable_sso(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def enable_radius(
        self, DirectoryId: str, RadiusSettings: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def enable_sso(self) -> None:
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
    def get_directory_limits(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_snapshot_limits(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_ip_routes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_log_subscriptions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_schema_extensions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def register_event_topic(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reject_shared_directory(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_ip_routes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_tags_from_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reset_user_password(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def restore_from_snapshot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def share_directory(
        self,
        DirectoryId: str,
        ShareTarget: Dict[str, Any],
        ShareMethod: str,
        ShareNotes: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def start_schema_extension(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def unshare_directory(
        self, DirectoryId: str, UnshareTarget: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_conditional_forwarder(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_number_of_domain_controllers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_radius(
        self, DirectoryId: str, RadiusSettings: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_trust(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def verify_trust(self) -> None:
        pass
