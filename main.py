import types


class FlatIterator:
    """
    - Доработать класс FlatIterator в коде ниже. Должен получиться итератор, который принимает список списков
    и возвращает их плоское представление, т. е. последовательность, состоящую из вложенных элементов.
    Функция test в коде ниже также должна отработать без ошибок.
    - Необязательное задание. Написать итератор, аналогичный итератору из задания 1, но обрабатывающий списки
    с любым уровнем вложенности.
    """

    def __init__(self, list_of_lists: list):

        self.list = list_of_lists

        # текущий список/итератор
        self.iterator = iter(self.list)
        # Копилка для списков/итераторов и подсписков/суб-итераторов
        self.temp = []

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            # пробуем получить начальный/следующий элемент итератора, если удачно, то пропускаем секцию except
            try:
                item = next(self.iterator)
            # в случае неудачи (последний элемент) не прекращаем цикл while
            except StopIteration:
                if not self.temp:
                    # если копилка пуста (все элементы всех списков возвращены) завершаем цикл while
                    raise StopIteration
                else:
                    # если не пуста, то извлекаем последний итератор (текущего уровня глубины) из копилки
                    # присваиваем его в текущий рабочий (таким образом поднимаемся на уровень выше/обратно)
                    self.iterator = self.temp.pop()
                    # и продолжаем цикл while, работая с текущим итератором
                    continue
            # тогда проверяем элемент список это или нет
            if isinstance(item, list):
                # если элемент является списком, то добавляем итератор верхнего списка в копилку чтобы не потерять его
                self.temp.append(self.iterator)
                # перезаписываем итератор на суб-итератор так как копию мы положили в копилку
                # и переходим к следующей итерации цикла while
                self.iterator = iter(item)
            else:
                # если элемент не список, то возвращаем его и продолжаем цикл while через __iter__ -> __next__
                return item


def flat_generator(list_of_lists: list):
    """
    - Доработать функцию flat_generator. Должен получиться генератор, который принимает список списков и возвращает
    их плоское представление. Функция test в коде ниже также должна отработать без ошибок.
    - Необязательное задание. Написать генератор, аналогичный генератору из задания 2, но обрабатывающий списки
    с любым уровнем вложенности.
    """
    if not isinstance(list_of_lists, list):
        raise TypeError('Argument\'s type must be a list')
    for item in list_of_lists:
        if not isinstance(item, list):
            yield item
        else:
            yield from flat_generator(item)


def test_1():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


def test_2():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


def test_4():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator(list_of_lists_2), types.GeneratorType)


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()
