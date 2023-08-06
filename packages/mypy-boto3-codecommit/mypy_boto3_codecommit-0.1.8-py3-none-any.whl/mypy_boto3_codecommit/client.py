from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    # pylint: disable=arguments-differ
    def batch_describe_merge_conflicts(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_get_commits(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def batch_get_repositories(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_branch(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_commit(
        self,
        repositoryName: str,
        branchName: str,
        parentCommitId: str = None,
        authorName: str = None,
        email: str = None,
        commitMessage: str = None,
        keepEmptyFolders: bool = None,
        putFiles: List[Any] = None,
        deleteFiles: List[Any] = None,
        setFileModes: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_pull_request(
        self,
        title: str,
        targets: List[Any],
        description: str = None,
        clientRequestToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_repository(
        self,
        repositoryName: str,
        repositoryDescription: str = None,
        tags: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_unreferenced_merge_commit(
        self,
        repositoryName: str,
        sourceCommitSpecifier: str,
        destinationCommitSpecifier: str,
        mergeOption: str,
        conflictDetailLevel: str = None,
        conflictResolutionStrategy: str = None,
        authorName: str = None,
        email: str = None,
        commitMessage: str = None,
        keepEmptyFolders: bool = None,
        conflictResolution: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_branch(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_comment_content(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_file(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_repository(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_merge_conflicts(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_pull_request_events(self) -> None:
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
    def get_blob(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_branch(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_comment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_comments_for_compared_commit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_comments_for_pull_request(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_commit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_differences(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_file(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_folder(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_merge_commit(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_merge_conflicts(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_merge_options(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_pull_request(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_repository(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_repository_triggers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_branches(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_pull_requests(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_repositories(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def merge_branches_by_fast_forward(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def merge_branches_by_squash(
        self,
        repositoryName: str,
        sourceCommitSpecifier: str,
        destinationCommitSpecifier: str,
        targetBranch: str = None,
        conflictDetailLevel: str = None,
        conflictResolutionStrategy: str = None,
        authorName: str = None,
        email: str = None,
        commitMessage: str = None,
        keepEmptyFolders: bool = None,
        conflictResolution: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def merge_branches_by_three_way(
        self,
        repositoryName: str,
        sourceCommitSpecifier: str,
        destinationCommitSpecifier: str,
        targetBranch: str = None,
        conflictDetailLevel: str = None,
        conflictResolutionStrategy: str = None,
        authorName: str = None,
        email: str = None,
        commitMessage: str = None,
        keepEmptyFolders: bool = None,
        conflictResolution: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def merge_pull_request_by_fast_forward(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def merge_pull_request_by_squash(
        self,
        pullRequestId: str,
        repositoryName: str,
        sourceCommitId: str = None,
        conflictDetailLevel: str = None,
        conflictResolutionStrategy: str = None,
        commitMessage: str = None,
        authorName: str = None,
        email: str = None,
        keepEmptyFolders: bool = None,
        conflictResolution: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def merge_pull_request_by_three_way(
        self,
        pullRequestId: str,
        repositoryName: str,
        sourceCommitId: str = None,
        conflictDetailLevel: str = None,
        conflictResolutionStrategy: str = None,
        commitMessage: str = None,
        authorName: str = None,
        email: str = None,
        keepEmptyFolders: bool = None,
        conflictResolution: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def post_comment_for_compared_commit(
        self,
        repositoryName: str,
        afterCommitId: str,
        content: str,
        beforeCommitId: str = None,
        location: Dict[str, Any] = None,
        clientRequestToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def post_comment_for_pull_request(
        self,
        pullRequestId: str,
        repositoryName: str,
        beforeCommitId: str,
        afterCommitId: str,
        content: str,
        location: Dict[str, Any] = None,
        clientRequestToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def post_comment_reply(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_file(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_repository_triggers(
        self, repositoryName: str, triggers: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, resourceArn: str, tags: Dict[str, Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def test_repository_triggers(
        self, repositoryName: str, triggers: List[Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_comment(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_default_branch(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_pull_request_description(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_pull_request_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_pull_request_title(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_repository_description(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_repository_name(self) -> None:
        pass
