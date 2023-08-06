from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def associate_vpc_with_hosted_zone(
        self, HostedZoneId: str, VPC: Dict[str, Any], Comment: str = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def change_resource_record_sets(
        self, HostedZoneId: str, ChangeBatch: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def change_tags_for_resource(
        self,
        ResourceType: str,
        ResourceId: str,
        AddTags: List[Any] = None,
        RemoveTagKeys: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_health_check(
        self, CallerReference: str, HealthCheckConfig: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_hosted_zone(
        self,
        Name: str,
        CallerReference: str,
        VPC: Dict[str, Any] = None,
        HostedZoneConfig: Dict[str, Any] = None,
        DelegationSetId: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_query_logging_config(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_reusable_delegation_set(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_traffic_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_traffic_policy_instance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_traffic_policy_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_vpc_association_authorization(
        self, HostedZoneId: str, VPC: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_health_check(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_hosted_zone(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_query_logging_config(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_reusable_delegation_set(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_traffic_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_traffic_policy_instance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_vpc_association_authorization(
        self, HostedZoneId: str, VPC: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def disassociate_vpc_from_hosted_zone(
        self, HostedZoneId: str, VPC: Dict[str, Any], Comment: str = None
    ) -> Dict[str, Any]:
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
    def get_account_limit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_change(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_checker_ip_ranges(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_geo_location(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_health_check(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_health_check_count(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_health_check_last_failure_reason(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_health_check_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_hosted_zone(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_hosted_zone_count(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_hosted_zone_limit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_query_logging_config(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_reusable_delegation_set(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_reusable_delegation_set_limit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_traffic_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_traffic_policy_instance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_traffic_policy_instance_count(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_geo_locations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_health_checks(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_hosted_zones(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_hosted_zones_by_name(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_query_logging_configs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_resource_record_sets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_reusable_delegation_sets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resources(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_traffic_policies(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_traffic_policy_instances(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_traffic_policy_instances_by_hosted_zone(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_traffic_policy_instances_by_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_traffic_policy_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_vpc_association_authorizations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def test_dns_answer(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_health_check(
        self,
        HealthCheckId: str,
        HealthCheckVersion: int = None,
        IPAddress: str = None,
        Port: int = None,
        ResourcePath: str = None,
        FullyQualifiedDomainName: str = None,
        SearchString: str = None,
        FailureThreshold: int = None,
        Inverted: bool = None,
        Disabled: bool = None,
        HealthThreshold: int = None,
        ChildHealthChecks: List[Any] = None,
        EnableSNI: bool = None,
        Regions: List[Any] = None,
        AlarmIdentifier: Dict[str, Any] = None,
        InsufficientDataHealthStatus: str = None,
        ResetElements: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_hosted_zone_comment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_traffic_policy_comment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_traffic_policy_instance(self) -> None:
        pass
