"""Interrupt the legacy journal and explicitly recover after isolated cold restarts."""

import argparse
import binascii
import ctypes
import hashlib
import json
import subprocess
import time
import traceback
from pathlib import Path

from flash_layout import COMMIT_ADDRESS, RECOVER_ADDRESS
from basic_native import TOKENS
from basic_smoke import Emulator, pair, scalar_integer


FAULTS = (
    "before_s2_erase", "before_s1_erase", "after_s1_erase", "middle_data",
    "after_last_data", "before_marker", "after_marker",
)
WATCHES = {"middle_data": 0x85000, "after_last_data": 0x85fef,
           "before_marker": 0x85ff0, "after_marker": 0x85ff5}


def powershell(command, timeout=70):
    return subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command",
         "$ErrorActionPreference='Stop'; "
         "[Console]::OutputEncoding=[Text.UTF8Encoding]::new($false); " + command],
        check=True, capture_output=True, encoding="utf-8", timeout=timeout).stdout.strip()


def listeners():
    text = powershell(
        "$ids=@(Get-NetTCPConnection -State Listen | "
        "Where-Object {$_.LocalPort -eq 3001} | "
        "Select-Object -ExpandProperty OwningProcess -Unique); "
        "@($ids | ForEach-Object {Get-CimInstance Win32_Process -Filter "
        "('ProcessId='+$_) | Select-Object ProcessId,ExecutablePath,CommandLine,CreationDate}) "
        "| ConvertTo-Json -Compress")
    value = json.loads(text) if text else []
    return value if isinstance(value, list) else [value]


def command_args(command):
    shell = ctypes.WinDLL("shell32", use_last_error=True)
    shell.CommandLineToArgvW.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_int)]
    shell.CommandLineToArgvW.restype = ctypes.POINTER(ctypes.c_wchar_p)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.LocalFree.argtypes = [ctypes.c_void_p]
    kernel.LocalFree.restype = ctypes.c_void_p
    count = ctypes.c_int()
    result = shell.CommandLineToArgvW(command, ctypes.byref(count))
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        return [result[index] for index in range(count.value)]
    finally:
        kernel.LocalFree(result)


class OwnedProcess:
    def __init__(self, exe, model):
        self.exe = exe.resolve(strict=True)
        self.model = model.resolve(strict=True)
        self.owner = None
        self.child = None
        self.emu = None

    def validate(self, owner):
        args = command_args(owner["CommandLine"])
        if (Path(owner["ExecutablePath"]).resolve() != self.exe or len(args) != 2
                or Path(args[0]).resolve() != self.exe or Path(args[1]).resolve() != self.model):
            raise ValueError(("MCP executable/model ownership mismatch", owner))
        return owner

    def attach(self):
        owners = listeners()
        if len(owners) != 1:
            raise ValueError(("Expected one owned MCP listener", owners))
        self.owner = self.validate(owners[0])
        self.emu = Emulator(self.model)
        return self.emu

    def start(self):
        if self.owner is not None or listeners():
            raise ValueError("Refusing to launch over an existing MCP process")
        self.child = subprocess.Popen([str(self.exe), str(self.model)], cwd=self.exe.parent)
        # Record the child before connecting so a failed handshake can still close it safely.
        text = powershell(
            f"Get-CimInstance Win32_Process -Filter 'ProcessId={self.child.pid}' | "
            "Select-Object ProcessId,ExecutablePath,CommandLine,CreationDate | ConvertTo-Json -Compress")
        if not text:
            raise RuntimeError("Emulator exited during startup")
        self.owner = self.validate(json.loads(text))
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            if self.child.poll() is not None:
                raise RuntimeError(("Emulator exited during startup", self.child.returncode))
            owners = listeners()
            if owners:
                if len(owners) != 1 or self.validate(owners[0]) != self.owner:
                    raise ValueError(("MCP listener is not the launched child", owners))
                self.emu = Emulator(self.model)
                self.emu.active()
                return self.emu
            time.sleep(0.2)
        raise TimeoutError("Owned emulator MCP did not become ready in 60 seconds")

    def close(self):
        if self.owner is None and self.child is not None:
            text = powershell(
                f"Get-CimInstance Win32_Process -Filter 'ProcessId={self.child.pid}' | "
                "Select-Object ProcessId,ExecutablePath,CommandLine,CreationDate | ConvertTo-Json -Compress")
            if text:
                self.owner = self.validate(json.loads(text))
            else:
                self.child.wait(timeout=5)
                self.child = None
        if self.owner is None:
            if listeners():
                raise ValueError("Cannot restore disk while an unowned MCP process is listening")
            return
        pid = int(self.owner["ProcessId"])
        text = powershell(
            f"Get-CimInstance Win32_Process -Filter 'ProcessId={pid}' | "
            "Select-Object ProcessId,ExecutablePath,CommandLine,CreationDate | ConvertTo-Json -Compress")
        if text:
            actual = self.validate(json.loads(text))
            if actual != self.owner:
                raise ValueError(("Owned process identity changed", actual))
            if self.emu is not None:
                self.emu.call("pause")
                image = b"".join(self.emu.memory(0x80000 + offset, 0x8000)
                                 for offset in range(0, 0x80000, 0x8000))
                # The emulator's ten-second timer persists NOR independently of CPU execution.
                deadline = time.monotonic() + 30
                while True:
                    try:
                        persisted = self.model.joinpath("flash.dmp").read_bytes()
                    except FileNotFoundError:
                        persisted = b""
                    if persisted == image:
                        break
                    if time.monotonic() >= deadline:
                        raise TimeoutError("Paused NOR image was not saved by the emulator")
                    time.sleep(0.1)
                assert self.emu.call("get_status")["paused"], "CPU resumed during persistence"
            powershell(
                f"$p=Get-Process -Id {pid}; "
                "if (-not $p.CloseMainWindow()) {throw 'CloseMainWindow failed'}; "
                "if (-not $p.WaitForExit(60000)) {throw 'Owned emulator did not exit'}")
        if self.emu is not None:
            self.emu.session.close()
        if self.child is not None:
            self.child.wait(timeout=5)
        self.owner = self.child = self.emu = None
        if listeners():
            raise ValueError("MCP is still listening after owned emulator exit")


