from __future__ import annotations

from typing import Any
from typing import Dict

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_lexicon(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_voices(self) -> None:
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
    def get_lexicon(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_speech_synthesis_task(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_lexicons(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_speech_synthesis_tasks(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_lexicon(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_speech_synthesis_task(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def synthesize_speech(self) -> None:
        pass
