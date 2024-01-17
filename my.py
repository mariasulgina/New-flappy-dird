import pygame
import random
import os


# Класс для представления падающей фигуры
class FallingShape:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width  # Ширина
        self.height = height  # Высота
        self.color = color

    # Метод для отрисовки фигуры на экране
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])


# Основной класс игры
class FlappyGame:
    def __init__(self):
        self.player = None
        # Инициализация текущего игрока (1 или 2)
        self.current_player = 1
        pygame.init()

        # Настройки игрового окна
        self.width = 1000
        self.height = 500
        self.fps = 60
        self.pink = (150, 90, 100)
        self.pink1 = (150, 90, 230)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.white1 = (200, 200, 200)

        # Инициализация игрового окна
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.timer = pygame.time.Clock()  # Создание объекта для отслеживания времени

        pygame.display.set_caption('new flappy')

        # Загрузка изображений для фона игры
        self.ground = pygame.image.load('1703822962_gagaru-club-p-oblaka-piksel-art-oboi-24.png')
        self.ground_rect = self.ground.get_rect()

        # Настройка шрифта для отображения текста
        self.font = pygame.font.Font(None, 20)

        # Начальные параметры для игрока и движения
        self.playx = 50
        self.playy = 50
        self.y_change = 0
        self.jump_height = 15
        self.grav = 0.9
        self.obst = [400, 700, 1000, 1300, 1600]
        self.places = True
        self.y_pos = []
        self.game_over = False
        self.speed = 3
        self.score = 0
        self.best_score = self.load_best_score()

        # Настройки главного меню
        self.main_menu = True
        self.game_over_menu = False
        self.start_button_rect = pygame.Rect(400, 200, 200, 50)
        self.main_menu_background = pygame.image.load('1679595213_bogatyr-club-p-pikselnoe-more-foni-pinterest-3.png')

        # Настройки экрана завершения игры
        self.game_over_back = pygame.image.load('1617805905_19-p-pikselnii-fon-21.jpeg')

        self.difficulty = 1  # Уровень сложности: 1 - легкий, 2 - сложный
        self.pipe_distance = 280 if self.difficulty == 1 else 200  # Расстояние между трубами
        self.falling_shapes = []  # Список для хранения падающих фигур

        self.default_but_rect = pygame.Rect(400, 300, 200, 50)
        self.default_but_text = self.font.render('Выбрать уровень', True, self.white)
        self.difficulty_changed = False

        # Размах крыла
        self.wing_flap_offset = 30

        self.player_button_rect = pygame.Rect(10, 400, 200, 50)
        self.player_button_text = self.font.render('  Изменить персонажа', True, self.white)
        self.but_pressed = False

    def draw_main_menu(self):
        # Отображение главного меню
        self.screen.blit(self.main_menu_background, (0, 0))  # Отображение фона
        pygame.draw.rect(self.screen, self.pink, self.start_button_rect)
        start_text = self.font.render('Начать игру', True, self.white)
        self.screen.blit(start_text, (420, 210))

        # Изменение цвета кнопки на феолетовенький, если уровень сложности изменен
        but_color = self.pink
        if self.difficulty_changed:
            but_color = (200, 20, 255)
        pygame.draw.rect(self.screen, but_color, self.default_but_rect)
        self.screen.blit(self.default_but_text, (420, 310))

        # Сброс флага difficulty_changed на предыдущий цвет
        self.difficulty_changed = False

        dif_text = self.font.render('Уровень сложности: ' + str(self.difficulty), True, self.black)
        self.screen.blit(dif_text, (10, self.height - 30))

        # Отрисовка прямоугольника кнопки с цветом
        pygame.draw.rect(self.screen, self.pink, self.player_button_rect)
        self.screen.blit(self.player_button_text, (10, 410))

        # Меняем цвет кнопки при нажатии
        player_color = self.pink
        if self.but_pressed:
            player_color = (200, 20, 255)
            self.but_pressed = False  # Сброс состояния кнопки

        if self.current_player == 1:
            self.id = 'розовый'
        if self.current_player == 2:
            self.id = 'синий'

        dif_text1 = self.font.render('Персонаж: ' + str(self.id), True, self.black)
        self.screen.blit(dif_text1, (220, self.height - 30))

        pygame.draw.rect(self.screen, player_color, self.player_button_rect)
        self.screen.blit(self.player_button_text, (10, 410))

    # Загрузка лучшего результата из файла best_score.txt, если файл существует.
    def load_best_score(self):
        if os.path.exists('best_score.txt'):
            with open('best_score.txt', 'r') as file:
                try:
                    return int(file.read())
                except ValueError:
                    return 0
        else:
            return 0

    # Сохранение лучшего результата в файл
    def save_best_score(self):
        with open('best_score.txt', 'w') as file:
            file.write(str(self.best_score))

    # Функция изменения уровня сложности игры.
    def difficulty_f(self):
        if self.difficulty == 1:
            self.difficulty = 2
        else:
            self.difficulty = 1
        self.difficulty_changed = True

    def draw_game_over_menu(self):
        # Отрисовка экрана с сообщением об окончании игры и текущим результатом
        self.screen.fill(self.pink)
        self.screen.blit(self.game_over_back, (0, 0))
        game_over_text = self.font.render(' Игра окончена, попробуй еще', True, self.white)
        score_text = self.font.render('Оценка: ' + str(self.score), True, self.white)
        best_score_text = self.font.render('     Лучший результат: ' + str(self.best_score), True, self.white)
        self.screen.blit(game_over_text, (350, 150))
        self.screen.blit(score_text, (420, 250))
        self.screen.blit(best_score_text, (350, 300))
        restart_text = self.font.render('           Нажмите пробел, чтобы начать заново', True, self.white)
        self.screen.blit(restart_text, (280, 350))
        self.save_best_score()

    def toggle_player(self):
        # Функция для переключениями между игроком 1 и 2
        self.current_player = 3 - self.current_player
        self.but_pressed = True

    # Обработка событий в главном меню
    def main_menu_events(self, event):
        # Обработка событий главного меню при нажатии кнопки мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.start_button_rect.collidepoint(event.pos):  # Проверка на попадание в область кнопок
                    self.main_menu = False
                elif self.default_but_rect.collidepoint(event.pos):
                    self.difficulty_f()  # Изменение уровня сложности
                elif self.player_button_rect.collidepoint(event.pos):
                    self.toggle_player()

    # Обработка событий в меню завершения игры
    def game_over_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.reset_game()

    # Сброс параметров игры при перезапуске
    def reset_game(self):
        self.playy = 50
        self.playx = 50
        self.y_change = 0
        self.places = True
        self.obst = [400, 700, 1000, 1300, 1600]
        self.y_pos = []
        self.score = 0
        self.game_over = False
        self.main_menu = True
        self.game_over_menu = False
        # Установливаю начальное расстояние между трубами в зависимости от уровня сложности
        self.pipe_distance = 280 if self.difficulty == 1 else 200
        # Очищаем список падающих фигур при сбросе игры
        self.falling_shapes = []

    def draw_game(self):
        # Отображение фона
        self.screen.blit(self.ground, (0, 0))
        # Отрисовка игрока
        self.player = self.draw_player()
        # Отрисовка препятствий
        self.draw_obst()
        # Если уровень сложности равен 2, отображаем падающие фигуры
        if self.difficulty == 2:
            self.falling_shapes_f()

        # Обновление положения препятствий, сморем не вышли ли они за пределы поля
        for i in range(len(self.obst)):
            # Перемещение труб влево с учетом скорости игры
            if not self.game_over:
                self.obst[i] -= self.speed
                # Удаление труб и генерация новых при достижении левого края экрана
                if self.obst[i] < -30:
                    self.obst.remove(self.obst[i])
                    self.y_pos.remove(self.y_pos[i])
                    self.obst.append(random.randint(self.obst[-1] + 280, self.obst[-1] + 320))
                    self.y_pos.append(random.randint(0, 300))
                    self.score += 1

        if self.score > self.best_score:
            self.best_score = self.score

        if self.game_over:
            self.draw_game_over_menu()
        else:
            score_text = self.font.render('Счёт: ' + str(self.score), True, self.white)  # cxtn d ntxtybt buhs
            self.screen.blit(score_text, (10, self.height - 30))

        # Рисуем фигуры - квадраты
        for shape in self.falling_shapes:
            shape.draw(self.screen)

        # Проверяем, не превышает ли позиция птицы верхнюю границу экрана
        if self.playy < 0:
            self.playy = 0

    def falling_shapes_f(self):
        if random.randint(1, 100) < 2:  # Вероятность создания новой фигуры
            x = random.randint(0, self.width - 30)  # Рандомная координата x
            y = 0  # Начальная координата y
            width = random.randint(20, 30)  # Рандомная ширина фигуры
            height = random.randint(20, 30)  # Рандомная высота фигуры
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Рандомный цвет
            new_shape = FallingShape(x, y, width, height, color)
            self.falling_shapes.append(new_shape)

        for shape in self.falling_shapes:
            shape.y += 3  # Скорость падения фигуры

            if shape.y > self.height:  # Удаляю фигуру, если она вышла за пределы экрана
                self.falling_shapes.remove(shape)

    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            # Если нажата клавиша пробела и игра не окончена, выполняем прыжок
            if event.key == pygame.K_SPACE and not self.game_over:
                self.y_change = -self.jump_height
                self.flap_wings()
                if self.playy > 0:  # Проверяем, не превышает ли позиция птицы верхнюю границу экрана
                    self.y_change = -self.jump_height
                    self.flap_wings()
            if event.key == pygame.K_SPACE and self.game_over:
                self.reset_game()

    def flap_wings(self):
        self.wing_flap_offset = 15

    # Отрисовываем персонажа
    def draw_player(self):
        if self.current_player == 1:
            mouth = pygame.draw.circle(self.screen, self.white, (self.playx + 25, self.playy + 14), 12)
            play = pygame.draw.rect(self.screen, self.pink, [self.playx, self.playy, 30, 30], 0, 12)
            play1 = pygame.draw.rect(self.screen, self.white, [self.playx, self.playy, 30, 30], 1, 12)
            eye = pygame.draw.circle(self.screen, self.white, (self.playx + 23, self.playy + 10), 6, 2)
            eye1 = pygame.draw.circle(self.screen, self.black, (self.playx + 23, self.playy + 10), 4)
        else:
            mouth = pygame.draw.circle(self.screen, self.white, (self.playx + 26, self.playy + 14), 12)
            play = pygame.draw.rect(self.screen, (0, 0, 200), [self.playx, self.playy, 30, 30], 0, 12)
            play1 = pygame.draw.rect(self.screen, self.white, [self.playx, self.playy, 30, 30], 1, 12)
            eye = pygame.draw.circle(self.screen, self.white, (self.playx + 24, self.playy + 10), 6, 2)
            eye1 = pygame.draw.circle(self.screen, self.black, (self.playx + 24, self.playy + 10), 4)

        wing_height = 6
        wing_width = 15

        pygame.draw.rect(self.screen, (200, 200, 100),
                         [self.playx + 4, self.playy + 13 - self.wing_flap_offset, wing_width, wing_height], 0,
                         50)
        pygame.draw.rect(self.screen, (200, 50, 100),
                         [self.playx + 4, self.playy + 18 - self.wing_flap_offset, wing_width, wing_height], 0,
                         50)
        pygame.draw.rect(self.screen, (200, 90, 100),
                         [self.playx + 4, self.playy + 23 - self.wing_flap_offset, wing_width, wing_height], 0,
                         50)

        if self.wing_flap_offset > 0:
            self.wing_flap_offset -= 2

        # Рисую хвост птице
        if self.y_change < 0:
            pygame.draw.rect(self.screen, (200, 200, 100), [self.playx - 10, self.playy + 30, 15, 6], 0, 50)
            pygame.draw.rect(self.screen, (200, 50, 100), [self.playx - 10, self.playy + 15, 15, 6], 0, 50)
            pygame.draw.rect(self.screen, (200, 90, 100), [self.playx - 10, self.playy, 15, 6], 0, 50)

            pygame.draw.rect(self.screen, self.white, [self.playx - 10, self.playy + 31, 4, 2], 0, 1)
            pygame.draw.rect(self.screen, self.white, [self.playx - 10, self.playy + 16, 4, 2], 0, 1)
            pygame.draw.rect(self.screen, self.white, [self.playx - 10, self.playy + 1, 4, 2], 0, 1)

        return play

    def draw_obst(self):
        for i in range(len(self.obst)):
            y_coord = self.y_pos[i]
            if self.difficulty == 1:
                self.id1 = 200
            if self.difficulty == 2:
                self.id1 = 170

            top_rect = pygame.draw.rect(self.screen, self.pink1, [self.obst[i], 0, 30, y_coord])
            bot_rect = pygame.draw.rect(self.screen, self.pink1,
                                        [self.obst[i], y_coord + self.id1, 30, self.height - y_coord])
            top1 = pygame.draw.rect(self.screen, self.pink1, [self.obst[i] - 4, y_coord - 20, 38, 20], 0, 5)
            top2 = pygame.draw.rect(self.screen, self.pink1, [self.obst[i] - 4, y_coord + self.id1, 38, 20], 0, 5)

            top_rect3 = pygame.draw.rect(self.screen, self.white1, [self.obst[i], 0, 30, y_coord], 2)
            bot_rect4 = pygame.draw.rect(self.screen, self.white1,
                                         [self.obst[i], y_coord + self.id1, 30, self.height - y_coord], 2)
            top3 = pygame.draw.rect(self.screen, self.white1, [self.obst[i] - 4, y_coord - 20, 38, 20], 2, 5)
            top4 = pygame.draw.rect(self.screen, self.white1, [self.obst[i] - 4, y_coord + self.id1, 38, 20], 2, 5)

            if top_rect.colliderect(self.player) or bot_rect.colliderect(self.player):
                self.game_over = True

            # Рисую звезды
            for _ in range(4):
                x_star = random.randint(self.obst[i], self.obst[i] + 30)
                y_star = random.randint(0, self.height)
                alpha = random.randint(200, 255)  # Прозрачность
                star_color = (180, 180, 250, alpha)
                pygame.draw.circle(self.screen, star_color, (x_star, y_star), 1)

    def run(self):
        # Основной цикл игры
        running = True
        while running:
            # Ограничение частоты кадров
            self.timer.tick(self.fps)

            for event in pygame.event.get():
                # Обработка события закрытия окна
                if event.type == pygame.QUIT:
                    running = False

                # Обработка событий в зависимости от текущего состояния
                if self.main_menu:
                    self.main_menu_events(event)
                elif self.game_over_menu:
                    self.game_over_menu_events(event)
                else:
                    self.handle_game_events(event)

            # Обновление состояния игры, если не находится в главном меню и не в меню завершения игры
            if not self.main_menu and not self.game_over_menu:
                # Обновление позиции игрока и других элементов
                if self.playy + self.y_change < self.height - 30:
                    self.playy += self.y_change
                    self.y_change += self.grav
                else:
                    self.playy = self.height - 30

                # Инициализация начальных позиций препятствий
                if self.places:
                    for i in range(len(self.obst)):
                        self.y_pos.append(random.randint(0, 300))
                    self.places = False

                # Отрисовка текущего состояния игры
                self.draw_game()

                #  Обновляем расстояние между трубами в зависимости от уровня сложности
                if not self.game_over:
                    self.pipe_distance = 280 if self.difficulty == 1 else 200

            if self.main_menu:
                self.draw_main_menu()
            elif self.game_over_menu:
                self.draw_game_over_menu()

            pygame.display.flip()

        # Завершение игры при выходе из основного цикла
        pygame.quit()


if __name__ == '__main__':
    game = FlappyGame()
    game.run()
