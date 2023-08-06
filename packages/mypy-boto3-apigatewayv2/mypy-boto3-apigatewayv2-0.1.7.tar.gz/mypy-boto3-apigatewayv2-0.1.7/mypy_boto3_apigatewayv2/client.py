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
    def create_api(
        self,
        Name: str,
        ProtocolType: str,
        RouteSelectionExpression: str,
        ApiKeySelectionExpression: str = None,
        Description: str = None,
        DisableSchemaValidation: bool = None,
        Version: str = None,
        Tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_api_mapping(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_authorizer(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_deployment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_domain_name(
        self,
        DomainName: str,
        DomainNameConfigurations: List[Any] = None,
        Tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_integration(
        self,
        ApiId: str,
        IntegrationType: str,
        ConnectionId: str = None,
        ConnectionType: str = None,
        ContentHandlingStrategy: str = None,
        CredentialsArn: str = None,
        Description: str = None,
        IntegrationMethod: str = None,
        IntegrationUri: str = None,
        PassthroughBehavior: str = None,
        RequestParameters: Dict[str, Any] = None,
        RequestTemplates: Dict[str, Any] = None,
        TemplateSelectionExpression: str = None,
        TimeoutInMillis: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_integration_response(
        self,
        ApiId: str,
        IntegrationId: str,
        IntegrationResponseKey: str,
        ContentHandlingStrategy: str = None,
        ResponseParameters: Dict[str, Any] = None,
        ResponseTemplates: Dict[str, Any] = None,
        TemplateSelectionExpression: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_model(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_route(
        self,
        ApiId: str,
        RouteKey: str,
        ApiKeyRequired: bool = None,
        AuthorizationScopes: List[Any] = None,
        AuthorizationType: str = None,
        AuthorizerId: str = None,
        ModelSelectionExpression: str = None,
        OperationName: str = None,
        RequestModels: Dict[str, Any] = None,
        RequestParameters: Dict[str, Any] = None,
        RouteResponseSelectionExpression: str = None,
        Target: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_route_response(
        self,
        ApiId: str,
        RouteId: str,
        RouteResponseKey: str,
        ModelSelectionExpression: str = None,
        ResponseModels: Dict[str, Any] = None,
        ResponseParameters: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_stage(
        self,
        ApiId: str,
        StageName: str,
        AccessLogSettings: Dict[str, Any] = None,
        ClientCertificateId: str = None,
        DefaultRouteSettings: Dict[str, Any] = None,
        DeploymentId: str = None,
        Description: str = None,
        RouteSettings: Dict[str, Any] = None,
        StageVariables: Dict[str, Any] = None,
        Tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_api(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_api_mapping(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_authorizer(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_deployment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_domain_name(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_integration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_integration_response(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_model(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_route(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_route_response(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_stage(self) -> None:
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
    def get_api(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_api_mapping(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_api_mappings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_apis(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_authorizer(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_authorizers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_deployment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_deployments(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_domain_name(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_domain_names(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_integration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_integration_response(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_integration_responses(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_integrations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_model(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_model_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_models(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_route(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_route_response(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_route_responses(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_routes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_stage(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_stages(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_tags(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(
        self, ResourceArn: str, Tags: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_api(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_api_mapping(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_authorizer(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_deployment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_domain_name(
        self, DomainName: str, DomainNameConfigurations: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_integration(
        self,
        ApiId: str,
        IntegrationId: str,
        ConnectionId: str = None,
        ConnectionType: str = None,
        ContentHandlingStrategy: str = None,
        CredentialsArn: str = None,
        Description: str = None,
        IntegrationMethod: str = None,
        IntegrationType: str = None,
        IntegrationUri: str = None,
        PassthroughBehavior: str = None,
        RequestParameters: Dict[str, Any] = None,
        RequestTemplates: Dict[str, Any] = None,
        TemplateSelectionExpression: str = None,
        TimeoutInMillis: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_integration_response(
        self,
        ApiId: str,
        IntegrationId: str,
        IntegrationResponseId: str,
        ContentHandlingStrategy: str = None,
        IntegrationResponseKey: str = None,
        ResponseParameters: Dict[str, Any] = None,
        ResponseTemplates: Dict[str, Any] = None,
        TemplateSelectionExpression: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_model(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_route(
        self,
        ApiId: str,
        RouteId: str,
        ApiKeyRequired: bool = None,
        AuthorizationScopes: List[Any] = None,
        AuthorizationType: str = None,
        AuthorizerId: str = None,
        ModelSelectionExpression: str = None,
        OperationName: str = None,
        RequestModels: Dict[str, Any] = None,
        RequestParameters: Dict[str, Any] = None,
        RouteKey: str = None,
        RouteResponseSelectionExpression: str = None,
        Target: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_route_response(
        self,
        ApiId: str,
        RouteId: str,
        RouteResponseId: str,
        ModelSelectionExpression: str = None,
        ResponseModels: Dict[str, Any] = None,
        ResponseParameters: Dict[str, Any] = None,
        RouteResponseKey: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_stage(
        self,
        ApiId: str,
        StageName: str,
        AccessLogSettings: Dict[str, Any] = None,
        ClientCertificateId: str = None,
        DefaultRouteSettings: Dict[str, Any] = None,
        DeploymentId: str = None,
        Description: str = None,
        RouteSettings: Dict[str, Any] = None,
        StageVariables: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass
