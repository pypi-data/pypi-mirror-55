from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def associate_entity_to_thing(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_flow_template(
        self, definition: Dict[str, Any], compatibleNamespaceVersion: int = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_system_instance(
        self,
        definition: Dict[str, Any],
        target: str,
        tags: List[Any] = None,
        greengrassGroupName: str = None,
        s3BucketName: str = None,
        metricsConfiguration: Dict[str, Any] = None,
        flowActionsRoleArn: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_system_template(
        self, definition: Dict[str, Any], compatibleNamespaceVersion: int = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_flow_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_namespace(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_system_instance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_system_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deploy_system_instance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deprecate_flow_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deprecate_system_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_namespace(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def dissociate_entity_from_thing(self) -> None:
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
    def get_entities(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_flow_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_flow_template_revisions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_namespace_deletion_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_system_instance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_system_template(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_system_template_revisions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_upload_status(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_flow_execution_messages(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def search_entities(
        self,
        entityTypes: List[Any],
        filters: List[Any] = None,
        nextToken: str = None,
        maxResults: int = None,
        namespaceVersion: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def search_flow_executions(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def search_flow_templates(
        self, filters: List[Any] = None, nextToken: str = None, maxResults: int = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def search_system_instances(
        self, filters: List[Any] = None, nextToken: str = None, maxResults: int = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def search_system_templates(
        self, filters: List[Any] = None, nextToken: str = None, maxResults: int = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def search_things(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, resourceArn: str, tags: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def undeploy_system_instance(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_flow_template(
        self,
        id: str,
        definition: Dict[str, Any],
        compatibleNamespaceVersion: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_system_template(
        self,
        id: str,
        definition: Dict[str, Any],
        compatibleNamespaceVersion: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def upload_entity_definitions(
        self,
        document: Dict[str, Any] = None,
        syncWithPublicNamespace: bool = None,
        deprecateExistingEntities: bool = None,
    ) -> Dict[str, Any]:
        pass
