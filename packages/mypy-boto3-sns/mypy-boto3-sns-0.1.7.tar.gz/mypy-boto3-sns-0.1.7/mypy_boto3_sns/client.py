from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def add_permission(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def check_if_phone_number_is_opted_out(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def confirm_subscription(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_platform_application(
        self, Name: str, Platform: str, Attributes: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_platform_endpoint(
        self,
        PlatformApplicationArn: str,
        Token: str,
        CustomUserData: str = None,
        Attributes: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_topic(
        self, Name: str, Attributes: Dict[str, Any] = None, Tags: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_endpoint(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_platform_application(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_topic(self) -> None:
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
    def get_endpoint_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_platform_application_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_sms_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_subscription_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_topic_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_endpoints_by_platform_application(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_phone_numbers_opted_out(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_platform_applications(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_subscriptions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_subscriptions_by_topic(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_topics(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def opt_in_phone_number(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def publish(
        self,
        Message: str,
        TopicArn: str = None,
        TargetArn: str = None,
        PhoneNumber: str = None,
        Subject: str = None,
        MessageStructure: str = None,
        MessageAttributes: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def remove_permission(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_endpoint_attributes(
        self, EndpointArn: str, Attributes: Dict[str, Any]
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_platform_application_attributes(
        self, PlatformApplicationArn: str, Attributes: Dict[str, Any]
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_sms_attributes(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def set_subscription_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_topic_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def subscribe(
        self,
        TopicArn: str,
        Protocol: str,
        Endpoint: str = None,
        Attributes: Dict[str, Any] = None,
        ReturnSubscriptionArn: bool = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, ResourceArn: str, Tags: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def unsubscribe(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass
