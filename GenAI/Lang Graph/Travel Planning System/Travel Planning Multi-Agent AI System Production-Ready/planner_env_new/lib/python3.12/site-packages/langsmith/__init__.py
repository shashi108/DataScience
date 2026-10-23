# pyright: basic
"""LangSmith Client."""

from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from langsmith import address
    from langsmith._expect import expect
    from langsmith._exceptions import (
        APIConnectionError,
        APIError,
        APIResponseValidationError,
        APIStatusError,
        APITimeoutError,
        AuthenticationError,
        BadRequestError,
        ConflictError,
        InternalServerError,
        LangsmithError,
        NotFoundError,
        PermissionDeniedError,
        RateLimitError,
        UnprocessableEntityError,
    )
    from langsmith.address import (
        Address,
        AgentAddress,
        EvaluatorAddress,
        ExperimentAddress,
        agent_address,
        experiment_address,
        evaluator_address,
    )
    from langsmith.async_client import AsyncClient
    from langsmith.client import Client, TracingMode
    from langsmith.evaluation import (
        aevaluate,
        aevaluate_existing,
        evaluate,
        evaluate_existing,
    )
    from langsmith.evaluation.evaluator import EvaluationResult, RunEvaluator
    from langsmith import anonymizer
    from langsmith._runtime_overrides import set_runtime_overrides
    from langsmith.prompt_cache import (
        AsyncCache,
        AsyncPromptCache,
        Cache,
        PromptCache,
        configure_global_async_prompt_cache,
        configure_global_prompt_cache,
    )
    from langsmith.run_helpers import (
        get_current_run_tree,
        get_tracing_context,
        set_run_metadata,
        trace,
        traceable,
        tracing_context,
    )
    from langsmith.run_trees import RunTree, configure
    from langsmith.secret import LangSmithSecret
    from langsmith.testing._internal import test, unit
    from langsmith.utils import ContextThreadPoolExecutor
    from langsmith.uuid import (
        compute_run_id_for_secondary_replica,
        uuid7,
        uuid7_from_datetime,
    )

    # Generated (Stainless) client surface. `Client`/`AsyncClient` are NOT
    # re-exported from the generated module: those names belong to the
    # hand-written tracing clients above; the generated ones are `Langsmith`
    # and `AsyncLangsmith`.
    from langsmith import resources, types
    from langsmith._base_client import (
        DefaultAioHttpClient,
        DefaultAsyncHttpxClient,
        DefaultHttpxClient,
    )
    from langsmith._client import (
        AsyncLangsmith,
        AsyncStream,
        Langsmith,
        RequestOptions,
        Stream,
        Timeout,
    )
    from langsmith._constants import (
        DEFAULT_CONNECTION_LIMITS,
        DEFAULT_MAX_RETRIES,
        DEFAULT_TIMEOUT,
    )
    from langsmith._models import BaseModel
    from langsmith._response import APIResponse, AsyncAPIResponse
    from langsmith._types import (
        NOT_GIVEN,
        NoneType,
        NotGiven,
        Omit,
        ProxiesTypes,
        Transport,
        not_given,
        omit,
    )
    from langsmith._utils import file_from_path

from ._version import __title__, __version__

version = __version__  # for backwards compatibility

# Metadata key to hide a traced run from LangSmith's Messages View.
LS_MESSAGE_VIEW_EXCLUDE: Final = "ls_message_view_exclude"


