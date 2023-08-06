from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def acknowledge_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def acknowledge_third_party_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_custom_action_type(
        self,
        category: str,
        provider: str,
        version: str,
        inputArtifactDetails: Dict[str, Any],
        outputArtifactDetails: Dict[str, Any],
        settings: Dict[str, Any] = None,
        configurationProperties: List[Any] = None,
        tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_pipeline(
        self, pipeline: Dict[str, Any], tags: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_custom_action_type(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_pipeline(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_webhook(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deregister_webhook_with_third_party(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disable_stage_transition(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def enable_stage_transition(self) -> None:
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
    def get_job_details(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_pipeline(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_pipeline_execution(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_pipeline_state(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_third_party_job_details(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_action_executions(
        self,
        pipelineName: str,
        filter: Dict[str, Any] = None,
        maxResults: int = None,
        nextToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_action_types(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_pipeline_executions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_pipelines(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_webhooks(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def poll_for_jobs(
        self,
        actionTypeId: Dict[str, Any],
        maxBatchSize: int = None,
        queryParam: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def poll_for_third_party_jobs(
        self, actionTypeId: Dict[str, Any], maxBatchSize: int = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_action_revision(
        self,
        pipelineName: str,
        stageName: str,
        actionName: str,
        actionRevision: Dict[str, Any],
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_approval_result(
        self,
        pipelineName: str,
        stageName: str,
        actionName: str,
        result: Dict[str, Any],
        token: str,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_job_failure_result(
        self, jobId: str, failureDetails: Dict[str, Any]
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_job_success_result(
        self,
        jobId: str,
        currentRevision: Dict[str, Any] = None,
        continuationToken: str = None,
        executionDetails: Dict[str, Any] = None,
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_third_party_job_failure_result(
        self, jobId: str, clientToken: str, failureDetails: Dict[str, Any]
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_third_party_job_success_result(
        self,
        jobId: str,
        clientToken: str,
        currentRevision: Dict[str, Any] = None,
        continuationToken: str = None,
        executionDetails: Dict[str, Any] = None,
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_webhook(
        self, webhook: Dict[str, Any], tags: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def register_webhook_with_third_party(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def retry_stage_execution(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_pipeline_execution(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, resourceArn: str, tags: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_pipeline(self, pipeline: Dict[str, Any]) -> Dict[str, Any]:
        pass
