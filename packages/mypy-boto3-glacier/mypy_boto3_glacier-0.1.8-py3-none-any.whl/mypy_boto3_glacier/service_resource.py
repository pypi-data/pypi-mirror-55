from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from boto3.resources.base import ServiceResource as Boto3ServiceResource
from boto3.resources.collection import ResourceCollection

# pylint: disable=import-self
import mypy_boto3_glacier.service_resource as mypy_boto3_glacier_scope


class ServiceResource(Boto3ServiceResource):
    vaults: mypy_boto3_glacier_scope.vaults
    # pylint: disable=arguments-differ
    def Account(self, id: str = None) -> mypy_boto3_glacier_scope.Account:
        pass

    # pylint: disable=arguments-differ
    def Archive(
        self, account_id: str = None, vault_name: str = None, id: str = None
    ) -> mypy_boto3_glacier_scope.Archive:
        pass

    # pylint: disable=arguments-differ
    def Job(
        self, account_id: str = None, vault_name: str = None, id: str = None
    ) -> mypy_boto3_glacier_scope.Job:
        pass

    # pylint: disable=arguments-differ
    def MultipartUpload(
        self, account_id: str = None, vault_name: str = None, id: str = None
    ) -> mypy_boto3_glacier_scope.MultipartUpload:
        pass

    # pylint: disable=arguments-differ
    def Notification(
        self, account_id: str = None, vault_name: str = None
    ) -> mypy_boto3_glacier_scope.Notification:
        pass

    # pylint: disable=arguments-differ
    def Vault(
        self, account_id: str = None, name: str = None
    ) -> mypy_boto3_glacier_scope.Vault:
        pass

    # pylint: disable=arguments-differ
    def create_vault(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass


class Account(Boto3ServiceResource):
    id: str
    vaults: mypy_boto3_glacier_scope.vaults
    # pylint: disable=arguments-differ
    def create_vault(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass


class Archive(Boto3ServiceResource):
    account_id: str
    vault_name: str
    id: str
    # pylint: disable=arguments-differ
    def delete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def initiate_archive_retrieval(self) -> None:
        pass


class Job(Boto3ServiceResource):
    job_id: str
    job_description: str
    action: str
    archive_id: str
    vault_arn: str
    creation_date: str
    completed: bool
    status_code: str
    status_message: str
    archive_size_in_bytes: int
    inventory_size_in_bytes: int
    sns_topic: str
    completion_date: str
    sha256_tree_hash: str
    archive_sha256_tree_hash: str
    retrieval_byte_range: str
    tier: str
    inventory_retrieval_parameters: Dict[str, Any]
    job_output_path: str
    select_parameters: Dict[str, Any]
    output_location: Dict[str, Any]
    account_id: str
    vault_name: str
    id: str
    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def get_output(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass


class MultipartUpload(Boto3ServiceResource):
    multipart_upload_id: str
    vault_arn: str
    archive_description: str
    part_size_in_bytes: int
    creation_date: str
    account_id: str
    vault_name: str
    id: str
    # pylint: disable=arguments-differ
    def abort(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def complete(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_available_subresources(self) -> List[str]:
        pass

    # pylint: disable=arguments-differ
    def parts(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def upload_part(self) -> None:
        pass


class Notification(Boto3ServiceResource):
    sns_topic: str
    events: List[Any]
    account_id: str
    vault_name: str
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
    def set(self, vaultNotificationConfig: Dict[str, Any] = None) -> None:
        pass


class Vault(Boto3ServiceResource):
    vault_arn: str
    vault_name: str
    creation_date: str
    last_inventory_date: str
    number_of_archives: int
    size_in_bytes: int
    account_id: str
    name: str
    completed_jobs: mypy_boto3_glacier_scope.completed_jobs
    failed_jobs: mypy_boto3_glacier_scope.failed_jobs
    jobs: mypy_boto3_glacier_scope.jobs
    jobs_in_progress: mypy_boto3_glacier_scope.jobs_in_progress
    multipart_uplaods: mypy_boto3_glacier_scope.multipart_uplaods
    multipart_uploads: mypy_boto3_glacier_scope.multipart_uploads
    succeeded_jobs: mypy_boto3_glacier_scope.succeeded_jobs
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
    def initiate_inventory_retrieval(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def initiate_multipart_upload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def load(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def upload_archive(self) -> None:
        pass


class vaults(ResourceCollection):
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


class completed_jobs(ResourceCollection):
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


class failed_jobs(ResourceCollection):
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


class jobs(ResourceCollection):
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


class jobs_in_progress(ResourceCollection):
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


class multipart_uplaods(ResourceCollection):
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


class multipart_uploads(ResourceCollection):
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


class succeeded_jobs(ResourceCollection):
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
