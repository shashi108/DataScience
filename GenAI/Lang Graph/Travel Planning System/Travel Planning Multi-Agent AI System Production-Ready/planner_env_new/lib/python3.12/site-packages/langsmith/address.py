"""Addresses that name features that hold traces in a tracing project.

!!! warning "Beta"
    Addressing runs to an agent is enabled per workspace. A workspace without
    it rejects the runs, so tracing is lost rather than falling back to a
    project. This API may change without notice.

An `Address` names the tracing project of a feature: an `AgentAddress`'s
environment, an `ExperimentAddress`, or the workspace's `EvaluatorAddress` traces.
Query APIs resolve an address to its project (`client.sessions.resolve`). Only an
`AgentAddress` can receive traces, so tracing entry points take an `AgentAddress`,
and anything else is rejected.
The environment of an agent is one of `LOCAL`, `DEVELOPMENT`, `STAGING` or
`PRODUCTION`. Factories accept any case.

Example:
    ```python
    import langsmith as ls

    support = ls.agent_address(id="customer-support", environment="production")


    @ls.traceable(address=support)
    def handle(order): ...


    with ls.tracing_context(address=ls.agent_address("customer-support", "staging")):
        handle(order)
    ```
"""

from __future__ import annotations

import re
from typing import Any, Optional, cast
from typing_extensions import Literal, TypedDict

from langsmith import utils

__all__ = [
    "Address",
    "AgentAddress",
    "ApiAddress",
    "EvaluatorAddress",
    "EnvAddressError",
    "ExperimentAddress",
    "agent_address",
    "experiment_address",
    "evaluator_address",
]

_AGENT_ID_PATTERN = re.compile(r"[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?")
_ENVIRONMENTS = ("local", "development", "staging", "production")
_UUID_PATTERN = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.IGNORECASE)


class AgentAddress(TypedDict):
    """(beta) An agent address. Use `agent_address` to validate and construct one.

    The id is a DNS label of 1 to 63 lowercase ASCII letters, digits or hyphens,
    starting with a letter and ending with a letter or digit. The environment is
    local, development, staging or production.
    """

    kind: Literal["AGENT"]
    id: str
    environment: Literal["LOCAL", "DEVELOPMENT", "STAGING", "PRODUCTION"]


class ExperimentAddress(TypedDict):
    """(beta) An experiment address. Use `experiment_address` to construct one."""

    kind: Literal["EXPERIMENT"]
    id: str


class EvaluatorAddress(TypedDict):
    """(beta) The address of the workspace's shared evaluators project."""

    kind: Literal["EVALUATOR"]


Address = AgentAddress | ExperimentAddress | EvaluatorAddress
ApiAddress = Address


class EnvAddressError(utils.LangSmithUserError):
    """(beta) The `LANGSMITH_AGENT_*` / project env vars can't address a run.

    Raised for half an address, an invalid one, or an address beside a project.
    Tracing entry points (`@traceable`, `trace`, `tracing_context`,
    `create_run`) catch it, log it and leave the call untraced, so a bad
    environment never breaks the code being traced. Explicit ingestion calls
    (`batch_ingest_runs`, `multipart_ingest`) let it raise for runs that name no
    destination, rather than drop part of a batch the caller built.
    """


def agent_address(id: str, environment: str) -> AgentAddress:
    """(beta) Construct an agent address with its kind and environment.

    Args:
        id: A DNS label of 1 to 63 lowercase ASCII letters, digits or hyphens,
            starting with a letter and ending with a letter or digit.
        environment: Local, development, staging or production.

    Raises:
        LangSmithUserError: If the id or environment is invalid.
    """
    if not isinstance(id, str) or not _AGENT_ID_PATTERN.fullmatch(id):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise utils.LangSmithUserError(
            "Address agent id must be 1 to 63 lowercase ASCII letters, digits, "
            "or hyphens, start with a letter, and end with a letter or digit, "
            f"got {id!r}. Use an id such as 'support-agent'."
        )
    normalized = environment.lower() if isinstance(environment, str) else None  # pyright: ignore[reportUnnecessaryIsInstance]
    if normalized not in _ENVIRONMENTS:
        raise utils.LangSmithUserError(
            f"Address environment must be one of {', '.join(_ENVIRONMENTS)}, got {environment!r}."
        )
    return {
        "kind": "AGENT",
        "id": id,
        "environment": cast(Literal["LOCAL", "DEVELOPMENT", "STAGING", "PRODUCTION"], cast(str, normalized).upper()),
    }


