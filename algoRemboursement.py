liste_person_balance = {'Martin': -9, 'Patrick': 12, 'Sam': 3, "Basil": -6}


def get_min_balance_positive(dict_balance):
    min_balance = 999999
    min_person = ""
    for i in range(len(dict_balance)):
        for v, name in zip(dict_balance.values(), dict_balance.keys()):
            if v > 0:
                if v <= min_balance:
                    min_balance = v
                    min_person = name
    return [min_person, min_balance]


def get_min_balance_negative(dict_balance):
    min_negative_balance = -99999
    min_negative_person = ""
    for i in range(len(dict_balance)):
        for v, name in zip(dict_balance.values(), dict_balance.keys()):
            if v < 0:
                if v >= min_negative_balance:
                    min_negative_balance = v
                    min_negative_person = name
    return [min_negative_person, min_negative_balance]


def check_to_balance(list_person_and_balance: dict):
    person_and_balance = dict(list_person_and_balance).copy()
    list_of_reimbursement = []
    while len(person_and_balance) != 0:
        if len(person_and_balance) == 1:
            break
        min_pos = get_min_balance_positive(person_and_balance)
        min_neg = get_min_balance_negative(person_and_balance)
        if (min_pos[1] + min_neg[1]) == 0:
            person_and_balance.pop(min_pos[0])
            person_and_balance.pop(min_neg[0])
            list_of_reimbursement.append(f"{min_pos[0]} doit {min_pos[1]}€ à {min_neg[0]}")
        elif (min_pos[1] + min_neg[1]) < 0:
            person_and_balance[min_neg[0]] = min_pos[1] + min_neg[1]
            person_and_balance.pop(min_pos[0])
            list_of_reimbursement.append(f"{min_pos[0]} doit {min_pos[1]}€ à {min_neg[0]}")
        elif (min_pos[1] + min_neg[1]) > 0:
            person_and_balance[min_pos[0]] = min_pos[1] + min_neg[1]
            person_and_balance.pop(min_neg[0])
            list_of_reimbursement.append(f"{min_pos[0]} doit {abs(min_neg[1])}€ à {min_neg[0]}")
    return list_of_reimbursement


print(check_to_balance(liste_person_balance))
