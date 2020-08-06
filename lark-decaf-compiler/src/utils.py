from .models.Type import Type, PrimitiveTypes


def calc_variable_size(variable_type: Type):
    if variable_type.name == PrimitiveTypes.DOUBLE.name:
        return 8
    elif variable_type.name == PrimitiveTypes.INT.name:
        return 4
    # TODO: what about string and bool and classes?
    return 4


def generate_clean_param_code(params_size: int) -> str:
    return f"\taddu $sp,$sp,{params_size}\t# clean parameters"


RETURN_ADDRESS = "-4($fp)"
PREV_FP = "$fp"
