from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    # pylint: disable=arguments-differ
    def add_custom_attributes(
        self, UserPoolId: str, CustomAttributes: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def admin_add_user_to_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def admin_confirm_sign_up(
        self, UserPoolId: str, Username: str, ClientMetadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def admin_create_user(
        self,
        UserPoolId: str,
        Username: str,
        UserAttributes: List[Any] = None,
        ValidationData: List[Any] = None,
        TemporaryPassword: str = None,
        ForceAliasCreation: bool = None,
        MessageAction: str = None,
        DesiredDeliveryMediums: List[Any] = None,
        ClientMetadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def admin_delete_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def admin_delete_user_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def admin_disable_provider_for_user(
        self, UserPoolId: str, User: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def admin_disable_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def admin_enable_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def admin_forget_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def admin_get_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def admin_get_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def admin_initiate_auth(
        self,
        UserPoolId: str,
        ClientId: str,
        AuthFlow: str,
        AuthParameters: Dict[str, Any] = None,
        ClientMetadata: Dict[str, Any] = None,
        AnalyticsMetadata: Dict[str, Any] = None,
        ContextData: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def admin_link_provider_for_user(
        self,
        UserPoolId: str,
        DestinationUser: Dict[str, Any],
        SourceUser: Dict[str, Any],
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def admin_list_devices(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def admin_list_groups_for_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def admin_list_user_auth_events(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def admin_remove_user_from_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def admin_reset_user_password(
        self, UserPoolId: str, Username: str, ClientMetadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def admin_respond_to_auth_challenge(
        self,
        UserPoolId: str,
        ClientId: str,
        ChallengeName: str,
        ChallengeResponses: Dict[str, Any] = None,
        Session: str = None,
        AnalyticsMetadata: Dict[str, Any] = None,
        ContextData: Dict[str, Any] = None,
        ClientMetadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def admin_set_user_mfa_preference(
        self,
        Username: str,
        UserPoolId: str,
        SMSMfaSettings: Dict[str, Any] = None,
        SoftwareTokenMfaSettings: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def admin_set_user_password(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def admin_set_user_settings(
        self, UserPoolId: str, Username: str, MFAOptions: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def admin_update_auth_event_feedback(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def admin_update_device_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def admin_update_user_attributes(
        self,
        UserPoolId: str,
        Username: str,
        UserAttributes: List[Any],
        ClientMetadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def admin_user_global_sign_out(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def associate_software_token(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def change_password(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def confirm_device(
        self,
        AccessToken: str,
        DeviceKey: str,
        DeviceSecretVerifierConfig: Dict[str, Any] = None,
        DeviceName: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def confirm_forgot_password(
        self,
        ClientId: str,
        Username: str,
        ConfirmationCode: str,
        Password: str,
        SecretHash: str = None,
        AnalyticsMetadata: Dict[str, Any] = None,
        UserContextData: Dict[str, Any] = None,
        ClientMetadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def confirm_sign_up(
        self,
        ClientId: str,
        Username: str,
        ConfirmationCode: str,
        SecretHash: str = None,
        ForceAliasCreation: bool = None,
        AnalyticsMetadata: Dict[str, Any] = None,
        UserContextData: Dict[str, Any] = None,
        ClientMetadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_identity_provider(
        self,
        UserPoolId: str,
        ProviderName: str,
        ProviderType: str,
        ProviderDetails: Dict[str, Any],
        AttributeMapping: Dict[str, Any] = None,
        IdpIdentifiers: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_resource_server(
        self, UserPoolId: str, Identifier: str, Name: str, Scopes: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_user_import_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_user_pool(
        self,
        PoolName: str,
        Policies: Dict[str, Any] = None,
        LambdaConfig: Dict[str, Any] = None,
        AutoVerifiedAttributes: List[Any] = None,
        AliasAttributes: List[Any] = None,
        UsernameAttributes: List[Any] = None,
        SmsVerificationMessage: str = None,
        EmailVerificationMessage: str = None,
        EmailVerificationSubject: str = None,
        VerificationMessageTemplate: Dict[str, Any] = None,
        SmsAuthenticationMessage: str = None,
        MfaConfiguration: str = None,
        DeviceConfiguration: Dict[str, Any] = None,
        EmailConfiguration: Dict[str, Any] = None,
        SmsConfiguration: Dict[str, Any] = None,
        UserPoolTags: Dict[str, Any] = None,
        AdminCreateUserConfig: Dict[str, Any] = None,
        Schema: List[Any] = None,
        UserPoolAddOns: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_user_pool_client(
        self,
        UserPoolId: str,
        ClientName: str,
        GenerateSecret: bool = None,
        RefreshTokenValidity: int = None,
        ReadAttributes: List[Any] = None,
        WriteAttributes: List[Any] = None,
        ExplicitAuthFlows: List[Any] = None,
        SupportedIdentityProviders: List[Any] = None,
        CallbackURLs: List[Any] = None,
        LogoutURLs: List[Any] = None,
        DefaultRedirectURI: str = None,
        AllowedOAuthFlows: List[Any] = None,
        AllowedOAuthScopes: List[Any] = None,
        AllowedOAuthFlowsUserPoolClient: bool = None,
        AnalyticsConfiguration: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_user_pool_domain(
        self, Domain: str, UserPoolId: str, CustomDomainConfig: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_identity_provider(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_resource_server(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_user_attributes(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_user_pool(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_user_pool_client(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_user_pool_domain(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_identity_provider(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_resource_server(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_risk_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_user_import_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_user_pool(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_user_pool_client(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_user_pool_domain(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def forget_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def forgot_password(
        self,
        ClientId: str,
        Username: str,
        SecretHash: str = None,
        UserContextData: Dict[str, Any] = None,
        AnalyticsMetadata: Dict[str, Any] = None,
        ClientMetadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
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
    def get_csv_header(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_identity_provider_by_identifier(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_signing_certificate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_ui_customization(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_user_attribute_verification_code(
        self,
        AccessToken: str,
        AttributeName: str,
        ClientMetadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_user_pool_mfa_config(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def global_sign_out(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def initiate_auth(
        self,
        AuthFlow: str,
        ClientId: str,
        AuthParameters: Dict[str, Any] = None,
        ClientMetadata: Dict[str, Any] = None,
        AnalyticsMetadata: Dict[str, Any] = None,
        UserContextData: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_devices(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_identity_providers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_resource_servers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_user_import_jobs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_user_pool_clients(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_user_pools(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_users(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_users_in_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def resend_confirmation_code(
        self,
        ClientId: str,
        Username: str,
        SecretHash: str = None,
        UserContextData: Dict[str, Any] = None,
        AnalyticsMetadata: Dict[str, Any] = None,
        ClientMetadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def respond_to_auth_challenge(
        self,
        ClientId: str,
        ChallengeName: str,
        Session: str = None,
        ChallengeResponses: Dict[str, Any] = None,
        AnalyticsMetadata: Dict[str, Any] = None,
        UserContextData: Dict[str, Any] = None,
        ClientMetadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def set_risk_configuration(
        self,
        UserPoolId: str,
        ClientId: str = None,
        CompromisedCredentialsRiskConfiguration: Dict[str, Any] = None,
        AccountTakeoverRiskConfiguration: Dict[str, Any] = None,
        RiskExceptionConfiguration: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def set_ui_customization(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_user_mfa_preference(
        self,
        AccessToken: str,
        SMSMfaSettings: Dict[str, Any] = None,
        SoftwareTokenMfaSettings: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def set_user_pool_mfa_config(
        self,
        UserPoolId: str,
        SmsMfaConfiguration: Dict[str, Any] = None,
        SoftwareTokenMfaConfiguration: Dict[str, Any] = None,
        MfaConfiguration: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def set_user_settings(
        self, AccessToken: str, MFAOptions: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def sign_up(
        self,
        ClientId: str,
        Username: str,
        Password: str,
        SecretHash: str = None,
        UserAttributes: List[Any] = None,
        ValidationData: List[Any] = None,
        AnalyticsMetadata: Dict[str, Any] = None,
        UserContextData: Dict[str, Any] = None,
        ClientMetadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def start_user_import_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def stop_user_import_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, ResourceArn: str, Tags: Dict[str, Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_auth_event_feedback(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_device_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_identity_provider(
        self,
        UserPoolId: str,
        ProviderName: str,
        ProviderDetails: Dict[str, Any] = None,
        AttributeMapping: Dict[str, Any] = None,
        IdpIdentifiers: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_resource_server(
        self, UserPoolId: str, Identifier: str, Name: str, Scopes: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_user_attributes(
        self,
        UserAttributes: List[Any],
        AccessToken: str,
        ClientMetadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_user_pool(
        self,
        UserPoolId: str,
        Policies: Dict[str, Any] = None,
        LambdaConfig: Dict[str, Any] = None,
        AutoVerifiedAttributes: List[Any] = None,
        SmsVerificationMessage: str = None,
        EmailVerificationMessage: str = None,
        EmailVerificationSubject: str = None,
        VerificationMessageTemplate: Dict[str, Any] = None,
        SmsAuthenticationMessage: str = None,
        MfaConfiguration: str = None,
        DeviceConfiguration: Dict[str, Any] = None,
        EmailConfiguration: Dict[str, Any] = None,
        SmsConfiguration: Dict[str, Any] = None,
        UserPoolTags: Dict[str, Any] = None,
        AdminCreateUserConfig: Dict[str, Any] = None,
        UserPoolAddOns: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_user_pool_client(
        self,
        UserPoolId: str,
        ClientId: str,
        ClientName: str = None,
        RefreshTokenValidity: int = None,
        ReadAttributes: List[Any] = None,
        WriteAttributes: List[Any] = None,
        ExplicitAuthFlows: List[Any] = None,
        SupportedIdentityProviders: List[Any] = None,
        CallbackURLs: List[Any] = None,
        LogoutURLs: List[Any] = None,
        DefaultRedirectURI: str = None,
        AllowedOAuthFlows: List[Any] = None,
        AllowedOAuthScopes: List[Any] = None,
        AllowedOAuthFlowsUserPoolClient: bool = None,
        AnalyticsConfiguration: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_user_pool_domain(
        self, Domain: str, UserPoolId: str, CustomDomainConfig: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def verify_software_token(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def verify_user_attribute(self) -> None:
        pass
