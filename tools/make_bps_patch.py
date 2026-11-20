"""Create (and check) a BPS patch that turns a clean Pokémon Emerald ROM into the hack.

    python3 tools/make_bps_patch.py CLEAN.gba pokeemerald.gba OUT.bps
    python3 tools/make_bps_patch.py --apply CLEAN.gba PATCH.bps OUT.gba

Creating a patch also applies it in memory and compares the result with the
hack byte for byte, so a patch this script writes is known to work.

BPS format (byuu): "BPS1", source size, target size, metadata size and text,
then actions until the last 12 bytes, which hold the CRC32 of the source, the
target and the patch itself. Each action is a number ((length - 1) << 2 | kind):
    0 SourceRead  copy `length` bytes from the source at the current output offset
    1 TargetRead  `length` literal bytes follow
    2 SourceCopy  copy from the source at a running offset, moved by a signed delta
    3 TargetCopy  copy from the output written so far (also how runs of one byte are encoded)
Numbers use byuu's variable-length encoding (7 bits per byte, high bit ends it).
"""

import argparse
import sys
import zlib
from pathlib import Path

SOURCE_READ, TARGET_READ, SOURCE_COPY, TARGET_COPY = range(4)
BLOCK = 16       # source index granularity: matches of at least this length are found
MIN_RUN = 32     # shortest run of one repeated byte worth a TargetCopy
MIN_SAME = 4     # shortest unchanged stretch worth a SourceRead


def encode_number(value):
    out = bytearray()
    while True:
        low = value & 0x7F
        value >>= 7
        if value == 0:
            out.append(0x80 | low)
            return bytes(out)
        out.append(low)
        value -= 1


def decode_number(data, pos):
    value, shift = 0, 1
    while True:
        byte = data[pos]
        pos += 1
        value += (byte & 0x7F) * shift
        if byte & 0x80:
            return value, pos
        shift <<= 7
        value += shift


def encode_offset(delta):
    return encode_number((abs(delta) << 1) | (delta < 0))


def match_length(a, a_pos, b, b_pos, limit):
    """How many bytes match from a[a_pos] and b[b_pos], checking big slices first."""
    length = 0
    step = 4096
    while length < limit:
        size = min(step, limit - length)
        if a[a_pos + length:a_pos + length + size] == b[b_pos + length:b_pos + length + size]:
            length += size
            continue
        if size <= 8:
            while length < limit and a[a_pos + length] == b[b_pos + length]:
                length += 1
            return length
        step = max(8, size // 8)
    return length


def create_patch(source, target, metadata=b""):
    index = {}
    for offset in range(0, len(source) - BLOCK + 1, BLOCK):
        index.setdefault(source[offset:offset + BLOCK], offset)

    out = bytearray(b"BPS1")
    out += encode_number(len(source)) + encode_number(len(target)) + encode_number(len(metadata)) + metadata
    literal = bytearray()
    source_rel = 0
    target_rel = 0

    def action(kind, length):
        out.extend(encode_number(((length - 1) << 2) | kind))

    def flush_literal():
        if literal:
            action(TARGET_READ, len(literal))
            out.extend(literal)
            literal.clear()

    pos, end = 0, len(target)
    while pos < end:
        # 1. Unchanged bytes at the same offset
        if pos < len(source) and source[pos] == target[pos]:
            same = match_length(source, pos, target, pos, min(len(source), end) - pos)
            if same >= MIN_SAME:
                flush_literal()
                action(SOURCE_READ, same)
                pos += same
                continue
        # 2. A run of one repeated byte (padding): copy the output onto itself
        if pos > 0 and target[pos] == target[pos - 1]:
            run = match_length(target, pos - 1, target, pos, end - pos)
            if run >= MIN_RUN:
                flush_literal()
                action(TARGET_COPY, run)
                out.extend(encode_offset(pos - 1 - target_rel))
                target_rel = pos - 1 + run
                pos += run
                continue
        # 3. Data that exists somewhere else in the source
        offset = index.get(target[pos:pos + BLOCK]) if pos + BLOCK <= end else None
        if offset is not None:
            length = match_length(source, offset, target, pos, min(len(source) - offset, end - pos))
            flush_literal()
            action(SOURCE_COPY, length)
            out.extend(encode_offset(offset - source_rel))
            source_rel = offset + length
            pos += length
            continue
        # 4. New bytes
        literal.append(target[pos])
        pos += 1
    flush_literal()

    out += zlib.crc32(source).to_bytes(4, "little") + zlib.crc32(target).to_bytes(4, "little")
    out += zlib.crc32(out).to_bytes(4, "little")
    return bytes(out)


def apply_patch(source, patch):
    if patch[:4] != b"BPS1":
        raise ValueError("not a BPS patch")
    if zlib.crc32(patch[:-4]) != int.from_bytes(patch[-4:], "little"):
        raise ValueError("the patch is damaged (patch checksum mismatch)")
    if zlib.crc32(source) != int.from_bytes(patch[-12:-8], "little"):
        raise ValueError("wrong source ROM: this patch needs a clean Pokémon Emerald (USA, Europe)")

    pos = 4
    source_size, pos = decode_number(patch, pos)
    target_size, pos = decode_number(patch, pos)
    metadata_size, pos = decode_number(patch, pos)
    pos += metadata_size
    if source_size != len(source):
        raise ValueError("wrong source ROM size")

    output = bytearray()
    source_rel = target_rel = 0
    end = len(patch) - 12
    while pos < end:
        data, pos = decode_number(patch, pos)
        kind, length = data & 3, (data >> 2) + 1
        if kind == SOURCE_READ:
            output += source[len(output):len(output) + length]
        elif kind == TARGET_READ:
            output += patch[pos:pos + length]
            pos += length
        else:
            delta, pos = decode_number(patch, pos)
            delta = -(delta >> 1) if delta & 1 else delta >> 1
            if kind == SOURCE_COPY:
                source_rel += delta
                output += source[source_rel:source_rel + length]
                source_rel += length
            else:
                target_rel += delta
                for _ in range(length):  # byte by byte: the copy may overlap what it writes
                    output.append(output[target_rel])
                    target_rel += 1
    if len(output) != target_size or zlib.crc32(output) != int.from_bytes(patch[-8:-4], "little"):
        raise ValueError("the patched ROM doesn't match the expected result")
    return bytes(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="apply PATCH to CLEAN instead of creating a patch")
    parser.add_argument("clean", type=Path)
    parser.add_argument("second", type=Path, help="the hack ROM (create) or the patch (--apply)")
    parser.add_argument("out", type=Path)
    args = parser.parse_args()

    clean = args.clean.read_bytes()
    if args.apply:
        args.out.write_bytes(apply_patch(clean, args.second.read_bytes()))
        print(f"wrote {args.out}")
        return

    target = args.second.read_bytes()
    patch = create_patch(clean, target)
    if apply_patch(clean, patch) != target:  # never ship a patch that doesn't rebuild the hack exactly
        sys.exit("internal error: the patch doesn't rebuild the ROM; nothing written")
    args.out.write_bytes(patch)
    print(f"wrote {args.out}: {len(patch):,} bytes, verified (rebuilds the ROM byte for byte)")


if __name__ == "__main__":
    main()
