from typing import List

from .models.Type import Type, PrimitiveTypes

ARRAY_LENGTH_SIZE = 4


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
    code = [
        f"\tlw $t{t_num},{size}($sp)\t#copy top stack to t{t_num}",
        f"\taddu $sp,$sp,{size}\t# move sp higher cause of pop",
    ]
    return code


def push_to_stack(t_num: int = 0, size: int = 4) -> List[str]:
    code = [
        f"\tsubu $sp,$sp,{size}\t# move sp down cause of push",
        f"\tsw $t{t_num},{size}($sp)\t#copy t{t_num} to stack",
    ]
    return code


# To load and save double, pointer must point to the end of double.


def pop_double_to_femp(f_num: int = 0, size: int = 8) -> List[str]:
    code = [
        f"\tl.d $f{f_num},0($sp)# move top stack to f{f_num}",
        f"\taddu $sp,$sp,{size}\t# move sp higher cause of pop",
    ]
    return code


def push_double_to_stack(f_num: int = 0, size: int = 8) -> List[str]:
    code = [
        f"\tsubu $sp,$sp,{size}\t# move sp down cause of push",
        f"\ts.d $f{f_num},0($sp)\t# copy f{f_num} to stack",
    ]
    return code


RETURN_ADDRESS = "-4($fp)"
THIS_ADDRESS = "4($fp)"
PREV_FP = "$fp"
DOUBLE_RETURN_REGISTER_NUMBER = 0
