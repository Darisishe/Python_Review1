from collections import deque
import random
import sys
import os


class Maze:
    def __init__(self, maze_graph, start, end):
        self.maze_graph = maze_graph
        self.start = start
        self.end = end


def DFS_generation(n, m):
    graph = [[list() for j in range(m)] for i in range(n)]
    used = [[False for j in range(m)] for i in range(n)]
    for i in range(0, n):
        for j in range(0, m):
            if i > 0:
                graph[i][j].append((i - 1, j))
            if i < n - 1:
                graph[i][j].append((i + 1, j))
            if j > 0:
                graph[i][j].append((i, j - 1))
            if j < m - 1:
                graph[i][j].append((i, j + 1))

    maze_graph = [[list() for j in range(m)] for i in range(n)]
    start = (0, 0)
    end = (-1, -1)
    stack = deque()
    stack.append(start)
    used[0][0] = True
    while stack:
        v = stack.pop()
        possible_next = []
        for to in graph[v[0]][v[1]]:
            if not used[to[0]][to[1]]:
                possible_next.append(to)

        if possible_next:
            next = random.choice(possible_next)
            used[next[0]][next[1]] = True
            maze_graph[v[0]][v[1]].append(next)
            maze_graph[next[0]][next[1]].append(v)
            stack.append(v)
            stack.append(next)
        elif end[0] == -1:
            end = v
    return Maze(maze_graph, start, end)


def initialize_DSU(n, m):
    parent = [[(x, y) for y in range(m)] for x in range(n)]
    rank = [[0] * m for x in range(n)]
    return (parent, rank)


def get(v, parent):
    (i, j) = v
    if v != parent[i][j]:
        parent[i][j] = get(parent[i][j], parent)
    return parent[i][j]


def union(v, u, parent, rank):
    v = get(v, parent)
    u = get(u, parent)
    if v == u:
        return
    (i, j) = v
    (x, y) = u
    if rank[i][j] == rank[x][y]:
        rank[i][j] += 1
    if rank[i][j] < rank[x][y]:
        parent[i][j] = u
    else:
        parent[x][y] = v


def Kruskal_generation(n, m):
    edges = []
    for i in range(0, n):
        for j in range(0, m):
            v = (i, j)
            if i > 0:
                to = (i - 1, j)
                edges.append((v, to))
            if i < n - 1:
                to = (i + 1, j)
                edges.append((v, to))
            if j > 0:
                to = (i, j - 1)
                edges.append((v, to))
            if j < m - 1:
                to = (i, j + 1)
                edges.append((v, to))

    (parent, rank) = initialize_DSU(n, m)
    random.shuffle(edges)
    maze_graph = [[list() for j in range(m)] for i in range(n)]
    for edge in edges:
        (v, u) = edge
        if get(v, parent) != get(u, parent):
            maze_graph[v[0]][v[1]].append(u)
            maze_graph[u[0]][u[1]].append(v)
            union(v, u, parent, rank)
    return Maze(maze_graph, (0, 0), (n - 1, m - 1))


def generation(n, m):
    if mode == 0:
        return DFS_generation(n, m)
    else:
        return Kruskal_generation(n, m)


def get_table(maze):
    n = len(maze.maze_graph)
    m = len(maze.maze_graph[0])
    table = [['#'] * (2 * m + 1) for i in range(2 * n + 1)]
    for i in range(0, n):
        for j in range(0, m):
            table[2 * i + 1][2 * j + 1] = ' '
            for to in maze.maze_graph[i][j]:
                delta = (to[0] - i, to[1] - j)
                table[2 * i + 1 + delta[0]][2 * j + 1 + delta[1]] = ' '
    table[2 * maze.start[0] + 1][2 * maze.start[1] + 1] = 'S'
    table[2 * maze.end[0] + 1][2 * maze.end[1] + 1] = 'F'
    return table


def print_table(table):
    for row in table:
        print(''.join(row))


def print_maze(maze):
    table = get_table(maze)
    print_table(table)


def write_maze(maze, filename):
    table = get_table(maze)
    with open(filename, 'w') as file:
        for row in table:
            file.write(''.join(row) + '\n')


def get_maze(table):
    n = (len(table) - 1) // 2
    m = (len(table[0]) - 1) // 2
    maze_graph = [[list() for j in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m):
            if table[2 * i + 1][2 * j + 1] == 'S':
                start = (i, j)
            elif table[2 * i + 1][2 * j + 1] == 'F':
                end = (i, j)
            neighbours = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
            for (x, y) in neighbours:
                delta = (x - i, y - j)
                if table[2 * i + 1 + delta[0]][2 * j + 1 + delta[1]] == ' ':
                    maze_graph[i][j].append((x, y))
    return Maze(maze_graph, start, end)


def read_maze(filename):
    file = open(filename, 'r')
    table = []
    for line in file:
        table.append(list(line.strip()))
    return get_maze(table)


def find_path(maze):
    maze_graph = maze.maze_graph
    start = maze.start
    end = maze.end
    n = len(maze_graph)
    m = len(maze_graph[0])
    used = [[False for j in range(m)] for i in range(n)]
    stack = deque()
    stack.append(start)
    used[start[0]][start[1]] = True
    while stack:
        v = stack.pop()
        if v == end:
            path = [v]
            while stack:
                v = stack.pop()
                path.append(v)
            path.reverse()
            return path

        for to in maze_graph[v[0]][v[1]]:
            if not used[to[0]][to[1]]:
                used[to[0]][to[1]] = True
                stack.append(v)
                stack.append(to)
                break


def print_with_path(maze):
    path = find_path(maze)
    table = get_table(maze)
    for i in range(0, len(path) - 1):
        (a, b) = path[i]
        (x, y) = path[i + 1]
        table[a + x + 1][b + y + 1] = '*'
        if i < len(path) - 2:
            table[2 * x + 1][2 * y + 1] = '*'
    print_table(table)


def generate():
    os.system('clear')
    print("Введите количество строк в лабиринте: ", end='')
    n = int(input())
    print("Введите количество столбцов в лабиринте: ", end='')
    m = int(input())
    maze = generation(n, m)
    os.system('clear')
    print('Ваш лабиринт сгенерирован!')
    return maze


def upload():
    print("Введите имя файла для загрузки: ")
    filename = input()
    maze = read_maze(filename)
    os.system('clear')
    print('Ваш лабиринт загружен!')
    return maze


def save(maze):
    print("Введите имя файла для сохранения: ", end='')
    filename = input()
    write_maze(maze, filename)
    print("Лабиринт успешно сохранен!")


def options(maze):
    proceed = True
    while proceed:
        print()
        print('Что хотите сделать?')
        print('1. Отобразить лабиринт')
        print('2. Сохранить лабиринт в файл')
        print('3. Решить лабиринт')
        print('4. Вернуться в меню')
        response = int(input())
        os.system('clear')
        if response == 1:
            print_maze(maze)
        elif response == 2:
            save(maze)
        elif response == 3:
            print_with_path(maze)
        else:
            proceed = False
    return True


def menu():
    os.system('clear')
    print("Выберите опцию:")
    print("1. Сгенерировать лабиринт")
    print("2. Загрузить готовый лабиринт из файла")
    print("3. Выйти из программы")
    response = int(input())
    if response == 1:
        maze = generate()
        return options(maze)
    elif response == 2:
        maze = upload()
        return options(maze)
    else:
        return False


mode = int(sys.argv[1])
running = True
while running:
    running = menu()
