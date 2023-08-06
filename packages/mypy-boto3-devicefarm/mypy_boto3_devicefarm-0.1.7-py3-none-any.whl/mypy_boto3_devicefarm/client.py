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
    def create_device_pool(
        self,
        projectArn: str,
        name: str,
        rules: List[Any],
        description: str = None,
        maxDevices: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_instance_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_network_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_project(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_remote_access_session(
        self,
        projectArn: str,
        deviceArn: str,
        instanceArn: str = None,
        sshPublicKey: str = None,
        remoteDebugEnabled: bool = None,
        remoteRecordEnabled: bool = None,
        remoteRecordAppArn: str = None,
        name: str = None,
        clientId: str = None,
        configuration: Dict[str, Any] = None,
        interactionMode: str = None,
        skipAppResign: bool = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_upload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_vpce_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_device_pool(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_instance_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_network_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_project(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_remote_access_session(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_run(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_upload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_vpce_configuration(self) -> None:
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
    def get_account_settings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_device_instance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_device_pool(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_device_pool_compatibility(
        self,
        devicePoolArn: str,
        appArn: str = None,
        testType: str = None,
        test: Dict[str, Any] = None,
        configuration: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def get_instance_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_network_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_offering_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_project(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_remote_access_session(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_run(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_suite(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_test(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_upload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_vpce_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def install_to_remote_access_session(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_artifacts(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_device_instances(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_device_pools(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_devices(
        self, arn: str = None, nextToken: str = None, filters: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_instance_profiles(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_jobs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_network_profiles(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_offering_promotions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_offering_transactions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_offerings(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_projects(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_remote_access_sessions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_runs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_samples(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_suites(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tests(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_unique_problems(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_uploads(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_vpce_configurations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def purchase_offering(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def renew_offering(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def schedule_run(
        self,
        projectArn: str,
        test: Dict[str, Any],
        appArn: str = None,
        devicePoolArn: str = None,
        deviceSelectionConfiguration: Dict[str, Any] = None,
        name: str = None,
        configuration: Dict[str, Any] = None,
        executionConfiguration: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def stop_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def stop_remote_access_session(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def stop_run(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, ResourceARN: str, Tags: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_device_instance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_device_pool(
        self,
        arn: str,
        name: str = None,
        description: str = None,
        rules: List[Any] = None,
        maxDevices: int = None,
        clearMaxDevices: bool = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_instance_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_network_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_project(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_upload(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_vpce_configuration(self) -> None:
        pass
