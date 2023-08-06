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
    def batch_get_aggregate_resource_config(
        self, ConfigurationAggregatorName: str, ResourceIdentifiers: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def batch_get_resource_config(self, resourceKeys: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_aggregation_authorization(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_config_rule(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_configuration_aggregator(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_configuration_recorder(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_delivery_channel(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_evaluation_results(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_organization_config_rule(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_pending_aggregation_request(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_remediation_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_remediation_exceptions(
        self, ConfigRuleName: str, ResourceKeys: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_retention_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deliver_config_snapshot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_aggregate_compliance_by_config_rules(
        self,
        ConfigurationAggregatorName: str,
        Filters: Dict[str, Any] = None,
        Limit: int = None,
        NextToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def describe_aggregation_authorizations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_compliance_by_config_rule(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_compliance_by_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_config_rule_evaluation_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_config_rules(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_configuration_aggregator_sources_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_configuration_aggregators(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_configuration_recorder_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_configuration_recorders(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_delivery_channel_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_delivery_channels(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_organization_config_rule_statuses(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_organization_config_rules(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_pending_aggregation_requests(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_remediation_configurations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_remediation_exceptions(
        self,
        ConfigRuleName: str,
        ResourceKeys: List[Any] = None,
        Limit: int = None,
        NextToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def describe_remediation_execution_status(
        self,
        ConfigRuleName: str,
        ResourceKeys: List[Any] = None,
        Limit: int = None,
        NextToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def describe_retention_configurations(self) -> None:
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
    def get_aggregate_compliance_details_by_config_rule(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_aggregate_config_rule_compliance_summary(
        self,
        ConfigurationAggregatorName: str,
        Filters: Dict[str, Any] = None,
        GroupByKey: str = None,
        Limit: int = None,
        NextToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_aggregate_discovered_resource_counts(
        self,
        ConfigurationAggregatorName: str,
        Filters: Dict[str, Any] = None,
        GroupByKey: str = None,
        Limit: int = None,
        NextToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_aggregate_resource_config(
        self, ConfigurationAggregatorName: str, ResourceIdentifier: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_compliance_details_by_config_rule(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_compliance_details_by_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_compliance_summary_by_config_rule(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_compliance_summary_by_resource_type(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_discovered_resource_counts(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_organization_config_rule_detailed_status(
        self,
        OrganizationConfigRuleName: str,
        Filters: Dict[str, Any] = None,
        Limit: int = None,
        NextToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_resource_config_history(
        self,
        resourceType: str,
        resourceId: str,
        laterTime: datetime = None,
        earlierTime: datetime = None,
        chronologicalOrder: str = None,
        limit: int = None,
        nextToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_aggregate_discovered_resources(
        self,
        ConfigurationAggregatorName: str,
        ResourceType: str,
        Filters: Dict[str, Any] = None,
        Limit: int = None,
        NextToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_discovered_resources(
        self,
        resourceType: str,
        resourceIds: List[Any] = None,
        resourceName: str = None,
        limit: int = None,
        includeDeletedResources: bool = None,
        nextToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_aggregation_authorization(
        self, AuthorizedAccountId: str, AuthorizedAwsRegion: str, Tags: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_config_rule(
        self, ConfigRule: Dict[str, Any], Tags: List[Any] = None
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_configuration_aggregator(
        self,
        ConfigurationAggregatorName: str,
        AccountAggregationSources: List[Any] = None,
        OrganizationAggregationSource: Dict[str, Any] = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_configuration_recorder(self, ConfigurationRecorder: Dict[str, Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_delivery_channel(self, DeliveryChannel: Dict[str, Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_evaluations(
        self, ResultToken: str, Evaluations: List[Any] = None, TestMode: bool = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_organization_config_rule(
        self,
        OrganizationConfigRuleName: str,
        OrganizationManagedRuleMetadata: Dict[str, Any] = None,
        OrganizationCustomRuleMetadata: Dict[str, Any] = None,
        ExcludedAccounts: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_remediation_configurations(
        self, RemediationConfigurations: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_remediation_exceptions(
        self,
        ConfigRuleName: str,
        ResourceKeys: List[Any],
        Message: str = None,
        ExpirationTime: datetime = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_retention_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def select_resource_config(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_config_rules_evaluation(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_configuration_recorder(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_remediation_execution(
        self, ConfigRuleName: str, ResourceKeys: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def stop_configuration_recorder(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, ResourceArn: str, Tags: List[Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass
