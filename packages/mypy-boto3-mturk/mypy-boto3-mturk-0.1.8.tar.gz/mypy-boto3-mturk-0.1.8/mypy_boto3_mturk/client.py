from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    # pylint: disable=arguments-differ
    def accept_qualification_request(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def approve_assignment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def associate_qualification_with_worker(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_additional_assignments_for_hit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_hit(
        self,
        LifetimeInSeconds: int,
        AssignmentDurationInSeconds: int,
        Reward: str,
        Title: str,
        Description: str,
        MaxAssignments: int = None,
        AutoApprovalDelayInSeconds: int = None,
        Keywords: str = None,
        Question: str = None,
        RequesterAnnotation: str = None,
        QualificationRequirements: List[Any] = None,
        UniqueRequestToken: str = None,
        AssignmentReviewPolicy: Dict[str, Any] = None,
        HITReviewPolicy: Dict[str, Any] = None,
        HITLayoutId: str = None,
        HITLayoutParameters: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_hit_type(
        self,
        AssignmentDurationInSeconds: int,
        Reward: str,
        Title: str,
        Description: str,
        AutoApprovalDelayInSeconds: int = None,
        Keywords: str = None,
        QualificationRequirements: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_hit_with_hit_type(
        self,
        HITTypeId: str,
        LifetimeInSeconds: int,
        MaxAssignments: int = None,
        Question: str = None,
        RequesterAnnotation: str = None,
        UniqueRequestToken: str = None,
        AssignmentReviewPolicy: Dict[str, Any] = None,
        HITReviewPolicy: Dict[str, Any] = None,
        HITLayoutId: str = None,
        HITLayoutParameters: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_qualification_type(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_worker_block(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_hit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_qualification_type(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_worker_block(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_qualification_from_worker(self) -> None:
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
    def get_account_balance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_assignment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_file_upload_url(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_hit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_qualification_score(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_qualification_type(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_assignments_for_hit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_bonus_payments(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_hits(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_hits_for_qualification_type(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_qualification_requests(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_qualification_types(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_review_policy_results_for_hit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_reviewable_hits(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_worker_blocks(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_workers_with_qualification_type(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def notify_workers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reject_assignment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reject_qualification_request(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def send_bonus(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def send_test_event_notification(
        self, Notification: Dict[str, Any], TestEventType: str
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_expiration_for_hit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_hit_review_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_hit_type_of_hit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_notification_settings(
        self, HITTypeId: str, Notification: Dict[str, Any] = None, Active: bool = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_qualification_type(self) -> None:
        pass
