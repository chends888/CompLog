; constants
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0
TRUE equ 1
FALSE equ 0


segment .data

segment .bss ; variables
  res RESB 1

section .text
  global _start

print:  ; subrotina print

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
  XOR ESI, ESI

print_dec: ; empilha todos os digitos
  MOV EDX, 0
  MOV EBX, 0x000A
  DIV EBX
  ADD EDX, '0'
  PUSH EDX
  INC ESI ; contador de digitos
  CMP EAX, 0
  JZ print_next ; quando acabar pula
  JMP print_dec

print_next:
  CMP ESI, 0
  JZ print_exit ; quando acabar de imprimir
  DEC ESI

  MOV EAX, SYS_WRITE
  MOV EBX, STDOUT

  POP ECX
  MOV [res], ECX
  MOV ECX, res

  MOV EDX, 1
  INT 0x80
  JMP print_next

print_exit:
  POP EBP
  RET

; subrotinas if/while
binop_je:
  JE binop_true
  JMP binop_false

binop_jg:
  JG binop_true
  JMP binop_false

binop_jl:
  JL binop_true
  JMP binop_false

binop_false:
  MOV EBX, False
  JMP binop_exit
binop_true:
  MOV EBX, True
binop_exit:
  RET

_start:

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer
  PUSH DWORD 0
  PUSH DWORD 0
  PUSH DWORD 0
  PUSH DWORD 0
  PUSH DWORD 0
  PUSH DWORD 0
  PUSH DWORD 0
  MOV EBX, 6
  MOV [EBP - 16], EBX
  MOV EBX, 0000
  MOV [EBP - 4], EBX
  MOV EBX, 1111
  MOV [EBP - 8], EBX
  MOV EBX, 00001111
  MOV [EBP - 12], EBX
  MOV EBX, TRUE
  MOV [EBP - 28], EBX
  LOOP_36:
  MOV EBX, [EBP - 16]
  PUSH EBX
  MOV EBX, 0
  POP EAX
  CMP EAX, EBX
  CALL binop_jg
  CMP EBX, False
  JE EXIT_36
  MOV EBX, [EBP - 16]
  PUSH EBX
  MOV EBX, [EBP - 16]
  PUSH EBX
  MOV EBX, 3
  POP EAX
  IDIV EBX
  MOV EBX, EAX
  PUSH EBX
  MOV EBX, 3
  POP EAX
  IMUL EBX
  MOV EBX, EAX
  POP EAX
  SUB EAX, EBX
  MOV EBX, EAX
  MOV [EBP - 20], EBX
  MOV EBX, [EBP - 16]
  PUSH EBX
  MOV EBX, [EBP - 16]
  PUSH EBX
  MOV EBX, 5
  POP EAX
  IDIV EBX
  MOV EBX, EAX
  PUSH EBX
  MOV EBX, 5
  POP EAX
  IMUL EBX
  MOV EBX, EAX
  POP EAX
  SUB EAX, EBX
  MOV EBX, EAX
  MOV [EBP - 24], EBX
  MOV EBX, [EBP - 16]
  PUSH EBX
  CALL print
  POP EBX
  IF_62:
  MOV EBX, [EBP - 20]
  PUSH EBX
  MOV EBX, 0
  POP EAX
  CMP EAX, EBX
  CALL binop_je
  PUSH EBX
  MOV EBX, [EBP - 24]
  PUSH EBX
  MOV EBX, 0
  POP EAX
  CMP EAX, EBX
  CALL binop_je
  POP EAX
  AND EAX, EBX
  MOV EBX, EAX
  CMP EBX, False
  JE ENDIF_62
  MOV EBX, [EBP - 12]
  PUSH EBX
  CALL print
  POP EBX
  MOV EBX, FALSE
  MOV [EBP - 28], EBX
  ENDIF_62:
  IF_79:
  MOV EBX, [EBP - 20]
  PUSH EBX
  MOV EBX, 0
  POP EAX
  CMP EAX, EBX
  CALL binop_je
  PUSH EBX
  MOV EBX, [EBP - 28]
  PUSH EBX
  MOV EBX, TRUE
  POP EAX
  CMP EAX, EBX
  CALL binop_je
  POP EAX
  AND EAX, EBX
  MOV EBX, EAX
  CMP EBX, False
  JE ENDIF_79
  MOV EBX, [EBP - 4]
  PUSH EBX
  CALL print
  POP EBX
  MOV EBX, FALSE
  MOV [EBP - 28], EBX
  ENDIF_79:
  IF_96:
  MOV EBX, [EBP - 24]
  PUSH EBX
  MOV EBX, 0
  POP EAX
  CMP EAX, EBX
  CALL binop_je
  PUSH EBX
  MOV EBX, [EBP - 28]
  PUSH EBX
  MOV EBX, TRUE
  POP EAX
  CMP EAX, EBX
  CALL binop_je
  POP EAX
  AND EAX, EBX
  MOV EBX, EAX
  CMP EBX, False
  JE ENDIF_96
  MOV EBX, [EBP - 8]
  PUSH EBX
  CALL print
  POP EBX
  MOV EBX, FALSE
  MOV [EBP - 28], EBX
  ENDIF_96:
  MOV EBX, TRUE
  MOV [EBP - 28], EBX
  MOV EBX, [EBP - 16]
  PUSH EBX
  MOV EBX, 1
  POP EAX
  SUB EAX, EBX
  MOV EBX, EAX
  MOV [EBP - 16], EBX
  JMP LOOP_36
  EXIT_36:
; output interruption
POP EBP
MOV EAX, 1
INT 0X80