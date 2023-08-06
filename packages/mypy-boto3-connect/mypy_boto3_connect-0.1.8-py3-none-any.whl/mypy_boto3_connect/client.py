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
    def create_user(
        self,
        Username: str,
        PhoneConfig: Dict[str, Any],
        SecurityProfileIds: List[Any],
        RoutingProfileId: str,
        InstanceId: str,
        Password: str = None,
        IdentityInfo: Dict[str, Any] = None,
        DirectoryUserId: str = None,
        HierarchyGroupId: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_user_hierarchy_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_user_hierarchy_structure(self) -> None:
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
    def get_contact_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_current_metric_data(
        self,
        InstanceId: str,
        Filters: Dict[str, Any],
        CurrentMetrics: List[Any],
        Groupings: List[Any] = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_federation_token(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_metric_data(
        self,
        InstanceId: str,
        StartTime: datetime,
        EndTime: datetime,
        Filters: Dict[str, Any],
        HistoricalMetrics: List[Any],
        Groupings: List[Any] = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_contact_flows(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_hours_of_operations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_phone_numbers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_queues(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_routing_profiles(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_security_profiles(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_user_hierarchy_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_users(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_outbound_voice_contact(
        self,
        DestinationPhoneNumber: str,
        ContactFlowId: str,
        InstanceId: str,
        ClientToken: str = None,
        SourcePhoneNumber: str = None,
        QueueId: str = None,
        Attributes: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def stop_contact(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_contact_attributes(
        self, InitialContactId: str, InstanceId: str, Attributes: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_user_hierarchy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_user_identity_info(
        self, IdentityInfo: Dict[str, Any], UserId: str, InstanceId: str
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_user_phone_config(
        self, PhoneConfig: Dict[str, Any], UserId: str, InstanceId: str
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_user_routing_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_user_security_profiles(self) -> None:
        pass
