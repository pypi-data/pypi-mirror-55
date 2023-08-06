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
    def cancel_update_stack(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def continue_update_rollback(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_change_set(
        self,
        StackName: str,
        ChangeSetName: str,
        TemplateBody: str = None,
        TemplateURL: str = None,
        UsePreviousTemplate: bool = None,
        Parameters: List[Any] = None,
        Capabilities: List[Any] = None,
        ResourceTypes: List[Any] = None,
        RoleARN: str = None,
        RollbackConfiguration: Dict[str, Any] = None,
        NotificationARNs: List[Any] = None,
        Tags: List[Any] = None,
        ClientToken: str = None,
        Description: str = None,
        ChangeSetType: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_stack(
        self,
        StackName: str,
        TemplateBody: str = None,
        TemplateURL: str = None,
        Parameters: List[Any] = None,
        DisableRollback: bool = None,
        RollbackConfiguration: Dict[str, Any] = None,
        TimeoutInMinutes: int = None,
        NotificationARNs: List[Any] = None,
        Capabilities: List[Any] = None,
        ResourceTypes: List[Any] = None,
        RoleARN: str = None,
        OnFailure: str = None,
        StackPolicyBody: str = None,
        StackPolicyURL: str = None,
        Tags: List[Any] = None,
        ClientRequestToken: str = None,
        EnableTerminationProtection: bool = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_stack_instances(
        self,
        StackSetName: str,
        Accounts: List[Any],
        Regions: List[Any],
        ParameterOverrides: List[Any] = None,
        OperationPreferences: Dict[str, Any] = None,
        OperationId: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_stack_set(
        self,
        StackSetName: str,
        Description: str = None,
        TemplateBody: str = None,
        TemplateURL: str = None,
        Parameters: List[Any] = None,
        Capabilities: List[Any] = None,
        Tags: List[Any] = None,
        AdministrationRoleARN: str = None,
        ExecutionRoleName: str = None,
        ClientRequestToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_change_set(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_stack(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_stack_instances(
        self,
        StackSetName: str,
        Accounts: List[Any],
        Regions: List[Any],
        RetainStacks: bool,
        OperationPreferences: Dict[str, Any] = None,
        OperationId: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_stack_set(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_account_limits(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_change_set(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_stack_drift_detection_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_stack_events(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_stack_instance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_stack_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_stack_resource_drifts(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_stack_resources(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_stack_set(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_stack_set_operation(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_stacks(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def detect_stack_drift(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def detect_stack_resource_drift(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def estimate_template_cost(
        self,
        TemplateBody: str = None,
        TemplateURL: str = None,
        Parameters: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def execute_change_set(self) -> None:
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
    def get_stack_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_template_summary(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_change_sets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_exports(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_imports(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_stack_instances(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_stack_resources(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_stack_set_operation_results(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_stack_set_operations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_stack_sets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_stacks(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_stack_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def signal_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def stop_stack_set_operation(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_stack(
        self,
        StackName: str,
        TemplateBody: str = None,
        TemplateURL: str = None,
        UsePreviousTemplate: bool = None,
        StackPolicyDuringUpdateBody: str = None,
        StackPolicyDuringUpdateURL: str = None,
        Parameters: List[Any] = None,
        Capabilities: List[Any] = None,
        ResourceTypes: List[Any] = None,
        RoleARN: str = None,
        RollbackConfiguration: Dict[str, Any] = None,
        StackPolicyBody: str = None,
        StackPolicyURL: str = None,
        NotificationARNs: List[Any] = None,
        Tags: List[Any] = None,
        ClientRequestToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_stack_instances(
        self,
        StackSetName: str,
        Accounts: List[Any],
        Regions: List[Any],
        ParameterOverrides: List[Any] = None,
        OperationPreferences: Dict[str, Any] = None,
        OperationId: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_stack_set(
        self,
        StackSetName: str,
        Description: str = None,
        TemplateBody: str = None,
        TemplateURL: str = None,
        UsePreviousTemplate: bool = None,
        Parameters: List[Any] = None,
        Capabilities: List[Any] = None,
        Tags: List[Any] = None,
        OperationPreferences: Dict[str, Any] = None,
        AdministrationRoleARN: str = None,
        ExecutionRoleName: str = None,
        OperationId: str = None,
        Accounts: List[Any] = None,
        Regions: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_termination_protection(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def validate_template(self) -> None:
        pass
