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
    def create_activity(self, name: str, tags: List[Any] = None) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_state_machine(
        self, name: str, definition: str, roleArn: str, tags: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_activity(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_state_machine(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_activity(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_execution(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_state_machine(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_state_machine_for_execution(self) -> None:
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
    def get_activity_task(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_execution_history(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_activities(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_executions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_state_machines(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def send_task_failure(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def send_task_heartbeat(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def send_task_success(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_execution(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def stop_execution(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, resourceArn: str, tags: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_state_machine(self) -> None:
        pass
