from __future__ import annotations

from typing import Any
from typing import Dict

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
    def create_component(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_application(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_component(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_application(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_component(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_component_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_component_configuration_recommendation(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_observation(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_problem(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_problem_observations(self) -> None:
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
    def list_applications(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_components(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_problems(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_application(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_component(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_component_configuration(self) -> None:
        pass
