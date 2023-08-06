from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    # pylint: disable=arguments-differ
    def accept_invitation(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def archive_findings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_detector(
        self,
        Enable: bool,
        ClientToken: str = None,
        FindingPublishingFrequency: str = None,
        Tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_filter(
        self,
        DetectorId: str,
        Name: str,
        FindingCriteria: Dict[str, Any],
        Description: str = None,
        Action: str = None,
        Rank: int = None,
        ClientToken: str = None,
        Tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_ip_set(
        self,
        DetectorId: str,
        Name: str,
        Format: str,
        Location: str,
        Activate: bool,
        ClientToken: str = None,
        Tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_members(
        self, DetectorId: str, AccountDetails: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_sample_findings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_threat_intel_set(
        self,
        DetectorId: str,
        Name: str,
        Format: str,
        Location: str,
        Activate: bool,
        ClientToken: str = None,
        Tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def decline_invitations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_detector(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_filter(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_invitations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_ip_set(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_members(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_threat_intel_set(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_from_master_account(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_members(self) -> None:
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
    def get_detector(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_filter(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_findings(
        self,
        DetectorId: str,
        FindingIds: List[Any],
        SortCriteria: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_findings_statistics(
        self,
        DetectorId: str,
        FindingStatisticTypes: List[Any],
        FindingCriteria: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_invitations_count(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_ip_set(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_master_account(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_members(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_threat_intel_set(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def invite_members(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_detectors(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_filters(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_findings(
        self,
        DetectorId: str,
        FindingCriteria: Dict[str, Any] = None,
        SortCriteria: Dict[str, Any] = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_invitations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_ip_sets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_members(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_threat_intel_sets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_monitoring_members(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def stop_monitoring_members(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, ResourceArn: str, Tags: Dict[str, Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def unarchive_findings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_detector(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_filter(
        self,
        DetectorId: str,
        FilterName: str,
        Description: str = None,
        Action: str = None,
        Rank: int = None,
        FindingCriteria: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_findings_feedback(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_ip_set(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_threat_intel_set(self) -> None:
        pass
