from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import *
import random

app = Ursina()

# Создание неба
Sky(texture="sky_sunset")

# Создание объекта тумана
fog = Entity(model='quad', scale=(100,200), texture='white_cube', color=color.gray, position=(0,1,0), rotation_x=90)

# Регулировка тумана
fog.model.set_shader_input('alpha', 0.5)  # Прозрачность тумана
fog.model.set_shader_input('cutoff', 1.5)  # Затухание тумана

# Создание лабиринта
maze = [
    '#########################################',
    '#                                       #',
    '#   ###   #####   ##########   ###   ### #',
    '#   #       #           #          #     #',
    '#   #   #   #   #####   #   ###    #   # #',
    '#   #   #   #       #   #           #   # #',
    '#   #   #   #########   ##########  ## # #',
    '#   #   #           #           #   #   # #',
    '#   #   #############   #####   #   #   #',
    '#   #       #           #       #   #   #',
    '#   #####   ##########  #########   #   #',
    '#       #   #           #       #   #   #',
    '#####   #   ##########  #####   #####   #',
    '#   #   #           #   #       #       #',
    '#       ##########  #   #   #########   #',
    '#   #               #   #           #   #',
    '#####   #############   ##########  ## #',
    '#       #           #           #   #   #',
    '#   #####   #####   ##########  #   #   #',
    '#       #       #           #   #   #   #',
    '#####   ###   ###   ###   ###   #   #####',
    '#   #           #       #       #       #',
    '#   #########   #########   #####   #####',
    '#           #               #           #',
    '#########################################'
]

# Создание стен и пола лабиринта
for y in range(len(maze)):
    for x in range(len(maze[y])):
        if maze[y][x] == '#':
            wall = Entity(model='cube', position=(x, 2, -y), scale=(1, 4, 1), color=color.white, collider='box', texture='white_cube')
        elif maze[y][x] == ' ':
            floor = Entity(model='cube', position=(x, 0, -y), scale=(1, 0.05, 1), color=color.black, collider='box', texture='white_cube')

# Поиск случайной позиции для игрока в пределах лабиринта
player_position = (random.randint(1, 23), 0, -random.randint(1, 23))
while maze[int(-player_position[2])][int(player_position[0])] == '#':
    player_position = (random.randint(1, 23), 0, -random.randint(1, 23))

# Создание игрока с видом от первого лица
player = FirstPersonController(collider="box", position=player_position)

# Создание предмета в случайном месте
item = Entity(model='cube', position=(random.randint(1, 23), 1, -random.randint(1, 23)), scale=(1, 1, 1), color=color.red, collider='box')

# Функция обновления
def update():
    global player
    if player.y < -5:
        player.position = player_position  # Возвращаем игрока в центр при достижении определенной высоты

    # Проверяем, коснулся ли игрок предмета
    if player.intersects(item).hit:
        player.position = (0, 20, 0)  # Перемещаем игрока выше лабиринта, чтобы он мог пройти

app.run()
