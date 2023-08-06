from __future__ import annotations

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
    def create_configuration_set(
        self,
        ConfigurationSetName: str,
        TrackingOptions: Dict[str, Any] = None,
        DeliveryOptions: Dict[str, Any] = None,
        ReputationOptions: Dict[str, Any] = None,
        SendingOptions: Dict[str, Any] = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_configuration_set_event_destination(
        self,
        ConfigurationSetName: str,
        EventDestinationName: str,
        EventDestination: Dict[str, Any],
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_dedicated_ip_pool(
        self, PoolName: str, Tags: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_deliverability_test_report(
        self,
        FromEmailAddress: str,
        Content: Dict[str, Any],
        ReportName: str = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_email_identity(
        self, EmailIdentity: str, Tags: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_configuration_set(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_configuration_set_event_destination(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_dedicated_ip_pool(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_email_identity(self) -> None:
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
    def get_account(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_blacklist_reports(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_configuration_set(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_configuration_set_event_destinations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_dedicated_ip(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_dedicated_ips(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_deliverability_dashboard_options(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_deliverability_test_report(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_domain_deliverability_campaign(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_domain_statistics_report(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_email_identity(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_configuration_sets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_dedicated_ip_pools(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_deliverability_test_reports(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_domain_deliverability_campaigns(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_email_identities(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_account_dedicated_ip_warmup_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_account_sending_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_configuration_set_delivery_options(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_configuration_set_reputation_options(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_configuration_set_sending_options(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_configuration_set_tracking_options(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_dedicated_ip_in_pool(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_dedicated_ip_warmup_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_deliverability_dashboard_option(
        self, DashboardEnabled: bool, SubscribedDomains: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_email_identity_dkim_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_email_identity_feedback_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_email_identity_mail_from_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def send_email(
        self,
        Destination: Dict[str, Any],
        Content: Dict[str, Any],
        FromEmailAddress: str = None,
        ReplyToAddresses: List[Any] = None,
        FeedbackForwardingEmailAddress: str = None,
        EmailTags: List[Any] = None,
        ConfigurationSetName: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, ResourceArn: str, Tags: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_configuration_set_event_destination(
        self,
        ConfigurationSetName: str,
        EventDestinationName: str,
        EventDestination: Dict[str, Any],
    ) -> Dict[str, Any]:
        pass
