;; chiqui_forth compiler WAT output

(module
  (import "forth" "emit" (func $emit (param i32)))
  (import "forth" "input" (func $input (result i32)))
  (import "forth" "print" (func $print (param i32)))
  (func (export "_start")
    i32.const 72
    call $emit
    i32.const 101
    call $emit
    i32.const 108
    call $emit
    i32.const 108
    call $emit
    i32.const 111
    call $emit
    i32.const 44
    call $emit
    i32.const 32
    call $emit
    i32.const 119
    call $emit
    i32.const 111
    call $emit
    i32.const 114
    call $emit
    i32.const 108
    call $emit
    i32.const 100
    call $emit
    i32.const 33
    call $emit
    i32.const 10
    call $emit
  )
)