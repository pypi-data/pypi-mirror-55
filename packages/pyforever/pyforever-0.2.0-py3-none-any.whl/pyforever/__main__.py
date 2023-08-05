#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import os
import subprocess
import sys

import watchgod

from . import watchers


def _run(args, clear=True):
    """
    Run the executable
    :param args: The full path and arguments to be run
    :param clear: Whether to clear the console or not (default: True)
    """

    if clear:
        os.system("cls") if os.name == "nt" else os.system("clear")

    proc = subprocess.Popen(args)
    return proc


async def _watch(args, proc=None):
    """
    Run the executable on changes
    :param args: The full path and arguments to be run
    :param proc: A process object that might already be running
    """

    script_path = sys.argv[1]
    script_mode = os.path.isfile(script_path)

    # use root path of the script (or cwd as a fall-back)
    root_path = os.getcwd()
    if script_mode:
        script_path = os.path.abspath(script_path)
        root_path = os.path.dirname(script_path)

    # only watch the script (or the entire cwd as a fall-back)
    watcher = watchgod.watcher.DefaultWatcher
    kwargs = None
    if script_mode:
        watcher = watchers.FileWatcher
        kwargs = dict(filename=os.path.basename(script_path))

    print("Watching for changes in", script_path if script_mode else root_path, "...")
    print()

    # watch for changes
    async for _ in watchgod.awatch(root_path, watcher_cls=watcher, watcher_kwargs=kwargs):
        if proc is not None:
            proc.kill()
        proc = _run(args)


def main():
    if len(sys.argv) == 1:
        sys.stderr.write("No arguments supplied.\n")
        sys.stderr.flush()
        exit(1)

    args = [sys.executable] + sys.argv[1:]

    # run once and start watching then
    proc = _run(args, clear=False)
    asyncio.run(_watch(args, proc))


if __name__ == "__main__":
    main()
