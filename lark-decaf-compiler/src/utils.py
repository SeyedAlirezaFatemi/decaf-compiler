from typing import List

from .models.Type import Type, PrimitiveTypes


def calc_variable_size(variable_type: Type):
    if variable_type == PrimitiveTypes.DOUBLE:
        return 8
    elif variable_type == PrimitiveTypes.INT:
        return 4
    # TODO: what about string and bool and classes?
    return 4


def generate_clean_param_code(params_size: int) -> str:
    return f"\taddu $sp,$sp,{params_size}\t# clean parameters"


def pop_to_temp(t_num: int = 0, size: int = 4) -> List[str]:
    code = [f"lw $t{t_num},{size}($sp)", f"addu $sp,$sp,{size}"]
    return code


def push_to_stack(t_num: int = 0, size: int = 4) -> List[str]:
    code = [f"subu $sp,$sp,{size}", f"sw $t{t_num},{size}($sp)"]
    return code


def pop_double_to_femp(f_num: int = 0, size: int = 8) -> List[str]:
    code = [f"lw $f{f_num},{size}($sp)", f"addu $sp,$sp,{size}"]
    return code


def push_double_to_stack(f_num: int = 0, size: int = 8) -> List[str]:
    code = [f"subu $sp,$sp,{size}", f"sw $f{f_num},{size}($sp)"]
    return code


RETURN_ADDRESS = "-4($fp)"
PREV_FP = "$fp"
