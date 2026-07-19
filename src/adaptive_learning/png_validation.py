"""Small structural PNG validator for untrusted format-0.3 pack assets."""

from __future__ import annotations

import zlib
from dataclasses import dataclass

from .errors import LearningError


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
KNOWN_CRITICAL_CHUNKS = {b"IHDR", b"PLTE", b"IDAT", b"IEND"}
VALID_DEPTHS = {
    0: {1, 2, 4, 8, 16},
    2: {8, 16},
    3: {1, 2, 4, 8},
    4: {8, 16},
    6: {8, 16},
}


@dataclass(frozen=True, slots=True)
class PngInfo:
    width: int
    height: int
    bit_depth: int
    color_type: int


def _fail(message: str) -> None:
    raise LearningError("PACK_VALIDATION_FAILED", message)


def validate_png(data: bytes, *, maximum_dimension: int = 4096) -> PngInfo:
    """Validate PNG framing and critical structure without decoding pixels."""

    if not isinstance(data, bytes) or not data.startswith(PNG_SIGNATURE):
        _fail("Asset bytes do not have the PNG signature.")
    offset = len(PNG_SIGNATURE)
    chunk_index = 0
    saw_ihdr = False
    saw_plte = False
    saw_idat = False
    idat_ended = False
    saw_iend = False
    width = height = bit_depth = color_type = 0

    while offset < len(data):
        if len(data) - offset < 12:
            _fail("PNG chunk framing is truncated.")
        length = int.from_bytes(data[offset : offset + 4], "big")
        chunk_type = data[offset + 4 : offset + 8]
        offset += 8
        if len(chunk_type) != 4 or any(not (65 <= byte <= 90 or 97 <= byte <= 122) for byte in chunk_type):
            _fail("PNG chunk type is invalid.")
        if 2**31 - 1 < length or len(data) - offset < length + 4:
            _fail("PNG chunk length exceeds the available bytes.")
        payload = data[offset : offset + length]
        declared_crc = int.from_bytes(data[offset + length : offset + length + 4], "big")
        actual_crc = zlib.crc32(chunk_type + payload) & 0xFFFFFFFF
        if declared_crc != actual_crc:
            _fail(f"PNG chunk {chunk_type.decode('ascii')} has an invalid CRC.")
        offset += length + 4

        if chunk_type[0] & 0x20 == 0 and chunk_type not in KNOWN_CRITICAL_CHUNKS:
            _fail("PNG contains an unsupported critical chunk.")
        if chunk_index == 0 and chunk_type != b"IHDR":
            _fail("PNG IHDR must be the first chunk.")
        if chunk_type == b"IHDR":
            if saw_ihdr or length != 13:
                _fail("PNG must contain one 13-byte IHDR chunk.")
            saw_ihdr = True
            width = int.from_bytes(payload[0:4], "big")
            height = int.from_bytes(payload[4:8], "big")
            bit_depth, color_type, compression, filtering, interlace = payload[8:13]
            if not 1 <= width <= maximum_dimension or not 1 <= height <= maximum_dimension:
                _fail("PNG dimensions are outside the format-0.3 limits.")
            if color_type not in VALID_DEPTHS or bit_depth not in VALID_DEPTHS[color_type]:
                _fail("PNG bit depth and color type are not a valid combination.")
            if compression != 0 or filtering != 0 or interlace not in {0, 1}:
                _fail("PNG IHDR uses an unsupported compression, filter, or interlace method.")
        elif chunk_type == b"PLTE":
            if not saw_ihdr or saw_plte or saw_idat or length == 0 or length % 3 or length > 768:
                _fail("PNG PLTE structure or ordering is invalid.")
            if color_type in {0, 4}:
                _fail("PNG PLTE is forbidden for grayscale color types.")
            saw_plte = True
        elif chunk_type == b"IDAT":
            if not saw_ihdr or idat_ended:
                _fail("PNG IDAT chunks must be consecutive and follow IHDR/PLTE.")
            if color_type == 3 and not saw_plte:
                _fail("Indexed-color PNG requires PLTE before IDAT.")
            saw_idat = True
        elif saw_idat and chunk_type != b"IEND":
            idat_ended = True
        if chunk_type == b"IEND":
            if not saw_idat or saw_iend or length != 0:
                _fail("PNG IEND structure or ordering is invalid.")
            saw_iend = True
            if offset != len(data):
                _fail("PNG has trailing bytes after IEND.")
            break
        chunk_index += 1

    if not saw_ihdr or not saw_idat or not saw_iend:
        _fail("PNG is missing IHDR, IDAT, or IEND.")
    return PngInfo(width, height, bit_depth, color_type)
