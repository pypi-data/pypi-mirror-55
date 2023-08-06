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
    def cancel_task_execution(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_agent(
        self,
        ActivationKey: str,
        AgentName: str = None,
        Tags: List[Any] = None,
        VpcEndpointId: str = None,
        SubnetArns: List[Any] = None,
        SecurityGroupArns: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_location_efs(
        self,
        EfsFilesystemArn: str,
        Ec2Config: Dict[str, Any],
        Subdirectory: str = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_location_nfs(
        self,
        Subdirectory: str,
        ServerHostname: str,
        OnPremConfig: Dict[str, Any],
        MountOptions: Dict[str, Any] = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_location_s3(
        self,
        S3BucketArn: str,
        S3Config: Dict[str, Any],
        Subdirectory: str = None,
        S3StorageClass: str = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_location_smb(
        self,
        Subdirectory: str,
        ServerHostname: str,
        User: str,
        Password: str,
        AgentArns: List[Any],
        Domain: str = None,
        MountOptions: Dict[str, Any] = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_task(
        self,
        SourceLocationArn: str,
        DestinationLocationArn: str,
        CloudWatchLogGroupArn: str = None,
        Name: str = None,
        Options: Dict[str, Any] = None,
        Excludes: List[Any] = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_agent(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_location(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_task(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_agent(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_location_efs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_location_nfs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_location_s3(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_location_smb(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_task(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_task_execution(self) -> None:
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
    def list_agents(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_locations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_task_executions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tasks(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_task_execution(
        self,
        TaskArn: str,
        OverrideOptions: Dict[str, Any] = None,
        Includes: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, ResourceArn: str, Tags: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_agent(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_task(
        self,
        TaskArn: str,
        Options: Dict[str, Any] = None,
        Excludes: List[Any] = None,
        Name: str = None,
        CloudWatchLogGroupArn: str = None,
    ) -> Dict[str, Any]:
        pass
