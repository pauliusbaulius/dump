/* Ancient egyptian multiplication algorithm in ARM */
.global main
.extern printf

.data
string: .asciz "a * b = %d\n"
a: .word 0
b: .word 56

main:
	// initialize r1 with a
	ldr r0, adr_a
	ldr r1, [r0]
	// initialize r2 with b
	ldr r0, adr_b
	ldr r2, [r0]
	// r5 = result storage
	mov r5, #0

	// Compare a==0 and b==0, if either of those are 0, jump to done and finish 
	cmp r1, #0
	beq done
	cmp r2, #0
	beq done

	b odd_check
	//todo something doesnt work there, need to fix 

	// If b<0, then negate a and b
	mov r0, #0
	cmp r2, #0
	bgt odd_check // if b>=0 go to oddcheck
	/* negation of b is just addig b to itself two times */
	/* same goes for a */
	/* i couldnt find invertion operation, so i did this instead */
	mov r0, r2
	add r2, r2, r0
	add r2, r2, r0
	mov r0, r1
	sub r1, r1, r0
	sub r1, r1, r0

odd_check:
	// Check if a is odd, if it is, then add its value to the result
	mov r0, #0
	and r0, r1, #1
	cmp r0, #1
	bne init
	add r5, r5, r1

init:
	// Check if b is even, if it is, then dont need to add a to result
	mov r0, #0
	and r0, r2, #1
	cmp r0, #0
	bne while
	mov r5, #0


	// While loop that loops until b reaches 1
	// This is where the multiplication happens
while:
	cmp r2, #1
	beq done
	// Double a using shift operation
	lsl r1, r1, #1
	// Halve b using shift operation
	lsr r2, r2, #1
	// If b is odd, a value is added to the result 
	mov r0, #0
	 // b&1 == 1, r4 stores the evaluation
	and  r0, r2, #1
	cmp r0, #1
	bne equal
	// if b is odd, add a to result
	add r5, r5, r1
equal:
	b while
done:
	// Program that prints the result to the console
	push {ip, lr}
        ldr r0, =string
        mov r1, r5
        bl printf
        pop {ip, pc}

adr_a: .word a
adr_b: .word b

