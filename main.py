# -*-coding:utf-8-*-

# Copycat v0.2.1
# An incomplete clone of Terry Cavanagh's Copycat. Written in python.
# Author of this clone: febilly

# 数字显示时间从1/3改为了2/3

from hpprime import *
from urandom import *
from math import floor

try:
    from time import sleep
except ImportError:
    # sleep = lambda x: eval("SLEEP({})".format(x))
    sleep = lambda x: None

map_width = 20
map_height = 11


# 换用towards_pos了
# 向四个方向移动一格
# def up_tile(p):
#     return Point(p.x, p.y - 1)
#
#
# def left_tile(p):
#     return Point(p.x - 1, p.y)
#
#
# def down_tile(p):
#     return Point(p.x, p.y + 1)
#
#
# def right_tile(p):
#     return Point(p.x + 1, p.y)
#
#
# # 获取剑应该所处的位置
# def sword_pos(p, facing):
#     if facing == "up":
#         return up_tile(p)
#     elif facing == "left":
#         return left_tile(p)
#     elif facing == "down":
#         return down_tile(p)
#     elif facing == "right":
#         return right_tile(p)
#     else:
#         return p


# 将两个坐标加起来
def delta_pos(p1, p2):  # 返回新的Pos
    return (p1[0] + p2[0], p1[1] + p2[1])


# 判断点是否在地图里面
def is_valid_point(p):  # 返回布尔值
    if p[0] < 0 or p[0] >= map_width:
        return False
    elif p[1] < 0 or p[1] >= map_height:
        return False
    else:
        return True


# 判断一个点是否没有被实体占用  # 返回布尔值
def is_no_entity_point(p, consider_player_sword=False, consider_enemy_sword=False,
                       consider_coming_enemy=False, consider_bomb=False, self=None):
    for enemy in enemy_list:
        if p == enemy.pos:
            if enemy.type != "bomb" or consider_bomb:
                return False
        if consider_enemy_sword:
            if enemy.type == "swordguy" and enemy != self:
                if p == towards_pos(enemy.pos, enemy.facing):
                    return False

    if consider_coming_enemy:
        for coming_enemy in coming_enemy_list:
            if p == coming_enemy.pos:
                return False

    if player and p == player.pos:
        return False
    # # 好像游戏里并不考虑玩家的剑？
    # # 敌人可以试图往玩家的剑里走，但是走不动
    # # 哎呀算了还是考虑玩家的剑吧，这样就不用处理到底敌人走不走得动的问题了
    # # sword不会直接死，dash会
    # # 但其实玩起来没多大差别吧，反正横竖都是死
    # 草 好像不考虑 管他的 加个选项吧
    if consider_player_sword:
        if player and player.type == "sword" and p == towards_pos(player.pos, player.facing):
            return False

    return True


# 废弃
# # 判断一个点是不是空的
# def is_empty_point(p):
#     if _map.get(p) == "wall":
#         return False
#     for enemy in enemy_list:
#         if p == enemy.pos:
#             return False
#         if consider_enemy_sword:
#             if enemy.type == "swordguy" and enemy != self:
#                 if p == towards_pos(enemy.pos, enemy.facing):
#                     return False
#     if p == player.pos:
#         return False
#     # # 好像游戏里并不考虑玩家的剑？
#     # # 敌人可以试图往玩家的剑里走，但是走不动
#     # # 哎呀算了还是考虑玩家的剑吧，这样就不用处理到底敌人走不走得动的问题了
#     # # sword不会直接死，dash会
#     # # 但其实玩起来没多大差别吧，反正横竖都是死
#     # 草 好像不考虑 管他的 加个选项吧
#     if consider_player_sword:
#         if player.type == "sword" and p == towards_pos(player.pos, player.facing):
#             return False
#     return True


# 获取一个点的属性
def get_point(p):  # 返回目标位置上的东西的属性，或者是目标位置上的敌人
    if not is_valid_point(p):
        return "out"
    for enemy in enemy_list:
        if p == enemy.pos:
            return enemy
        if enemy.type == "swordguy":
            if p == towards_pos(enemy.pos, enemy.facing):
                return "sword"
        if player:
            if p == player.pos:
                return "player"

    if player:
        if player.type == "sword" and p == towards_pos(player.pos, player.facing):
            return "sword_player"
    return main_map.get(p)


# 点，包含自定义的 ==
# class Point:
#     def __init__(self, x: int, y: int):
#         self[0] = x
#         self[1] = y
#
#     def __eq__(self, other):
#         if other[0] == self[0] and other[1] == self[1]:
#             return True
#         else:
#             return False
#
#     def __add__(self, other):
#         return Point(self[0] + other[0], self[1] + other[1])


# 玩家
class Player:
    def __init__(self, pos, facing, _type):
        self.pos = pos
        self.facing = facing
        self.type = _type
        # 给bomb用的
        self.cooldown = 0


# 地图，不只是主地图
class Map:
    def __init__(self, width, height, default=None):
        self.width = width
        self.height = height
        self.default = default
        # 这种东西还是别太oo吧
        self.map = [[self.default for i in range(height)] for j in range(width)]

    # 随机放墙
    def place_walls(self):
        for i in range(self.width):
            for j in range(self.height):
                self.map[i][j] = choice(["ground", "ground", "ground", "wall"])
                pass

    def get(self, p):  # 返回类型
        if is_valid_point(p):
            return self.map[p[0]][p[1]]
        else:
            return self.default

    def get2(self, x, y):  # 返回类型
        return self.get((x, y))

    def set(self, p, value):
        if is_valid_point(p):
            self.map[p[0]][p[1]] = value

    def set2(self, x, y, value):
        self.set((x, y), value)


class MainMap(Map):
    def set(self, p, value):
        global map_changes
        if is_valid_point(p):
            self.map[p[0]][p[1]] = value
            map_changes.append([p, value])


def get_neighbours(center: tuple, morph):

    neighbours = []
    x = center[0]
    y = center[1]

    if morph:
        if x > 0:
            if main_map.get2(x - 1, y) != "wall":
                neighbours.append((x - 1, y))
        if x < map_width - 1:
            if main_map.get2(x + 1, y) != "wall":
                neighbours.append((x + 1, y))
        if y > 0:
            if main_map.get2(x, y - 1) != "wall":
                neighbours.append((x, y - 1))
        if y < map_height - 1:
            if main_map.get2(x, y + 1) != "wall":
                neighbours.append((x, y + 1))
    else:
        if y < map_height - 1:
            if main_map.get2(x, y + 1) != "wall":
                neighbours.append((x, y + 1))
        if y > 0:
            if main_map.get2(x, y - 1) != "wall":
                neighbours.append((x, y - 1))
        if x < map_width - 1:
            if main_map.get2(x + 1, y) != "wall":
                neighbours.append((x + 1, y))
        if x > 0:
            if main_map.get2(x - 1, y) != "wall":
                neighbours.append((x - 1, y))

    return neighbours


# 把每个敌人下一步要走的方向存在它自己的next_chase_facing里面
# https://www.redblobgames.com/pathfinding/a-star/implementation.html
def pathfinding(start_point):
    global randomizer
    randomizer += random()
    randomizer -= 0.5
    if randomizer > 0.5:
        randomizer = 0.5
    if randomizer < -0.5:
        randomizer = -0.5
    morph = (randomizer >= 0)

    enemy_pos_list = set()
    for enemy in enemy_list:
        # 把敌人的坐标都先存下来，方便比较
        enemy_pos_list.add(enemy.pos)

        # 朝向的默认值
        enemy.next_chase_facing = None

    # # 先来个默认值
    # for enemy in enemy_list:
    #     enemy.next_chase_facing = None

    # 然后全图bfs
    enemy_count = len(enemy_list)
    reached_enemy_count = 0

    frontier = [start_point]
    reached = [start_point]

    while len(frontier):
        current = frontier.pop(0)
        for next in get_neighbours(current, morph):
            if next not in reached:
                frontier.append(next)
                reached.append(next)
                if next in enemy_pos_list:
                    for enemy in enemy_list:
                        if next == enemy.pos:
                            # n: int = enemy_pos_list.index(next)
                            if next[0] < current[0]:
                                towards = "right"
                            elif next[0] > current[0]:
                                towards = "left"
                            elif next[1] < current[1]:
                                towards = "down"
                            elif next[1] > current[1]:
                                towards = "up"
                            else:
                                print("Error in pathfinding")
                                raise

                            enemy.next_chase_facing = towards

                            reached_enemy_count += 1
                            if reached_enemy_count == enemy_count:
                                return

    # 如果现在有enemy没被给一个next_chase_facing，就是None了
    pass


