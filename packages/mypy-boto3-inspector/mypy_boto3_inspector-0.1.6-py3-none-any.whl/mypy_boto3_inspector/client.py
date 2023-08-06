from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def add_attributes_to_findings(
        self, findingArns: List[Any], attributes: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_assessment_target(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_assessment_template(
        self,
        assessmentTargetArn: str,
        assessmentTemplateName: str,
        durationInSeconds: int,
        rulesPackageArns: List[Any],
        userAttributesForFindings: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_exclusions_preview(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_resource_group(self, resourceGroupTags: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_assessment_run(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_assessment_target(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_assessment_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_assessment_runs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_assessment_targets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_assessment_templates(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_cross_account_access_role(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_exclusions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_findings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_resource_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_rules_packages(self) -> None:
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
    def get_assessment_report(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_exclusions_preview(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_telemetry_metadata(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_assessment_run_agents(
        self,
        assessmentRunArn: str,
        filter: Dict[str, Any] = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_assessment_runs(
        self,
        assessmentTemplateArns: List[Any] = None,
        filter: Dict[str, Any] = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_assessment_targets(
        self,
        filter: Dict[str, Any] = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_assessment_templates(
        self,
        assessmentTargetArns: List[Any] = None,
        filter: Dict[str, Any] = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_event_subscriptions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_exclusions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_findings(
        self,
        assessmentRunArns: List[Any] = None,
        filter: Dict[str, Any] = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_rules_packages(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def preview_agents(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def register_cross_account_access_role(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_attributes_from_findings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_tags_for_resource(self, resourceArn: str, tags: List[Any] = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_assessment_run(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def stop_assessment_run(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def subscribe_to_event(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def unsubscribe_from_event(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_assessment_target(self) -> None:
        pass
