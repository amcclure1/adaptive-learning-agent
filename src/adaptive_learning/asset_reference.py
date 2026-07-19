"""Core-issued logical references for installed static pack assets."""

from __future__ import annotations

import base64
import json
import re
from dataclasses import dataclass

from .errors import LearningError
from .pack_digest import canonical_json_bytes


SCHEME = "ala-pack-asset-v1"
TOKEN = re.compile(r"^[A-Za-z0-9_-]+$")
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True, slots=True)
class AssetReference:
    pack_id: str
    pack_version: str
    pack_digest: str
    asset_id: str


def issue_asset_reference(pack_id: str, pack_version: str, pack_digest: str, asset_id: str) -> str:
    payload = canonical_json_bytes([pack_id, pack_version, pack_digest, asset_id])
    token = base64.urlsafe_b64encode(payload).rstrip(b"=").decode("ascii")
    return f"{SCHEME}:{token}"


def parse_asset_reference(value: object) -> AssetReference:
    if not isinstance(value, str) or not value.startswith(f"{SCHEME}:"):
        raise LearningError("ASSET_REFERENCE_INVALID", "The logical asset reference is malformed.")
    token = value[len(SCHEME) + 1 :]
    if not token or not TOKEN.fullmatch(token):
        raise LearningError("ASSET_REFERENCE_INVALID", "The logical asset reference is malformed.")
    try:
        payload = base64.b64decode(token + "=" * (-len(token) % 4), altchars=b"-_", validate=True)
        values = json.loads(payload.decode("utf-8"))
    except (ValueError, UnicodeError, json.JSONDecodeError) as exc:
        raise LearningError("ASSET_REFERENCE_INVALID", "The logical asset reference is malformed.") from exc
    if (
        not isinstance(values, list)
        or len(values) != 4
        or any(not isinstance(item, str) for item in values)
        or not IDENTIFIER.fullmatch(values[0])
        or not values[1]
        or not SHA256.fullmatch(values[2])
        or not IDENTIFIER.fullmatch(values[3])
        or issue_asset_reference(*values) != value
    ):
        raise LearningError("ASSET_REFERENCE_INVALID", "The logical asset reference is malformed.")
    return AssetReference(*values)