# 敌人
class Enemy:
    def __init__(self, pos, facing, _type, stun=0, countdown=0, can_attack_bombguy=True):
        self.pos = pos
        self.facing = facing
        self.type = _type
        # 给dashguy（一直）、gunguy（刚出场）和bomb（爆炸倒数）用的
        self.stun = stun
        self.next_chase_facing = None
        # 给bombguy用的
        self.countdown = countdown
        # 给bomb用的
        self.can_attack_bombguy = can_attack_bombguy

    # 单独拎出来吧
    # 计算下一步这个敌人应该向哪边走
    # def ai(self):
    #     if self.type == "swordguy" or self.type == "gunguy":
    #         return get_astar(self.pos, player.pos)
    #     else:
    #         return choice(["up", "left", "down", "right"])
    #         pass


# 即将到来的敌人
class ComingEnemy:
    def __init__(self, pos, facing, _type, timer=3):
        self.pos = pos
        self.facing = facing
        self.type = _type
        self.timer = timer

    # 倒计时
    def tick(self):
        if self.timer >= 1:
            self.timer -= 1
        else:
            # if self.type == "swordguy":
            #     if _map.get(towards_pos(self.pos, self.facing)) == "wall":
            #         _map.set(towards_pos(self.pos, self.facing), "ground")

            add_enemy(self.pos, self.facing, self.type)
            coming_enemy_list.remove(self)


# 画出单个点
def draw_tile(p, tile, g=0):

    _x = p[0] * 16
    _y = p[1] * 20

    # if tile.startswith("sword"):
    #     eval("G6:=AFiles(\"" + tile + ".png" + "\")")
    #     strblit2(g, _x, _y, 16, 20, 6, 0, 0, 16, 20)
    #     pass
    # else:
    strblit2(g, _x, _y, 16, 20, 1, 16 * dict_tile_id[tile], 0, 16, 20)

    # strblit2(g, _x, _y, 16, 20, 1, 16 * dict_tile_id[tile], 0, 16, 20)
    # eval("BLIT_P(G" + str(g) + ", " + str(_x) + ", " + str(_y) + ", " + str(_x + 16) + ", " + str(_y + 20) +
    #      ", " + "G1" + ", " +str(16 * dict_tile_id[tile]) + ", " + "0" +
    #      ", " +str(16 * dict_tile_id[tile] + 16) + ", " + "20" + "0x114514)")


# g1是存贴图的
# main_map是绘制在g2上的
# map_changes存储了main_map有改动的点
# 每次更新画面的时候，先根据map_changes里的记录来更新g2
# 再把g2复制到g3
# 再在g3上绘制spirits
# （下面一直循环，直到有新的有效的按键输入为止）
# 把g3复制到g4，在g4上搞一些PostFX
# 最后上屏，即把g4复制到g0
# 闪屏的时候，把g0暂存到g5
# G6是用来中转读取的图像
# G7存状态栏
# G8存数字


# 重绘整个地图
def draw_map():
    # ground
    for i in range(map_width):
        for j in range(map_height):
            if main_map.get2(i, j) == "ground":
                draw_tile((i, j), "ground", 2)
            elif main_map.get2(i, j) == "wall":
                draw_tile((i, j), "wall", 2)
            elif main_map.get2(i, j) == "dead":
                draw_tile((i, j), "dead", 2)


# 更新画面
def draw_map_delta():
    sword_map = Map(map_width, map_height, None)
    sword_exists = False

    # update the map
    for change in map_changes:
        draw_tile(change[0], change[1], 2)

    # g2 -> g3
    blit(3, 0, 0, 2)

    # enemy
    # 先画bomb，因为它会被其他敌人覆盖掉
    for enemy in enemy_list:
        if enemy.type == "bomb":
            draw_tile(enemy.pos, "bombb", 3)  # bombx，x是1~7之间的数字，或者b，表示那个炸弹图标；加一个w后缀表示是白色的

    for enemy in enemy_list:
        tile = None

        if enemy.type == "swordguy":
            tile = "swordguy"

            # sword
            sword_exists = True
            pos = towards_pos(enemy.pos, enemy.facing)
            if enemy.facing in list_y_facing:
                if sword_map.get(pos) == "x" or sword_map.get(pos) == "x2":
                    sword_map.set(pos, "xy")
                elif sword_map.get(pos) == "y":
                    sword_map.set(pos, "y2")
                elif sword_map.get(pos) is None:
                    sword_map.set(pos, "y")

            else:
                if sword_map.get(pos) == "x":
                    sword_map.set(pos, "x2")
                elif sword_map.get(pos) == "y" or sword_map.get(pos) == "y2":
                    sword_map.set(pos, "xy")
                elif sword_map.get(pos) is None:
                    sword_map.set(pos, "x")

        elif enemy.type == "dashguy":
            tile = "dashguy"

        elif enemy.type == "gunguy":
            if enemy.facing == "up":
                tile = "gunguyu"
            elif enemy.facing == "left":
                tile = "gunguyl"
            elif enemy.facing == "down":
                tile = "gunguyd"
            elif enemy.facing == "right":
                tile = "gunguyr"

            if not enemy.stun:
                if is_valid_point(towards_pos(enemy.pos, enemy.facing)):
                    target_pos = raycast_with_sword(enemy.pos, enemy.facing)
                    target_pos = towards_pos(target_pos, enemy.facing)
                    current_pos = towards_pos(enemy.pos, enemy.facing)
                    while current_pos != target_pos:
                        red_flashing_points.append(current_pos)
                        current_pos = towards_pos(current_pos, enemy.facing)

                    if is_valid_point(current_pos):
                        red_flashing_points.append(current_pos)

        elif enemy.type == "bombguy":
            tile = "bombguy"
        elif enemy.type == "buildguy":
            tile = "buildguy"

        if tile is not None:
            draw_tile(enemy.pos, tile, 3)

    # player
    # draw_tile(player.pos, player.type)
    if player is not None:
        tile = "p"
        tile += player.type  # [:-3]
        tile += dict_facing_abbr[player.facing]
        draw_tile(player.pos, tile, 3)

        # sword
        if player.type == "sword":
            sword_exists = True
            pos = towards_pos(player.pos, player.facing)

            if player.facing in list_y_facing:
                if sword_map.get(pos) == "x" or sword_map.get(pos) == "x2":
                    sword_map.set(pos, "xy")
                elif sword_map.get(pos) == "y":
                    sword_map.set(pos, "y2")
                elif sword_map.get(pos) is None:
                    sword_map.set(pos, "y")

            else:
                if sword_map.get(pos) == "x":
                    sword_map.set(pos, "x2")
                elif sword_map.get(pos) == "y" or sword_map.get(pos) == "y2":
                    sword_map.set(pos, "xy")
                elif sword_map.get(pos) is None:
                    sword_map.set(pos, "x")
            # print(sword_map.get(pos))

    # coming enemy
    for coming_enemy in coming_enemy_list:
        tile = "n"
        tile += coming_enemy.type[:-3]
        tile += dict_facing_rev_abbr[coming_enemy.facing]
        draw_tile(coming_enemy.pos, tile, 3)

    # sword
    if sword_exists:
        for i in range(map_width):
            for j in range(map_height):
                if sword_map.get((i, j)) is not None:
                    draw_tile((i, j), dict_sword_tile[sword_map.get((i, j))], 3)


# 添加敌人的接口，以防以后存储敌人的方式要变
# 暂时把添加stun的逻辑也写在这儿了
def add_enemy(pos, facing, _type, stun=None, attack_bombguy=True):
    if _type == "swordguy":
        if main_map.get(towards_pos(pos, facing)) == "wall":
            main_map.set(towards_pos(pos, facing), "ground")

    if stun is None:
        if _type == "gunguy":
            enemy_list.append(Enemy(pos, facing, _type, 4))
        elif _type == "dashguy":  # 2 1是倒计时 0是即将dash
            enemy_list.append(Enemy(pos, facing, _type, randint(0, 2)))
        elif _type == "bomb":  # bomb爆炸前会倒数7回合
            enemy_list.append(Enemy(pos, facing, _type, 7, can_attack_bombguy=attack_bombguy))
        else:
            enemy_list.append(Enemy(pos, facing, _type))

    else:
        enemy_list.append(Enemy(pos, facing, _type, stun))


