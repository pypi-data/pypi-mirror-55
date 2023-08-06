from __future__ import annotations

from typing import Any
from typing import Dict

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def associate_domain(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def associate_website_authorization_provider(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def associate_website_certificate_authority(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_fleet(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_fleet(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_audit_stream_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_company_network_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_device_policy_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_domain(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_fleet_metadata(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_identity_provider_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_website_certificate_authority(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_domain(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_website_authorization_provider(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_website_certificate_authority(self) -> None:
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
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_devices(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_domains(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_fleets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_website_authorization_providers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_website_certificate_authorities(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def restore_domain_access(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def revoke_domain_access(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def sign_out_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_audit_stream_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_company_network_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_device_policy_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_domain_metadata(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_fleet_metadata(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_identity_provider_configuration(self) -> None:
        pass
