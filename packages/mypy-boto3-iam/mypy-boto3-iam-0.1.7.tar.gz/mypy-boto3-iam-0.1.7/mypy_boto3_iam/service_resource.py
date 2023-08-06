from __future__ import annotations

from datetime import datetime
from typing import Any
from typing import Dict
from typing import List

from boto3.resources.base import ServiceResource as Boto3ServiceResource
from boto3.resources.collection import ResourceCollection

# pylint: disable=import-self
import mypy_boto3_iam.service_resource as mypy_boto3_iam_scope


class ServiceResource(Boto3ServiceResource):
    groups: mypy_boto3_iam_scope.groups
    instance_profiles: mypy_boto3_iam_scope.instance_profiles
    policies: mypy_boto3_iam_scope.policies
    roles: mypy_boto3_iam_scope.roles
    saml_providers: mypy_boto3_iam_scope.saml_providers
    server_certificates: mypy_boto3_iam_scope.server_certificates
    users: mypy_boto3_iam_scope.users
    virtual_mfa_devices: mypy_boto3_iam_scope.virtual_mfa_devices

    # pylint: disable=arguments-differ
    def AccessKey(
        self, user_name: str = None, id: str = None
    ) -> mypy_boto3_iam_scope.AccessKey:
        pass

    # pylint: disable=arguments-differ
    def AccessKeyPair(
        self, user_name: str = None, id: str = None, secret: str = None
    ) -> mypy_boto3_iam_scope.AccessKeyPair:
        pass

    # pylint: disable=arguments-differ
    def AccountPasswordPolicy(self) -> mypy_boto3_iam_scope.AccountPasswordPolicy:
        pass

    # pylint: disable=arguments-differ
    def AccountSummary(self) -> mypy_boto3_iam_scope.AccountSummary:
        pass

    # pylint: disable=arguments-differ
    def AssumeRolePolicy(
        self, role_name: str = None
    ) -> mypy_boto3_iam_scope.AssumeRolePolicy:
        pass

    # pylint: disable=arguments-differ
    def CurrentUser(self) -> mypy_boto3_iam_scope.CurrentUser:
        pass

    # pylint: disable=arguments-differ
    def Group(self, name: str = None) -> mypy_boto3_iam_scope.Group:
        pass

    # pylint: disable=arguments-differ
    def GroupPolicy(
        self, group_name: str = None, name: str = None
    ) -> mypy_boto3_iam_scope.GroupPolicy:
        pass

    # pylint: disable=arguments-differ
    def InstanceProfile(self, name: str = None) -> mypy_boto3_iam_scope.InstanceProfile:
        pass

    # pylint: disable=arguments-differ
    def LoginProfile(self, user_name: str = None) -> mypy_boto3_iam_scope.LoginProfile:
        pass

    # pylint: disable=arguments-differ
    def MfaDevice(
        self, user_name: str = None, serial_number: str = None
    ) -> mypy_boto3_iam_scope.MfaDevice:
        pass

    # pylint: disable=arguments-differ
    def Policy(self, policy_arn: str = None) -> mypy_boto3_iam_scope.Policy:
        pass

    # pylint: disable=arguments-differ
    def PolicyVersion(
        self, arn: str = None, version_id: str = None
    ) -> mypy_boto3_iam_scope.PolicyVersion:
        pass

    # pylint: disable=arguments-differ
    def Role(self, name: str = None) -> mypy_boto3_iam_scope.Role:
        pass

    # pylint: disable=arguments-differ
    def RolePolicy(
        self, role_name: str = None, name: str = None
    ) -> mypy_boto3_iam_scope.RolePolicy:
        pass

    # pylint: disable=arguments-differ
    def SamlProvider(self, arn: str = None) -> mypy_boto3_iam_scope.SamlProvider:
        pass

    # pylint: disable=arguments-differ
    def ServerCertificate(
        self, name: str = None
    ) -> mypy_boto3_iam_scope.ServerCertificate:
        pass

    # pylint: disable=arguments-differ
    def SigningCertificate(
        self, user_name: str = None, id: str = None
    ) -> mypy_boto3_iam_scope.SigningCertificate:
        pass

    # pylint: disable=arguments-differ
    def User(self, name: str = None) -> mypy_boto3_iam_scope.User:
        pass

    # pylint: disable=arguments-differ
    def UserPolicy(
        self, user_name: str = None, name: str = None
    ) -> mypy_boto3_iam_scope.UserPolicy:
        pass

    # pylint: disable=arguments-differ
    def VirtualMfaDevice(
        self, serial_number: str = None
    ) -> mypy_boto3_iam_scope.VirtualMfaDevice:
        pass

    # pylint: disable=arguments-differ
    def change_password(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_account_alias(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_account_password_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_instance_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_policy(self) -> None:
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
    ) -> mypy_boto3_iam_scope.Role:
        pass

    # pylint: disable=arguments-differ
    def create_saml_provider(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_server_certificate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_signing_certificate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_user(
        self,
        UserName: str,
        Path: str = None,
        PermissionsBoundary: str = None,
        Tags: List[Any] = None,
    ) -> mypy_boto3_iam_scope.User:
        pass

    # pylint: disable=arguments-differ
    def create_virtual_mfa_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass


class AccessKey(Boto3ServiceResource):
    access_key_id: str
    status: str
    create_date: datetime
    user_name: str
    id: str

    # pylint: disable=arguments-differ
    def activate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deactivate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass


class AccessKeyPair(Boto3ServiceResource):
    access_key_id: str
    status: str
    secret_access_key: str
    create_date: datetime
    user_name: str
    id: str
    secret: str

    # pylint: disable=arguments-differ
    def activate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deactivate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass


class AccountPasswordPolicy(Boto3ServiceResource):
    minimum_password_length: int
    require_symbols: bool
    require_numbers: bool
    require_uppercase_characters: bool
    require_lowercase_characters: bool
    allow_users_to_change_password: bool
    expire_passwords: bool
    max_password_age: int
    password_reuse_prevention: int
    hard_expiry: bool

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update(self) -> None:
        pass


class AccountSummary(Boto3ServiceResource):
    summary_map: Dict[str, Any]

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass


class AssumeRolePolicy(Boto3ServiceResource):
    role_name: str

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def update(self) -> None:
        pass


class CurrentUser(Boto3ServiceResource):
    path: str
    user_name: str
    user_id: str
    arn: str
    create_date: datetime
    password_last_used: datetime
    permissions_boundary: Dict[str, Any]
    tags: List[Any]
    access_keys: mypy_boto3_iam_scope.access_keys
    mfa_devices: mypy_boto3_iam_scope.mfa_devices
    signing_certificates: mypy_boto3_iam_scope.signing_certificates

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass


class Group(Boto3ServiceResource):
    path: str
    group_name: str
    group_id: str
    arn: str
    create_date: datetime
    name: str
    attached_policies: mypy_boto3_iam_scope.attached_policies
    policies: mypy_boto3_iam_scope.policies
    users: mypy_boto3_iam_scope.users

    # pylint: disable=arguments-differ
    def add_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def attach_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def detach_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update(self) -> None:
        pass


class GroupPolicy(Boto3ServiceResource):
    policy_name: str
    policy_document: str
    group_name: str
    name: str

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass


class InstanceProfile(Boto3ServiceResource):
    path: str
    instance_profile_name: str
    instance_profile_id: str
    arn: str
    create_date: datetime
    roles_attribute: List[Any]
    name: str

    # pylint: disable=arguments-differ
    def add_role(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_role(self) -> None:
        pass


class LoginProfile(Boto3ServiceResource):
    create_date: datetime
    password_reset_required: bool
    user_name: str

    # pylint: disable=arguments-differ
    def create(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update(self) -> None:
        pass


class MfaDevice(Boto3ServiceResource):
    enable_date: datetime
    user_name: str
    serial_number: str

    # pylint: disable=arguments-differ
    def associate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def resync(self) -> None:
        pass


class Policy(Boto3ServiceResource):
    policy_name: str
    policy_id: str
    path: str
    default_version_id: str
    attachment_count: int
    permissions_boundary_usage_count: int
    is_attachable: bool
    description: str
    create_date: datetime
    update_date: datetime
    arn: str
    attached_groups: mypy_boto3_iam_scope.attached_groups
    attached_roles: mypy_boto3_iam_scope.attached_roles
    attached_users: mypy_boto3_iam_scope.attached_users
    versions: mypy_boto3_iam_scope.versions

    # pylint: disable=arguments-differ
    def attach_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def attach_role(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def attach_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def detach_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def detach_role(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def detach_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass


class PolicyVersion(Boto3ServiceResource):
    document: str
    is_default_version: bool
    create_date: datetime
    arn: str
    version_id: str

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_as_default(self) -> None:
        pass


class Role(Boto3ServiceResource):
    path: str
    role_name: str
    role_id: str
    arn: str
    create_date: datetime
    assume_role_policy_document: str
    description: str
    max_session_duration: int
    permissions_boundary: Dict[str, Any]
    tags: List[Any]
    name: str
    attached_policies: mypy_boto3_iam_scope.attached_policies
    instance_profiles: mypy_boto3_iam_scope.instance_profiles
    policies: mypy_boto3_iam_scope.policies

    # pylint: disable=arguments-differ
    def attach_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def detach_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass


class RolePolicy(Boto3ServiceResource):
    policy_name: str
    policy_document: str
    role_name: str
    name: str

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass


class SamlProvider(Boto3ServiceResource):
    saml_metadata_document: str
    create_date: datetime
    valid_until: datetime
    arn: str

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update(self) -> None:
        pass


class ServerCertificate(Boto3ServiceResource):
    server_certificate_metadata: Dict[str, Any]
    certificate_body: str
    certificate_chain: str
    name: str

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update(self) -> None:
        pass


class SigningCertificate(Boto3ServiceResource):
    certificate_id: str
    certificate_body: str
    status: str
    upload_date: datetime
    user_name: str
    id: str

    # pylint: disable=arguments-differ
    def activate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deactivate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass


class User(Boto3ServiceResource):
    path: str
    user_name: str
    user_id: str
    arn: str
    create_date: datetime
    password_last_used: datetime
    permissions_boundary: Dict[str, Any]
    tags: List[Any]
    name: str
    access_keys: mypy_boto3_iam_scope.access_keys
    attached_policies: mypy_boto3_iam_scope.attached_policies
    groups: mypy_boto3_iam_scope.groups
    mfa_devices: mypy_boto3_iam_scope.mfa_devices
    policies: mypy_boto3_iam_scope.policies
    signing_certificates: mypy_boto3_iam_scope.signing_certificates

    # pylint: disable=arguments-differ
    def add_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def attach_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create(
        self, Path: str = None, PermissionsBoundary: str = None, Tags: List[Any] = None
    ) -> mypy_boto3_iam_scope.User:
        pass

    # pylint: disable=arguments-differ
    def create_access_key_pair(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_login_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def detach_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def enable_mfa(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update(self) -> None:
        pass


class UserPolicy(Boto3ServiceResource):
    policy_name: str
    policy_document: str
    user_name: str
    name: str

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass


class VirtualMfaDevice(Boto3ServiceResource):
    base32_string_seed: bytes
    qr_code_png: bytes
    user_attribute: Dict[str, Any]
    enable_date: datetime
    serial_number: str

    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass


class groups(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class instance_profiles(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class policies(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class roles(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class saml_providers(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class server_certificates(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class users(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class virtual_mfa_devices(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class access_keys(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class mfa_devices(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class signing_certificates(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class attached_policies(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class attached_groups(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class attached_roles(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class attached_users(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass


class versions(ResourceCollection):
    @classmethod
    # pylint: disable=arguments-differ
    def all(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def filter(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def iterator(cls) -> ResourceCollection:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def limit(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def page_size(cls) -> None:
        pass

    @classmethod
    # pylint: disable=arguments-differ
    def pages(cls) -> List[Boto3ServiceResource]:
        pass