# 基本同上
def add_coming_enemy(pos, facing, _type, timer):
    coming_enemy_list.append(ComingEnemy(pos, facing, _type, timer))


# +1
def remove_enemy(enemy):
    enemy_list.remove(enemy)


# 添加新的敌人（自然生成）
# 如果timer>0，说明是ComingEnemy
def new_enemy(_type=None, timer=0):
    # 判断其可能在地图的哪条边上
    possible_direction = []
    if player.pos[0] > 0:
        possible_direction.append("left")
    if player.pos[0] < map_width - 1:
        possible_direction.append("right")
    if player.pos[1] > 0:
        possible_direction.append("up")
    if player.pos[1] < map_height - 1:
        possible_direction.append("down")

    # 随机摇一个type出来s
    if _type is None:
        global score
        if score >= 10:
            _type2 = choice(["swordguy", "dashguy", "gunguy", "swordguy", "dashguy", "gunguy", "bombguy", "buildguy"])
        else:
            _type2 = choice(["swordguy", "dashguy", "gunguy"])
        # _type2 = "buildguy"
        # _type2 = choice(["swordguy", "dashguy"])
    else:
        _type2 = _type

    # 随机摇一条边出来
    direction = choice(possible_direction)
    # 根据摇出来的边，随机出来一个坐标
    if direction == "left":
        pos = (0, randint(1, map_height - 2))
        facing = "right"
    if direction == "up":
        pos = (randint(1, map_width - 2), 0)
        facing = "down"
    if direction == "right":
        pos = (map_width - 1, randint(1, map_height - 2))
        facing = "left"
    if direction == "down":
        pos = (randint(1, map_width - 2), map_height - 1)
        facing = "up"

    # 判断这里是不是空位
    if is_no_entity_point(pos, True, True, True):
        # don't spawn enemy on wall
        if main_map.get(pos) == "wall":
            main_map.set(pos, "ground")

        # 人出来了再消
        # # don't spawn sword on wall
        # if _type2 == "swordguy":
        #     if _map.get(towards_pos(pos, facing)) == "wall":
        #         _map.set(towards_pos(pos, facing), "ground")
        if timer == 0:
            add_enemy(pos, facing, _type2)
        else:
            add_coming_enemy(pos, facing, _type2, timer)
    # 如果不是空位，就放弃本次尝试，再来一次
    else:
        new_enemy(_type, timer)


# def get_key():
#     # up, left, down, right, enter
#     key = keyboard()
#     return [key & (1 << 2), key & (1 << 7), key & (1 << 12), key & (1 << 8), key & (1 << 31)]
#     pass

# # 我还是用内置的GETKEY()吧，懒得造轮子了
# def get_key():
#     # up, left, down, right, enter
#     key = -1
#     while key == -1:
#         key = eval("WAIT()")
#     if key in dict_key_num_to_name:
#         return dict_key_num_to_name[key]
#     else:
#         return None


def get_key():
    # up, left, down, right, enter
    key = eval("GETKEY()")
    if key in dict_key_num_to_name:
        return dict_key_num_to_name[key]
    else:
        return None


def time():
    return eval("time")


# 攻击特定的敌人
def kill_enemy(enemy):
    if enemy.type == "bomb":
        # TODO 这儿这样偷懒一下应该没问题吧
        return

    global screen_flash
    screen_flash = True
    if player.type == "build":
        if main_map.get(towards_pos(player.pos, player.facing)) == "wall":
            main_map.set(towards_pos(player.pos, player.facing), "ground")
    player.type = enemy.type[:-3]
    if player.type != "bomb":
        player.cooldown = 0
    remove_enemy(enemy)  # first
    global score
    score += 1

    if player.type == "sword" or player.type == "build":  # second
        player_sword_touch(towards_pos(player.pos, player.facing), flash=False)
    if player.type == "build":
        if main_map.get(towards_pos(player.pos, player.facing)) == "ground":
            main_map.set(towards_pos(player.pos, player.facing), "wall")


# 考虑剑的raycast（不能穿过剑），返回停下来的地方的坐标（在障碍物面前，不是障碍物的坐标）
def raycast_with_sword(p, towards, add_flashing_pos=False, nth=0):
    next_pos = towards_pos(p, towards)
    next_tile = get_point(next_pos)

    if next_tile == "out" or next_tile == "wall" or next_tile == "player" or next_tile == "sword_player" or next_tile == "sword":
        return p
    elif type(next_tile) == Enemy:
        return p
    else:
        if add_flashing_pos and nth:
            # white_flashing_points.append([p, -1])
            white_flashing_points[p] = -1

        return raycast_with_sword(next_pos, towards, add_flashing_pos, nth + 1)


# 不考虑剑的raycast（能穿过剑），返回停下来的地方的坐标（在障碍物面前，不是障碍物的坐标）
def raycast_without_sword(p, towards, add_flashing_pos=False, nth=0):
    next_pos = towards_pos(p, towards)
    next_tile = get_point(next_pos)

    if next_tile == "out" or next_tile == "wall" or next_tile == "player":
        return p
    elif type(next_tile) == Enemy:
        return p
    else:
        if add_flashing_pos and nth:
            # white_flashing_points.append([p, -1])
            white_flashing_points[p] = -1

        return raycast_without_sword(next_pos, towards, add_flashing_pos, nth + 1)


# 处理敌人的剑扫过的单个点
def enemy_sword_touch(p):
    if main_map.get(p) == "wall":
        main_map.set(p, "ground")
    # white_flashing_points.append([p, -1])
    white_flashing_points[p] = -1


# 处理敌人的剑的扫动，只清理wall，不考虑碰到玩家
def enemy_sword_swing(enemy, towards):
    for delta_point in dict_sword_swing_points[enemy.facing][towards]:
        # swing_pos = delta_pos(enemy.pos, delta_point)
        swing_pos = delta_pos(enemy.pos, delta_point)
        if is_valid_point(swing_pos):
            enemy_sword_touch(swing_pos)


# 处理bomb爆炸触及的单个点
def enemy_bomb_touch(p, can_attack_bombguy=True):
    if can_attack_bombguy is None:
        can_attack_bombguy = True

    for enemy in enemy_list:
        if enemy.pos == p and enemy.type != "bomb" and (enemy.type != "bombguy" or can_attack_bombguy):
            kill_enemy(enemy)
    if player and player.pos == p:
        global do_exit
        do_exit = True
        return
    if main_map.get(p) == "wall":
        main_map.set(p, "ground")
    # white_flashing_points.append([p, -1])
    white_flashing_points[p] = -1


# 处理玩家的剑扫过的单个点
def player_sword_touch(p, break_wall=True, kill=True, flash=True):
    if break_wall and main_map.get(p) == "wall":
        main_map.set(p, "ground")

    if kill:
        for enemy in enemy_list:
            if p == enemy.pos:
                kill_enemy(enemy)
    if flash:
        # white_flashing_points.append([p, -1])
        white_flashing_points[p] = -1


# 处理玩家的剑的扫动.
def player_sword_swing(towards, break_wall=True, kill=True, flash=True):
    for delta_point in dict_sword_swing_points[player.facing][towards]:
        # swing_pos = delta_pos(player.pos, delta_point)
        swing_pos = delta_pos(player.pos, delta_point)
        if is_valid_point(swing_pos):
            player_sword_touch(swing_pos, break_wall, kill, flash)


# 把敌人向后推
def push_enemy_backwards(enemy):
    original_pos = enemy.pos
    towards = dict_facing_rev[enemy.facing]
    next_pos = towards_pos(enemy.pos, towards)
    next_tile = get_point(next_pos)
    if next_tile == "out" or next_tile == "wall" or next_tile == "player":
        return False
    elif type(next_tile) == Enemy:
        return False
    else:
        dest = raycast_without_sword(next_pos, towards, True)
        # print(dest.x, dest.y)
        enemy.pos = dest
        if enemy.stun == 0:
            enemy.stun = 1

        current_pos = original_pos
        while current_pos != dest:
            red_flashing_points.append(current_pos)
            current_pos = towards_pos(current_pos, towards)
            # white_flashing_points.append([current_pos, -1])
            white_flashing_points[current_pos] = -1

        #if is_valid_point(current_pos):
        #    gun_flashing_points.append(current_pos)

        return True


