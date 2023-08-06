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
    def create_bot_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_intent_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_slot_type_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_bot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_bot_alias(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_bot_channel_association(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_bot_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_intent(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_intent_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_slot_type(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_slot_type_version(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_utterances(self) -> None:
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
    def get_bot(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_bot_alias(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_bot_aliases(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_bot_channel_association(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_bot_channel_associations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_bot_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_bots(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_builtin_intent(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_builtin_intents(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_builtin_slot_types(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_export(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_import(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_intent(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_intent_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_intents(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_slot_type(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_slot_type_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_slot_types(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_utterances_view(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def put_bot(
        self,
        name: str,
        locale: str,
        childDirected: bool,
        description: str = None,
        intents: List[Any] = None,
        clarificationPrompt: Dict[str, Any] = None,
        abortStatement: Dict[str, Any] = None,
        idleSessionTTLInSeconds: int = None,
        voiceId: str = None,
        checksum: str = None,
        processBehavior: str = None,
        createVersion: bool = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_bot_alias(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_intent(
        self,
        name: str,
        description: str = None,
        slots: List[Any] = None,
        sampleUtterances: List[Any] = None,
        confirmationPrompt: Dict[str, Any] = None,
        rejectionStatement: Dict[str, Any] = None,
        followUpPrompt: Dict[str, Any] = None,
        conclusionStatement: Dict[str, Any] = None,
        dialogCodeHook: Dict[str, Any] = None,
        fulfillmentActivity: Dict[str, Any] = None,
        parentIntentSignature: str = None,
        checksum: str = None,
        createVersion: bool = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_slot_type(
        self,
        name: str,
        description: str = None,
        enumerationValues: List[Any] = None,
        checksum: str = None,
        valueSelectionStrategy: str = None,
        createVersion: bool = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def start_import(self) -> None:
        pass
