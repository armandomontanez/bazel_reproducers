"""Minimal ELF64 reader for inspecting debug info in build outputs.

Deliberately avoids llvm-dwarfdump/readelf so that results don't depend on
which binutils happen to be installed on the host.
"""

import dataclasses
import json
import re
import struct
import zlib

_ELF_MAGIC = b"\x7fELF"
_ELFCLASS64 = 2
_ELFDATA2LSB = 1
_SHT_NOBITS = 8
_SHT_RELA = 4
_SHT_REL = 9
_SHF_EXECINSTR = 0x4
_SHF_COMPRESSED = 0x800
_ELFCOMPRESS_ZLIB = 1

# Comp dirs that are identical on every machine. Bazel sets PWD=/proc/self/cwd
# for compile actions on non-Darwin exec platforms, which gcc/clang will use
# instead of getcwd() when it resolves to the same directory.
_STABLE_PATH_PREFIXES = ("/proc/self/cwd",)

# Path fragments that only exist inside a Bazel output base, sandbox, or
# remote worker's execroot.
_BUILD_ENVIRONMENT_MARKERS = ("/execroot/", "/sandbox/", "/_bazel_")

STABLE = "stable"
BUILD_ENVIRONMENT = "build environment"
PREBUILT_INPUT = "prebuilt input"

_ABSOLUTE_PATH = re.compile(rb"(?<![\x21-\x7e])/[\w.@+-]+(?:/[\w.@+-]+)+/?")
_DWO_NAME = re.compile(rb"[\w./@+-]+\.dwo(?![\w.])")


@dataclasses.dataclass(frozen=True)
class Section:
    name: str
    size_on_disk: int
    data: bytes
    compressed: bool
    executable: bool


@dataclasses.dataclass(frozen=True)
class Variant:
    name: str
    features: list[str]
    fission: bool
    files: list[str]

    def files_with_suffix(self, suffix):
        return [f for f in self.files if f.endswith(suffix)]


def load_variant(manifest_path):
    with open(manifest_path) as f:
        return Variant(**json.load(f))


def read_sections(path):
    with open(path, "rb") as f:
        elf = f.read()

    if elf[:4] != _ELF_MAGIC or elf[4] != _ELFCLASS64 or elf[5] != _ELFDATA2LSB:
        raise ValueError(f"{path} is not a little-endian ELF64 file")

    (shoff,) = struct.unpack_from("<Q", elf, 0x28)
    shentsize, shnum, shstrndx = struct.unpack_from("<HHH", elf, 0x3A)

    headers = [
        struct.unpack_from("<IIQQQQIIQQ", elf, shoff + i * shentsize)
        for i in range(shnum)
    ]
    shstrtab_offset, shstrtab_size = headers[shstrndx][4:6]
    shstrtab = elf[shstrtab_offset : shstrtab_offset + shstrtab_size]

    sections = []
    for name_offset, sh_type, flags, _, offset, size, *_ in headers:
        name = shstrtab[name_offset : shstrtab.index(b"\0", name_offset)].decode()
        if sh_type == _SHT_NOBITS:
            data = b""
            size = 0
        else:
            data = elf[offset : offset + size]
        compressed = bool(flags & _SHF_COMPRESSED)
        if compressed:
            data = _decompress(path, name, data)
        if sh_type in (_SHT_REL, _SHT_RELA):
            data = b""
        executable = bool(flags & _SHF_EXECINSTR)
        sections.append(Section(name, size, data, compressed, executable))
    return sections


def _decompress(path, section_name, data):
    # Elf64_Chdr: ch_type, ch_reserved, ch_size, ch_addralign.
    ch_type, _, ch_size, _ = struct.unpack_from("<IIQQ", data)
    if ch_type != _ELFCOMPRESS_ZLIB:
        raise ValueError(
            f"{path}:{section_name} uses unsupported compression type {ch_type}"
        )
    decompressed = zlib.decompress(data[24:])
    assert len(decompressed) == ch_size
    return decompressed


def is_debug_section(section):
    return section.name.startswith((".debug", ".gdb_index"))


def find_absolute_paths(sections):
    """Returns {path: {section names}} for absolute paths in string data."""
    found = {}
    for section in sections:
        if section.executable:
            continue
        for match in _ABSOLUTE_PATH.finditer(section.data):
            found.setdefault(match.group().decode(), set()).add(section.name)
    return found


def classify_path(path):
    """Classifies an absolute path found in a build output.

    BUILD_ENVIRONMENT paths differ between machines (and between sandboxes on
    the same machine), so they make outputs irreproducible. PREBUILT_INPUT paths
    were already present in an input, such as the debug info of a prebuilt
    sanitizer runtime, and are the same everywhere that input is used.
    """
    if path.startswith(_STABLE_PATH_PREFIXES):
        return STABLE
    if any(marker in path + "/" for marker in _BUILD_ENVIRONMENT_MARKERS):
        return BUILD_ENVIRONMENT
    return PREBUILT_INPUT


def find_dwo_names(sections):
    """Returns DW_AT_dwo_name values recorded by split DWARF skeleton units."""
    names = set()
    for section in sections:
        if section.name in (".debug_str", ".debug_info"):
            names.update(m.group().decode() for m in _DWO_NAME.finditer(section.data))
    return names