# 处理角色为sword的玩家的移动
def player_move_sword(key):
    # 返回操作是否成功
    # rotate
    if key == "left":
        player_sword_swing(key)
        player.facing = dict_facing_rotate_left[player.facing]
        return True

    elif key == "right":
        player_sword_swing(key)
        player.facing = dict_facing_rotate_right[player.facing]
        return True

    # forward
    elif key == "up":
        # deal with the tile in front of the player
        next_pos = towards_pos(player.pos, player.facing)
        next_sword_pos = towards_pos(towards_pos(player.pos, player.facing), player.facing)
        new_tile = get_point(next_pos)
        next_sword_tile = get_point(next_sword_pos)
        if new_tile == "out":
            # cancel the movement
            return False
        # 击剑是第一生产力
        elif new_tile == "sword":
            # well, that's confused
            for enemy in enemy_list:
                if enemy.type == "swordguy":
                    # 是不是面对面击剑
                    # TODO: 如果推不动，就要把屏幕晃几下
                    if next_pos == towards_pos(enemy.pos, enemy.facing):
                        if player.facing in list_x_facing and enemy.facing in list_x_facing:
                            if not push_enemy_backwards(enemy):
                                return False
                        elif player.facing in list_y_facing and enemy.facing in list_y_facing:
                            if not push_enemy_backwards(enemy):
                                return False

        elif next_sword_tile == "wall":
            # break the wall
            main_map.set(next_sword_pos, "ground")
        elif type(next_sword_tile) == Enemy:
            # kill the enemy
            kill_enemy(next_sword_tile)

        player.pos = next_pos
        return True

    # backwards
    elif key == "down":
        next_pos = towards_pos(player.pos, dict_facing_rev[player.facing])
        new_tile = get_point(next_pos)
        if (type(new_tile) == Enemy and new_tile.type != "bomb") == Enemy or new_tile == "out" or new_tile == "wall":
            # cancel the movement
            return False
        else:
            player.pos = towards_pos(player.pos, dict_facing_rev[player.facing])
            return True
        pass

    # action
    elif key == "enter":
        # 啥也干不了呀。。。
        return False


# 处理角色为dash的玩家的移动
def player_move_dash(key):
    # 返回操作是否成功
    # rotate
    if key == "left":
        player.facing = dict_facing_rotate_left[player.facing]
        return True

    if key == "right":
        player.facing = dict_facing_rotate_right[player.facing]
        return True

    elif key == "up":
        next_pos = towards_pos(player.pos, player.facing)
        new_tile = get_point(next_pos)
        if (type(new_tile) == Enemy and new_tile.type != "bomb") or new_tile == "out" or new_tile == "wall":
            # cancel the movement
            return False
        else:
            player.pos = next_pos
            return True

    elif key == "down":
        next_pos = towards_pos(player.pos, dict_facing_rev[player.facing])
        new_tile = get_point(next_pos)
        if (type(new_tile) == Enemy and new_tile.type != "bomb") == Enemy or new_tile == "out" or new_tile == "wall":
            # cancel the movement
            return False
        else:
            player.pos = next_pos
            return True

    # action
    elif key == "enter":
        next_pos = raycast_with_sword(player.pos, player.facing, True)
        next_facing_pos = towards_pos(next_pos, player.facing)
        next_facing_tile = get_point(next_facing_pos)
        if next_facing_tile == "wall":
            main_map.set(next_facing_pos, "ground")
            player.pos = next_pos
            return True
        elif type(next_facing_tile) == Enemy:
            # white_flashing_points.append([next_pos, -1])
            white_flashing_points[next_pos] = -1
            player.pos = next_facing_pos
            kill_enemy(next_facing_tile)
            return True
        elif next_facing_tile == "sword":
            game_over()
            return False
        elif next_facing_tile == "out":
            if not next_pos == player.pos:
                player.pos = next_pos
                return True
            else:
                return False
        pass
    pass


# 处理角色为gun的玩家的移动
def player_move_gun(key):
    # 基本和gun差不多
    # 返回操作是否成功

    # 移动起来都是一样的
    # rotate
    if key == "left":
        player.facing = dict_facing_rotate_left[player.facing]
        return True

    if key == "right":
        player.facing = dict_facing_rotate_right[player.facing]
        return True

    elif key == "up":
        next_pos = towards_pos(player.pos, player.facing)
        new_tile = get_point(next_pos)
        if (type(new_tile) == Enemy and new_tile.type != "bomb") or new_tile == "out" or new_tile == "wall":
            # cancel the movement
            return False
        else:
            player.pos = next_pos
            return True

    elif key == "down":
        next_pos = towards_pos(player.pos, dict_facing_rev[player.facing])
        new_tile = get_point(next_pos)
        if (type(new_tile) == Enemy and new_tile.type != "bomb") or new_tile == "out" or new_tile == "wall":
            # cancel the movement
            return False
        else:
            player.pos = next_pos
            return True

    # 只有技能部分有点不一样，不过反正都是要raycast的嘛，而且这个还简单些
    # action
    elif key == "enter":
        next_pos = raycast_with_sword(player.pos, player.facing, True)
        next_facing_pos = towards_pos(next_pos, player.facing)
        white_flashing_points[next_pos] = -1
        next_facing_tile = get_point(next_facing_pos)
        if next_facing_tile == "wall":
            main_map.set(next_facing_pos, "ground")
        elif type(next_facing_tile) == Enemy:
            kill_enemy(next_facing_tile)
            white_flashing_points[next_facing_pos] = -1
        return True
    pass

# 处理角色为bomb的玩家的移动
def player_move_bomb(key):
    # 基本和gun差不多
    # 返回操作是否成功

    # 妈的，之前写的的代码真一坨大便，以后得重构一下，改得更面向对象一点

    # 移动起来都是一样的
    # rotate
    if key == "left":
        player.facing = dict_facing_rotate_left[player.facing]
        return True

    if key == "right":
        player.facing = dict_facing_rotate_right[player.facing]
        return True

    elif key == "up":
        next_pos = towards_pos(player.pos, player.facing)
        new_tile = get_point(next_pos)
        if (type(new_tile) == Enemy and new_tile.type != "bomb") or new_tile == "out" or new_tile == "wall":
            # cancel the movement
            return False
        else:
            player.pos = next_pos
            return True

    elif key == "down":
        next_pos = towards_pos(player.pos, dict_facing_rev[player.facing])
        new_tile = get_point(next_pos)
        if (type(new_tile) == Enemy and new_tile.type != "bomb") or new_tile == "out" or new_tile == "wall":
            # cancel the movement
            return False
        else:
            player.pos = next_pos
            return True

    # 玩家可以在cooldown到0的时候马上再次放置炸弹
    # action
    elif player.cooldown <= 0 and key == "enter":
        add_enemy(player.pos, "up", "bomb", attack_bombguy=True)
        player.cooldown = 7
        return True
        pass
    pass


