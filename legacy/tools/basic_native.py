"""Native fx-5800P BASIC interfaces for the verified ROM-A27 image."""

ROM_SHA256 = "9a190cb85d1c3c1f096dfabf0cd8393580beb59ae603e56871f76b721ce7de75"
FLASH_SIZE = 0x80000
STACK_LOW = 0x8292
NATIVE_STACK_MARGIN = 900
MATH_ADDRESS = 0x8000
MATH_SIZE = 0x70
WORKSPACE_POINTER = 0x8086
FONT_STATE = 0x80a0
VARIABLE_A = 0x47086
VARIABLE_ANS = 0x4728e
NUMBER_SIZE = 20

# Six native prefixes; prefixed tokens are stored high byte first.
PREFIXES = (0x7f, 0xe5, 0xe6, 0xe7, 0xf7, 0xf9)
BOUNDARIES = (0, 0x0c, 0x0d, 0x3a)
TOKEN_BASE = 0xf9e0
TOKEN_NAMES = (
    "PEEK", "PEEK16", "POKE", "POKE16", "CALL", "BAND", "BOR", "BXOR",
    "SHL", "SHR", "INKEY", "TICKS", "POINT", "COPY", "FILL", "FLASHWRITE",
    "CLS", "PSET", "LINE", "RECT", "BLIT", "TEXT", "REFRESH", "ASM", "ENDASM",
)
TOKENS = {name: TOKEN_BASE + i for i, name in enumerate(TOKEN_NAMES)}
FUNCTIONS = frozenset(("PEEK", "PEEK16", "CALL", "BAND", "BOR", "BXOR",
                       "SHL", "SHR", "INKEY", "TICKS", "POINT"))
NX_CATEGORIES = (
    ("MEM", ("PEEK", "PEEK16", "POKE", "POKE16", "COPY", "FILL", "FLASHWRITE")),
    ("ASM", ("CALL", "ASM", "ENDASM")),
    ("GFX", ("CLS", "PSET", "POINT", "LINE", "RECT", "BLIT", "TEXT", "REFRESH")),
    ("TOOLS", ("BAND", "BOR", "BXOR", "SHL", "SHR", "INKEY", "TICKS")),
)

# C7B6E: ER0/R2 points to a mutable three-byte source cursor. R3 requests
# the initial fetch. Caller stack: cache offset/bank, result offset/bank,
# mode, each in a two-byte slot. R0 alone is success (1) or failure (0).
EVALUATE = 0xc7b6e
EVALUATE_WORKSPACE = 0xc7c12
EVALUATE_CORE = 0xc701e
EVALUATE_ARGS = {"cache": 0, "cache_bank": 2, "result": 4,
                 "result_bank": 6, "mode": 8}
EVALUATE_ARG_SIZE = 10
# Native argument boundary: operator 95 is recognized at C68F2..C691C,
# leaving ')' cached. C354C stores the first operator at stack+2, count at+0.
# Preseed it explicitly: native flag0010 also enables speculative recovery
# (C7404..C7476), which restores the last operand after a failed reduction.
# That recovery must not turn argument arithmetic errors into valid values.
# Retain C7B6E's normal value permissions and error propagation.
EVALUATE_ARGUMENT_FLAGS = 0x0f00
EVALUATE_ARGUMENT_SENTINEL = 0x95
# PUSH LR saves four bytes; PUSH ER14 adds two before establishing FP.
FRAME_ARGS = 6
EVALUATE_FRAME_SIZE = 168
CORE_FRAME_SIZE = 66
WORKSPACE_FRAME_SIZE = 328

TOKEN_FETCH = 0xc3794
TOKEN_DECODE = 0x10b7e
TOKEN_ADMISSION = 0xc30d8
NUMBER_COPY = 0x19b72
ERROR_WRITE = 0xe8fba
STATEMENT = 0xcd664
STATEMENT_FINISH = 0xcdfba
SOURCE_OPEN = 0xe5c76
SOURCE_ACTIVATE = 0xe76c4
ROOT_ADDRESS = 0x47600
ROOT_SIZE = 0x36
ROOT_DEPTH = 0x80ab

PROGRAM_EDITOR = 0xc8626
PROGRAM_FUNCTION = 0xdf3fa
PROGRAM_LOOKUP = 0xe2f86
PROGRAM_CREATE = 0xe2e60
PROGRAM_INSERT = 0xe302e
PROGRAM_DELETE = 0xe322e
PROGRAM_SERIALIZE = 0xd5f20
PROGRAM_HEADER_SIZE = 6
LIBRARY_LOOKUP = 0xf0484

# F0484 writes a three-byte descriptor pointer through caller stack +6.
# F0582/F0584/F0586 store it; F05C6..F05E4 read these descriptor fields.
LIBRARY_ALLOCATION_OFFSET = 0x10
LIBRARY_PAYLOAD_OFFSET = 0x14
ROOT_NAME_OFFSET = 8  # E7856/E7858: name copied to active root +8.
ROOT_SOURCE_OFFSET = 0  # E7882/E7886: current activation's source.
EDITOR_FRAME = {"caret": -42, "token": -36, "source": -32,
                "name": -68, "length": -72, "payload": -76,
                "allocation": -80, "content_length": -82}

# Byte signatures guard the actual Flash seams; ordinary paths replay
# displaced instructions and retain native continuation/error behavior.
HOOKS = {
    "admission_first": (0xc70ec, bytes.fromhex("01 fc d8 30")),
    "admission_next": (0xc75f2, bytes.fromhex("01 fc d8 30")),
    "function": (0xc71fe, bytes.fromhex("5b 70 00 51")),
    "statement": (0xcd696, bytes.fromhex("85 f0 a0 82")),
    "program_function": (0xc8936, bytes.fromhex("01 fd fa f3")),
    "program_input": (0xc884e, bytes.fromhex("25 f2 22 c9")),
    "program_menu_key": (0xdf550, bytes.fromhex("01 f1 fc 25")),
    "spelling": (0xdfc02, bytes.fromhex("ce f8 5e fc")),
    "if_false": (0xe5fce, bytes.fromhex("46 bc 48 d0")),
    "else_skip": (0xe6060, bytes.fromhex("46 bc 48 d0")),
    "for_skip": (0xe662c, bytes.fromhex("01 fe 42 5a")),
    "while_skip": (0xe6876, bytes.fromhex("01 fe 42 5a")),
    "break_skip": (0xe6bc4, bytes.fromhex("46 bc 48 d0")),
    "goto_skip": (0xe6f9c, bytes.fromhex("01 fe 42 5a")),
}

# Native C2774 checks these separators. Control-flow scanners own their
# cursor: Goto uses FP-4, while the other handlers use the execution cursor.
SCANNER_RETURNS = {
    "if_false": 0xe6000,
    "else_skip": 0xe6092,
    "for_skip": 0xe6630,
    "while_skip": 0xe687a,
    "break_skip": 0xe6bc2,
    "goto_skip": 0xe6fa0,
}
