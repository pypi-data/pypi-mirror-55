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
    def create_certificate_authority(
        self,
        CertificateAuthorityConfiguration: Dict[str, Any],
        CertificateAuthorityType: str,
        RevocationConfiguration: Dict[str, Any] = None,
        IdempotencyToken: str = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_certificate_authority_audit_report(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_permission(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_certificate_authority(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_permission(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_certificate_authority(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_certificate_authority_audit_report(self) -> None:
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
    def get_certificate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_certificate_authority_certificate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_certificate_authority_csr(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def import_certificate_authority_certificate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def issue_certificate(
        self,
        CertificateAuthorityArn: str,
        Csr: bytes,
        SigningAlgorithm: str,
        Validity: Dict[str, Any],
        TemplateArn: str = None,
        IdempotencyToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_certificate_authorities(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_permissions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def restore_certificate_authority(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def revoke_certificate(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_certificate_authority(
        self, CertificateAuthorityArn: str, Tags: List[Any]
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def untag_certificate_authority(
        self, CertificateAuthorityArn: str, Tags: List[Any]
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_certificate_authority(
        self,
        CertificateAuthorityArn: str,
        RevocationConfiguration: Dict[str, Any] = None,
        Status: str = None,
    ) -> None:
        pass