def save_json(path, value):
    path.write_text(json.dumps(value, indent=2), encoding="utf-8")


def wait_paused(emu, address=None):
    deadline = time.monotonic() + 60
    while True:
        status = emu.call("get_status")
        if status["paused"]:
            registers = emu.registers()
            if status["run_status"] != 2 or (address is not None and status["program_counter"] != address):
                raise AssertionError(("Unexpected CPU stop", address, status, registers))
            return {"status": status, "registers": registers}
        if time.monotonic() >= deadline:
            emu.call("pause")
            raise TimeoutError(("CPU did not pause in 60 seconds", address, status, emu.registers()))
        time.sleep(0.05)


def er(registers, index):
    return registers[f"r{index}"] | registers[f"r{index + 1}"] << 8


def stop_transaction(emu, fault, payload):
    emu.active()
    snapshot = emu.call("save_snapshot", label="Before legacy journal power fault")["id"]
    emu.call("clear_execution_breakpoints")
    emu.call("clear_memory_breakpoints")
    page = emu.memory(0x84100, 1) + payload
    emu.call("write_memory", address=0x8800, bytes=list(page))
    registers = {"sp": 0x8c00, "psw": 0, "lr": 0}
    registers.update(pair(0, 0x4100) | pair(2, 0x8800))
    for name, value in registers.items():
        emu.call("write_register", name=name, value=value)
    emu.call("write_register", name="pc", value=COMMIT_ADDRESS)
    emu.call("add_execution_breakpoint", address=0)
    emu.call("add_execution_breakpoint", address=0x4ef4)
    emu.call("resume")
    stops = [wait_paused(emu, 0x4ef4)]
    assert stops[-1]["registers"]["r0"] == 2, stops[-1]
    if fault != "before_s2_erase":
        emu.call("step_into")
        wait_paused(emu, 0x4ef6)
        emu.call("add_execution_breakpoint", address=0x4ef4)
        emu.call("resume")
        stops.append(wait_paused(emu, 0x4ef4))
        assert stops[-1]["registers"]["r0"] == 1, stops[-1]
        if fault != "before_s1_erase":
            emu.call("clear_execution_breakpoints")
            emu.call("add_execution_breakpoint", address=0)
            if fault == "after_s1_erase":
                emu.call("add_execution_breakpoint", address=0x4e86)
            else:
                emu.call("add_memory_breakpoint", address=WATCHES[fault], write=True,
                         enabled=True, break_when_hit=True)
            emu.call("step_into")
            wait_paused(emu, 0x4ef6)
            emu.call("resume")
            stops.append(wait_paused(emu, 0x4e86 if fault == "after_s1_erase" else None))
            registers = stops[-1]["registers"]
            if fault == "after_s1_erase":
                assert er(registers, 0) == 0x4000 and er(registers, 2) == 8, stops[-1]
            else:
                # ROM 004eba writes R2 to R6:[ER4]; the watch fires on that byte store.
                assert registers["r6"] == 8 and er(registers, 4) == WATCHES[fault] & 0xffff, stops[-1]
                assert stops[-1]["status"]["program_counter"] in (0x4eba, 0x4ebe), stops[-1]
    assert emu.memory(0x8800, 32) == page, "Legacy journal page changed during commit"
    return {"fault": fault, "snapshot": snapshot, "watch_address": WATCHES.get(fault), "stops": stops}


