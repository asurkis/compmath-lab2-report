import numpy as np


def eval_rectangle_left(f, xs):
    ys = f(xs[:-1])
    hs = xs[1:] - xs[:-1]
    return np.sum(ys * hs)


def eval_rectangle_right(f, xs):
    ys = f(xs[1:])
    hs = xs[1:] - xs[:-1]
    return np.sum(ys * hs)


def eval_rectangle_middle(f, xs):
    ys = f(0.5 * (xs[1:] + xs[:-1]))
    hs = xs[1:] - xs[:-1]
    return np.sum(ys * hs)


def eval_trapeze(f, xs):
    ys = f(xs)
    hs = xs[1:] - xs[:-1]
    return 0.5 * np.sum((ys[1:] + ys[:-1]) * hs)


def eval_simpson(f, xs):
    ys = f(xs)
    xevens = xs[::2]
    yevens = ys[::2]
    xodds = xs[1::2]
    yodds = ys[1::2]

    x1 = xevens[:-1]
    y1 = yevens[:-1]
    x2 = xodds
    y2 = yodds
    x3 = xevens[1:]
    y3 = yevens[1:]

    return np.sum(
            (2 * (y1 * (x2 - x3) -
                  y2 * (x1 - x3) +
                  y3 * (x1 - x2)) * (x3 ** 3 - x1 ** 3) -
             3 * (y1 * (x2 ** 2 - x3 ** 2) -
                  y2 * (x1 ** 2 - x3 ** 2) +
                  y3 * (x1 ** 2 - x2 ** 2)) * (x3 ** 2 - x1 ** 2) +
             6 * (y1 * x2 * x3 * (x2 - x3) -
                  y2 * x1 * x3 * (x1 - x3) +
                  y3 * x1 * x2 * (x1 - x2)) * (x3 - x1))
            / (6 * (x1 - x2) * (x1 - x3) * (x2 - x3)))


def iterate(f, e, l, r, p):
    n = 4
    result = 0.0
    delta = 0.0
    while True:
        xs = np.linspace(l, r, n + 1)
        result_new = e(f, xs)
        delta = abs(result_new - result)
        if delta < p:
            return result, n, delta
        result = result_new
        n *= 2


def polynomial(*ks):
    fun = lambda x: sum(k * x ** i for i, k in enumerate(reversed(ks)))
    name = ''
    for i, k in enumerate(ks):
        p = len(ks) - i - 1
        if k != 0:
            abs_k_str = ''
            if abs(k) != 1 or p == 0:
                abs_k_str = str(abs(k))
            x_str = ''
            if p > 0:
                x_str = 'x'
            if p > 1:
                x_str += '^{0}'.format(p)
            if name == '':
                name = '' if k > 0 else '-'
            else:
                name += ' + ' if k > 0 else ' - '
            name += abs_k_str + x_str
    return fun, name


functions_to_choose = [
    polynomial(5, -2, 3, -15),  # ������� 15
    polynomial(1, -3, 6, -19),  # ������� 19
    polynomial(2, -2, 7, -14),  # ������� 14
    polynomial(3, 5, 3, -6),  # ������� 6
    polynomial(-1, -1, 1, 3),  # ������� 3
    polynomial(1, 0),  # x
    polynomial(1),  # 1
]

methods_to_choose = [
    (eval_rectangle_left, '����� ����� ���������������'),
    (eval_rectangle_right, '����� ������ ���������������'),
    (eval_rectangle_middle, '����� ������� ���������������'),
    (eval_trapeze, '����� ��������'),
    (eval_simpson, '����� ��������'),
]

print('�������� ������� ��� ���������� ���������:')
for i, (_, s) in enumerate(functions_to_choose):
    print('{0}) {1}'.format(i + 1, s))
chosen_index = int(input())
chosen_function, chosen_string = functions_to_choose[chosen_index - 1]
print('������� ������� ({0}): {1}'.format(chosen_index, chosen_string))

print('�������� ����� ���������� ���������:')
for i, (_, s) in enumerate(methods_to_choose):
    print('{0}) {1}'.format(i + 1, s))
chosen_index = int(input())
chosen_evaluator, chosen_string = methods_to_choose[chosen_index - 1]
print('������ ����� ({0}): {1}'.format(chosen_index, chosen_string))

print('�������� ����� ������� ���������:')
chosen_left = float(input())
print('������� ����� ������� ���������: {0}'.format(chosen_left))

print('�������� ������ ������� ���������:')
chosen_right = float(input())
print('������� ������ ������� ���������: {0}'.format(chosen_right))

print('�������� ��������:')
chosen_precision = float(input())
print('������� �������� {0}'.format(chosen_precision))

print('��������...')
result, result_n, result_delta = iterate(chosen_function,
                                         chosen_evaluator,
                                         chosen_left,
                                         chosen_right,
                                         chosen_precision)
print('������')
print('�������� ���������: {0}'.format(result))
print('���������� ��������: {0}'.format(result_n))
print('�����������: {0}'.format(result_delta))
