"""Deterministic, runtime-independent authored-content infrastructure."""

from .canonical import artifact_digest, canonical_json_bytes, normalize_markdown
from .compiler import AUTHORING_COMPILER_VERSION, compile_candidate, finalize_release_evidence
from .operations import AuthoringOperations
from .validation import validate_workspace
from .workspace import initialize_workspace

__all__ = [
    "AUTHORING_COMPILER_VERSION",
    "AuthoringOperations",
    "artifact_digest",
    "canonical_json_bytes",
    "compile_candidate",
    "finalize_release_evidence",
    "initialize_workspace",
    "normalize_markdown",
    "validate_workspace",
]