# 处理角色为build的玩家的移动
def player_move_build(key):
    # 先把面前的墙消掉
    wall_pos = towards_pos(player.pos, player.facing)
    wall_tile = get_point(wall_pos)
    if wall_tile == "wall":
        main_map.set(wall_pos, "ground")

    ret = False
    # rotate
    # 如果左边或者右边有方块，会转不了
    if key == "left":
        if main_map.get(delta_pos(player.pos, dict_towards_delta_pos[dict_facing_rotate_left[player.facing]])) == "wall":
            ret = False
        else:
            player_sword_swing("left", break_wall=False, flash=False)
            player.facing = dict_facing_rotate_left[player.facing]
            ret = True

    elif key == "right":
        if main_map.get(delta_pos(player.pos, dict_towards_delta_pos[dict_facing_rotate_right[player.facing]])) == "wall":
            ret = False
        else:
            player_sword_swing("right", break_wall=False, flash=False)
            player.facing = dict_facing_rotate_right[player.facing]
            ret = True

    elif key == "up":
        next_pos = towards_pos(player.pos, player.facing)
        new_tile = get_point(next_pos)
        if new_tile == "out":
            # cancel the movement
            ret = False
        else:
            player.pos = next_pos
            player_sword_touch(towards_pos(player.pos, player.facing), break_wall=False, flash=False)
            ret = True

    elif key == "down":
        next_pos = towards_pos(player.pos, dict_facing_rev[player.facing])
        new_tile = get_point(next_pos)
        if (type(new_tile) == Enemy and new_tile.type != "bomb") or new_tile == "out" or new_tile == "wall":
            # cancel the movement
            ret = False
        else:
            player.pos = next_pos
            ret = True

    # 只有技能部分有点不一样，不过反正都是要raycast的嘛，而且这个还简单些
    # action
    elif key == "enter":
        acted = False
        # 在函数的最前面已经把墙消掉了，所以玩家面前的墙不会影响raycast
        next_pos = raycast_without_sword(player.pos, player.facing, True)
        next_tile = get_point(next_pos)
        next_facing_pos = towards_pos(next_pos, player.facing)
        next_facing_tile = get_point(next_facing_pos)
        if type(next_facing_tile) == Enemy:
            kill_enemy(next_facing_tile)
            main_map.set(next_facing_pos, "wall")
            acted = True
        elif next_pos != towards_pos(player.pos, player.facing) and next_tile == "ground":
            main_map.set(next_pos, "wall")
            acted = True
        ret = acted

    # 算了，还是把生成方块的事儿放在player_move里面吧
    return ret


# 总管玩家的移动
def player_move(key):
    if key is None:
        return False

    is_success = False
    if player.type == "sword":
        is_success = player_move_sword(key)
    elif player.type == "dash":
        is_success = player_move_dash(key)
    elif player.type == "gun":
        is_success = player_move_gun(key)
    elif player.type == "bomb":
        is_success = player_move_bomb(key)
    elif player.type == "build":
        is_success = player_move_build(key)

    if is_success:
        if player and player.cooldown > 0:
            player.cooldown -= 1
    if player and player.type == "build":
        wall_pos = towards_pos(player.pos, player.facing)
        main_map.set(wall_pos, "wall")

    return is_success

# def where_to_go(original_facing, p1, p2):
#     if p1[0] < p2[0] and original_facing == "":


# 只根据坐标关系，判断应该向哪边旋转
def which_side_to_turn(original_facing, p1, p2):
    if dict_facing_to_xy[original_facing] == "x":
        if p1[1] <= p2[1]:
            return dict_side_to_turn[original_facing]["down"]
        else:
            return dict_side_to_turn[original_facing]["up"]

    else:
        if p1[0] <= p2[0]:
            return dict_side_to_turn[original_facing]["right"]
        else:
            return dict_side_to_turn[original_facing]["left"]


# swordguy的移动
def enemy_move_swordguy(enemy):
    global do_exit
    if enemy.stun > 0:
        enemy.stun -= 1
        return

    # 特殊情况判定，如果玩家是sword或build，并且这个敌人和玩家正在击剑，就原地不动
    # 因为在原版游戏里面
    # （1）玩家和敌人面对面的时候本来就走不动
    # （2）侧向击剑的时候敌人应该不会直接把玩家打死
    if player and (player.type == "sword" or player.type == "build") and entity_towards_pos(enemy) == entity_towards_pos(player):
        return

    # 检查能不能直接杀死玩家
    # 前
    next_facing = towards_pos(enemy.pos, enemy.facing)
    next_sword_pos = towards_pos(next_facing, enemy.facing)
    if player.pos == next_sword_pos:
        if not (player.type == "sword" and next_facing == towards_pos(player.pos, player.facing)):
            enemy.pos = next_facing
            # if _map.get(next_sword_pos) == "wall":
            #     _map.set(next_sword_pos, "ground")
            game_over()
        return

    # 左右
    if abs(player.pos[0] - enemy.pos[0]) + abs(player.pos[1] - enemy.pos[1]) <= 2:
        left_range = dict_sword_swing_points[enemy.facing]["left"]
        for delta_point in left_range:
            # point = delta_pos(enemy.pos, delta_point)
            point = delta_pos(enemy.pos, delta_point)
            if player.pos == point:
                enemy_sword_swing(enemy, "left")
                enemy.facing = dict_facing_rotate_left[enemy.facing]
                game_over()
                # TODO 这里可能会导致在玩家死的时候有些应该被破坏的wall没有被破坏，但应该影响不大，反正人都寄了
                return

        right_range = dict_sword_swing_points[enemy.facing]["right"]
        for delta_point in right_range:
            # point = delta_pos(enemy.pos, delta_point)
            point = delta_pos(enemy.pos, delta_point)
            if player.pos == point:
                enemy_sword_swing(enemy, "right")
                enemy.facing = dict_facing_rotate_right[enemy.facing]
                game_over()
                return

    # 看来是不能，那就靠近玩家
    next_facing = enemy.next_chase_facing
    # print(towards)
    if next_facing is None:
        # 寻不到路，直接放弃
        return
    elif next_facing == enemy.facing:
        # 向前走
        # 既然astar都叫它向前走，说明它人前面肯定是没墙的，但是剑会不会碰到墙就不一定了
        # TODO 可能有问题？
        # deal with the tile in front of the enemy
        next_pos = towards_pos(enemy.pos, enemy.facing)
        if not is_no_entity_point(next_pos, True, False, False, enemy):
            return

        # 处理移动后的剑会不会破墙的问题
        next_sword_pos = towards_pos(towards_pos(enemy.pos, enemy.facing), enemy.facing)
        next_sword_tile = get_point(next_sword_pos)

        if next_sword_tile == "wall":
            # break the wall
            main_map.set(next_sword_pos, "ground")

        enemy.pos = next_pos
    else:
        # 转向
        # 先看是不是向左或者向右
        if dict_facing_rotate_left[enemy.facing] == next_facing:
            enemy_sword_swing(enemy, "left")
            enemy.facing = next_facing
        elif dict_facing_rotate_right[enemy.facing] == next_facing:
            enemy_sword_swing(enemy, "right")
            enemy.facing = next_facing

        # 看来是要向后转。。。但是不能直接向后转，只能先向面朝玩家的方向转
        else:
            side_to_turn = which_side_to_turn(enemy.facing, enemy.pos, player.pos)
            if side_to_turn == "left":
                enemy_sword_swing(enemy, "left")
                enemy.facing = dict_facing_rotate_left[enemy.facing]
            else:
                enemy_sword_swing(enemy, "right")
                enemy.facing = dict_facing_rotate_right[enemy.facing]

        # if not dict_facing_rotate_back[enemy.facing] == next_facing:
        #     enemy.facing = next_facing
        # else:
        #     enemy.facing = dict_facing_rotate_right[enemy.facing]


# 写的什么东西啊我这是 /////
# # dashguy和gunguy共用的判断玩家是否在攻击范围内的逻辑
# def is_in_same_empty_line(p1, p2):
#     if p1.x == p2.x and p1.y == p2.y:
#         pass


# dashguy的移动
def enemy_move_dashguy(enemy):
    if enemy.stun > 0:
        enemy.stun -= 1
    else:
        enemy.stun = 2

        # 向四个方向raycast，看看能不能直接打中玩家
        # # 不过也不要浪费计算资源
        # 。。其实还不如直接astar？
        if enemy.pos == player.pos:
            game_over()
            return

        # facing = choice(["up", "left", "down", "right"])

        # facing = None
        # if enemy.pos.x == player.pos.x:
        #     if enemy.pos.y < player.pos.y:
        #         facing = "down"
        #     elif enemy.pos.y > player.pos.y:
        #         facing = "up"
        # elif enemy.pos.y == player.pos.y:
        #     if enemy.pos.x < player.pos.x:
        #         facing = "right"
        #     elif enemy.pos.x > player.pos.x:
        #         facing = "left"
        #
        # if facing is not None:
        #     next_pos = raycast_with_sword(enemy.pos, facing)
        #     next_facing_pos = towards_pos(next_pos, facing)
        #     next_facing_tile = get_point(next_facing_pos)

        # 草，原来dashguy也是用了astar
        facing = enemy.next_chase_facing
        if facing is None:
            if enemy.pos[0] == player.pos[0]:
                if enemy.pos[1] < player.pos[1]:
                    facing = "down"
                elif enemy.pos[1] > player.pos[1]:
                    facing = "up"
            elif enemy.pos[1] == player.pos[1]:
                if enemy.pos[0] < player.pos[0]:
                    facing = "right"
                elif enemy.pos[0] > player.pos[0]:
                    facing = "left"
            else:
                facing = choice(["up", "left", "down", "right"])

        original_pos = enemy.pos
        next_pos = raycast_with_sword(enemy.pos, facing, True)
        next_facing_pos = towards_pos(next_pos, facing)
        next_facing_tile = get_point(next_facing_pos)

        if next_facing_tile == "wall":
            if original_pos != next_pos:
                main_map.set(next_pos, "ground")
            enemy.pos = next_pos
        elif next_facing_tile == "out" or next_facing_tile == "sword" or type(next_facing_tile) == Enemy:
            enemy.pos = next_pos
        elif next_facing_tile == "sword_player":
            enemy.pos = next_facing_pos
            player_sword_touch(next_facing_pos, False)
        elif next_facing_tile == "player":
            # white_flashing_points.append([next_pos, -1])
            white_flashing_points[next_pos] = -1
            enemy.pos = next_facing_pos
            game_over()

        main_map.set(original_pos, "wall")
        main_map.set(enemy.pos, "ground")
    pass


