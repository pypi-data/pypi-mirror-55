from __future__ import annotations

from typing import Any
from typing import Dict

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    # pylint: disable=arguments-differ
    def associate_service_quota_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_service_quota_increase_request_from_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_service_quota_template(self) -> None:
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
    def get_association_for_service_quota_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_aws_default_service_quota(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_requested_service_quota_change(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_service_quota(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_service_quota_increase_request_from_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_aws_default_service_quotas(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_requested_service_quota_change_history(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_requested_service_quota_change_history_by_quota(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_service_quota_increase_requests_in_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_service_quotas(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_services(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_service_quota_increase_request_into_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def request_service_quota_increase(self) -> None:
        pass