def disk_image(model):
    data = model.joinpath("flash.dmp").read_bytes()
    if len(data) != 524288:
        raise ValueError(("Unexpected persisted Flash size", len(data)))
    return data


def image_evidence(data):
    return {"sha256": hashlib.sha256(data).hexdigest(),
            "s1_metadata": data[0x5ff0:0x6000].hex(),
            "s2_metadata": data[0x7ff0:0x8000].hex(),
            "s1_payload_sha256": hashlib.sha256(data[0x4000:0x5ff0]).hexdigest(),
            "s2_payload_sha256": hashlib.sha256(data[0x6000:0x7ff0]).hexdigest()}


def valid_sector(data, start):
    crc = binascii.crc_hqx(data[start:start + 8176], 0xffff)
    meta = data[start + 8176:start + 8192]
    return (meta[:2] == crc.to_bytes(2, "little")
            and meta[2:4] == (crc ^ 0xffff).to_bytes(2, "little")
            and meta[4:6] == b"\x4a\xb6")


def unchanged_native(data, baseline):
    assert data[:0x4000] == baseline[:0x4000], "Non-journal S0 bytes changed"
    assert data[0x8000:] == baseline[0x8000:], "Non-S1/S2 Flash changed (including native S5/S6)"


def check_fault(fault, data, baseline, old, new):
    unchanged_native(data, baseline)
    s1 = data[0x4000:0x5ff0]
    marker = data[0x5ff4:0x5ff6]
    if fault == "before_s2_erase":
        assert s1 == old and valid_sector(data, 0x4000), "S1 changed before backup"
    else:
        assert valid_sector(data, 0x6000), "Backup is not CRC/marker-valid"
        assert data[0x6000:0x7ff0] == old, "Backup does not preserve old S1"
        if fault == "before_s1_erase":
            assert s1 == old and valid_sector(data, 0x4000), "S1 changed before erase"
        elif fault == "after_s1_erase":
            assert data[0x4000:0x6000] == b"\xff" * 8192, "S1 was not fully erased"
        elif fault == "middle_data":
            assert s1[:0x1001] == new[:0x1001] and s1[0x1001:] == b"\xff" * (8176 - 0x1001), "Wrong partial data boundary"
            assert data[0x5ff0:0x6000] == b"\xff" * 16, "Metadata written before data ended"
        else:
            assert s1 == new, "Completed data does not match requested replacement"
            if fault == "after_last_data":
                assert data[0x5ff0:0x6000] == b"\xff" * 16, "Metadata written before last-data stop"
            elif fault == "before_marker":
                assert marker == b"\xff\xff", "Completion marker already written"
                assert data[0x5ff0] == binascii.crc_hqx(new, 0xffff) & 255, "CRC byte was not programmed"
            else:
                assert valid_sector(data, 0x4000), "Full completion marker/CRC missing"


