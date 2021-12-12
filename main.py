import numpy as np
from random import randrange
import constants as const
import matplotlib.pyplot as plt


def init_manual_field():
    """
        Инициализация поля
        :return: Поле
    """

    print('Введите размер поля по шаблону [КоличествоЯчеекПоГоризонтали-КоличествоЯчеекПоВертикали] (например, 10-10)')
    size = input().split(sep='-')
    field = np.zeros((int(size[0]), int(size[1])), dtype=np.int8)
    const.field_rows = int(size[0])
    const.field_cols = int(size[1])
    print(field)
    return field


def init_auto_field(rows_max, cols_max):
    """
        Инициализация поля
        :param rows_max: Количество строк
        :param cols_max: Количество столбцов
        :return: Поле
    """

    field = np.zeros((rows_max, cols_max), dtype=np.int8)
    return field


def init_manual_start_point(field):
    """
        Инициализация ячейки старт
        :param field: Поле
        :return: Поле
    """

    print('Введите координаты клетки СТАРТ по шаблону [НомерСтроки-НомерСтолбца] (например, 1-3)')
    startPoint = input().split(sep='-')
    field[int(startPoint[0]) - 1][int(startPoint[1]) - 1] = const.cell_start
    print(field)
    return field


def init_auto_start_point(field, rows_max, col_max):
    """
        Инициализация ячейки старт
        :param field: Поле
        :return: Поле
    """

    field[randrange(rows_max)][randrange(col_max)] = const.cell_start
    return field


def init_manual_finish_point(field):
    """
        Инициализация ячейки финиш
        :param field: Поле
        :return: Поле
    """

    print('Введите координаты клетки ФИНИШ [НомерСтроки-НомерСтолбца] (например, 10-5)')
    finishPoint = input().split(sep='-')
    field[int(finishPoint[0]) - 1][int(finishPoint[1]) - 1] = const.cell_finish
    print(field)
    return field


def init_auto_finish_point(field, rows_max, col_max):
    """
        Инициализация ячейки финиш
        :param field: Поле
        :return: Поле
    """

    field[randrange(rows_max)][randrange(col_max)] = const.cell_finish
    return field


def wall_checked(wall):
    """
        Валидация возможности нарисовать стену
        :param wall: Ячейка стены
        :return: True - стену можно нарисовать, False - стену нельзя нарисовать
    """

    if len(wall) <= 1:
        return False
    else:
        pointBefore = [const.cell_wall, const.cell_wall]
        for point in wall:
            if (pointBefore == [const.cell_wall, const.cell_wall]):
                pointBefore[0] = point[0]
                pointBefore[1] = point[1]
                continue
            elif (pointBefore[0] != point[0] and pointBefore[1] != point[1]):
                return False
            else:
                pointBefore[0] = point[0]
                pointBefore[1] = point[1]
    return True


def init_manual_wall(field):
    """
        Инициализация стены
        :param field: Поле
        :return: Поле
    """

    print('Введите координаты СТЕНЫ с указанием угловых точек [НомерСтрокиНачало-НомерСтолбцаНачало, НомерСтрокиПоворот-НомерСтолбцаПоворот, НомерСтрокиКонец-НомерСтолбцаКонец] (например, 2-3, 8-3, 8-7)')
    wall = input().replace(" ","").split(sep=',')
    if (not wall_checked(wall)):
        print('Не удалось построить стену по указанным точкам. Проверьте, что стена не строится по диагонали и задано более 1 точки')
        init_manual_wall(field)
    else:
        pointBefore = [const.cell_wall, const.cell_wall]
        for point in wall:
            if (pointBefore == [const.cell_wall, const.cell_wall]):
                curr = point.split('-')
                pointBefore[0] = curr[0]
                pointBefore[1] = curr[1]
                continue
            else:
                curr = point.split('-')
                if (pointBefore[0] == curr[0]):
                    for i in range(int(pointBefore[1]), int(curr[1])):
                        field[int(pointBefore[0]) - 1][int(i) - 1] = const.cell_wall
                else:
                    for i in range(int(pointBefore[0]), int(curr[0])):
                        field[int(i) - 1][int(pointBefore[1]) - 1] = const.cell_wall
                pointBefore[0] = curr[0]
                pointBefore[1] = curr[1]

        for point in wall:
            point = point.split('-')
            field[int(point[0]) - 1][int(point[1]) - 1] = const.cell_wall
        print(field)
        return field


def init_auto_wall(field, rows_max, col_max, points_on_wall):
    """
        Инициализация стены
        :param field: Поле
        :return: Поле
    """

    prevPoint = [randrange(rows_max), randrange(col_max)]
    for i in range(1, points_on_wall):
        turn = randrange(2)
        if turn == 0:
            nextPoint = [prevPoint[0], randrange(col_max)]
            for j in range(prevPoint[1], nextPoint[1]):
                field[prevPoint[0]][j] = const.cell_wall
        else:
            nextPoint = [randrange(rows_max), prevPoint[1]]
            for j in range(prevPoint[0], nextPoint[0]):
                field[j][prevPoint[1]] = const.cell_wall
    return field


def init_auto_walls(field, rows_max, col_max, count, points_on_wall):
    """
        Инициализация стен
        :param field: Поле
        :param rows_max: Количество строк
        :param col_max: Количество столбцов
        :param count: Количество стен
        :param points_on_wall: Количество углов, включая стартовую ячейку и финишную
        :return: Поле
    """

    for i in range(count):
        field = init_auto_wall(field, rows_max, col_max, points_on_wall)
    return field