# gunguy的移动
def enemy_move_gunguy(enemy):
    if enemy.stun > 0:
        enemy.stun -= 1
        return

    # 这个也和dashguy差不多

    # 先是dashguy的逻辑
    # 向四个方向raycast，看看能不能直接打中玩家
    # 不过也不要浪费计算资源
    if enemy.pos == player.pos:
        game_over()
        return

    facing = None
    if enemy.pos[0] == player.pos[0]:
        if enemy.pos[1] < player.pos[1]:
            facing = "down"
        elif enemy.pos[1] > player.pos[1]:
            facing = "up"
    elif enemy.pos[1] == player.pos[1]:
        if enemy.pos[0] < player.pos[0]:
            facing = "right"
        elif enemy.pos[0] > player.pos[0]:
            facing = "left"

    # 是否可以命中
    if facing is not None:
        next_pos = raycast_with_sword(enemy.pos, facing)
        next_facing_pos = towards_pos(next_pos, facing)
        next_facing_tile = get_point(next_facing_pos)

        if next_facing_tile == "player":
            enemy.facing = facing
            game_over()
            return

    # 没有命中，之后就是swordguy的逻辑了
    next_facing = enemy.next_chase_facing
    # print(towards)
    if next_facing is None:
        return
    elif next_facing == enemy.facing:
        # deal with the tile in front of the enemy
        next_pos = towards_pos(enemy.pos, enemy.facing)
        if not (is_no_entity_point(next_pos, True, False, False, enemy) and main_map.get(next_pos) == "ground"):
            return

        enemy.pos = next_pos
    else:
        if dict_facing_rotate_left[enemy.facing] == next_facing:
            enemy.facing = next_facing
        elif dict_facing_rotate_right[enemy.facing] == next_facing:
            enemy.facing = next_facing

        else:
            side_to_turn = which_side_to_turn(enemy.facing, enemy.pos, player.pos)
            if side_to_turn == "left":
                enemy.facing = dict_facing_rotate_left[enemy.facing]
            else:
                enemy.facing = dict_facing_rotate_right[enemy.facing]

    pass


# 曼哈顿距离
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


# 随机打乱一个列表，不使用内置的库，使用Knuth-Durstenfeld Shuffle
# 会直接打乱传入的列表，因为没有用深复制
def shuffle_list(list_to_shuffle):
    for i in range(len(list_to_shuffle) - 1, 0, -1):
        j = randint(0, i)
        list_to_shuffle[i], list_to_shuffle[j] = list_to_shuffle[j], list_to_shuffle[i]


# 计算逃跑的方向
# 不用寻路算法，就朝着玩家的反方向逃就行，如果路被堵了就随机走
def flee_facing(pos, wander=False):
    facing_list = []
    # 先计算理想情况下应该往哪边跑
    # 先把顺序弄出来
    # 如果位置和玩家位置重合，就随机排顺序咯
    if pos == player.pos or wander:
        facing_list = ["up", "left", "down", "right"]
        shuffle_list(facing_list)
    # 在同一条线上的时候，原版游戏是敌人优先避免在同一条线上，防止拿着远程武器的玩家直接去打死它
    # 如果在同一x坐标，即上下排列，则优先左右跑（两个东西顺序随机），其次反着跑，最后朝向玩家跑
    elif pos[0] == player.pos[0]:
        if random() > 0.5:
            facing_list.append("left")
            facing_list.append("right")
        else:
            facing_list.append("right")
            facing_list.append("left")
        if pos[1] < player.pos[1]:
            facing_list.append("up")
            facing_list.append("down")
        else:
            facing_list.append("down")
            facing_list.append("up")
    # 如果在同一y坐标，即左右排列，则优先上下跑（两个东西顺序随机），其次反着跑，最后朝向玩家跑
    elif pos[1] == player.pos[1]:
        if random() > 0.5:
            facing_list.append("up")
            facing_list.append("down")
        else:
            facing_list.append("down")
            facing_list.append("up")
        if pos[0] < player.pos[0]:
            facing_list.append("left")
            facing_list.append("right")
        else:
            facing_list.append("right")
            facing_list.append("left")

    # 不在同一直线上
    else:
        # 先看是优先左右逃还是优先上下逃，判断的依据是：哪个坐标轴上距离近，就优先拉开哪个坐标轴上的距离
        # 如果都一样就优先左右逃，因为地图横向比纵向长嘛
        if abs(pos[0] - player.pos[0]) <= abs(pos[1] - player.pos[1]):
            if pos[0] < player.pos[0]:
                facing_list.append("left")
                facing_list.append("right")
            else:
                facing_list.append("right")
                facing_list.append("left")
            if pos[1] < player.pos[1]:
                facing_list.insert(1, "up")
                facing_list.insert(2, "down")
            else:
                facing_list.insert(1, "down")
                facing_list.insert(2, "up")
        else:
            if pos[1] < player.pos[1]:
                facing_list.append("up")
                facing_list.append("down")
            else:
                facing_list.append("down")
                facing_list.append("up")
            if pos[0] < player.pos[0]:
                facing_list.insert(1, "left")
                facing_list.insert(2, "right")
            else:
                facing_list.insert(1, "right")
                facing_list.insert(2, "left")

    # 然后依次查看此方向上有没有路，如果有路就返回这个方向
    for facing in facing_list:
        delta = dict_towards_delta_pos[facing]
        new_pos = delta_pos(delta, pos)
        if is_valid_point(new_pos) and main_map.get(new_pos) != "wall":
            return facing
    return None


# bombguy的移动
def enemy_move_bombguy(enemy):
    if enemy.stun > 0:
        enemy.stun -= 1
        return

    # 移动逻辑：
    #     逃跑计时器=0:
    #         如果距离玩家的曼哈顿距离<=4：
    #             逃跑计时器设为7
    #             生成bomb
    #         追逐玩家
    #     否则：
    #         逃跑计时器-1
    #         逃离玩家（不用寻路算法，就朝着玩家的反方向逃就行，如果路被堵了就随机走）

    if enemy.pos == player.pos:
        game_over()
        return

    if enemy.countdown == 0:
        if manhattan_distance(enemy.pos, player.pos) <= 4:
            # 逃跑计时器设为7
            enemy.countdown = 7
            # 生成bomb
            add_enemy(enemy.pos, "up", "bomb", attack_bombguy=False)
        # 追逐玩家
        next_facing = enemy.next_chase_facing
    else:
        # 逃跑计时器-1
        enemy.countdown -= 1
        # 逃离玩家
        next_facing = flee_facing(enemy.pos)
    # print(towards)
    if next_facing is None:
        return
    enemy.facing = next_facing
    # bombguy没有朝向的问题，四个方向都能直接走
    next_pos = towards_pos(enemy.pos, enemy.facing)
    if not (is_no_entity_point(next_pos, True, False, False, False, enemy) and main_map.get(next_pos) != "wall"):
        return
    enemy.pos = next_pos


