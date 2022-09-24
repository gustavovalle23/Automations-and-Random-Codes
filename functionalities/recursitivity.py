def count_down(target_num):
    if target_num == 0:
        print('Go!')
    else:
        print(target_num, '...')
        count_down(target_num-1)

# count_down(5)


def sum_elements_in_list(list_nums: list, index, qtd_items: int, count: int):
    if qtd_items == index:
        return count
    return sum_elements_in_list(list_nums, index+1, qtd_items, list_nums[index] + count)


list_items = [2, 2, 3, 13]
result = sum_elements_in_list(list_items, 0, len(list_items), 0)
print(result)


print('\n\n******************\n\n')
def show_results(lista: list, index, qtd_items):
    if qtd_items == index:
        return
    print(lista[index])
    return show_results(lista, index+1, qtd_items)

results = list(map(lambda x: x+1, [1,2,3]))
show_results(results, 0, len(results))
