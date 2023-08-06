from __future__ import annotations

from typing import Any
from typing import Dict

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_backup_plan(
        self,
        BackupPlan: Dict[str, Any],
        BackupPlanTags: Dict[str, Any] = None,
        CreatorRequestId: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_backup_selection(
        self,
        BackupPlanId: str,
        BackupSelection: Dict[str, Any],
        CreatorRequestId: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_backup_vault(
        self,
        BackupVaultName: str,
        BackupVaultTags: Dict[str, Any] = None,
        EncryptionKeyArn: str = None,
        CreatorRequestId: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_backup_plan(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_backup_selection(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_backup_vault(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_backup_vault_access_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_backup_vault_notifications(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_recovery_point(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_backup_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_backup_vault(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_protected_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_recovery_point(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_restore_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def export_backup_plan_template(self) -> None:
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
    def get_backup_plan(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_backup_plan_from_json(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_backup_plan_from_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_backup_selection(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_backup_vault_access_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_backup_vault_notifications(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_recovery_point_restore_metadata(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_supported_resource_types(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_backup_jobs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_backup_plan_templates(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_backup_plan_versions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_backup_plans(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_backup_selections(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_backup_vaults(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_protected_resources(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_recovery_points_by_backup_vault(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_recovery_points_by_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_restore_jobs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_backup_vault_access_policy(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_backup_vault_notifications(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_backup_job(
        self,
        BackupVaultName: str,
        ResourceArn: str,
        IamRoleArn: str,
        IdempotencyToken: str = None,
        StartWindowMinutes: int = None,
        CompleteWindowMinutes: int = None,
        Lifecycle: Dict[str, Any] = None,
        RecoveryPointTags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def start_restore_job(
        self,
        RecoveryPointArn: str,
        Metadata: Dict[str, Any],
        IamRoleArn: str,
        IdempotencyToken: str = None,
        ResourceType: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def stop_backup_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, ResourceArn: str, Tags: Dict[str, Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_backup_plan(
        self, BackupPlanId: str, BackupPlan: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_recovery_point_lifecycle(
        self,
        BackupVaultName: str,
        RecoveryPointArn: str,
        Lifecycle: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass
