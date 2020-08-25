.data

message: .word 10

.global main

/*
	Calculate parity bit of a message.
*/

main:
ldr r1, message
mov r2, #0 /* r2 is used for parity sum */

/* 000x check */
mov r0, r1
and r0, r0, #1
add r2, r2, r0

/* 00x0 check */ 
mov r0, r1
and r0, r0, #2
add r2, r2, r0

/* 0x00 check */ 
mov r0, r1
add r0, r0, #4
add r2, r2, r0

/* x000 check */ 
mov r0, r1
add r0, r0, #8
add r2, r2, r0

/* calculate r2 as bit */
and r2, r2, #1
/* add parity bit to the end of message */
lsl r1, r1, #1
orr r1, r1, r2
mov r0, r1
bx lr
