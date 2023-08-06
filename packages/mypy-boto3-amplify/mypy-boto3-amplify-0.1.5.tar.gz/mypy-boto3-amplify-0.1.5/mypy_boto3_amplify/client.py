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
    def create_app(
        self,
        name: str,
        description: str = None,
        repository: str = None,
        platform: str = None,
        iamServiceRoleArn: str = None,
        oauthToken: str = None,
        accessToken: str = None,
        environmentVariables: Dict[str, Any] = None,
        enableBranchAutoBuild: bool = None,
        enableBasicAuth: bool = None,
        basicAuthCredentials: str = None,
        customRules: List[Any] = None,
        tags: Dict[str, Any] = None,
        buildSpec: str = None,
        enableAutoBranchCreation: bool = None,
        autoBranchCreationPatterns: List[Any] = None,
        autoBranchCreationConfig: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_branch(
        self,
        appId: str,
        branchName: str,
        description: str = None,
        stage: str = None,
        framework: str = None,
        enableNotification: bool = None,
        enableAutoBuild: bool = None,
        environmentVariables: Dict[str, Any] = None,
        basicAuthCredentials: str = None,
        enableBasicAuth: bool = None,
        tags: Dict[str, Any] = None,
        buildSpec: str = None,
        ttl: str = None,
        displayName: str = None,
        enablePullRequestPreview: bool = None,
        pullRequestEnvironmentName: str = None,
        backendEnvironmentArn: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_deployment(
        self, appId: str, branchName: str, fileMap: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_domain_association(
        self,
        appId: str,
        domainName: str,
        subDomainSettings: List[Any],
        enableAutoSubDomain: bool = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_webhook(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_app(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_branch(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_domain_association(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_webhook(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def generate_access_logs(self) -> None:
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
    def get_app(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_artifact_url(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_branch(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_domain_association(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def get_webhook(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_apps(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_artifacts(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_branches(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_domain_associations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_jobs(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_webhooks(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_deployment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def stop_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, resourceArn: str, tags: Dict[str, Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_app(
        self,
        appId: str,
        name: str = None,
        description: str = None,
        platform: str = None,
        iamServiceRoleArn: str = None,
        environmentVariables: Dict[str, Any] = None,
        enableBranchAutoBuild: bool = None,
        enableBasicAuth: bool = None,
        basicAuthCredentials: str = None,
        customRules: List[Any] = None,
        buildSpec: str = None,
        enableAutoBranchCreation: bool = None,
        autoBranchCreationPatterns: List[Any] = None,
        autoBranchCreationConfig: Dict[str, Any] = None,
        repository: str = None,
        oauthToken: str = None,
        accessToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_branch(
        self,
        appId: str,
        branchName: str,
        description: str = None,
        framework: str = None,
        stage: str = None,
        enableNotification: bool = None,
        enableAutoBuild: bool = None,
        environmentVariables: Dict[str, Any] = None,
        basicAuthCredentials: str = None,
        enableBasicAuth: bool = None,
        buildSpec: str = None,
        ttl: str = None,
        displayName: str = None,
        enablePullRequestPreview: bool = None,
        pullRequestEnvironmentName: str = None,
        backendEnvironmentArn: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_domain_association(
        self,
        appId: str,
        domainName: str,
        subDomainSettings: List[Any],
        enableAutoSubDomain: bool = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_webhook(self) -> None:
        pass
