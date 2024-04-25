.global _start

.equ GPIO_BASE, 0xFE200000
.equ GPFSEL2, 0x08

.equ GPIO_21_OUTPUT, 0x8 ;//# 1 << 3

.equ GPFSET0, 0x1c
.equ GPFCLR0, 0x28

.equ GPIOVAL, 0x200000 ;//# 1 << 21

_start:

	;//# base of our GPIO structure
	ldr r0, =GPIO_BASE

	;//# set the GPIO 21 function as output
	ldr r1, =GPIO_21_OUTPUT
	str r1, [r0, #GPFSEL2]

	# set counter
	ldr r2, =0x800000

loop:
	# turn on the LED
	ldr r1, =GPIOVAL ;//# value to write to set register
	str r1, [r0, #GPFSET0] ;//# store in set register

	# Wait for some time, delay
    # Even Duty Cycle
    # 3200/3200 for 1 Hz
    # 50/190 for 430 Hz 
    # 1000/1000 for 4 Hz
    # 32/32 for 3.8 kHz
    # 500/500 for 16 Hz
    # 100/100 for 410 Hz
    # 50/50 for 1.5 kHz
    # 50/30 for 2.5 kHz
    # 60/60 for 1.1 kHz
    # 10/10 for 33 kHz
    # 5/5 for 122 kHz ==> 60% Duty
    # -----------------
    # 87/87 | 50/50 for 800 Hz ==> 75% Duty
    # 98/98 | 1/1 for 850 Hz ==> 99.99% Duty
    # 1/1 | 98/98 for 850 Hz ==> 0.02% Duty

	mov r9, #1      ;//# Adjust the number of repetitions 
	mov r8, #1   ;//# Adjust the initial value for each chunk delay

delay_outer:
	mov r10, r8    ;//# Preserve the initial value for each chunk delay

delay_inner:
	subs r10, r10, #1
	bne delay_inner

	subs r9, r9, #1
	bne delay_outer



	# turn off the LED
	ldr r1, =GPIOVAL ;//# value to write to set register
	str r1, [r0, #GPFCLR0] ;//# store in set register

	# Wait for some time, delay
	mov r9, #98      ;//# Adjust the number of repetitions
	mov r8, #98   ;//# Adjust the initial value for each chunk delay

delay_outer1:
	mov r10, r8    ;//# Preserve the initial value for each chunk delay

delay_inner1:
	subs r10, r10, #1
	bne delay_inner1

	subs r9, r9, #1
	bne delay_outer1


	b loop