# bomb的移动
def enemy_move_bomb(enemy):
    # 实际上bomb并不会移动，因此只要倒数和爆炸就行了
    global do_exit
    if enemy.stun > 0:
        enemy.stun -= 1

    if enemy.stun == 0:  # 从1减到0后马上爆炸
        # 在所有敌人行动完了之后，再在enemy_move里面删除stun==0的bomb
        global screen_flash
        screen_flash = True
        for delta in list_3x3_delta_pos:
            pos = delta_pos(enemy.pos, delta)
            enemy_bomb_touch(pos, enemy.can_attack_bombguy)
            if do_exit:
                remove_enemy(enemy)
                game_over() # TODO 这里影响相对就有点大了，可能会导致该死的敌人没死，从而算分算漏，但也就先这样吧懒得改了
                return
    pass


# buildguy的移动
def enemy_move_buildguy(enemy):
    # stun：432走 1 不动 0边走边建
    if enemy.stun > 0:
        enemy.stun -= 1
    else:
        enemy.stun = 4

    if enemy.pos == player.pos:
        game_over()
        return

    # 建砖
    if enemy.stun == 0:
        main_map.set(enemy.pos, "wall")

    # 随机游走
    if enemy.stun != 1:
        next_facing = flee_facing(enemy.pos, wander=True)
        # print(towards)
        if next_facing is None:
            return
        enemy.facing = next_facing
        next_pos = towards_pos(enemy.pos, enemy.facing)
        if not (is_no_entity_point(next_pos, True, False, False, False, enemy) and main_map.get(next_pos) != "wall"):
            return
        enemy.pos = next_pos

    # 自己所在的地方不能是wall
    if main_map.get(enemy.pos) == "wall":
        main_map.set(enemy.pos, "ground")


# 总管enemy的移动
def enemy_move():
    global do_exit  # , astar_map
    # astar_map = [[node(i, j) for i in range(map_width)] for j in range(map_height)]

    pathfinding(player.pos)
    for enemy in enemy_list:
        if enemy.type == "swordguy":
            enemy_move_swordguy(enemy)
            if do_exit:
                return
        elif enemy.type == "dashguy":
            enemy_move_dashguy(enemy)
            if do_exit:
                return
        elif enemy.type == "gunguy":
            enemy_move_gunguy(enemy)
            if do_exit:
                return
        elif enemy.type == "bombguy":
            enemy_move_bombguy(enemy)
            if do_exit:
                return
        elif enemy.type == "bomb":
            enemy_move_bomb(enemy)
            if do_exit:
                return
        elif enemy.type == "buildguy":
            enemy_move_buildguy(enemy)
            if do_exit:
                return

    index = 0
    while index < len(enemy_list):
        enemy = enemy_list[index]
        if enemy.type == "bomb" and enemy.stun == 0:
            remove_enemy(enemy)
            index -= 1
        index += 1
    pass


# 计算面前的点的坐标
def towards_pos(p, facing):
    # print(type(p))
    # print(type(facing))
    # next_pos = delta_pos(dict_towards_delta_pos[facing], p)
    next_pos = delta_pos(dict_towards_delta_pos[facing], p)
    return next_pos
def entity_towards_pos(entity):
    # print(type(p))
    # print(type(facing))
    # next_pos = delta_pos(dict_towards_delta_pos[facing], p)
    next_pos = delta_pos(dict_towards_delta_pos[entity.facing], entity.pos)
    return next_pos


# GG
def game_over():
    global player, do_exit, red_flashing_points, screen_flash
    player = None
    screen_flash = True
    red_flashing_points = []
    draw_map_delta()
    write_flashing_points_start_time()
    postfx()
    # eval("TEXTOUT_P(\"GAME OVER!\",G0,0,0,7,#FFFF00,320,#000000)")
    draw_status_bar(0, True)
    # key = -1
    # while key == -1:
    #     key = eval("WAIT()")
    # do_exit = True

    while get_key() != "enter":
        pass
    do_exit = True

    pass


# 处理闪光啊，弹道啊之类的
def postfx():
    global screen_flash

    # 全屏闪光
    if screen_flash:
        # fillrect(0, 0, 0, 320, 240, #FFFFFF, #FFFFFF)
        eval("RECT_P(G0, 0, 0, 319, 239, #FFFFFF)")
        eval("WAIT(0.05)")
        screen_flash = False

    _time = time()

    # bomb闪烁，是画在G3里面的！
    bomb_white = ((_time % 0.4) < 0.2)
    bomb_number = ((_time % 0.6) < 0.4)
    for enemy in enemy_list:
        if enemy.type == "bomb":
            # TODO 先临时打个补丁，之后再修为什么会把bomb0画出来的问题
            if enemy.stun == 0:
                continue

            if not is_no_entity_point(enemy.pos, True, True, True, False):
                continue

            tile = "bomb"
            if bomb_number:
                tile += str(enemy.stun)
            else:
                tile += "b"
            if bomb_white:
                tile += "w"
            draw_tile(enemy.pos, tile, 3)

    # dashguy闪光，也是画在G3里面的
    for enemy in enemy_list:
        if enemy.type == "dashguy":
            if enemy.stun == 0:
                if (_time % 0.2) > 0.1:
                    draw_tile(enemy.pos, "dashguy_white", 3)
                else:
                    draw_tile(enemy.pos, "dashguy", 3)

    blit(4, 0, 0, 3)

    light = []
    # 在绘制闪光之前，先处理bomb每秒一次的闪光，将其添加到white_flashing_points中
    # 每秒中：前半秒一直是最亮，后半秒逐渐变暗
    # 用一个global变量当静态变量用，记录上一次闪光的时间
    global bomb_last_flash_time
    if _time - bomb_last_flash_time <= 0.5:
        for enemy in enemy_list:
            if enemy.type == "bomb":
                for delta in list_3x3_delta_pos:
                    pos = delta_pos(enemy.pos, delta)
                    white_flashing_points[pos] = _time
    elif _time - bomb_last_flash_time >= 1:
        bomb_last_flash_time = _time  # 如果用+= 1的话，刚开局的时候就不好处理了

    # gunguy以及玩家的弹道
    for i in red_flashing_points:
        _x = i[0] * 16
        _y = i[1] * 20
        color = 0xBDFF0000
        # fillrect(4, _x, _y, 16, 20, color, color)
        cmd = "RECT_P(G4, " + str(_x) + ", " + str(_y) + ", " + str(_x+15) + ", " + str(_y+19) + ", " + str(color) + ")"
        eval(cmd)

    # 闪光
    to_remove = []
    to_flash = []
    count = 0
    for key in white_flashing_points:
        if _time != 0 and _time - white_flashing_points[key] >= 0.5:
            to_remove.append(key)
            continue

        dot = key
        pos = [dot[0], dot[1]]
        alpha = floor(192 + 126 * (_time - white_flashing_points[key]))
        color = 0xFFFFFF + 0x01000000 * alpha
        if pos in to_flash:
            light[to_flash.index(pos)] = min(color, light[to_flash.index(pos)])
        else:
            to_flash.append(pos)
            light.append(color)
            count += 1

    for i in range(count):
        # 透明度从192变到255，总共0.5s
        _x = to_flash[i][0] * 16
        _y = to_flash[i][1] * 20
        color = light[i]
        # fillrect(4, _x, _y, 16, 20, color, color)
        cmd = "RECT_P(G4, " + str(_x) + ", " + str(_y) + ", " + str(_x+15) + ", " + str(_y+19) + ", " + str(color) + ")"
        eval(cmd)

    for key in to_remove:
        white_flashing_points.pop(key)

    # 上屏
    blit(0, 0, 0, 4)
    pass


def is_player_in_sword():
    if player is None:
        return True   # ??我之前为啥这么写的
    for enemy in enemy_list:
        if enemy.type == "swordguy":
            if player.pos == towards_pos(enemy.pos, enemy.facing):
                return True

    return False


def write_flashing_points_start_time():
    _time = time()
    for key in white_flashing_points:
        if white_flashing_points[key] == -1:
            white_flashing_points[key] = _time


def deal_with_player_gun_trajectory():
    global red_flashing_points

    if player:
        if player.type == "gun":
            if is_valid_point(towards_pos(player.pos, player.facing)):
                target_pos = raycast_with_sword(player.pos, player.facing)
                target_pos = towards_pos(target_pos, player.facing)
                current_pos = towards_pos(player.pos, player.facing)
                while current_pos != target_pos:
                    red_flashing_points.append(current_pos)
                    current_pos = towards_pos(current_pos, player.facing)

                if is_valid_point(current_pos):
                    red_flashing_points.append(current_pos)


