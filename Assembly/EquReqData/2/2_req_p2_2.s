@ Deliverable: Describe what .req is used for.  How is this different than .equ?
@ Deliverable: Add the classinclude.s include file with changes to last two lines.

val1	.req r1
val2	.req r2
sum	.req r0
	.text
	.global _start
_start:	mov	val1, #0x25

	mov	val2, #0x34
	add	sum, val1, val2
	mov	r7, #1
	svc	0
	.EQU sys_read
	.EQU sys_exit

	