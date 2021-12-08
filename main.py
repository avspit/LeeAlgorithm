import numpy as np
from random import randrange


def init_manual_field():
    print('Введите размер поля по шаблону [КоличествоЯчеекПоГоризонтали-КоличествоЯчеекПоВертикали] (например, 10-10)')
    size = input().split(sep='-')
    field = np.zeros((int(size[0]), int(size[1])), dtype=np.int8)
    print(field)
    return field


def init_auto_field(rows_max, cols_max):
    field = np.zeros((rows_max, cols_max), dtype=np.int8)
    return field


def init_manual_start_point(field, code):
    print('Введите координаты клетки СТАРТ по шаблону [НомерСтроки-НомерСтолбца] (например, 1-3)')
    startPoint = input().split(sep='-')
    field[int(startPoint[0]) - 1][int(startPoint[1]) - 1] = code
    print(field)
    return field


def init_auto_start_point(field, rows_max, col_max, code):
    field[randrange(rows_max)][randrange(col_max)] = code
    return field


def init_manual_finish_point(field, code):
    print('Введите координаты клетки ФИНИШ [НомерСтроки-НомерСтолбца] (например, 10-5)')
    finishPoint = input().split(sep='-')
    field[int(finishPoint[0]) - 1][int(finishPoint[1]) - 1] = code
    print(field)
    return field


def init_auto_finish_point(field, rows_max, col_max, code):
    field[randrange(rows_max)][randrange(col_max)] = code
    return field


def wall_checked(wall, code):
    if len(wall) <= 1:
        return False
    else:
        pointBefore = [code,code]
        for point in wall:
            if (pointBefore == [code,code]):
                pointBefore[0] = point[0]
                pointBefore[1] = point[1]
                continue
            elif (pointBefore[0] != point[0] and pointBefore[1] != point[1]):
                return False
            else:
                pointBefore[0] = point[0]
                pointBefore[1] = point[1]
    return True


def init_manual_wall(field, code):
    print('Введите координаты СТЕНЫ с указанием угловых точек [НомерСтрокиНачало-НомерСтолбцаНачало, НомерСтрокиПоворот-НомерСтолбцаПоворот, НомерСтрокиКонец-НомерСтолбцаКонец] (например, 2-3, 8-3, 8-7)')
    wall = input().replace(" ","").split(sep=',')
    if (not wall_checked(wall, code)):
        print('Не удалось построить стену по указанным точкам. Проверьте, что стена не строится по диагонали и задано более 1 точки')
        init_manual_wall(field, code)
    else:
        pointBefore = [code, code]
        for point in wall:
            if (pointBefore == [code, code]):
                curr = point.split('-')
                pointBefore[0] = curr[0]
                pointBefore[1] = curr[1]
                continue
            else:
                curr = point.split('-')
                if (pointBefore[0] == curr[0]):
                    for i in range(int(pointBefore[1]), int(curr[1])):
                        field[int(pointBefore[0]) - 1][int(i) - 1] = code
                else:
                    for i in range(int(pointBefore[0]), int(curr[0])):
                        field[int(i) - 1][int(pointBefore[1]) - 1] = code
                pointBefore[0] = curr[0]
                pointBefore[1] = curr[1]

        for point in wall:
            point = point.split('-')
            field[int(point[0]) - 1][int(point[1]) - 1] = code
        print(field)
        return field


def init_auto_wall(field, rows_max, col_max, points_on_wall, code):
    prevPoint = [randrange(rows_max), randrange(col_max)]
    for i in range(1, points_on_wall):
        turn = randrange(2)
        if turn == 0:
            nextPoint = [prevPoint[0], randrange(col_max)]
            for j in range(prevPoint[1], nextPoint[1]):
                field[prevPoint[0]][j] = code
        else:
            nextPoint = [randrange(rows_max), prevPoint[1]]
            for j in range(prevPoint[0], nextPoint[0]):
                field[j][prevPoint[1]] = code
    return field


def init_auto_walls(field, rows_max, col_max, count, points_on_wall, code):
    for i in range(count):
        field = init_auto_wall(field, rows_max, col_max, points_on_wall, code)
    return field


def init_manual_map():
    field = init_manual_field()
    field = init_manual_wall(field, code=-2)
    field = init_manual_start_point(field, code=1)
    field = init_manual_finish_point(field, code=-1)


def init_auto_map():
    rows_max = 10
    col_max = 10
    field = init_auto_field(rows_max, col_max)
    field = init_auto_walls(field, rows_max, col_max, count=3, points_on_wall=3, code=-2)
    field = init_auto_start_point(field, rows_max, col_max, code=1)
    field = init_auto_finish_point(field, rows_max, col_max, code=-1)
    print(field)


def start_app():
    print('Как вы хотите сгенерировать поле? Введите "a" - для автоматической генерации, "m" - для ручной генерации "s" - для остановки приложения')
    mode = input()
    if (mode == 'a'):
        init_auto_map()
        start_app()
    elif (mode == 'm'):
        init_manual_map()
        start_app()
    else:
        exit()


if __name__ == '__main__':
    start_app()

