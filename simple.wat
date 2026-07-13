;; chiqui_forth compiler WAT output

(module
  (import "forth" "emit" (func $emit (param i32)))
  (import "forth" "input" (func $input (result i32)))
  (import "forth" "print" (func $print (param i32)))
  (func (export "_start")
    i32.const 1
    i32.const 2
    i32.add
    i32.const 4
    i32.mul
    call $print
  )
)