def run(args):
    if args.out.resolve().is_relative_to(args.model.resolve()):
        raise ValueError("Evidence must be outside the validation model")
    args.out.mkdir(parents=True, exist_ok=False)
    process = OwnedProcess(args.exe, args.model)
    baseline = None
    original_flash = None
    original_bin = args.model.joinpath("flash.bin").read_bytes()
    results = []
    failed = True
    try:
        emu = process.attach()
        emu.active()
        files = emu.records()
        save_json(args.out / "native-files.json", files)
        original_flash = b"".join(emu.memory(0x80000 + offset, 32768)
                                   for offset in range(0, 524288, 32768))
        (args.out / "original-flash.dmp").write_bytes(original_flash)
        # Establish a valid legacy journal independently of any installed raw code.
        emu.erase_flash(1)
        emu.erase_flash(2)
        payload = bytes.fromhex("2a0000011ffe") + original_flash[0x4006:0x4020]
        registers, _ = emu.invoke(COMMIT_ADDRESS, pair(0, 0x4000) | pair(2, 0x8800),
                                  [(0x8800, payload)], seconds=60)
        assert er(registers, 0) == 0, "Failed to initialize the legacy journal fixture"
        process.close()
        baseline = disk_image(args.model)
        (args.out / "baseline-flash.dmp").write_bytes(baseline)
        save_json(args.out / "baseline.json", image_evidence(baseline))
        old = baseline[0x4000:0x5ff0]
        assert old[:6] == bytes.fromhex("2a0000011ffe"), "S1 CALL(540672) must return 42"
        assert valid_sector(baseline, 0x4000), "Initial S1 must be committed"
        original = old[0x101:0x120]
        payload = bytes(value ^ 0x5a for value in original)
        new = old[:0x101] + payload + old[0x120:]
        emu = process.start()
        assert emu.records() == files, "Initial cold boot changed native records/header/source"
        for fault in FAULTS:
            out = args.out / fault
            out.mkdir()
            assert emu.records() == files, "Native files changed before fault injection"
            assert emu.memory(0x84000, 8176) == old, "Previous case did not restore S1"
            record = stop_transaction(emu, fault, payload)
            save_json(out / "paused.json", record)
            # Close while paused: do not execute native OFF or restore the CPU snapshot.
            process.close()
            interrupted = disk_image(args.model)
            (out / "fault-flash.dmp").write_bytes(interrupted)
            record["fault_image"] = image_evidence(interrupted)
            save_json(out / "paused.json", record)
            check_fault(fault, interrupted, baseline, old, new)

            emu = process.start()
            assert emu.records() == files, "Cold restart changed native records/header/source"
            registers, _ = emu.invoke(RECOVER_ADDRESS, {}, seconds=60)
            assert er(registers, 0) == 0, "Explicit legacy journal recovery failed"
            recovery_registers = registers
            source = TOKENS["CALL"].to_bytes(2, "big") + b"(540672)"
            registers, data = emu.evaluate(source, seconds=60)
            recovery = {"registers": registers, "number": data[0].hex(), "cursor": data[1].hex(),
                        "recovery_registers": recovery_registers,
                        "files": emu.records(), "status": emu.call("get_status")}
            save_json(out / "recovered.json", recovery)
            assert registers["r0"] == 1 and data[0] == scalar_integer(42), "CALL after explicit recovery did not return 42"
            assert registers["sp"] == 0x8c00, "Native CALL left an unbalanced stack"
            assert recovery["files"] == files, "Recovery changed native records/header/source"
            expected = new if fault == "after_marker" else old
            assert emu.memory(0x84000, 8176) == expected, "Recovery selected the wrong S1 image"
            process.close()
            recovered = disk_image(args.model)
            (out / "recovered-flash.dmp").write_bytes(recovered)
            recovery["image"] = image_evidence(recovered)
            save_json(out / "recovered.json", recovery)
            unchanged_native(recovered, baseline)
            assert recovered[0x4000:0x5ff0] == expected and valid_sector(recovered, 0x4000), "Persisted recovered S1 differs"

            emu = process.start()
            registers, restored = emu.invoke(
                COMMIT_ADDRESS, pair(0, 0x4100) | pair(2, 0x8800),
                [(0x8800, old[0x100:0x101] + original)], [(0x84000, 8176)], seconds=60)
            status = er(registers, 0)
            assert status == 0 and restored[0] == old, "Legacy COMMIT did not restore the 31-byte fixture"
            assert emu.records() == files, "Restoring fixture changed native records/header/source"
            save_json(out / "restored.json", {"status": status, "registers": registers,
                                              "s1_payload_sha256": hashlib.sha256(restored[0]).hexdigest()})
            results.append({"fault": fault, "passed": True, "recovered": "new" if expected == new else "old"})
            save_json(args.out / "cases.json", results)
        failed = False
    except BaseException:
        save_json(args.out / "failure.json", {"traceback": traceback.format_exc(), "completed": results})
        raise
    finally:
        # Never replace a live emulator's backing file. A close failure leaves its data intact.
        try:
            process.close()
            if original_flash is not None:
                final = disk_image(args.model)
                (args.out / ("failure-flash.dmp" if failed else "final-flash.dmp")).write_bytes(final)
                args.model.joinpath("flash.bin").write_bytes(original_bin)
                args.model.joinpath("flash.dmp").write_bytes(original_flash)
                save_json(args.out / "cleanup.json", {"restored_sha256": hashlib.sha256(original_flash).hexdigest(),
                                                        "mcp_closed": True})
        except BaseException:
            save_json(args.out / "cleanup-failure.json", {"traceback": traceback.format_exc()})
            raise
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--exe", type=Path, required=True)
    args = parser.parse_args()
    results = run(args)
    print(json.dumps({"passed": len(results), "out": str(args.out), "mcp_closed": True}))


if __name__ == "__main__":
    main()
