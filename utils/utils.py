from models.models import OperationEnum


def define_operation_code(operation: OperationEnum) -> str:
    if operation == OperationEnum.PAID:
        return "0"
    elif operation == OperationEnum.ORDER:
        return "2"
    else:
        raise ValueError("Invalid operation")


def format_table_number(operation: OperationEnum, table: int) -> str:
    table_number = str(table)[::-1]
    code = define_operation_code(operation)
    table_digits = ["0", "0", code]

    for index, value in enumerate([digit for digit in table_number]):
        table_digits[index] = value

    table_digits = ''.join(table_digits[::-1])
    return table_digits
