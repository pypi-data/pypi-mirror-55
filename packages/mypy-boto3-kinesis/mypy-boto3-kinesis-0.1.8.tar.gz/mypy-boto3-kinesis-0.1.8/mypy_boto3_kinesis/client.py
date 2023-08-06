from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    # pylint: disable=arguments-differ
    def add_tags_to_stream(self, StreamName: str, Tags: Dict[str, Any]) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_stream(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def decrease_stream_retention_period(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_stream(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def deregister_stream_consumer(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_limits(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_stream(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_stream_consumer(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_stream_summary(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disable_enhanced_monitoring(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def enable_enhanced_monitoring(self) -> None:
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
    def get_records(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_shard_iterator(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def increase_stream_retention_period(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_shards(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_stream_consumers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_streams(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags_for_stream(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def merge_shards(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_record(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_records(self, Records: List[Any], StreamName: str) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def register_stream_consumer(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def remove_tags_from_stream(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def split_shard(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_stream_encryption(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def stop_stream_encryption(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def subscribe_to_shard(
        self, ConsumerARN: str, ShardId: str, StartingPosition: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_shard_count(self) -> None:
        pass
