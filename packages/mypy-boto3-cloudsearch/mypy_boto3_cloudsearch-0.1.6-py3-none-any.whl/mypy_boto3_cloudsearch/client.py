from __future__ import annotations

from typing import Any
from typing import Dict

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def build_suggesters(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_domain(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def define_analysis_scheme(
        self, DomainName: str, AnalysisScheme: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def define_expression(
        self, DomainName: str, Expression: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def define_index_field(
        self, DomainName: str, IndexField: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def define_suggester(
        self, DomainName: str, Suggester: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_analysis_scheme(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_domain(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_expression(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_index_field(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_suggester(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_analysis_schemes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_availability_options(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_domains(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_expressions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_index_fields(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_scaling_parameters(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_service_access_policies(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_suggesters(self) -> None:
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
    def index_documents(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_domain_names(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_availability_options(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_scaling_parameters(
        self, DomainName: str, ScalingParameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_service_access_policies(self) -> None:
        pass
