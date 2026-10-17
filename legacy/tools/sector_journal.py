"""Power-loss journal for the fx-5800P program sector.

CPU 8:3000 commits ER0 (32-byte-aligned S1 page, 4000..5fe0) from
ER2 (32 bytes of internal RAM; only 16 data bytes in the final page);
CPU 8:3800 recovers before editor reads.
CPU 8:3e00 prepares a verified backup and erases S1 (no arguments), then
CPU 8:3f00 finishes a transformed S1 (ER0 = expected CRC-CCITT of its
8176 data bytes). Both return ER0=0/-1 and preserve XR4 and R8..R15.
Between these entries a caller may program transformed bytes using
8:3cc0 (ER0=S1 destination, ER4=segment-zero RAM source, ER6=byte count);
the wrapper sets the flash destination segment to 8, preserves XR4/R8..R15,
and returns ER0=0/-1. The caller must verify every rewritten byte against
the intended output before finishing. CPU 8:3f80 updates CRC-CCITT with
ER0=running CRC (start ffff), R2=next byte; result ER0, clobbers R2/R3.
The full-sector CRC at 8:3a00 takes ER0=flash offset, ER2=length.
Commit/recovery also return ER0=0 or -1, preserving XR4 and R8..R15.
The caller must not use staged bytes after commit starts, even on failure.

S1 4000..5fef is program data; S2 6000..7fef is its full backup. Each
sector reserves its last 16 bytes: CRC-CCITT (little endian), one's
complement, a two-byte 4a b6 completion marker, and ten erased bytes.
The marker is written last. S2 is verified byte-for-byte before S1 erase;
S1 is verified against S2 except for the staged page before its marker.
Recovery trusts only a matching marker and data CRC, preferentially keeps
valid S1 (even if S2 holds an older image), otherwise restores valid S2.
With neither valid, a completely erased S1 is the initial virgin state;
anything else fails closed. Once S2 is valid it is never erased until the
next commit's recovery has finished successfully.
"""

from u8_emit import Code

COMMIT_ADDRESS = 0x83000
RECOVER_ADDRESS = 0x83800
BACKUP_ADDRESS = 0x83e00
FINISH_ADDRESS = 0x83f00
CRC_UPDATE_ADDRESS = 0x83f80
PROGRAM_RAM_ADDRESS = 0x83cc0
_CRC = 0x83a00
_COMPARE = 0x83a80
_CHECK = 0x83b00
_ERASED = 0x83c00
_PROGRAM = 0x83d80
_META = 0x83d00
_FLASH_PROGRAM = 0x4e86
_FLASH_ERASE = 0x4ef4


def _load(c, pointer, register):
    # L Rn,8:[ERpointer]; the flash data window is physical segment 8.
    c.db(8, 0xe3, pointer, 0x90 | register)


def _mov_pair(c, dest, source):
    c.db((source << 4) | 5, 0xf0 | dest)


def _result(c):
    c.raw("8e f2")  # POP PC; BL's link register was saved on entry.

def _must(c, label):
    c.raw("05 f0")  # MOV ER0,ER0 sets Z from the ROM/helper result
    c.branch("eq", label)
    c.jump("fail")
    c.label(label)



