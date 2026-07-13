# ==============================================================================
# File: wat_launcher.py
#
# A generic host script for loading, compiling, and executing arbitrary
# WebAssembly modules from within Python using the Wasmtime runtime.
# ==============================================================================

from wasmtime import Store, Module, Instance


def call_wat_fun(file_name, fn_name, *args):
    """Loads, compiles, and executes a WebAssembly function.

    Args:
        file_name (str): The path to the .wat or .wasm file.
        fn_name (str): The name of the exported Wasm function to invoke.
        *args: Variable length argument list to pass to the Wasm function.

    Returns:
        Any: The marshaled result returned from the WebAssembly function execution.
    """
    store = Store()
    module = Module.from_file(store.engine, file_name)
    instance = Instance(store, module, [])
    function = instance.exports(store).get(fn_name)
    return function(store, *args)


if __name__ == '__main__':
    print(call_wat_fun('example.wat', 'average', 1.0, 2.0, 6.0))
    print(call_wat_fun('example.wat', 'average', 2.5, 2.7, 5.8))
    print(call_wat_fun('example.wat', 'fah_to_cel', 212.0))
    print(call_wat_fun('example.wat', 'fah_to_cel', 32.0))
    print(call_wat_fun('example.wat', 'fah_to_cel', -40.0))
