from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    # pylint: disable=arguments-differ
    def add_client_id_to_open_id_connect_provider(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def add_role_to_instance_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def add_user_to_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def attach_group_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def attach_role_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def attach_user_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def change_password(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_access_key(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_account_alias(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_instance_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_login_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_open_id_connect_provider(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_policy_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_role(
        self,
        RoleName: str,
        AssumeRolePolicyDocument: str,
        Path: str = None,
        Description: str = None,
        MaxSessionDuration: int = None,
        PermissionsBoundary: str = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_saml_provider(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_service_linked_role(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_service_specific_credential(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_user(
        self,
        UserName: str,
        Path: str = None,
        PermissionsBoundary: str = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_virtual_mfa_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deactivate_mfa_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_access_key(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_account_alias(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_account_password_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_group_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_instance_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_login_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_open_id_connect_provider(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_policy_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_role(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_role_permissions_boundary(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_role_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_saml_provider(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_server_certificate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_service_linked_role(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_service_specific_credential(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_signing_certificate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_ssh_public_key(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_user_permissions_boundary(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_user_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_virtual_mfa_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def detach_group_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def detach_role_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def detach_user_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def enable_mfa_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def generate_credential_report(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def generate_organizations_access_report(self) -> None:
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
    def generate_service_last_accessed_details(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_access_key_last_used(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_account_authorization_details(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_account_password_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_account_summary(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_context_keys_for_custom_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_context_keys_for_principal_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_credential_report(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_group_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_instance_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_login_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_open_id_connect_provider(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_organizations_access_report(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_policy_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_role(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_role_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_saml_provider(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_server_certificate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_service_last_accessed_details(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_service_last_accessed_details_with_entities(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_service_linked_role_deletion_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_ssh_public_key(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_user_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_access_keys(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_account_aliases(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_attached_group_policies(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_attached_role_policies(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_attached_user_policies(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_entities_for_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_group_policies(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_groups_for_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_instance_profiles(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_instance_profiles_for_role(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_mfa_devices(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_open_id_connect_providers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_policies(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_policies_granting_service_access(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_policy_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_role_policies(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_role_tags(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_roles(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_saml_providers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_server_certificates(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_service_specific_credentials(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_signing_certificates(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_ssh_public_keys(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_user_policies(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_user_tags(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_users(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_virtual_mfa_devices(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_group_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_role_permissions_boundary(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_role_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_user_permissions_boundary(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_user_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_client_id_from_open_id_connect_provider(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_role_from_instance_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_user_from_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reset_service_specific_credential(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def resync_mfa_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_default_policy_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_security_token_service_preferences(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def simulate_custom_policy(
        self,
        PolicyInputList: List[Any],
        ActionNames: List[Any],
        ResourceArns: List[Any] = None,
        ResourcePolicy: str = None,
        ResourceOwner: str = None,
        CallerArn: str = None,
        ContextEntries: List[Any] = None,
        ResourceHandlingOption: str = None,
        MaxItems: int = None,
        Marker: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def simulate_principal_policy(
        self,
        PolicySourceArn: str,
        ActionNames: List[Any],
        PolicyInputList: List[Any] = None,
        ResourceArns: List[Any] = None,
        ResourcePolicy: str = None,
        ResourceOwner: str = None,
        CallerArn: str = None,
        ContextEntries: List[Any] = None,
        ResourceHandlingOption: str = None,
        MaxItems: int = None,
        Marker: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def tag_role(self, RoleName: str, Tags: List[Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_user(self, UserName: str, Tags: List[Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def untag_role(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def untag_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_access_key(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_account_password_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_assume_role_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_login_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_open_id_connect_provider_thumbprint(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_role(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_role_description(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_saml_provider(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_server_certificate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_service_specific_credential(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_signing_certificate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_ssh_public_key(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def upload_server_certificate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def upload_signing_certificate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def upload_ssh_public_key(self) -> None:
        pass
