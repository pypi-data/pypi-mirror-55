from __future__ import annotations

from typing import Any
from typing import Dict

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    # pylint: disable=arguments-differ
    def abort_multipart_upload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def abort_vault_lock(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def add_tags_to_vault(
        self, vaultName: str, accountId: str = None, Tags: Dict[str, Any] = None
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def complete_multipart_upload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def complete_vault_lock(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_vault(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_archive(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_vault(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_vault_access_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_vault_notifications(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_vault(self) -> None:
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
    def get_data_retrieval_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_job_output(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_vault_access_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_vault_lock(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_vault_notifications(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def initiate_job(
        self,
        vaultName: str,
        accountId: str = None,
        jobParameters: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def initiate_multipart_upload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def initiate_vault_lock(
        self, vaultName: str, accountId: str = None, policy: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_jobs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_multipart_uploads(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_parts(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_provisioned_capacity(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_vault(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_vaults(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def purchase_provisioned_capacity(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_tags_from_vault(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_data_retrieval_policy(
        self, accountId: str = None, Policy: Dict[str, Any] = None
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_vault_access_policy(
        self, vaultName: str, accountId: str = None, policy: Dict[str, Any] = None
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def set_vault_notifications(
        self,
        vaultName: str,
        accountId: str = None,
        vaultNotificationConfig: Dict[str, Any] = None,
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def upload_archive(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def upload_multipart_part(self) -> None:
        pass