def journal_code():
    """Return nonoverlapping (physical S0 offset, machine-code bytes) spans."""
    c = Code(COMMIT_ADDRESS)
    c.raw("ce f8 6e f4 6e f8 5e fc 5e fe")  # LR, XR4, XR8, ER12, ER14
    _mov_pair(c, 14, 0)  # page
    _mov_pair(c, 12, 2)  # staged RAM
    c.raw("1f 20")  # AND R0,1f; reject unaligned pages
    c.branch("ne", "fail_near")
    c.raw("40 71")  # CMP R1,40
    c.branch("lt", "fail_near")
    c.raw("5f 71")
    c.branch("lt", "page_ok")
    c.branch("ne", "fail_near")
    c.raw("e0 80")  # MOV R0,R14; alignment test consumed the input low byte
    c.raw("f0 70")  # 5ff0 is metadata, not program data
    c.branch("lt", "page_ok")
    c.label("fail_near")
    c.jump("fail")
    c.label("page_ok")
    c.call(BACKUP_ADDRESS)
    _must(c, "backup_ready")

    # Copy all bytes before the edited page from the verified S2 image.
    _mov_pair(c, 6, 14)
    c.raw("c0 17")  # high byte -= 0x40
    c.mov_er(4, 0x6000)
    c.mov_er(0, 0x4000)
    c.call(_PROGRAM)
    _must(c, "prefix_written")
    _mov_pair(c, 0, 14)
    _mov_pair(c, 4, 12)
    c.mov_er(6, 32)
    c.mov_er(2, 0x5fe0)
    c.raw("27 f0")
    c.branch("ne", "full_page")
    c.mov_er(6, 16)
    c.label("full_page")
    c.call(PROGRAM_RAM_ADDRESS)
    _must(c, "page_written")
    # Copy the remainder from S2, stopping before the metadata.
    _mov_pair(c, 4, 14)
    c.mov_er(2, 0x5fe0)
    c.raw("27 f4")
    c.branch("ne", "full_suffix")
    c.raw("90 e4")  # source = page + 16
    c.mov_er(6, 0x5ff0)
    c.raw("e8 86 f9 87 f0 e6")  # count = data end - page - 16
    _mov_pair(c, 0, 14)
    c.raw("90 e0")
    c.branch("al", "write_suffix")
    c.label("full_suffix")
    c.raw("a0 e4")  # source = page + 32
    c.mov_er(6, 0x5ff0)
    c.raw("e8 86 f9 87 e0 e6")  # count = data end - page - 32
    _mov_pair(c, 0, 14)
    c.raw("a0 e0")
    c.label("write_suffix")
    c.raw("20 15")  # source high byte += 0x20
    c.call(_PROGRAM)
    _must(c, "suffix_written")

    # Compare three regions without loading the sector into internal RAM.
    c.mov_er(0, 0x4000)
    c.mov_er(2, 0x6000)
    _mov_pair(c, 4, 14)
    c.raw("c0 15")  # count high -= 0x40
    c.call(_COMPARE)
    _must(c, "prefix_compared")
    _mov_pair(c, 0, 14)
    _mov_pair(c, 2, 12)
    c.mov_er(4, 32)
    c.mov_er(6, 0x5fe0)
    c.raw("67 f0")
    c.branch("ne", "full_compare")
    c.mov_er(4, 16)
    c.label("full_compare")
    c.call(_COMPARE_RAM)
    _must(c, "page_compared")
    _mov_pair(c, 0, 14)
    c.mov_er(2, 0x5fe0)
    c.raw("27 f0")
    c.branch("ne", "full_compare_suffix")
    c.raw("90 e0")
    c.branch("al", "compare_suffix")
    c.label("full_compare_suffix")
    c.raw("a0 e0")
    c.label("compare_suffix")
    _mov_pair(c, 2, 0)
    c.raw("20 13")
    c.mov_er(4, 0x5ff0)
    c.raw("08 84 19 85")  # SUB R4,R0; SUBC R5,R1: count = 0x5ff0 - page end
    c.call(_COMPARE)
    _must(c, "suffix_compared")
    c.mov_er(0, 0x4000)
    c.mov_er(2, 0x1ff0)
    c.call(_CRC)
    c.call(FINISH_ADDRESS)
    _must(c, "s1_checked")
    c.mov_er(0, 0)
    c.jump("done")
    c.label("fail")
    c.mov_er(0, 0xffff)
    c.label("done")
    c.raw("1e fe 1e fc 2e f8 2e f4")
    _result(c)
    commit = c.build()

    c = Code(RECOVER_ADDRESS)
    c.raw("ce f8 6e f4 6e f8 5e fc 5e fe")
    c.mov_er(0, 0x4000)
    c.call(_CHECK)
    c.raw("05 f0")
    c.branch("eq", "good")
    c.mov_er(0, 0x6000)
    c.call(_CHECK)
    c.raw("05 f0")
    c.branch("eq", "restore")
    c.mov_er(0, 0x4000)
    c.mov_er(2, 0x2000)
    c.call(_ERASED)  # a virgin erased S1 needs no marker
    c.raw("05 f0")
    c.branch("eq", "good")
    c.jump("bad")
    c.label("restore")
    # Retain the backup checksum across ROM erase/program calls.
    c.mov_er(0, 0x6000)
    c.mov_er(2, 0x1ff0)
    c.call(_CRC)
    _mov_pair(c, 12, 0)
    c.mov(0, 1)
    c.call(_FLASH_ERASE)
    c.raw("05 f0")
    c.branch("ne", "bad")
    c.mov_er(0, 0x4000)
    c.mov_er(4, 0x6000)
    c.mov_er(6, 0x1ff0)
    c.call(_PROGRAM)
    c.raw("05 f0")
    c.branch("ne", "bad")
    c.mov_er(0, 0x4000)
    c.mov_er(2, 0x6000)
    c.mov_er(4, 0x1ff0)
    c.call(_COMPARE)
    c.raw("05 f0")
    c.branch("ne", "bad")
    c.mov_er(0, 0x5ff0)
    _mov_pair(c, 2, 12)
    c.call(_META)
    c.raw("05 f0")
    c.branch("ne", "bad")
    c.mov_er(0, 0x4000)
    c.call(_CHECK)
    c.raw("05 f0")
    c.branch("ne", "bad")
    c.label("good")
    c.mov_er(0, 0)
    c.branch("al", "out")
    c.label("bad")
    c.mov_er(0, 0xffff)
    c.label("out")
    c.raw("1e fe 1e fc 2e f8 2e f4")
    _result(c)
    recover = c.build()

    # CRC-CCITT, initial ffff, polynomial 1021, no reflection/xorout.
    # ER0 flash address, ER2 length -> ER0 CRC. ER4, ER6, ER8, R2 clobbered.
    c = Code(_CRC)
    _mov_pair(c, 4, 0)
    _mov_pair(c, 6, 2)
    c.mov_er(8, 0xffff)
    c.label("byte")
    _load(c, 0x40, 0)
    c.raw("04 89")  # XOR R9,R0 (CRC high byte)
    c.mov(2, 8)
    c.label("bit")
    c.raw("90 80 80 20")  # MOV R0,R9; AND R0,80
    c.raw("1b 99 1a 98 00 70")  # high reads old low, then shift low
    c.branch("eq", "no_poly")
    c.raw("21 48 10 49")  # XOR R8,21; XOR R9,10
    c.label("no_poly")
    c.raw("ff 12")
    c.branch("ne", "bit")
    c.raw("81 e4 ff e6")
    c.branch("ne", "byte")
    _mov_pair(c, 0, 8)
    c.raw("1f fe")  # RT (no nested BL)
    crc = c.build()

    # Compare ER0 flash with ER2 flash (or RAM), ER4 byte count.
    compares = []
    for address, ram in ((_COMPARE, False), (_COMPARE_RAM, True)):
        c = Code(address)
        _mov_pair(c, 6, 0)
        _mov_pair(c, 8, 2)
        _mov_pair(c, 10, 4)
        c.label("loop")
        c.raw("a5 fa")
        c.branch("eq", "equal")
        _load(c, 0x60, 0)
        if ram:
            c.raw("80 91")  # L R1,[ER8], segment zero
        else:
            _load(c, 0x80, 1)
        c.raw("17 80")  # CMP R0,R1
        c.branch("ne", "different")
        c.raw("81 e6 81 e8 ff ea")
        c.branch("al", "loop")
        c.label("equal")
        c.mov_er(0, 0)
        c.raw("1f fe")
        c.label("different")
        c.mov_er(0, 0xffff)
        c.raw("1f fe")
        compares.append(c.build())
    compare, compare_ram = compares

    # Validate completion marker, CRC/complement, and entire data range.
    c = Code(_CHECK)
    c.raw("ce f8 5e fc 5e fe 5e f4")
    _mov_pair(c, 12, 0)
    c.mov_er(2, 0x1ff0)
    c.call(_CRC)
    _mov_pair(c, 14, 0)
    _mov_pair(c, 4, 12)
    c.raw("f0 14 1f 65")  # meta offset = data offset + 1ff0
    for expected in (14, 15):
        _load(c, 0x40, 0)
        c.db((expected << 4) | 7, 0x80)  # CMP R0,R14/R15
        c.branch("ne", "bad")
        c.raw("81 e4")
    for expected in (14, 15):
        _load(c, 0x40, 0)
        c.raw("ff 40")
        c.db((expected << 4) | 7, 0x80)
        c.branch("ne", "bad")
        c.raw("81 e4")
    for value in (0x4a, 0xb6):
        _load(c, 0x40, 0)
        c.db(value, 0x70)
        c.branch("ne", "bad")
        c.raw("81 e4")
    c.mov_er(0, 0)
    c.branch("al", "out")
    c.label("bad")
    c.mov_er(0, 0xffff)
    c.label("out")
    c.raw("1e f4 1e fe 1e fc")
    _result(c)
    check = c.build()

    c = Code(_ERASED)
    _mov_pair(c, 4, 0)
    _mov_pair(c, 6, 2)
    c.label("loop")
    _load(c, 0x40, 0)
    c.raw("ff 70")
    c.branch("ne", "bad")
    c.raw("81 e4 ff e6")
    c.branch("ne", "loop")
    c.mov_er(0, 0)
    c.raw("1f fe")
    c.label("bad")
    c.mov_er(0, 0xffff)
    c.raw("1f fe")
    erased = c.build()

    # Flash is not readable while the NOR program command is in progress.
    # Copy ER6 bytes from flash ER4 to flash ER0 in RAM-staged 16-byte
    # chunks. A segment-8 source passed directly to ROM 0:4e86 would be
    # fetched only after its AMD unlock and A0 program-setup commands.
    c = Code(_PROGRAM)
    c.raw("ce f8 6e f4 6e f8 5e fc 5e fe f0 e1")
    _mov_pair(c, 8, 0)  # destination
    _mov_pair(c, 10, 4)  # flash source
    _mov_pair(c, 12, 6)  # bytes left
    c.raw("1a ae")  # scratch address = SP
    c.label("chunk")
    c.raw("c5 fc")
    c.branch("eq", "done")
    _mov_pair(c, 0, 12)
    c.mov_er(2, 16)
    c.raw("27 f0")  # CMP ER0,ER2
    c.branch("lt", "short")
    c.mov_er(6, 16)
    c.branch("al", "copy")
    c.label("short")
    _mov_pair(c, 6, 12)
    c.label("copy")
    _mov_pair(c, 0, 14)  # RAM write pointer
    c.raw("60 83")  # MOV R3,R6; count <=16
    c.label("copy_byte")
    _load(c, 0xa0, 2)  # L R2,8:[ER10]
    c.raw("01 92")  # ST R2,[ER0] in internal RAM
    c.raw("81 ea 81 e0 ff 13")
    c.branch("ne", "copy_byte")
    _mov_pair(c, 0, 8)
    _mov_pair(c, 4, 14)
    c.raw("5e f6")  # keep the chunk length across the ROM writer
    c.call(PROGRAM_RAM_ADDRESS)
    c.raw("1e f6 05 f0")
    c.branch("ne", "bad")
    c.raw("66 f8")  # ADD ER8,ER6
    c.raw("68 8c 79 8d")  # SUB R12,R6; SUBC R13,R7
    c.branch("al", "chunk")
    c.label("done")
    c.mov_er(0, 0)
    c.branch("al", "out")
    c.label("bad")
    c.mov_er(0, 0xffff)
    c.label("out")
    c.raw("10 e1 1e fe 1e fc 2e f8 2e f4")
    _result(c)
    program = c.build()

    # Same ROM interface with a segment-zero RAM source.
    c = Code(PROGRAM_RAM_ADDRESS)
    c.raw("ce f8 6e f4 7e f8 5e f6")  # LR, XR4, QR8, count
    c.mov(8, 0)
    c.raw("4e f8 5e f4")
    c.mov_er(2, 8)
    c.call(_FLASH_PROGRAM)
    c.raw("06 e1 3e f8 2e f4")
    _result(c)
    program_ram = c.build()

    # ER0 metadata destination, ER2 CRC. CRC/complement are programmed
    # first; the 4a b6 marker is a separate final flash operation.
    c = Code(_META)
    c.raw("ce f8 5e fc 5e f6")
    _mov_pair(c, 12, 0)
    _mov_pair(c, 0, 2)
    c.raw("ff 40 ff 41 5e f0 5e f2")
    c.raw("1a a4")  # [SP] = CRC, [SP+2] = complement
    c.mov_er(6, 4)
    _mov_pair(c, 0, 12)
    c.call(PROGRAM_RAM_ADDRESS)
    c.raw("04 e1 05 f0")
    c.branch("ne", "bad")
    c.mov_er(0, 0xb64a)
    c.raw("5e f0 1a a4")
    c.mov_er(6, 2)
    _mov_pair(c, 0, 12)
    c.raw("84 e0")  # add 4 to destination
    c.call(PROGRAM_RAM_ADDRESS)
    c.raw("02 e1 05 f0")
    c.branch("ne", "bad")
    c.mov_er(0, 0)
    c.branch("al", "out")
    c.label("bad")
    c.mov_er(0, 0xffff)
    c.label("out")
    c.raw("1e f6 1e fc")
    _result(c)
    meta = c.build()

    # Split transaction entry for sector-wide transforms. S2 is complete
    # and self-validating when control returns with S1 erased.
    c = Code(BACKUP_ADDRESS)
    c.raw("ce f8 6e f4 6e f8 5e fc 5e fe")
    c.call(RECOVER_ADDRESS)
    c.raw("05 f0")
    c.branch("ne", "bad")
    c.mov(0, 2)  # ROM erase table: 2 -> 8:6000
    c.call(_FLASH_ERASE)
    c.raw("05 f0")
    c.branch("ne", "bad")
    c.mov_er(0, 0x6000)
    c.mov_er(4, 0x4000)
    c.mov_er(6, 0x1ff0)
    c.call(_PROGRAM)
    c.raw("05 f0")
    c.branch("ne", "bad")
    c.mov_er(0, 0x4000)
    c.mov_er(2, 0x6000)
    c.mov_er(4, 0x1ff0)
    c.call(_COMPARE)
    c.raw("05 f0")
    c.branch("ne", "bad")
    c.mov_er(0, 0x6000)
    c.mov_er(2, 0x1ff0)
    c.call(_CRC)
    _mov_pair(c, 2, 0)
    c.mov_er(0, 0x7ff0)
    c.call(_META)
    c.raw("05 f0")
    c.branch("ne", "bad")
    c.mov_er(0, 0x6000)
    c.call(_CHECK)
    c.raw("05 f0")
    c.branch("ne", "bad")
    c.mov(0, 1)  # ROM erase table: 1 -> 8:4000
    c.call(_FLASH_ERASE)
    c.raw("05 f0")
    c.branch("ne", "bad")
    c.mov_er(0, 0)
    c.branch("al", "out")
    c.label("bad")
    c.mov_er(0, 0xffff)
    c.label("out")
    c.raw("1e fe 1e fc 2e f8 2e f4")
    _result(c)
    backup = c.build()

    # ER0 is the caller's CRC of the intended 8176-byte result. A
    # transformer must have verified the rewritten flash against its
    # intended bytes before requesting this completion marker.
    c = Code(FINISH_ADDRESS)
    c.raw("ce f8 6e f4 6e f8 5e fc 5e fe")
    _mov_pair(c, 12, 0)
    c.mov_er(0, 0x6000)
    c.call(_CHECK)
    c.raw("05 f0")
    c.branch("ne", "bad")
    c.mov_er(0, 0x4000)
    c.mov_er(2, 0x1ff0)
    c.call(_CRC)
    c.raw("c7 f0")  # CMP ER0,ER12
    c.branch("ne", "bad")
    _mov_pair(c, 2, 12)
    c.mov_er(0, 0x5ff0)
    c.call(_META)
    c.raw("05 f0")
    c.branch("ne", "bad")
    c.mov_er(0, 0x4000)
    c.call(_CHECK)
    c.raw("05 f0")
    c.branch("ne", "bad")
    c.mov_er(0, 0)
    c.branch("al", "out")
    c.label("bad")
    c.mov_er(0, 0xffff)
    c.label("out")
    c.raw("1e fe 1e fc 2e f8 2e f4")
    _result(c)
    finish = c.build()

    # ER0 running CRC, R2 next byte -> ER0 updated CRC. Initialize ER0
    # to ffff; R2/R3 are scratch, XR4 and R8..R15 remain unchanged.
    c = Code(CRC_UPDATE_ADDRESS)
    c.raw("24 81")  # XOR R1,R2
    c.mov(3, 8)
    c.label("bit")
    c.raw("10 82 80 22")  # MOV R2,R1; AND R2,80
    c.raw("1b 91 1a 90")  # high reads old low, then shift low
    c.raw("00 72")  # CMP R2,0
    c.branch("eq", "next")
    c.raw("21 40 10 41")
    c.label("next")
    c.raw("ff 13")
    c.branch("ne", "bit")
    c.raw("1f fe")
    crc_update = c.build()

    return ((0x3000, commit), (RECOVER_ADDRESS & 0xffff, recover),
            (_CRC & 0xffff, crc), (_COMPARE & 0xffff, compare),
            (_CHECK & 0xffff, check), (_ERASED & 0xffff, erased),
            (_PROGRAM & 0xffff, program), (PROGRAM_RAM_ADDRESS & 0xffff, program_ram),
            (_META & 0xffff, meta), (_COMPARE_RAM & 0xffff, compare_ram),
            (BACKUP_ADDRESS & 0xffff, backup), (FINISH_ADDRESS & 0xffff, finish),
            (CRC_UPDATE_ADDRESS & 0xffff, crc_update))


_COMPARE_RAM = 0x83c40