def init_manual_map():
    """
        Инициализация поля
        :return: Поле
    """

    field = init_manual_field()
    field = init_manual_wall(field)
    field = init_manual_start_point(field)
    field = init_manual_finish_point(field)
    return field


def init_auto_map():
    """
        Инициализация поля
        :return: Поле
    """

    rows_max = const.field_rows
    col_max = const.field_cols
    field = init_auto_field(rows_max, col_max)
    field = init_auto_walls(field, rows_max, col_max, count=3, points_on_wall=3)
    field = init_auto_start_point(field, rows_max, col_max)
    field = init_auto_finish_point(field, rows_max, col_max)
    return field


def path_restoration(field, wave):
    """
        Шаг 2 алгоритма. Восстановление пути
        :param field: Поле
        :param wave: Тип волны
    """

    finish_point = np.where(field == const.cell_finish)
    row = finish_point[0][0]
    col = finish_point[1][0]
    curr = field[row, col]
    before = curr
    while curr != const.cell_start:
        for delta in wave:
            r, c, success = calc_index(row, col, delta)
            if success:
                curr = field[r, c]
                if curr == const.cell_start:
                    break
                elif (curr == before-1 or before == const.cell_finish) and curr != const.cell_start and curr != const.cell_finish and curr != const.cell_wall and curr != const.cell_empty:
                    field[r, c] = const.cell_path
                    before = curr
                    break
        row = r
        col = c


def calc_index(row, col, delta):
    """
        Вычисление индекса ячейки
        :param row: Индекс строки ячейки от которой вычисление
        :param col: Индекс колонки ячейки от которой высиление
        :param delta: На какое значение отступать
        :return: Новый индекс строки, Новый индекс колонки, True - если новую ячейку можно получить по новым индексам; False - если нельзя
    """

    r = row + delta[0]
    c = col + delta[1]
    return r, c, r >= const.cell_empty and c >= const.cell_empty and r < const.field_rows and c < const.field_cols


def wave_arround(field, row, col, step, wave):
    """
        Пускаем волну вокруг ячейки
        :param field: Поле
        :param row: Индекс строки ячейки
        :param col: Индекс колонки ячейки
        :param step: Текущий шаг
        :param wave: Тип волны
        :return: True - достигли ячейки финиша, False - не достигли
    """

    finish = False
    for delta in wave:
        r, c, success = calc_index(row, col, delta)
        if success:
            curr_val = field[r, c]
            if curr_val == const.cell_empty:
                field[r, c] = step + 1
            elif curr_val == const.cell_finish:
                finish = True
    return finish


def wave_propagation(field, wave):
    """
        Шаг 1 алгоритма. Пускание волны
        :param field: Поле
        :param wave: Тип волны
    """

    can_wave = True
    finish = False
    step = 1
    while can_wave:
        for row in range(const.field_rows):
            for col in range(const.field_cols):
                curr = field[row, col]
                if curr == step:
                    finish = wave_arround(field, row, col, step, wave)
                    if finish: break
            if finish: break
        step += 1
        can_wave = (const.cell_empty in field) and not finish


def run_lee_algorithm(field, wave):
    """
        Волновой алгоритм
        :param field: Поле
        :param wave: Тип волны
    """

    wave_propagation(field, wave)
    path_restoration(field, wave)


def run_lee(field, wave_type='n'):
    if (wave_type == 'm'):
        run_lee_algorithm(field, const.moore_wave)
    else:
        run_lee_algorithm(field, const.neyman_wave)
    print(field)


def prepare_table_for_colouring(field):
    """
        Подготовка поля к раскраске и выводу графика
        :param field: Поле
        :return: Поле
    """

    for row in range(const.field_rows):
        for col in range(const.field_cols):
            curr = field[row][col]
            if (curr != const.cell_start and curr != const.cell_finish and curr != const.cell_wall and curr != const.cell_path):
                field[row][col] = const.cell_empty
    return field


def prepare_table_colours(field):
    """
        Подготовка и раскраска поля для вывода графика
        :param field: Поле
        :return: Новое поле для графика
    """

    field = prepare_table_for_colouring(field)
    colours = field.astype(np.str)
    colours[colours == str(const.cell_start)] = const.cell_start_color
    colours[colours == str(const.cell_finish)] = const.cell_finish_color
    colours[colours == str(const.cell_wall)] = const.cell_wall_color
    colours[colours == str(const.cell_empty)] = const.cell_empty_color
    colours[colours == str(const.cell_path)] = const.cell_path_color
    return colours


def show_graf(field):
    """
        Отображение графика
        :param field: Поле
    """

    fig, ax = plt.subplots(1, 1)
    ax.axis('tight')
    ax.axis('off')
    colors = prepare_table_colours(field)
    table = ax.table(cellText=field, loc="center", cellColours=colors)
    table.scale(0.5, 1.5)
    plt.show()


def start_app():
    print('Создать новое поле? Введите "a" - для автоматической генерации, "m" - для ручной генерации "s" - для остановки приложения')
    mode = input()
    print('Выберите тип распространения волны. Введите "m" - окрестности Мура, "n" - окрестности фон Неймана')
    wave_type = input()
    if (mode == 'a'):
        field = init_auto_map()
        run_lee(field, wave_type)
        show_graf(field)
        start_app()
    elif (mode == 'm'):
        field = init_manual_map()
        run_lee(field, wave_type)
        show_graf(field)
        start_app()
    else:
        exit()


if __name__ == '__main__':
    start_app()