def experiment_address(id: str) -> ExperimentAddress:
    """(beta) Construct an experiment address with its kind and lowercase UUID.

    Raises:
        LangSmithUserError: If the id is not a canonical, hyphenated UUID.
    """
    if not isinstance(id, str) or not _UUID_PATTERN.fullmatch(id):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise utils.LangSmithUserError(
            f"An experiment id must be a UUID with hyphens, such as '0190c3d4-0000-7000-8000-0000000000b1', got {id!r}."
        )
    return {"kind": "EXPERIMENT", "id": id.lower()}


def evaluator_address() -> EvaluatorAddress:
    """(beta) Construct the address of the workspace's shared evaluators project."""
    return {"kind": "EVALUATOR"}


def ensure_agent(address: Any) -> AgentAddress:
    """Validate a plain agent address at a tracing entry point."""
    if isinstance(address, dict):
        address = cast(dict[str, Any], address)
        if address.get("kind") == "AGENT":
            return agent_address(cast(str, address.get("id")), cast(str, address.get("environment")))
        if address.get("kind") in ("EXPERIMENT", "EVALUATOR"):
            raise utils.LangSmithUserError(f"Only an `AgentAddress` can receive traces, got {address!r}.")
    raise utils.LangSmithUserError(
        f"An address must be an `AgentAddress` such as `ls.agent_address(id, environment)`, got {address!r}."
    )


def ensure_address(address: Any) -> Address:
    """Validate an `Address` of any kind, as a lookup takes it.

    For the calls that only resolve an address to its project, such as
    `get_run_url`. Whatever receives traces takes `ensure_agent`. A string is
    not an address.

    Raises:
        LangSmithUserError: If `address` is not an `Address`.
    """
    if isinstance(address, dict):
        address = cast(dict[str, Any], address)
        kind = address.get("kind")
        if kind == "AGENT":
            return agent_address(cast(str, address.get("id")), cast(str, address.get("environment")))
        if kind == "EXPERIMENT":
            return experiment_address(cast(str, address.get("id")))
        if kind == "EVALUATOR":
            return evaluator_address()
    raise utils.LangSmithUserError(
        f"An address must be an `AgentAddress`, `ExperimentAddress` or `EvaluatorAddress`, got {address!r}."
    )


def address_from_env() -> Optional[AgentAddress]:
    """Read and validate LANGSMITH_AGENT_ID and LANGSMITH_AGENT_ENVIRONMENT."""
    values = env_values()
    if not any(values.values()):
        return None
    missing = [name for name, value in values.items() if not value]
    try:
        if missing:
            raise utils.LangSmithUserError(f"An address needs {' and '.join(missing)} as well.")
        return agent_address(cast(str, values["LANGSMITH_AGENT_ID"]), cast(str, values["LANGSMITH_AGENT_ENVIRONMENT"]))
    except utils.LangSmithUserError as e:
        present = ", ".join(f"{name}={value!r}" for name, value in values.items() if value)
        raise EnvAddressError(f"The LANGSMITH_AGENT_* env vars can't address a run ({present}): {e}") from e


def env_values() -> dict[str, Optional[str]]:
    """Return each LANGSMITH_AGENT_* env var an address reads, with its value."""
    return {
        f"LANGSMITH_{name}": utils.get_env_var(name, namespaces=("LANGSMITH",))
        for name in ("AGENT_ID", "AGENT_ENVIRONMENT")
    }
