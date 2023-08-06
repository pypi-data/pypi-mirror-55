from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def activate_event_source(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_event_bus(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_partner_event_source(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deactivate_event_source(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_event_bus(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_partner_event_source(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_rule(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_event_bus(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_event_source(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_partner_event_source(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_rule(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disable_rule(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def enable_rule(self) -> None:
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
    def list_event_buses(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_event_sources(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_partner_event_source_accounts(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_partner_event_sources(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_rule_names_by_target(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_rules(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_targets_by_rule(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_events(self, Entries: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_partner_events(self, Entries: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_permission(
        self,
        Action: str,
        Principal: str,
        StatementId: str,
        EventBusName: str = None,
        Condition: Dict[str, Any] = None,
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_rule(
        self,
        Name: str,
        ScheduleExpression: str = None,
        EventPattern: str = None,
        State: str = None,
        Description: str = None,
        RoleArn: str = None,
        Tags: List[Any] = None,
        EventBusName: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_targets(
        self, Rule: str, Targets: List[Any], EventBusName: str = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def remove_permission(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_targets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, ResourceARN: str, Tags: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def test_event_pattern(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass
