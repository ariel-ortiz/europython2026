(;===================================================================
    File: example.wat

    WebAssembly text format (WAT) source code example.
=====================================================================;)
(module
  ;; Compute the average of three values
  (func
    (export "average")

    (param $x f64)
    (param $y f64)
    (param $z f64)

    (result f64)

    local.get $x
    local.get $y
    f64.add

    local.get $z
    f64.add

    f64.const 3.0
    f64.div
  )
  (func
    (export "fah_to_cel")
    (param $F f64)
    (result f64)
    local.get $F
    f64.const 32.0
    f64.sub
    f64.const 5.0
    f64.mul
    f64.const 9.0
    f64.div
  )
  (func
    (export "quadratic_root")
    (param $a f64)
    (param $b f64)
    (param $c f64)
    (result f64)
    local.get $b
    f64.neg
    local.get $b
    local.get $b
    f64.mul
    f64.const 4.0
    local.get $a
    f64.mul
    local.get $c
    f64.mul
    f64.sub
    f64.sqrt
    f64.add
    f64.const 2.0
    local.get $a
    f64.mul
    f64.div
  )
)
