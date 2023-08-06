from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from boto3.resources.base import ServiceResource as Boto3ServiceResource
from boto3.resources.collection import ResourceCollection

# pylint: disable=import-self
import mypy_boto3_sns.service_resource as mypy_boto3_sns_scope


class ServiceResource(Boto3ServiceResource):
    platform_applications: mypy_boto3_sns_scope.platform_applications
    subscriptions: mypy_boto3_sns_scope.subscriptions
    topics: mypy_boto3_sns_scope.topics

    # pylint: disable=arguments-differ
    def PlatformApplication(
        self, arn: str = None
    ) -> mypy_boto3_sns_scope.PlatformApplication:
        pass

    # pylint: disable=arguments-differ
    def PlatformEndpoint(
        self, arn: str = None
    ) -> mypy_boto3_sns_scope.PlatformEndpoint:
        pass

    # pylint: disable=arguments-differ
    def Subscription(self, arn: str = None) -> mypy_boto3_sns_scope.Subscription:
        pass

    # pylint: disable=arguments-differ
    def Topic(self, arn: str = None) -> mypy_boto3_sns_scope.Topic:
        pass

    # pylint: disable=arguments-differ
    def create_platform_application(
        self, Name: str, Platform: str, Attributes: Dict[str, Any]
    ) -> mypy_boto3_sns_scope.PlatformApplication:
        pass

    # pylint: disable=arguments-differ
    def create_topic(
        self, Name: str, Attributes: Dict[str, Any] = None, Tags: List[Any] = None
    ) -> mypy_boto3_sns_scope.Topic:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass


class PlatformApplication(Boto3ServiceResource):
    attributes: Dict[str, Any]
    arn: str
    endpoints: mypy_boto3_sns_scope.endpoints

    # pylint: disable=arguments-differ
    def create_platform_endpoint(
        self, Token: str, CustomUserData: str = None, Attributes: Dict[str, Any] = None
    ) -> mypy_boto3_sns_scope.PlatformEndpoint:
        pass

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_attributes(self, Attributes: Dict[str, Any]) -> None:
        pass


class PlatformEndpoint(Boto3ServiceResource):
    attributes: Dict[str, Any]
    arn: str

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def publish(
        self,
        Message: str,
        TopicArn: str = None,
        PhoneNumber: str = None,
        Subject: str = None,
        MessageStructure: str = None,
        MessageAttributes: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_attributes(self, Attributes: Dict[str, Any]) -> None:
        pass


class Subscription(Boto3ServiceResource):
    attributes: Dict[str, Any]
    arn: str

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_attributes(self) -> None:
        pass


class Topic(Boto3ServiceResource):
    attributes: Dict[str, Any]
    arn: str
    subscriptions: mypy_boto3_sns_scope.subscriptions

    # pylint: disable=arguments-differ
    def add_permission(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def confirm_subscription(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def publish(
        self,
        Message: str,
        TargetArn: str = None,
        PhoneNumber: str = None,
        Subject: str = None,
        MessageStructure: str = None,
        MessageAttributes: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_permission(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def subscribe(
        self,
        Protocol: str,
        Endpoint: str = None,
        Attributes: Dict[str, Any] = None,
        ReturnSubscriptionArn: bool = None,
    ) -> mypy_boto3_sns_scope.Subscription:
        pass


class platform_applications(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class subscriptions(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class topics(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class endpoints(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass
