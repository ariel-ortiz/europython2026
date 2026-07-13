# File: chiqui_forth_rt.py
# Copyright (C) 2026 Ariel Ortiz
# SPDX-License-Identifier: GPL-3.0-or-later

""" The chiqui_forth runtime

To run, at the terminal type:

    python chiqui_forth_rt.py some_program.wasm
"""

from sys import argv, stderr, exit
from wasmtime import Engine, Store, Module, Linker, FuncType, ValType


def create_linker_and_store(engine):
    """Create a Linker and Store, and register the Python functions
    that will be callable from the WASM module.
    """
    store = Store(engine)
    linker = Linker(engine)

    #----------------------------------------------------------------
    # Functions to be imported from the WASM module.

    def _emit(x):
        print(chr(x), end='')

    def _input():
        try:
            return int(input())
        except ValueError:
            return 0

    def _print(x):
        print(x, end=' ')

    #----------------------------------------------------------------

    # Define the signatures and define them in the "forth" module
    linker.define_func("forth", "emit", FuncType([ValType.i32()], []), _emit)
    linker.define_func("forth", "input", FuncType([], [ValType.i32()]), _input)
    linker.define_func("forth", "print", FuncType([ValType.i32()], []), _print)

    return linker, store


def create_instance(file_name, engine):
    """Use wasmtime API to take care of all the details required to
    instantiate a module contained in a WASM file.
    """
    module = Module.from_file(engine, file_name)
    linker, store = create_linker_and_store(engine)

    # Instantiate the module using the linker and the store
    instance = linker.instantiate(store, module)
    return instance, store


def check_args():
    """Verify that there is one command line argument; if not, display
    an error message and exit.
    """
    if len(argv) != 2:
        print('Please specify the name of a Wasm binary file.',
              file=stderr)
        exit(1)


def main():
    """Control the steps to execute a Wasm module."""
    check_args()

    # Initialize the global Wasmtime Engine
    engine = Engine()

    instance, store = create_instance(argv[1], engine)

    # Look up and run the exported _start function
    start_func = instance.exports(store).get("_start")
    if start_func:
        start_func(store)
    else:
        print("Error: '_start' function not found in WASM module.", file=stderr)
        exit(1)


if __name__ == '__main__':
    main()
