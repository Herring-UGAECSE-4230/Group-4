@ mmap part taken from by https://bob.cs.sonoma.edu/IntroCompOrg-RPi/sec-gpio-mem.html

@ GPOI21 Related
.equ    GPFSEL1, 0x04                   @ function register offset
.equ    GPCLR0, 0x28                    @ clear register offset
.equ    GPSET0, 0x1c                    @ set register offset
.equ    GPFSEL1_GPIO11_MASK, 0b111000   @ Mask for fn register
.equ    MAKE_GPIO11_OUTPUT, 0b1000      @ use pin for ouput
.equ    PIN, 11                         @ Used to set PIN high / low

.equ    D_ON, 10 @4294967295                  @delay counter
.equ    D_OFF, 100 @4294967295  

@ Args for mmap
.equ    OFFSET_FILE_DESCRP, 0   @ file descriptor
.equ    mem_fd_open, 3
.equ    BLOCK_SIZE, 4096        @ Raspbian memory page
.equ    ADDRESS_ARG, 3          @ device address

@ Misc
.equ    SLEEP_IN_S,1            @ sleep one second

@ The following are defined in /usr/include/asm-generic/mman-common.h:
.equ    MAP_SHARED,1    @ share changes with other processes
.equ    PROT_RDWR,0x3   @ PROT_READ(0x1)|PROT_WRITE(0x2)

@ Constant program data
    .section .rodata
device:
    .asciz  "/dev/gpiomem"


@ The program
    .text
    .global main

main:
@ Open /dev/gpiomem for read/write and syncing
    ldr     r1, O_RDWR_O_SYNC   @ flags for accessing device
    ldr     r0, mem_fd          @ address of /dev/gpiomem
    bl      open     
    mov     r4, r0              @ use r4 for file descriptor

@ Map the GPIO registers to a main memory location so we can access them
@ mmap(addr[r0], length[r1], protection[r2], flags[r3], fd[r4])
    str     r4, [sp, #OFFSET_FILE_DESCRP]   @ r4=/dev/gpiomem file descriptor
    mov     r1, #BLOCK_SIZE                 @ r1=get 1 page of memory
    mov     r2, #PROT_RDWR                  @ r2=read/write this memory
    mov     r3, #MAP_SHARED                 @ r3=share with other processes
    mov     r0, #mem_fd_open                @ address of /dev/gpiomem
    ldr     r0, GPIO_BASE                   @ address of GPIO
    str     r0, [sp, #ADDRESS_ARG]          @ r0=location of GPIO
    bl      mmap
    mov     r5, r0           @ save the virtual memory address in r5

@ Set up the GPIO pin funtion register in programming memory
    add     r0, r5, #GPFSEL1            @ calculate address for GPFSEL2
    ldr     r2, [r0]                    @ get entire GPFSEL2 register
    bic     r2, r2, #GPFSEL1_GPIO11_MASK@ clear pin field
    orr     r2, r2, #MAKE_GPIO11_OUTPUT @ enter function code
    str     r2, [r0]                    @ update register


   
LED_ON:
    add     r0, r5, #GPSET0 @ calc GPSET0 address
    mov     r3, #1          @ turn on bit
    lsl     r3, r3, #PIN    @ shift bit to pin position
    orr     r2, r2, r3      @ set bit
    str     r2, [r0]        @ update register
    
    ldr     r8, =420000
    @mov     r8, #D_ON
    b       on_delay

on_delay:
    subs    r8, r8, #1      @decreasing counter
    bne     on_delay       
    b       LED_OFF

LED_OFF: 
    add     r0, r5, #GPCLR0 @ calc GPCLR0 address
    mov     r3, #1          @ turn off bit
    lsl     r3, r3, #PIN    @ shift bit to pin position
    orr     r2, r2, r3      @ set bit
    str     r2, [r0]        @ update register
    
    ldr     r8, =420000
    @mov     r8, #D_OFF
    b       off_delay

off_delay:
    subs    r8, r8, #1       @decreasing counter
    bne     off_delay
    b       LED_ON

GPIO_BASE:
    .word   0xfe200000  @GPIO Base address Raspberry pi 4

mem_fd:
    .word   device

O_RDWR_O_SYNC:
    .word   2|256       @ O_RDWR (2)|O_SYNC (256).

@100hz =4460000
@1khz =420000
