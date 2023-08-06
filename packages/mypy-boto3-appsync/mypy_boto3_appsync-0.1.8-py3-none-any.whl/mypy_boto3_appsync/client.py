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
    def create_api_key(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_data_source(
        self,
        apiId: str,
        name: str,
        type: str,
        description: str = None,
        serviceRoleArn: str = None,
        dynamodbConfig: Dict[str, Any] = None,
        lambdaConfig: Dict[str, Any] = None,
        elasticsearchConfig: Dict[str, Any] = None,
        httpConfig: Dict[str, Any] = None,
        relationalDatabaseConfig: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_function(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_graphql_api(
        self,
        name: str,
        authenticationType: str,
        logConfig: Dict[str, Any] = None,
        userPoolConfig: Dict[str, Any] = None,
        openIDConnectConfig: Dict[str, Any] = None,
        tags: Dict[str, Any] = None,
        additionalAuthenticationProviders: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_resolver(
        self,
        apiId: str,
        typeName: str,
        fieldName: str,
        requestMappingTemplate: str,
        dataSourceName: str = None,
        responseMappingTemplate: str = None,
        kind: str = None,
        pipelineConfig: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_type(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_api_key(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_data_source(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_function(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_graphql_api(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_resolver(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_type(self) -> None:
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
    def get_data_source(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_function(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_graphql_api(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_introspection_schema(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_resolver(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_schema_creation_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_type(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_api_keys(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_data_sources(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_functions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_graphql_apis(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_resolvers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_resolvers_by_function(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_types(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_schema_creation(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, resourceArn: str, tags: Dict[str, Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_api_key(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_data_source(
        self,
        apiId: str,
        name: str,
        type: str,
        description: str = None,
        serviceRoleArn: str = None,
        dynamodbConfig: Dict[str, Any] = None,
        lambdaConfig: Dict[str, Any] = None,
        elasticsearchConfig: Dict[str, Any] = None,
        httpConfig: Dict[str, Any] = None,
        relationalDatabaseConfig: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_function(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_graphql_api(
        self,
        apiId: str,
        name: str,
        logConfig: Dict[str, Any] = None,
        authenticationType: str = None,
        userPoolConfig: Dict[str, Any] = None,
        openIDConnectConfig: Dict[str, Any] = None,
        additionalAuthenticationProviders: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_resolver(
        self,
        apiId: str,
        typeName: str,
        fieldName: str,
        requestMappingTemplate: str,
        dataSourceName: str = None,
        responseMappingTemplate: str = None,
        kind: str = None,
        pipelineConfig: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_type(self) -> None:
        pass
