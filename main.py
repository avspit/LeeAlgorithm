import numpy as np
from random import randrange
import constants as const
import matplotlib.pyplot as plt


def init_manual_field():
    print('Введите размер поля по шаблону [КоличествоЯчеекПоГоризонтали-КоличествоЯчеекПоВертикали] (например, 10-10)')
    size = input().split(sep='-')
    field = np.zeros((int(size[0]), int(size[1])), dtype=np.int8)
    const.field_rows = size[0]
    const.field_cols = size[1]
    print(field)
    return field


def init_auto_field(rows_max, cols_max):
    field = np.zeros((rows_max, cols_max), dtype=np.int8)
    return field


def init_manual_start_point(field):
    print('Введите координаты клетки СТАРТ по шаблону [НомерСтроки-НомерСтолбца] (например, 1-3)')
    startPoint = input().split(sep='-')
    field[int(startPoint[0]) - 1][int(startPoint[1]) - 1] = const.start
    print(field)
    return field


def init_auto_start_point(field, rows_max, col_max):
    field[randrange(rows_max)][randrange(col_max)] = const.start
    return field


def init_manual_finish_point(field):
    print('Введите координаты клетки ФИНИШ [НомерСтроки-НомерСтолбца] (например, 10-5)')
    finishPoint = input().split(sep='-')
    field[int(finishPoint[0]) - 1][int(finishPoint[1]) - 1] = const.finish
    print(field)
    return field


def init_auto_finish_point(field, rows_max, col_max):
    field[randrange(rows_max)][randrange(col_max)] = const.finish
    return field


def wall_checked(wall):
    if len(wall) <= 1:
        return False
    else:
        pointBefore = [const.wall, const.wall]
        for point in wall:
            if (pointBefore == [const.wall, const.wall]):
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
    print('Введите координаты СТЕНЫ с указанием угловых точек [НомерСтрокиНачало-НомерСтолбцаНачало, НомерСтрокиПоворот-НомерСтолбцаПоворот, НомерСтрокиКонец-НомерСтолбцаКонец] (например, 2-3, 8-3, 8-7)')
    wall = input().replace(" ","").split(sep=',')
    if (not wall_checked(wall)):
        print('Не удалось построить стену по указанным точкам. Проверьте, что стена не строится по диагонали и задано более 1 точки')
        init_manual_wall(field)
    else:
        pointBefore = [const.wall, const.wall]
        for point in wall:
            if (pointBefore == [const.wall, const.wall]):
                curr = point.split('-')
                pointBefore[0] = curr[0]
                pointBefore[1] = curr[1]
                continue
            else:
                curr = point.split('-')
                if (pointBefore[0] == curr[0]):
                    for i in range(int(pointBefore[1]), int(curr[1])):
                        field[int(pointBefore[0]) - 1][int(i) - 1] = const.wall
                else:
                    for i in range(int(pointBefore[0]), int(curr[0])):
                        field[int(i) - 1][int(pointBefore[1]) - 1] = const.wall
                pointBefore[0] = curr[0]
                pointBefore[1] = curr[1]

        for point in wall:
            point = point.split('-')
            field[int(point[0]) - 1][int(point[1]) - 1] = const.wall
        print(field)
        return field


def init_auto_wall(field, rows_max, col_max, points_on_wall):
    prevPoint = [randrange(rows_max), randrange(col_max)]
    for i in range(1, points_on_wall):
        turn = randrange(2)
        if turn == 0:
            nextPoint = [prevPoint[0], randrange(col_max)]
            for j in range(prevPoint[1], nextPoint[1]):
                field[prevPoint[0]][j] = const.wall
        else:
            nextPoint = [randrange(rows_max), prevPoint[1]]
            for j in range(prevPoint[0], nextPoint[0]):
                field[j][prevPoint[1]] = const.wall
    return field


def init_auto_walls(field, rows_max, col_max, count, points_on_wall):
    for i in range(count):
        field = init_auto_wall(field, rows_max, col_max, points_on_wall)
    return field


def init_manual_map():
    field = init_manual_field()
    field = init_manual_wall(field)
    field = init_manual_start_point(field)
    field = init_manual_finish_point(field)
    return field


def init_auto_map():
    rows_max = 10
    col_max = 10
    field = init_auto_field(rows_max, col_max)
    field = init_auto_walls(field, rows_max, col_max, count=3, points_on_wall=3)
    field = init_auto_start_point(field, rows_max, col_max)
    field = init_auto_finish_point(field, rows_max, col_max)
    return field


def path_moore_restoration(field):
    f=1


def path_neyman_restoration(field):
    finish_point = np.where(field == const.finish)
    row = finish_point[0][0]
    col = finish_point[1][0]
    curr = field[row, col]
    before = curr
    while curr != const.start:
        for delta in const.neyman_wave:
            r, c, success = calc_index(row, col, delta)
            if success:
                curr = field[r, c]
                if curr == const.start:
                    break
                elif (curr == before-1 or before == const.finish) and curr != const.start and curr != const.finish and curr != const.wall and curr != 0:
                    field[r, c] = const.path
                    before = curr
                    break
        row = r
        col = c


def wave_moore_propagation(field):
    f=1


def calc_index(row, col, delta):
    r = row + delta[0]
    c = col + delta[1]
    return r, c, r >= 0 and c >= 0 and r < const.field_rows and c < const.field_cols


def wave_neyman_arround(field, row, col, step):
    finish = False
    for delta in const.neyman_wave:
        r, c, success = calc_index(row, col, delta)
        if success:
            curr_val = field[r, c]
            if curr_val == 0:
                field[r, c] = step + 1
            elif curr_val == const.finish:
                finish = True
    return finish


def wave_neyman_propagation(field):
    can_wave = True
    finish = False
    step = 1
    while can_wave:
        for row in range(const.field_rows):
            for col in range(const.field_cols):
                curr = field[row, col]
                if curr == step:
                    finish = wave_neyman_arround(field, row, col, step)
                    if finish: break
            if finish: break
        step += 1
        can_wave = (0 in field) and not finish


def run_lee_moore(field):
    wave_moore_propagation(field)
    path_moore_restoration(field)
    print(field)


def run_lee_neyman(field):
    wave_neyman_propagation(field)
    path_neyman_restoration(field)


def run_lee(field, wave_type="n"):
    if (wave_type == 'm'):
        run_lee_moore(field)
    else:
        run_lee_neyman(field)
    print(field)


def prepare_table_for_colouring(field):
    for row in range(const.field_rows):
        for col in range(const.field_cols):
            curr = field[row][col]
            if (curr != const.start and curr != const.finish and curr != const.wall and curr != const.path):
                field[row][col] = 0
    return field


def prepare_table_colours(field):
    field = prepare_table_for_colouring(field)
    colours = field.astype(np.str)
    colours[colours == str(const.start)] = "#ADFF2F"
    colours[colours == str(const.finish)] = "#ADFF2F"
    colours[colours == str(const.wall)] = "#FAEBD7"
    colours[colours == str(0)] = "w"
    colours[colours == str(const.path)] = "#FFB6C1"
    return colours


def show_graf(field):
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

