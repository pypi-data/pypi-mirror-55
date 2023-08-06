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
    def create_identity_pool(
        self,
        IdentityPoolName: str,
        AllowUnauthenticatedIdentities: bool,
        AllowClassicFlow: bool = None,
        SupportedLoginProviders: Dict[str, Any] = None,
        DeveloperProviderName: str = None,
        OpenIdConnectProviderARNs: List[Any] = None,
        CognitoIdentityProviders: List[Any] = None,
        SamlProviderARNs: List[Any] = None,
        IdentityPoolTags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_identities(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_identity_pool(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_identity(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_identity_pool(self) -> None:
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
    def get_credentials_for_identity(
        self, IdentityId: str, Logins: Dict[str, Any] = None, CustomRoleArn: str = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_id(
        self, IdentityPoolId: str, AccountId: str = None, Logins: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_identity_pool_roles(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_open_id_token(
        self, IdentityId: str, Logins: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_open_id_token_for_developer_identity(
        self,
        IdentityPoolId: str,
        Logins: Dict[str, Any],
        IdentityId: str = None,
        TokenDuration: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_identities(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_identity_pools(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def lookup_developer_identity(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def merge_developer_identities(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_identity_pool_roles(
        self,
        IdentityPoolId: str,
        Roles: Dict[str, Any],
        RoleMappings: Dict[str, Any] = None,
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, ResourceArn: str, Tags: Dict[str, Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def unlink_developer_identity(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def unlink_identity(
        self, IdentityId: str, Logins: Dict[str, Any], LoginsToRemove: List[Any]
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_identity_pool(
        self,
        IdentityPoolId: str,
        IdentityPoolName: str,
        AllowUnauthenticatedIdentities: bool,
        AllowClassicFlow: bool = None,
        SupportedLoginProviders: Dict[str, Any] = None,
        DeveloperProviderName: str = None,
        OpenIdConnectProviderARNs: List[Any] = None,
        CognitoIdentityProviders: List[Any] = None,
        SamlProviderARNs: List[Any] = None,
        IdentityPoolTags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass
