from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def batch_update_schedule(
        self,
        ChannelId: str,
        Creates: Dict[str, Any] = None,
        Deletes: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_channel(
        self,
        ChannelClass: str = None,
        Destinations: List[Any] = None,
        EncoderSettings: Dict[str, Any] = None,
        InputAttachments: List[Any] = None,
        InputSpecification: Dict[str, Any] = None,
        LogLevel: str = None,
        Name: str = None,
        RequestId: str = None,
        Reserved: str = None,
        RoleArn: str = None,
        Tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_input(
        self,
        Destinations: List[Any] = None,
        InputSecurityGroups: List[Any] = None,
        MediaConnectFlows: List[Any] = None,
        Name: str = None,
        RequestId: str = None,
        RoleArn: str = None,
        Sources: List[Any] = None,
        Tags: Dict[str, Any] = None,
        Type: str = None,
        Vpc: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_input_security_group(
        self, Tags: Dict[str, Any] = None, WhitelistRules: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_tags(self, ResourceArn: str, Tags: Dict[str, Any] = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_channel(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_input(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_input_security_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_reservation(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_schedule(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_tags(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_channel(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_input(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_input_security_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_offering(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_reservation(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_schedule(self) -> None:
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
    def list_channels(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_input_security_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_inputs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_offerings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_reservations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def purchase_offering(
        self,
        Count: int,
        OfferingId: str,
        Name: str = None,
        RequestId: str = None,
        Start: str = None,
        Tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def start_channel(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def stop_channel(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_channel(
        self,
        ChannelId: str,
        Destinations: List[Any] = None,
        EncoderSettings: Dict[str, Any] = None,
        InputAttachments: List[Any] = None,
        InputSpecification: Dict[str, Any] = None,
        LogLevel: str = None,
        Name: str = None,
        RoleArn: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_channel_class(
        self, ChannelClass: str, ChannelId: str, Destinations: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_input(
        self,
        InputId: str,
        Destinations: List[Any] = None,
        InputSecurityGroups: List[Any] = None,
        MediaConnectFlows: List[Any] = None,
        Name: str = None,
        RoleArn: str = None,
        Sources: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_input_security_group(
        self,
        InputSecurityGroupId: str,
        Tags: Dict[str, Any] = None,
        WhitelistRules: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_reservation(self) -> None:
        pass
