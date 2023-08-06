from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def bulk_publish(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_dataset(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_dataset(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_identity_pool_usage(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_identity_usage(self) -> None:
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
    def get_bulk_publish_details(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_cognito_events(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_identity_pool_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_datasets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_identity_pool_usage(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_records(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def register_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_cognito_events(self, IdentityPoolId: str, Events: Dict[str, Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_identity_pool_configuration(
        self,
        IdentityPoolId: str,
        PushSync: Dict[str, Any] = None,
        CognitoStreams: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def subscribe_to_dataset(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def unsubscribe_from_dataset(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_records(
        self,
        IdentityPoolId: str,
        IdentityId: str,
        DatasetName: str,
        SyncSessionToken: str,
        DeviceId: str = None,
        RecordPatches: List[Any] = None,
        ClientContext: str = None,
    ) -> Dict[str, Any]:
        pass
