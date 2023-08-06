from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    # pylint: disable=arguments-differ
    def associate_phone_number_with_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def associate_phone_numbers_with_voice_connector(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def associate_phone_numbers_with_voice_connector_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_delete_phone_number(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_suspend_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_unsuspend_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_update_phone_number(
        self, UpdatePhoneNumberRequestItems: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def batch_update_user(
        self, AccountId: str, UpdateUserRequestItems: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_account(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_bot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_phone_number_order(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_voice_connector(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_voice_connector_group(
        self, Name: str, VoiceConnectorItems: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_account(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_events_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_phone_number(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_voice_connector(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_voice_connector_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_voice_connector_origination(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_voice_connector_streaming_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_voice_connector_termination(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_voice_connector_termination_credentials(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_phone_number_from_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_phone_numbers_from_voice_connector(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_phone_numbers_from_voice_connector_group(self) -> None:
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
    def get_account(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_account_settings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_bot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_events_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_global_settings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_phone_number(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_phone_number_order(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_phone_number_settings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_user_settings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_voice_connector(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_voice_connector_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_voice_connector_logging_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_voice_connector_origination(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_voice_connector_streaming_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_voice_connector_termination(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_voice_connector_termination_health(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def invite_users(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_accounts(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_bots(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_phone_number_orders(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_phone_numbers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_users(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_voice_connector_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_voice_connector_termination_credentials(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_voice_connectors(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def logout_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_events_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_voice_connector_logging_configuration(
        self, VoiceConnectorId: str, LoggingConfiguration: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_voice_connector_origination(
        self, VoiceConnectorId: str, Origination: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_voice_connector_streaming_configuration(
        self, VoiceConnectorId: str, StreamingConfiguration: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_voice_connector_termination(
        self, VoiceConnectorId: str, Termination: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_voice_connector_termination_credentials(
        self, VoiceConnectorId: str, Credentials: List[Any] = None
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def regenerate_security_token(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reset_personal_pin(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def restore_phone_number(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def search_available_phone_numbers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_account(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_account_settings(
        self, AccountId: str, AccountSettings: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_bot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_global_settings(
        self, BusinessCalling: Dict[str, Any], VoiceConnector: Dict[str, Any]
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_phone_number(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_phone_number_settings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_user_settings(
        self, AccountId: str, UserId: str, UserSettings: Dict[str, Any]
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_voice_connector(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_voice_connector_group(
        self, VoiceConnectorGroupId: str, Name: str, VoiceConnectorItems: List[Any]
    ) -> Dict[str, Any]:
        pass
