import random

def create_quadratic_problem():
    '''
    return list of coefficents and answer
    '''
    root_1 = random.randint(1, 15)
    root_2 = random.randint(1, 15)

    c = root_1 * root_2
    b = root_1 + root_2
    a = random.choice([1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 5])
    tmp = max(root_1, root_2)
    tmp_2 = min(root_1, root_2)
    return [a, -b * a, c * a, tmp, tmp_2]


def create_plus_problem():
    '''
    return list of conditions and answer: +
    '''
    x1 = random.randint(10, 200)
    x2 = random.randint(10, 200)
    ans = x1 + x2
    return [x1, x2, ans]


def create_minus_problem():
    '''
    return list of conditions and answer: -
    '''
    x1 = random.randint(10, 200)
    x2 = random.randint(10, 200)
    ans = x1 - x2
    return [x1, x2, ans]


def create_multi_problem():
    '''
    return list of conditions and answer: *
    '''
    x1 = random.randint(5, 20)
    x2 = random.randint(5, 20)
    ans = x1 * x2
    return [x1, x2, ans]