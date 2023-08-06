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
    def cancel_rotate_secret(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_secret(
        self,
        Name: str,
        ClientRequestToken: str = None,
        Description: str = None,
        KmsKeyId: str = None,
        SecretBinary: bytes = None,
        SecretString: str = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_resource_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_secret(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_secret(self) -> None:
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
    def get_random_password(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_resource_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_secret_value(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_secret_version_ids(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_secrets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_resource_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_secret_value(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def restore_secret(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def rotate_secret(
        self,
        SecretId: str,
        ClientRequestToken: str = None,
        RotationLambdaARN: str = None,
        RotationRules: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, SecretId: str, Tags: List[Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_secret(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_secret_version_stage(self) -> None:
        pass
