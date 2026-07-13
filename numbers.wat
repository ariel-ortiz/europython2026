;; chiqui_forth compiler WAT output

(module
  (import "forth" "emit" (func $emit (param i32)))
  (import "forth" "input" (func $input (result i32)))
  (import "forth" "print" (func $print (param i32)))
  (func (export "_start")
    (local $x i32)
    (local $y i32)
    i32.const 62
    call $emit
    i32.const 32
    call $emit
    call $input
    local.set $x
    i32.const 62
    call $emit
    i32.const 32
    call $emit
    call $input
    local.set $y
    local.get $x
    call $print
    i32.const 43
    call $emit
    i32.const 32
    call $emit
    local.get $y
    call $print
    i32.const 61
    call $emit
    i32.const 32
    call $emit
    local.get $x
    local.get $y
    i32.add
    call $print
    i32.const 10
    call $emit
    local.get $x
    call $print
    i32.const 42
    call $emit
    i32.const 32
    call $emit
    local.get $y
    call $print
    i32.const 61
    call $emit
    i32.const 32
    call $emit
    local.get $x
    local.get $y
    i32.mul
    call $print
    i32.const 10
    call $emit
  )
)