# 打印状态栏
# 状态栏在地图的下方
# 高度是24像素（也就是一格）
# 宽度是320像素
# 底色：gun是64,64,0  sword是64,0,0  dash是0,64,0
# 字的颜色：gun是256,256,0  sword是256,0,0  dash是0,256,0
# def print_status_bar():
def draw_status_bar(g=0, is_game_over=False):
    if is_game_over:
        typeid = dict_type_name_to_id["gameover"]
    else:
        typeid = dict_type_name_to_id[player.type]

    # 先是栏本身
    strblit2(g, 0, 220, 320, 20, 7, 0, typeid * 20, 320, 20)

    # 然后是数字
    score_text = str(score)
    x = 320 - 64
    y = 20 * 11 + 5
    for character in score_text:
        number = int(character)
        strblit2(g, x, y, 12, 10, 8, number * 12, typeid * 10, 12, 10)
        x = x + 16

    pass



# 读取tiles文件夹中的贴图，并存入G1中
def read_tiles():
    # 先是方块
    global dict_tile_id
    dict_tile_id = {}
    # all_files: list = eval("AFiles(\"tiles\\\")")
    all_files = eval("AFiles()")
    tile_files = list()

    # print(all_files)

    # 把所有png文件选出来
    for file in all_files:
        if (not file.startswith("_")) and file.endswith(".png"):
            tile_files.append(file)

    sum = len(tile_files)
    # print(sum)
    eval("dimgrob_p(G1, " + str(16 * sum) + ", 20, #FFFFFFFFh)")
    # eval("dimgrob_p(G1, " + str(16 * sum) + ", 20, 0xFF")

    # eval("G1:=AFiles(\"tiles.png\")")
    # strblit2(g, _x, _y, 16, 20, 1, dict_tile_offset[tile], 0, 16, 20)
    index = 0
    for file in tile_files:
        # 把G6当作中转站
        eval("G6:=AFiles(\"" + file + "\")")
        # 把G6复制到G1的目标位置
        strblit2(1, index * 16, 0, 16, 20, 6, 0, 0, 16, 20)
        dict_tile_id[file[:-4]] = index
        index += 1

    # print(dict_tile_id)

    # 然后是状态栏
    eval("G7:=AFiles(\"_bar.png\")")
    eval("G8:=AFiles(\"_numbers.png\")")


# 核心循环
def core_loop():
    global do_exit, red_flashing_points, screen_flash
    do_exit = False
    new_enemy_timer = 3
    while not do_exit:
        sleep(0.005)
        
        # postfx
        postfx()
        key = get_key()
        if not player_move(key):
            continue

        # action
        if is_player_in_sword():
            game_over()
        if do_exit:
            return

        enemy_move()
        if do_exit:
            return

        if new_enemy_timer > 0 and len(enemy_list) + len(coming_enemy_list) >= 2 + score // 10:
            new_enemy_timer -= 1
        else:
            # new_enemy("swordguy", 3)
            new_enemy(None, 3)
            new_enemy_timer = 12

        for coming_enemy in coming_enemy_list:
            coming_enemy.tick()

        red_flashing_points = []
        draw_map_delta()
        deal_with_player_gun_trajectory()
        #
        # if screen_flash:
        #     blit(0, 0, 5, 0)

        write_flashing_points_start_time()
        draw_status_bar(3)
                
        pass


dimgrob(2, 320, 240, 0x000000)
dimgrob(3, 320, 240, 0x000000)
dimgrob(4, 320, 240, 0x000000)
dimgrob(5, 320, 240, 0x000000)

dict_tile_id = {}
read_tiles()

dict_sword_tile = {"x":  "swordx", "x2": "swordx2", "y": "swordy", "y2": "swordy2",
                   "xy": "swordxy"}
dict_facing_abbr = {"up": "u", "left": "l", "down": "d", "right": "r"}
dict_facing_rev_abbr = {"up": "d", "left": "r", "down": "u", "right": "l"}
dict_sword_swing_points = {"up":    {"left":  [(0, -1), (-1, -1), (-1, 0)],
                                     "right": [(0, -1), (1, -1), (1, 0)]},
                           "left":  {"left":  [(-1, 0), (-1, 1), (0, 1)],
                                     "right": [(-1, 0), (-1, -1), (0, -1)]},
                           "down":  {"left":  [(0, 1), (1, 1), (1, 0)],
                                     "right": [(0, 1), (-1, 1), (-1, 0)]},
                           "right": {"left":  [(1, 0), (1, -1), (0, -1)],
                                     "right": [(1, 0), (1, 1), (0, 1)]}}
dict_side_to_turn = {"up":    {"left":  "left", "right": "right"},
                     "left":  {"down":  "left", "up":    "right"},
                     "down":  {"right": "left", "left":  "right"},
                     "right": {"up":    "left", "down":  "right"}}
dict_key_num_to_name = {2: "up", 7: "left", 12: "down", 8: "right", 30: "enter",
                        18: "up", 23: "left", 24: "down", 25: "right", 21: "enter", 49: "enter",
                        39: "up", 14: "left", 34: "down", 17: "right"}
dict_towards_delta_pos = {"up": (0, -1), "left": (-1, 0), "down": (0, 1), "right": (1, 0)}
dict_facing_rev = {"up": "down", "left": "right", "down": "up", "right": "left"}
dict_facing_rotate_left = {"up": "left", "left": "down", "down": "right", "right": "up"}
dict_facing_rotate_right = {"up": "right", "left": "up", "down": "left", "right": "down"}
dict_facing_rotate_back = {"up": "down", "left": "right", "down": "up", "right": "left"}
dict_facing_to_xy = {"up": "y", "left": "x", "down": "y", "right": "x"}
dict_type_name_to_id = {"sword": 0, "gun": 1, "dash": 2, "bomb": 3, "build": 4, "gameover": 5}

list_x_facing = ["left", "right"]
list_y_facing = ["up", "down"]
list_facing = list_x_facing + list_y_facing
list_3x3_delta_pos = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]


while True:
    score = 0
    randomizer = 0
    bomb_last_flash_time = 0
    enemy_list = []
    coming_enemy_list = []
    screen_flash = False

    map_changes = []  # 每一项为[Point, string]
    white_flashing_points = {}  # 每一项为Point: start_time，先把其他逻辑处理完，再统一写入start_time
    red_flashing_points = []  # 每一项为Point

    main_map = MainMap(map_width, map_height, "wall")
    main_map.place_walls()
    # print(_map.map)

    # player = Player(Point(5, 5), "left", "sword")
    # player = Player(Point(5, 5), "left", "sword")
    player = Player((5, 5), "left", choice(["sword", "gun", "dash"]))
    main_map.set(player.pos, "ground")
    main_map.set(towards_pos(player.pos, player.facing), "ground")

    new_enemy("swordguy")
    new_enemy("swordguy")
    # new_enemy()
    # new_enemy()

    # add_enemy(Point(3,4), "up", "swordguy")
    # _map.set(Point(3,4), "ground")
    # _map.set(Point(3,3), "ground")

    # new_enemy(timer=3)
    # new_enemy(timer=3)

    # enemy_list += [Enemy("swordguy", Point(0, 7), "right")]
    # enemy_list += [Enemy("gunguy", Point(15, 3), "down")]
    #
    # enemy_list += [Enemy("swordguy", Point(0, 3), "right")]
    # enemy_list += [Enemy("swordguy", Point(2, 3), "left")]
    # _map.set(Point(1, 3), "ground")
    #
    # enemy_list += [Enemy("swordguy", Point(5, 0), "down")]
    # enemy_list += [Enemy("swordguy", Point(5, 2), "up")]
    # _map.set(Point(5, 1), "ground")
    #
    # enemy_list += [Enemy("swordguy", Point(12, 7), "right")]
    # enemy_list += [Enemy("swordguy", Point(14, 7), "left")]
    # enemy_list += [Enemy("swordguy", Point(13, 6), "down")]
    # _map.set(Point(13, 7), "ground")

    draw_map()
    draw_map_delta()
    draw_status_bar(3)

    core_loop()
