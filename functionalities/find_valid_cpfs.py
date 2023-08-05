def is_valid_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf) != 11:
        return False

    total = 0
    for i in range(9):
        total += int(cpf[i]) * (10 - i)
    remainder = total % 11
    digit_1 = 0 if remainder < 2 else 11 - remainder

    if int(cpf[9]) != digit_1:
        return False

    total = 0
    for i in range(10):
        total += int(cpf[i]) * (11 - i)
    remainder = total % 11
    digit_2 = 0 if remainder < 2 else 11 - remainder

    if int(cpf[10]) != digit_2:
        return False

    return True


def find_all_possibilities(middle_number):
    possibilities = []
    for i in range(10):
        for j in range(10):
            for k in range(10):
                for l in range(10):
                    for m in range(10):
                        number = f"{i}{j}{k}{middle_number}{l}{m}"
                        possibilities.append(number)
    
    return possibilities



if __name__ == "__main__":
    result: list[str] = find_all_possibilities("XXXXXX")
    valid_numbers = []
    for num in result:
        if is_valid_cpf(num) and not num.startswith('00') and not num.startswith('99'):
            valid_numbers.append(num)

    print(valid_numbers)

