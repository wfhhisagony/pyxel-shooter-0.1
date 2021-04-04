from _2_enemy import *
from _3_mytimer import *
from _4_player import *
from _5_powerbar import *
from _6_recruit import *
from _7_scoreboard import *
from _8_skill import *
from _9_utils import *


start_time = time.time()
mytime = myTimer(start_time)
pb = powerBar(20)
list_process = ListProcess()
sb = ScoreBoard()


# 碰撞检测与碰撞事件是在main中进行的
def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.alive:
            if isinstance(elem, GenralEnemy):
                if pb.current < pb.total:
                    pb.current += 1
            list.pop(i)
        else:
            i += 1

class Background:
    def __init__(self):
        self.star_list = []
        for i in range(STAR_COUNT):
            self.star_list.append(
                (random() * pyxel.width, random() * pyxel.height, random() * 1.5 + 1)
            )

    def update(self):
        for i, (x, y, speed) in enumerate(self.star_list):
            y += speed
            if y >= pyxel.height:
                y -= pyxel.height
            self.star_list[i] = (x, y, speed)

    def draw(self):
        for (x, y, speed) in self.star_list:
            pyxel.pset(x, y, STAR_COLOR_HIGH if speed > 1.8 else STAR_COLOR_LOW)


class Blast:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BLAST_START_RADIUS
        self.alive = True

        blast_list.append(self)

    def update(self):
        self.radius += 1

        if self.radius > BLAST_END_RADIUS:
            self.alive = False

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, BLAST_COLOR_IN)
        pyxel.circb(self.x, self.y, self.radius, BLAST_COLOR_OUT)


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="PPP")
        #向pyxel仓库中放入东西
        pyxel.image(0).set(
            0,
            0,
            [
                "00c00c00",
                "0c7007c0",
                "0c7007c0",
                "c703b07c",
                "77033077",
                "785cc587",
                "85c77c58",
                "0c0880c0",
            ],
        )

        pyxel.image(0).set(
            8,
            0,
            [
                "00088000",
                "00ee1200",
                "08e2b180",
                "02882820",
                "00222200",
                "00012280",
                "08208008",
                "80008000",
            ],
        )
        pyxel.image(0).load(16, 0, "assets/copyplayer.png")
        pyxel.image(1).load(0, 0, "assets/noguchi_tileset_128x128.png")
        pyxel.image(1).load(0, 128, "assets/boss1.png")
        pyxel.image(1).load(28, 128, "assets/boss2.png")
        pyxel.image(1).load(56, 128, "assets/boss3.png")
        pyxel.image(1).load(84, 128, "assets/skill3_1.png")
        pyxel.image(1).load(86, 128, "assets/skill3_2.png")
        pyxel.image(1).load(88, 128, "assets/skill3_3.png")

        pyxel.sound(0).set("a3a2c1a1", "p", "7", "s", 5)
        pyxel.sound(1).set("a3a2c2c2", "n", "7742", "s", 10)

        self.scene = SCENE_TITLE
        self.score = 0
        self.finish_time = -1
        self.background = Background()
        self.player = 0
        self.boss_come = False
        sb.setParent(self)

        # 循环执行update和draw
        pyxel.run(self.update, self.draw)

    # update中放入其它函数
    def update(self):
        self.background.update()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()
        elif self.scene == SCENE_WIN:
            self.update_win_scene()

    def update_title_scene(self):
        self.boss_come = False

        if pyxel.btnp(pyxel.KEY_1):
            mytime.reset()
            mytime.start_time = time.time()
            pb.set(15, 15)
            self.player = Player(pyxel.width / 2, pyxel.height - 20, 0, pb)
            self.scene = SCENE_PLAY

        elif pyxel.btnp(pyxel.KEY_2):
            mytime.reset()
            mytime.start_time = time.time()
            pb.set(20, 0)
            self.player = Player(pyxel.width / 2, pyxel.height - 20, 1, pb)
            self.scene = SCENE_PLAY

        elif pyxel.btnp(pyxel.KEY_3):
            mytime.reset()
            mytime.start_time = time.time()
            pb.set(10, 10)
            self.player = Player(pyxel.width / 2, pyxel.height - 20, 2, pb)
            self.scene = SCENE_PLAY


    def update_win_scene(self):
        list_process.update_list(bullet_list)
        list_process.update_list(enemy_list)
        list_process.update_list(blast_list)
        list_process.update_list(boss_list)
        list_process.update_list(recruit_list)

        cleanup_list(enemy_list)
        cleanup_list(bullet_list)
        cleanup_list(blast_list)
        cleanup_list(boss_list)
        cleanup_list(recruit_list)

        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_TITLE
            self.player.x = pyxel.width / 2
            self.player.y = pyxel.height - 20
            self.score = 0
            mytime.reset()

            enemy_list.clear()
            bullet_list.clear()
            blast_list.clear()
            boss_list.clear()
            recruit_list.clear()

    def update_play_scene(self):
        # 每0.5s 产生敌人
        if pyxel.frame_count % 30 == 0 and self.boss_come is False:
            # 随机位置
            if randrange(0, 10):
                Enemy(random() * (pyxel.width - PLAYER_WIDTH), 0, ENEMY_SPEED)
                Enemy(random() * (pyxel.width - PLAYER_WIDTH), 0, ENEMY_SPEED)
            else:
                Octopus(random() * (pyxel.width - PLAYER_WIDTH), 0)
            if randrange(0, 100) < 5:
                Recruit(randrange(10, 150),  randrange(0, 3), 0.75, ENEMY_SPEED)

        elif mytime.current >= BOSS_COME_TIME and self.boss_come is False:         # 100s 后 boss 降临
            Boss()
            self.boss_come = True
        if self.boss_come is True:
            if pyxel.frame_count % 24 == 0 and randrange(0, 10):
                Octopus(random() * (pyxel.width - PLAYER_WIDTH), 0)
            if randrange(0, 1000) < 5:
                Recruit(randrange(10, 150),  randrange(0, 3), 0.75, ENEMY_SPEED)
            if pyxel.frame_count % 300 == 0:
                Recruit(randrange(10, 150),  randrange(0, 3), 0.75, ENEMY_SPEED)

        for r in recruit_list:
            if collisionCheck(r, self.player):
                r.alive = False
                pyxel.play(1, 1)
                if r.number == 0:
                    self.player.status[1].release()
                elif r.number == 1:
                    self.player.status[2].release()
                elif r.number == 2:
                    self.player.status[3].release()

        for a in boss_list:
            for b in bullet_list:
                if (
                    a.x + a.w > b.x
                    and b.x + b.w > a.x
                    and a.y + a.h > b.y
                    and b.y + b.h > a.y
                ):
                    a.blood -= 1 if not isinstance(b, Laser) else 2
                    if a.blood <= 0:
                        a.alive = False
                        self.score += 1000
                        self.finish_time = mytime.current
                        self.scene = SCENE_WIN

                    b.alive = False if not isinstance(b, Laser) else True

                    blast_list.append(
                        Blast(b.x + BULLET_WIDTH / 2, b.y)
                    )
                    pyxel.play(1, 1)

        # 去撞boss
        for a in boss_list:
            if (
                    self.player.x + self.player.w > a.x
                    and a.x + a.w > self.player.x
                    and self.player.y + self.player.h > a.y
                    and a.y + a.h > self.player.y
            ):
                a.blood -= 1
                if a.blood <= 0:
                    a.alive = False
                    self.score += 1000
                    self.finish_time = mytime.current
                    self.scene = SCENE_WIN

                else:
                    self.scene = SCENE_GAMEOVER
                # 自爆
                blast_list.append(
                    Blast(
                        self.player.x + PLAYER_WIDTH / 2,
                        self.player.y + PLAYER_HEIGHT / 2,
                    )
                )
                pyxel.play(1, 1)

        # 判断是子弹与敌人是否相撞
        for a in enemy_list:
            for b in bullet_list:
                if (
                    a.x + a.w > b.x
                    and b.x + b.w > a.x
                    and a.y + a.h > b.y
                    and b.y + b.h > a.y
                ):
                    a.alive = False
                    b.alive = False if not isinstance(b, Laser) else True

                    blast_list.append(
                        Blast(a.x + ENEMY_WIDTH / 2, a.y + ENEMY_HEIGHT / 2)
                    )

                    pyxel.play(1, 1)

                    self.score += 10

        # 被敌人撞毁
        for enemy in enemy_list:
            if (
                self.player.x + self.player.w > enemy.x
                and enemy.x + enemy.w > self.player.x
                and self.player.y + self.player.h > enemy.y
                and enemy.y + enemy.h > self.player.y
            ):
                enemy.alive = False
                # 自爆
                blast_list.append(
                    Blast(
                        self.player.x + PLAYER_WIDTH / 2,
                        self.player.y + PLAYER_HEIGHT / 2,
                    )
                )

                pyxel.play(1, 1)

                self.scene = SCENE_GAMEOVER

        self.player.update()
        list_process.update_list(bullet_list)
        list_process.update_list(enemy_list)
        list_process.update_list(blast_list)
        list_process.update_list(self.player.status)
        list_process.update_list(boss_list)
        list_process.update_list(recruit_list)

        mytime.update()
        pb.update()
        sb.update()

        cleanup_list(enemy_list)
        cleanup_list(bullet_list)
        cleanup_list(blast_list)
        cleanup_list(boss_list)
        cleanup_list(recruit_list)

    def update_gameover_scene(self):
        list_process.update_list(bullet_list)
        list_process.update_list(enemy_list)
        list_process.update_list(blast_list)
        list_process.update_list(boss_list)
        list_process.update_list(recruit_list)

        cleanup_list(enemy_list)
        cleanup_list(bullet_list)
        cleanup_list(blast_list)
        cleanup_list(boss_list)
        cleanup_list(recruit_list)

        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_TITLE
            self.player.x = pyxel.width / 2
            self.player.y = pyxel.height - 20
            self.score = 0

            boss_list.clear()
            recruit_list.clear()
            enemy_list.clear()
            bullet_list.clear()
            blast_list.clear()

    def draw(self):
        pyxel.cls(0)

        self.background.draw()

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()
        elif self.scene == SCENE_WIN:
            self.draw_win_scene()

    def draw_win_scene(self):
        self.player.draw()
        list_process.draw_list(bullet_list)
        list_process.draw_list(enemy_list)
        list_process.draw_list(blast_list)
        list_process.draw_list(boss_list)
        list_process.draw_list(recruit_list)

        mytime.draw()
        pb.draw()
        sb.draw()

        list_process.draw_skill(self.player.status)

        pyxel.text(35, 66, "You Win", 8)
        pyxel.text(33, 80, "YOUR SCORE {0}".format(self.score), 12)
        pyxel.text(33, 90, "YOUR TIME {0}".format(self.finish_time), 12)
        # pyxel.text(33, 100, "Best SCORE {0}".format(file.read()),8)
        # pyxel.text(33, 110, "Best TIME {0}".format(file.read()),8)

        pyxel.text(10, 126, "- PRESS ENTER TO TRY AGAIN-", 13)

    def draw_title_scene(self):
        pyxel.text(26, 35, "Pyxel Shooter 0.1", pyxel.frame_count % 16)
        pyxel.text(23, 96, "- CHOOSE YOUR ROLE -", 15)
        pyxel.text(30, 116, "1 FOR SHADOW", 15)
        pyxel.text(30, 126, "2 FOR LASER", 15)
        pyxel.text(30, 136, "3 FOR TEMPO", 15)

    def draw_play_scene(self):
        self.player.draw()
        list_process.draw_list(bullet_list)
        list_process.draw_list(enemy_list)
        list_process.draw_list(blast_list)
        list_process.draw_list(boss_list)
        list_process.draw_list(recruit_list)

        mytime.draw()
        pb.draw()
        sb.draw()

        list_process.draw_skill(self.player.status)

    def draw_gameover_scene(self):
        list_process.draw_list(bullet_list)
        list_process.draw_list(enemy_list)
        list_process.draw_list(blast_list)
        list_process.draw_list(boss_list)
        list_process.draw_list(recruit_list)

        pyxel.text(40, 66, "GAME OVER", 8)
        pyxel.text(15, 126, "- PRESS ENTER RESTART-", 13)


if __name__ == '__main__':
    App()
