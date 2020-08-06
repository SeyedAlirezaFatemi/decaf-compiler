standard_library_functions = """
_PrintInt:
        subu    $sp, $sp, 8
        sw      $fp, 8($sp)
        sw      $ra, 4($sp)
        addiu   $fp, $sp, 8
        li      $v0, 1
        lw      $a0, 4($fp)
        syscall
        move    $sp, $fp
        lw      $ra, -4($fp)
        lw      $fp, 0($fp)
        jr      $ra

_PrintDouble:
        subu    $sp, $sp, 8
        sw      $fp, 8($sp)
        sw      $ra, 4($sp)
        addiu   $fp, $sp, 8
        
        li      $v0, 3
        l.d     $f12, 8($fp)    # load double value to $f12
        syscall
        
        move    $sp, $fp
        lw      $ra, -4($fp)
        lw      $fp, 0($fp)
        jr      $ra


_PrintString:
        subu    $sp, $sp, 8
        sw      $fp, 8($sp)
        sw      $ra, 4($sp)
        addiu   $fp, $sp, 8
        li      $v0, 4
        lw      $a0, 4($fp)
        syscall
        move    $sp, $fp
        lw      $ra, -4($fp)
        lw      $fp, 0($fp)
        jr      $ra


_PrintNewLine:
        subu    $sp, $sp, 8
        sw      $fp, 8($sp)
        sw      $ra, 4($sp)
        addiu   $fp, $sp, 8
        li      $v0, 4
        lw      $a0, NEWLINE
        syscall
        move    $sp, $fp
        lw      $ra, -4($fp)
        lw      $fp, 0($fp)
        jr      $ra


_PrintBool:
        subu    $sp, $sp, 8
        sw      $fp, 8($sp)
        sw      $ra, 4($sp)
        addiu   $fp, $sp, 8
        lw      $t1, 4($fp)
        blez    $t1, fbr
        li      $v0, 4          # system call for print_str
        la      $a0, TRUE       # address of str to print
        syscall
        b end

fbr:    li      $v0, 4          # system call for print_str
        la      $a0, FALSE      # address of str to print
        syscall

end:    move    $sp, $fp
        lw      $ra, -4($fp)
        lw      $fp, 0($fp)
        jr      $ra


_Alloc:
        subu    $sp, $sp, 8
        sw      $fp, 8($sp)
        sw      $ra, 4($sp)
        addiu   $fp, $sp, 8
        li      $v0, 9
        lw      $a0, 4($fp)
        syscall
        move    $sp, $fp
        lw      $ra, -4($fp)
        lw      $fp, 0($fp)
        jr      $ra


_StringEqual:
        subu    $sp, $sp, 8     # decrement sp to make space to save ra, fp
        sw      $fp, 8($sp)     # save fp
        sw      $ra, 4($sp)     # save ra
        addiu   $fp, $sp, 8     # set up new fp
        subu    $sp, $sp, 4     # decrement sp to make space for locals/temps

        li      $v0, 0

        #Determine length string 1
        lw      $t0, 4($fp)
        li      $t3, 0

bloop1: lb      $t5, ($t0)
        beqz    $t5, eloop1
        addi    $t0, 1
        addi    $t3, 1
        b       bloop1

eloop1: # Determine length string 2
        lw      $t1, 8($fp)
        li      $t4, 0

bloop2: lb      $t5, ($t1)
        beqz    $t5, eloop2
        addi    $t1, 1
        addi    $t4, 1
        b       bloop2

eloop2: bne     $t3,$t4,end1    # Check String Lengths Same

        lw      $t0, 4($fp)
        lw      $t1, 8($fp)
        li      $t3, 0

bloop3: lb      $t5, ($t0)
        lb      $t6, ($t1)
        bne     $t5, $t6, end1
        beqz    $t5, eloop3     # if zero, then we hit the end of both strings
        addi    $t3, 1
        addi    $t0, 1
        addi    $t1, 1
        b       bloop3

eloop3: li      $v0, 1

end1:   move    $sp, $fp        # pop callee frame off stack
        lw      $ra, -4($fp)    # restore saved ra
        lw      $fp, 0($fp)     # restore saved fp
        jr      $ra             # return from function


_Halt:
        li      $v0, 10
        syscall


_ReadInteger:
        subu    $sp, $sp, 8     # decrement sp to make space to save ra, fp
        sw      $fp, 8($sp)     # save fp
        sw      $ra, 4($sp)     # save ra
        addiu   $fp, $sp, 8     # set up new fp
        subu    $sp, $sp, 4     # decrement sp to make space for locals/temps
        li      $v0, 5
        syscall
        move    $sp, $fp        # pop callee frame off stack
        lw      $ra, -4($fp)    # restore saved ra
        lw      $fp, 0($fp)     # restore saved fp
        jr      $ra


_ReadLine:
        subu    $sp, $sp, 8     # decrement sp to make space to save ra, fp
        sw      $fp, 8($sp)     # save fp
        sw      $ra, 4($sp)     # save ra
        addiu   $fp, $sp, 8     # set up new fp
        subu    $sp, $sp, 4     # decrement sp to make space for locals/temps

        # allocate space to store memory
        li      $a0, 128        # request 128 bytes
        li      $v0, 9          # syscall "sbrk" for memory allocation
        syscall                 # do the system call

        # read in the new line
        li      $a1, 128        # size of the buffer
        move    $a0, $v0        # location of the buffer
        li      $v0, 8
        syscall

        move    $t1, $a0

bloop4: lb      $t5, ($t1)
        beqz    $t5, eloop4
        addi    $t1, 1
        b       bloop4

eloop4: addi    $t1, -1         # add \0 at the end.
        li      $t6, 0
        sb      $t6, ($t1)

        move    $v0, $a0        # save buffer location to v0 as return value  
        move    $sp, $fp        # pop callee frame off stack
        lw      $ra, -4($fp)    # restore saved ra
        lw      $fp, 0($fp)     # restore saved fp
        jr      $ra


.data
TRUE:.asciiz "true"
FALSE:.asciiz "false"
NEWLINE:.asciiz "\n"
"""