def __getattr__(name: str) -> Any:
    if name == "__version__":
        return version
    elif name == "Client":
        from langsmith.client import Client

        return Client
    elif name == "TracingMode":
        from langsmith.client import TracingMode

        return TracingMode
    elif name == "AsyncClient":
        from langsmith.async_client import AsyncClient

        return AsyncClient
    elif name == "RunTree":
        from langsmith.run_trees import RunTree

        return RunTree
    elif name == "EvaluationResult":
        from langsmith.evaluation.evaluator import EvaluationResult

        return EvaluationResult
    elif name == "RunEvaluator":
        from langsmith.evaluation.evaluator import RunEvaluator

        return RunEvaluator
    elif name == "trace":
        from langsmith.run_helpers import trace

        return trace
    elif name == "traceable":
        from langsmith.run_helpers import traceable

        return traceable

    elif name == "test":
        from langsmith.testing._internal import test

        return test

    elif name == "expect":
        from langsmith._expect import expect

        return expect
    elif name == "evaluate":
        from langsmith.evaluation import evaluate

        return evaluate

    elif name == "evaluate_existing":
        from langsmith.evaluation import evaluate_existing

        return evaluate_existing
    elif name == "aevaluate":
        from langsmith.evaluation import aevaluate

        return aevaluate
    elif name == "aevaluate_existing":
        from langsmith.evaluation import aevaluate_existing

        return aevaluate_existing
    elif name == "address":
        import importlib

        # `from langsmith import address` would re-enter this hook.
        return importlib.import_module("langsmith.address")
    elif name in (
        "Address",
        "AgentAddress",
        "EvaluatorAddress",
        "ExperimentAddress",
        "agent_address",
        "experiment_address",
        "evaluator_address",
    ):
        from langsmith import address

        return getattr(address, name)
    elif name == "tracing_context":
        from langsmith.run_helpers import tracing_context

        return tracing_context

    elif name == "get_tracing_context":
        from langsmith.run_helpers import get_tracing_context

        return get_tracing_context
    elif name == "get_current_run_tree":
        from langsmith.run_helpers import get_current_run_tree

        return get_current_run_tree
    elif name == "set_run_metadata":
        from langsmith.run_helpers import set_run_metadata

        return set_run_metadata

    elif name == "unit":
        from langsmith.testing._internal import unit

        return unit
    elif name == "ContextThreadPoolExecutor":
        from langsmith.utils import ContextThreadPoolExecutor

        return ContextThreadPoolExecutor
    elif name == "configure":
        from langsmith.run_trees import configure

        return configure
    elif name == "compute_run_id_for_secondary_replica":
        from langsmith.uuid import compute_run_id_for_secondary_replica

        return compute_run_id_for_secondary_replica
    elif name == "uuid7":
        from langsmith.uuid import uuid7

        return uuid7
    elif name == "uuid7_from_datetime":
        from langsmith.uuid import uuid7_from_datetime

        return uuid7_from_datetime
    elif name == "PromptCache":
        from langsmith.prompt_cache import PromptCache

        return PromptCache
    elif name == "AsyncPromptCache":
        from langsmith.prompt_cache import AsyncPromptCache

        return AsyncPromptCache
    elif name == "Cache":
        from langsmith.prompt_cache import Cache

        return Cache
    elif name == "AsyncCache":
        from langsmith.prompt_cache import AsyncCache

        return AsyncCache
    elif name == "configure_global_prompt_cache":
        from langsmith.prompt_cache import configure_global_prompt_cache

        return configure_global_prompt_cache

    elif name == "configure_global_async_prompt_cache":
        from langsmith.prompt_cache import configure_global_async_prompt_cache

        return configure_global_async_prompt_cache

    elif name == "LangSmithSecret":
        from langsmith.secret import LangSmithSecret

        return LangSmithSecret

    elif name == "set_runtime_overrides":
        from langsmith._runtime_overrides import set_runtime_overrides

        return set_runtime_overrides

    elif name in (
        "LangsmithError",
        "APIError",
        "APIResponseValidationError",
        "APIStatusError",
        "APIConnectionError",
        "APITimeoutError",
        "BadRequestError",
        "AuthenticationError",
        "PermissionDeniedError",
        "NotFoundError",
        "ConflictError",
        "UnprocessableEntityError",
        "RateLimitError",
        "InternalServerError",
    ):
        import langsmith._exceptions as _exceptions

        exception = getattr(_exceptions, name)
        exception.__module__ = __name__
        return exception

    elif name in _GENERATED_EXPORTS:
        import importlib

        from langsmith._utils._logs import setup_logging

        setup_logging()
        module = importlib.import_module(_GENERATED_EXPORTS[name])
        return getattr(module, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# Public names of the generated Stainless client, resolved lazily so that
# `import langsmith` stays cheap (no httpx/pydantic/anyio at import time).
_GENERATED_EXPORTS: Final[dict[str, str]] = {
    "types": "langsmith.types",
    "resources": "langsmith.resources",
    "NoneType": "langsmith._types",
    "Transport": "langsmith._types",
    "ProxiesTypes": "langsmith._types",
    "NotGiven": "langsmith._types",
    "NOT_GIVEN": "langsmith._types",
    "not_given": "langsmith._types",
    "Omit": "langsmith._types",
    "omit": "langsmith._types",
    "Timeout": "langsmith._client",
    "RequestOptions": "langsmith._client",
    "Stream": "langsmith._client",
    "AsyncStream": "langsmith._client",
    "Langsmith": "langsmith._client",
    "AsyncLangsmith": "langsmith._client",
    "file_from_path": "langsmith._utils",
    "BaseModel": "langsmith._models",
    "APIResponse": "langsmith._response",
    "AsyncAPIResponse": "langsmith._response",
    "DEFAULT_TIMEOUT": "langsmith._constants",
    "DEFAULT_MAX_RETRIES": "langsmith._constants",
    "DEFAULT_CONNECTION_LIMITS": "langsmith._constants",
    "DefaultHttpxClient": "langsmith._base_client",
    "DefaultAsyncHttpxClient": "langsmith._base_client",
    "DefaultAioHttpClient": "langsmith._base_client",
}


__all__ = [
    "Client",
    "AsyncClient",
    "TracingMode",
    "PromptCache",
    "AsyncPromptCache",
    "Cache",
    "AsyncCache",
    "configure_global_prompt_cache",
    "configure_global_async_prompt_cache",
    "RunTree",
    "configure",
    "__version__",
    "EvaluationResult",
    "RunEvaluator",
    "anonymizer",
    "traceable",
    "trace",
    "unit",
    "test",
    "expect",
    "evaluate",
    "evaluate_existing",
    "aevaluate_existing",
    "aevaluate",
    "tracing_context",
    "get_tracing_context",
    "address",
    "Address",
    "AgentAddress",
    "ExperimentAddress",
    "EvaluatorAddress",
    "agent_address",
    "experiment_address",
    "evaluator_address",
    "get_current_run_tree",
    "set_run_metadata",
    "ContextThreadPoolExecutor",
    "compute_run_id_for_secondary_replica",
    "uuid7",
    "uuid7_from_datetime",
    "set_runtime_overrides",
    "LangSmithSecret",
    "LS_MESSAGE_VIEW_EXCLUDE",
    "LangsmithError",
    "APIError",
    "APIResponseValidationError",
    "APIStatusError",
    "APIConnectionError",
    "APITimeoutError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
    "__title__",
    # generated client (see _GENERATED_EXPORTS)
    "types",
    "resources",
    "NoneType",
    "Transport",
    "ProxiesTypes",
    "NotGiven",
    "NOT_GIVEN",
    "not_given",
    "Omit",
    "omit",
    "Timeout",
    "RequestOptions",
    "Stream",
    "AsyncStream",
    "Langsmith",
    "AsyncLangsmith",
    "file_from_path",
    "BaseModel",
    "APIResponse",
    "AsyncAPIResponse",
    "DEFAULT_TIMEOUT",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_CONNECTION_LIMITS",
    "DefaultHttpxClient",
    "DefaultAsyncHttpxClient",
    "DefaultAioHttpClient",
]
