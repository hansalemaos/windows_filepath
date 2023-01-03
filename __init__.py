import os
import tempfile
from functools import reduce

import regex
from flatten_everything import flatten_everything
from touchtouch import touch

forbiddennames = r"""(?:CON|PRN|AUX|NUL|COM0|COM1|COM2|COM3|COM4|COM5|COM6|COM7|COM8|COM9|LPT0|LPT1|LPT2|LPT3|LPT4|LPT5|LPT6|LPT7|LPT8|LPT9)"""
compregex = regex.compile(
    rf"(^.*?\\?)?\b{forbiddennames}\b(\.?[^\\]*$)?", flags=regex.I
)
forbiddenchars = [
    "<",
    ">",
    ":",
    '"',
    "/",
    "\\",
    "|",
    "?",
    "*",
]
allcontrols_s = (
    "\x00",
    "\x01",
    "\x02",
    "\x03",
    "\x04",
    "\x05",
    "\x06",
    "\x07",
    "\x08",
    "\x09",
    "\x0a",
    "\x0b",
    "\x0c",
    "\x0d",
    "\x0e",
    "\x0f",
    "\x10",
    "\x11",
    "\x12",
    "\x13",
    "\x14",
    "\x15",
    "\x16",
    "\x17",
    "\x18",
    "\x19",
    "\x1a",
    "\x1b",
    "\x1c",
    "\x1d",
    "\x1e",
    "\x1f",
)


def allow_long_path_windows():
    winr = r"""Windows Registry Editor Version 5.00
    [HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem]
    "LongPathsEnabled"=dword:00000001
    """
    tem = get_tmpfile(suffix=".reg")
    with open(tem, mode="w", encoding="utf-8") as f:
        f.write(winr)
    os.startfile(tem)


def get_tmpfile(suffix=".bin"):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = os.path.normpath(filename)
    tfp.close()
    touch(filename)
    return filename


def make_filepath_windows_comp(
    filepath,
    fillvalue="_",
    reduce_fillvalue=True,
    remove_backslash_and_col=False,
    spaceforbidden=True,
    other_to_replace=(";", ",", "[", "]", "`", "="),
    slash_to_backslash=True,
):
    if slash_to_backslash:
        filepath = filepath.replace("/", "\\")
    filepath = filepath.strip()
    filepath = reduce(lambda a, b: a.replace(b, fillvalue), allcontrols_s, filepath)
    if other_to_replace:
        filepath = reduce(
            lambda a, b: a.replace(b, fillvalue), other_to_replace, filepath
        )

    filepath = filepath.strip()
    if spaceforbidden:
        filepath = regex.sub(r"\s", fillvalue, filepath)
    for c in forbiddenchars:
        if not remove_backslash_and_col:
            if c == ":":
                filepath = filepath[:2] + filepath[2:].replace(c, fillvalue)
                continue
            if c == "\\":
                filepath = regex.sub(r"\\+", "\\\\", filepath)
                continue
        filepath = filepath.replace(c, fillvalue)
    filepath2 = "".join(
        [
            x if x != "" else "_"
            for x in (flatten_everything(compregex.findall(filepath)))
        ]
    )
    if filepath2 != "":
        filepath = filepath2
        regex.sub(r"\\+\.", r"\\_.", filepath)

    filepath = filepath.strip().strip("\\").strip().strip(".")
    filepath = regex.sub(r"\.+", r".", filepath)
    if reduce_fillvalue:
        filepath = regex.sub(rf"{fillvalue}+", rf"{fillvalue}", filepath)
        if len(filepath) > 1:
            filepath = filepath.strip(fillvalue)
    if len(filepath) == 0:
        filepath = fillvalue
    filepath = os.path.normpath(filepath)
    return filepath
