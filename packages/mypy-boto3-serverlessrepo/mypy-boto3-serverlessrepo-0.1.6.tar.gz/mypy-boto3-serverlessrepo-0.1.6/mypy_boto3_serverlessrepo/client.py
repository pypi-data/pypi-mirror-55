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
    def create_application(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_application_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_cloud_formation_change_set(
        self,
        ApplicationId: str,
        StackName: str,
        Capabilities: List[Any] = None,
        ChangeSetName: str = None,
        ClientToken: str = None,
        Description: str = None,
        NotificationArns: List[Any] = None,
        ParameterOverrides: List[Any] = None,
        ResourceTypes: List[Any] = None,
        RollbackConfiguration: Dict[str, Any] = None,
        SemanticVersion: str = None,
        Tags: List[Any] = None,
        TemplateId: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_cloud_formation_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_application(self) -> None:
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
    def get_application(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_application_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_cloud_formation_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_application_dependencies(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_application_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_applications(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_application_policy(
        self, ApplicationId: str, Statements: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_application(self) -> None:
        pass
