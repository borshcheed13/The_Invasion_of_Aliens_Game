from tkinter import *
from PIL import ImageTk, Image
from random import randrange, randint
from time import sleep
from tkinter import font
import screeninfo
import json

#*****************************************************************************
#                       КОНСТАНТЫ и ПЕРЕМЕННЫЕ
#*****************************************************************************
#Размеры окна
screen_info = screeninfo.get_monitors()
SCREEN_WIDTH = screen_info[0].width
SCREEN_HEIGHT = screen_info[0].height
#Габариты игрового поля
LEFT = 480
RIGHT = 1440
UP = 100
DOWN = SCREEN_HEIGHT-100
#Игра начата
game_has_started = False
#Переменные для сохранения экземпляров классов Rocket, Explosion
rocket = None
explosion = None
#Габариты виджетов
alien_width = 55
alien_height = 65
spaceship_width = 100
spaceship_height = 100
rocket_width = 20
rocket_height = 35
explosion_width = 20
explosion_height = 20
game_over_width = 800
game_over_height = 1200
#Минимальное расстояние между ракетой и инопланетным кораблем, после которого происходит детонация
distance_between_sprites = (alien_width + rocket_width)/2

#*****************************************************************************
#                       ФУНКЦИИ
#*****************************************************************************
def run_game():
    if game_has_started:
        space_ship.move_spaceship()
        aliens.move_fleet()
    if game_has_started:
        interface.updating_the_interfaces()
    if rocket is not None:
        rocket.move_rocket()
    if isinstance(explosion, Explosion):
        explosion.explosion_animation()

    create_window.root.after(50, run_game)

#*****************************************************************************
#                       КЛАССЫ
#*****************************************************************************
class CreateWindow:
    def __init__(self):
        global level
        '''Создание окна и холста'''
        #создание окна
        self.root = Tk()
        self.root.title("The Invasion of Aliens")
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.wm_attributes('-fullscreen', True)
        self.root.resizable(width=False, height=False)
        #создание холста
        self.cnv = Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="blue")
        self.cnv.place(x=0, y=0)
        #установка шрифта для Canvas
        self.font = font.Font(root=self.root, size=12, weight='bold')

    def background_settings(self):
        '''Метод для установки основного фона'''
        self.background = self.main_background(level)
        self.cnv.create_image(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, image=self.background)

    @staticmethod
    def main_background(level):
        '''функция для выбора основного фона окна в зависимости от уровня игры'''
        image1 = Image.open(r'all_picture/picture_background/background_1.png')
        image_resize1 = image1.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
        background_1 = ImageTk.PhotoImage(image_resize1)

        image = Image.open(r'all_picture/picture_background/background_2.png')
        image_resize2 = image.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
        background_2 = ImageTk.PhotoImage(image_resize2)

        image = Image.open(r'all_picture/picture_background/background_3.png')
        image_resize3 = image.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
        background_3 = ImageTk.PhotoImage(image_resize3)

        temporary_list = [background_1, background_2, background_3]
        backg = temporary_list[(level.level_id % 3) - 1]
        return backg

class Interface:
    def __init__(self):
        #Создание кнопки СТАРТ
        self.start_button = Button(create_window.cnv, text='СТАРТ', width=20, height=2, bg='maroon', fg='black', command=level.start_game, state=DISABLED, font=create_window.font)
        self.start_button.place(x=50, y=50)
        #Создание метки СЧЕТ ИГРЫ
        self.score_label = Label(create_window.cnv, text=f'СЧЕТ ИГРЫ: {gamer.score}', width=20, height=2, bg='brown', font=create_window.font)
        self.score_label.place(x=480, y=50)
        #Создание метки КОЛИЧЕСТВО ИНОПЛАНЕТЯН
        self.quantity_of_aliens_label = Label(create_window.cnv, text=f'КОЛИЧЕСТВО ИНОПЛАНЕТЯН: {aliens.quantity_of_aliens}', width=30, height=2, bg='Brown', font=create_window.font)
        self.quantity_of_aliens_label.place(x=800, y=50)
        #Создание метки УРОВЕНЬ
        self.level_label = Label(create_window.cnv, text=f'УРОВЕНЬ: {level.level_id}', width=20, height=2, bg='Brown', font=create_window.font)
        self.level_label.place(x=1235, y=50)
        #Создание метки УПРАВЛЕНИЕ
        self.control_label = Label(create_window.cnv, text=f'УПРАВЛЕНИЕ:\nesc - выйти из игры\n← - движение влево\n→ - движение вправо\nпробел - выстрел', width=20, height=5, bg='maroon', font=create_window.font)
        self.control_label.place(x=1665, y=50)

    def updating_the_interfaces(self):
        self.score_label['text'] = f'СЧЕТ ИГРЫ: {gamer.score}'
        self.quantity_of_aliens_label['text'] = f'КОЛИЧЕСТВО ИНОПЛАНЕТЯН: {aliens.quantity_of_aliens}'
        self.level_label['text'] = f'УРОВЕНЬ: {level.level_id}'

class Level:
    '''класс для подсчета уровней игры'''
    def __init__(self):
        self.level_id = 1

    def start_game(self):
        global game_has_started
        game_has_started = True
        interface.start_button['state'] = 'disabled'
        run_game()
    def next_level(self):
        global aliens, \
               space_ship
        self.level_id += 1
        interface.updating_the_interfaces()
        if self.level_id <=9:
            interface.start_button['state'] = 'active'
            create_window.background_settings()
            space_ship = SpaceShip()
            aliens = Aliens()
        else:
            self.you_win()
            gamer.show_ratings()

    def game_over(self):
        global game_has_started, \
                rocket, \
                aliens
        rocket = None
        #удаляем виджеты космического корабля и инопланетян
        create_window.cnv.delete(space_ship.id)
        for row in range(len(aliens.fleet_template)):
            for column in range(len(aliens.fleet_template[row])):
                if aliens.fleet_template[row][column] is not None:
                    create_window.cnv.delete(aliens.fleet[row][column])
        #рисуем виджет GAME OVER
        image = Image.open('all_picture/picture_game_over/game_over.png')
        image_res = image.resize((game_over_width, game_over_height))
        self.image_tk = ImageTk.PhotoImage(image_res)
        self.image_game_over = create_window.cnv.create_image(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, image=self.image_tk)
        create_window.root.update()
        sleep(1)
        gamer.show_ratings()
    def you_win(self):
        # create_window.cnv.destroy()
        self.cnv = Canvas(create_window.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.cnv.place(x=0, y=0)
        image_win = Image.open('all_picture/picture_you_win/pic_you_win.png')
        image_you_win_resize = image_win.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.image_you_win = ImageTk.PhotoImage(image_you_win_resize)
        self.cnv.create_image(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, image=self.image_you_win)
        gamer.show_ratings()
        create_window.root.update()

class Gamer:
    def __init__(self):
        self.score = 0

    def name_request(self):
        self.message = Message(create_window.cnv, width=400, text='ВВЕДИТЕ ВАШЕ ИМЯ И НАЖМИТЕ "ЗАПИСАТЬ"', bg='darkgoldenrod', font=create_window.font)
        self.message.place(x=750, y=455)
        self.name_entry = Entry(create_window.cnv, bg='darkgoldenrod', width=44, justify=CENTER, font=create_window.font)
        self.name_entry.focus()
        self.name_entry.place(x=750, y=500)
        self.button = Button(create_window.cnv, text='ЗАПИСАТЬ', bg='darkgoldenrod', width=39, command=self.save_name, font=create_window.font)
        self.button.place(x=750, y=545)

    def save_name(self):
        self.gamer_name = self.name_entry.get()
        self.message.destroy()
        self.name_entry.destroy()
        self.button.destroy()
        interface.start_button['state'] = NORMAL

    def player_ratings(self):
        best_players = json.load(open('PlayerRatings.json'))
        # проверяю, есть ли среди лучших новый игрок
        any_score = best_players.get(self.gamer_name, None)
        # если есть, то определяю максимальное количество очков
        if any_score is not None:
            self.score = max(any_score, self.score)
        # добавляю игрока с максимальным количеством очков в словарь
        best_players[self.gamer_name] = self.score
        # сортирую игроков по количеству набранных очков
        best_players_sorted = sorted(best_players.items(), key=lambda x: x[1], reverse=True)
        #создаю новый словарь с рейтингом игроков, десериализую и перезаписываю файл
        self.ten_players = {}
        for key, value in best_players_sorted[0:10]:
            self.ten_players[key] = value
        json.dump(self.ten_players, open('PlayerRatings.json', 'w'))
    def show_ratings(self):
        #выводим рейтинг игроков
        self.player_ratings()
        frame = Frame(create_window.root, bg='white', relief=SUNKEN, width=500, height=100, background='#%02x%02x%02x' % (175, 238, 238))
        frame.place(x=635, y=650)

        heading = Label(master=frame, text='ЛУЧШИЕ ИГРОКИ', font=('Helvetica', 15), bg='#%02x%02x%02x' % (95, 158, 160), width=57,
                    anchor=CENTER, relief=RIDGE, bd=3)
        heading.grid(row=0, columnspan=3)

        n = 0
        for name, score in self.ten_players.items():
            n += 1
            lbl = Label(master=frame, text=n, font=('Helvetica', 15), bg='#%02x%02x%02x' % (175, 238, 238), width= 5, anchor=CENTER, relief=RIDGE, bd=3)
            lbl.grid(row=n+1, column=0)
            lbl = Label(master=frame, text=name, font=('Helvetica', 15), bg='#%02x%02x%02x' % (175, 238, 238), width=30, anchor=CENTER, relief=RIDGE, bd=3)
            lbl.grid(row=n+1, column=1)
            lbl = Label(master=frame, text=score, font=('Helvetica', 15), bg='#%02x%02x%02x' % (175, 238, 238), width=20, anchor=CENTER, relief=RIDGE, bd=3)
            lbl.grid(row=n+1, column=2)

class SpaceShip:
    '''класс, создающий космический корабль игрока и описывающий его движение влево-вправо. При нажатии пробела инициирует создание ракеты'''
    def __init__(self):
        image = Image.open('all_picture/picture_spaceship/Space_Ship.png')
        image_res = image.resize((spaceship_width, spaceship_height))
        self.image_tk = ImageTk.PhotoImage(image_res)
        self.id = create_window.cnv.create_image(randrange(LEFT, RIGHT+1, 5), SCREEN_HEIGHT-100, image=self.image_tk)
        #задаю начальную скорость и направление космического корабля
        self.speed_x = 0
        #формирую управление космическим кораблем
        create_window.cnv.bind_all('<KeyPress-Left>', self.move_spaceship_to_left)
        create_window.cnv.bind_all('<KeyPress-Right>', self.move_spaceship_to_right)
        create_window.cnv.bind_all('<KeyPress-space>', self.shot_of_spaceship)
    def move_spaceship_to_left(self, event):
        self.speed_x = -5
    def move_spaceship_to_right(self, event):
        self.speed_x = 5
    def move_spaceship(self):
        create_window.cnv.move(self.id, self.speed_x, 0)
        self.spaceship_position = create_window.cnv.coords(self.id)
        if self.spaceship_position[0] < LEFT:
            self.speed_x = 0
        elif self.spaceship_position[0] > RIGHT:
            self.speed_x = 0
    def shot_of_spaceship(self, event):
        global rocket
        if isinstance(rocket, type(None)) and game_has_started:
            x, y = create_window.cnv.coords(self.id) #координаты космического корабля для создания в этой точке ракеты
            rocket = Rocket(x, y)

class Rocket:
    '''класс, создающий ракету и описывающий ее полет'''
    frame_number_explosion = 0
    def __init__(self, starting_x, starting_y):
        #начальные координаты ракеты соответствуют координатам космического корабля в момент нажатия пробела
        self.starting_x = starting_x
        self.starting_y = starting_y
        #список, в котором будут сохраняться картинки полета ракеты
        self.list_with_picture = []
        #переменная для перебора картинок полета ракеты
        self.picture_number = 0
        #скорость ракеты
        self.speed = 20
        #заполняю список картинками полета ракеты
        for i in range(4):
            image = Image.open(f'all_picture/picture_rocket/rocket0{i+1}.png')
            image_res = image.resize((rocket_width, rocket_height))
            self.image_tk = ImageTk.PhotoImage(image_res)
            self.list_with_picture.append(self.image_tk)
        #создаю спрайт ракеты на canvas и перемещаю ее в начальные координаты
        self.rocket_id = create_window.cnv.create_image(0, 0, image=self.list_with_picture[0])
        create_window.cnv.move(self.rocket_id, self.starting_x, self.starting_y - 60)

    def move_rocket(self):
        '''метод, который перемещает ракету по Canvas'''
        if create_window.cnv.coords(self.rocket_id)[1] <= UP:
            global rocket
            create_window.cnv.delete(self.rocket_id)
            rocket = None
        else:
            create_window.cnv.delete(self.rocket_id) #удаляю предыдущую картинку ракеты с Canvas
            self.starting_y -= self.speed
            self.picture_number += 1
            create_window.cnv.image = self.image_tk
            self.rocket_id = create_window.cnv.create_image(0, 0, image=self.list_with_picture[self.picture_number%4])
            create_window.cnv.move(self.rocket_id, self.starting_x, self.starting_y-60)
            self.detonation_of_the_rocket() #проверяем положение ракеты относительно положения инопланетян
    def detonation_of_the_rocket(self):
        '''метод, который рассчитывает расстояние между ракетой и каждым инопланетянином'''
        '''изменения при попадании ракеты в инопланетянина:
                - единица шаблона инопланетного флота (aliens.fleet_template) заменяется на None
                - уменьшается на единицу КОЛИЧЕСТВО ИНОПЛАНЕТЯН для класса Interface
                - удаляется виджет rocket
                - изменяется значение глобальной переменной rocket на None
                - создается экземпляр класса Explosion
                - увеличивается СЧЕТ игрока для класса Gamer'''
        global rocket, \
                explosion, \
                game_has_started

        rocket_x, rocket_y = create_window.cnv.coords(self.rocket_id)
        #перебираю флот инопланетян
        for row in range(len(aliens.fleet)):
            for column in range(len(aliens.fleet[row])):
                #если элемент в шаблоне флота - это виджет, а не None и не все инопланетянины уничтожены
                if aliens.fleet_template[row][column] is not None and aliens.quantity_of_aliens != 0:
                    #сохраняю в переменных координаты виджета
                    alien_x, alien_y = create_window.cnv.coords(aliens.fleet[row][column])
                    #рассчитываю расстояние между инопланетяниным и ракетой
                    distance = (abs(rocket_x - alien_x) ** 2 + abs(rocket_y - alien_y) ** 2) ** 0.5
                    #если расстояние меньше расстояния детонации
                    if distance <= distance_between_sprites:
                        #удаляю корабль инопланетян
                        aliens.fleet_template[row][column] = None
                        aliens.quantity_of_aliens -= 1
                        #удаляю виджет ракеты
                        create_window.cnv.delete(self.rocket_id)
                        rocket = None
                        #запускаю класс - имитация взрыва - и передаю в него текущие координаты ракеты
                        explosion = Explosion(rocket_x, rocket_y)
                        #прибавляю очки к общему счету игрока
                        gamer.score += 10
                        #если все инопланетяне уничтожены
                        if aliens.quantity_of_aliens == 0:
                            explosion = None
                            game_has_started = False
                            level.next_level()
                            break

class Explosion:
    '''класс имитации взрыва после детонации ракеты'''
    def __init__(self, x, y):
        #переменная для перебора кадров взрыва
        self.frame_number_explosion = 0
        #атрибуты с координатами взрыва
        self.explosion_coord_x = x
        self.explosion_coord_y = y
    def explosion_animation(self):
        global explosion
        self.frame_number_explosion += 1
        #если все кадры взрыва показаны на CANVAS, удаляю виджет
        if self.frame_number_explosion == 9:
            create_window.cnv.delete(self.explosion_id)
            explosion = None
        #иначе покадрово отрисовываю имитацию взрыва
        else:
            self.image_explosion = PhotoImage(file=f'all_picture/picture_explosion/expl0{self.frame_number_explosion}.png')
            self.explosion_id = create_window.cnv.create_image(self.explosion_coord_x, self.explosion_coord_y, image=self.image_explosion)

class Aliens:
    '''класс, создающий и управляющий флотом инопланетян. Флот инопланетян случайным образом генерится из 3 видов кораблей. Каждый корабль имеет две позы'''
    #переменная для смены позы корабля
    posture = 0
    def __init__(self):
        # генерируем шаблон флота tuple(тип, координата Х, координата Y)
        self.fleet_template = Aliens.generation_of_types_of_ships()
        # количество инопланетян
        self.quantity_of_aliens = len(self.fleet_template)*len(self.fleet_template[0])
        #создаем списки с картинками кораблей. Каждый из 3 видов корабля имеет две картинки - две позы
        image1 = ['all_picture/picture_aliens/inv01.png', 'all_picture/picture_aliens/inv02.png', 'all_picture/picture_aliens/inv03.png']
        self.first_position_of_the_aliens = Aliens.generation_of_texture_aliens(image1)
        image2 = ['all_picture/picture_aliens/inv01_move.png', 'all_picture/picture_aliens/inv02_move.png', 'all_picture/picture_aliens/inv03_move.png']
        self.second_position_of_the_aliens = Aliens.generation_of_texture_aliens(image2)
        # создаем макет флота
        self.fleet = [[None for _ in j] for j in self.fleet_template]
        #создаю нулевые атрибуты - общее смещение флота
        self.x_offset = 0
        self.y_offset = 0
        # начальное направление движения флота
        self.speed_x = 10
    def move_fleet(self):
        '''функция, перемещающая флот инопланетян'''
        global game_has_started
        #выбираю набор картинок из двух поз кораблей
        self.posture += 1
        if self.posture % 2 == 0:
            self.fleet_pose_pictures = self.first_position_of_the_aliens
        else:
            self.fleet_pose_pictures = self.second_position_of_the_aliens

        # каждый раз удаляем существующий флот и создаем новый, но в другой позе кораблей
        [create_window.cnv.delete(i) for j in self.fleet for i in j]
        for row in range(len(self.fleet_template)):
            for column in range(len(self.fleet_template[row])):
                if isinstance(self.fleet_template[row][column], tuple):
                    kind_of_fleet = self.fleet_template[row][column][0]
                    starting_position_X = self.fleet_template[row][column][1]
                    starting_position_Y = self.fleet_template[row][column][2]
                    self.fleet[row][column] = create_window.cnv.create_image((starting_position_X + self.x_offset), (starting_position_Y + self.y_offset), image=self.fleet_pose_pictures[kind_of_fleet - 1])

        # если количество инопланетян >0, актуализирую атрибуты, хранящие габаритные координаты флота инопланетян
        if self.quantity_of_aliens > 0:
            self.determining_the_coordinates_of_the_fleet()

        # если флот касается левой или правой границы игрового поля, то направление движения меняется на противоположное,
        # а флот опускается ниже
        if self.fleet_coordinates_left <= LEFT:
            self.x_offset += 10
            self.y_offset += 50
            self.speed_x = 10
        elif self.fleet_coordinates_right >= RIGHT:
            self.x_offset -= 10
            self.y_offset += 50
            self.speed_x = -10
        elif self.fleet_coordinates_down >= DOWN-(spaceship_width+alien_width/2):
            #если флот инопланетян опустился до космического корабля, то запускается метод GAME_OVER
            game_has_started = False
            create_window.root.update()
            sleep(1)
            level.game_over()

        else: #если флот находится где-то посередине
            self.x_offset += self.speed_x

    @staticmethod
    def generation_of_types_of_ships():
        '''метод случайным образом в зависимости от уровня игры генерирует виды кораблей инопланетян и рассчитывает координаты каждого корабля инопланетян'''
        #количество рядов и столбцов инопланетных кораблей в зависимости от уровня игры
        number_of_row = (level.level_id-1)//3 + 2
        number_of_columns = 2+level.level_id-1-(level.level_id-1)//3
        #генерация шаблона флота (№ вида каждого корабля инопланетян, координата x, координата y)
        fleet_template = [[(randint(1, 3), LEFT+column*100, UP+row*100) for column in range(number_of_columns)] for row in range(number_of_row)]
        return fleet_template
    @staticmethod
    def generation_of_texture_aliens(links):
        '''метод обрабатывает ссылки на картинки и возвращает список с картинками'''
        list_of_images = []
        for i in links:
            image = Image.open(i)
            image_res = image.resize((alien_width, alien_height))
            image_tk = ImageTk.PhotoImage(image_res)
            list_of_images.append(image_tk)
        return list_of_images

    def determining_the_coordinates_of_the_fleet(self):
        '''метод создает атрибуты с координатами углов габаритов флота'''
        list_of_coordinates = [create_window.cnv.coords(j) for i in self.fleet for j in i]
        filter_list_of_coordinates = list(filter(lambda x: len(x)!=0, list_of_coordinates))
        self.fleet_coordinates_left = min(map(lambda x: x[0], filter_list_of_coordinates))
        self.fleet_coordinates_right = max(map(lambda x: x[0], filter_list_of_coordinates))
        self.fleet_coordinates_down = max(map(lambda x: x[1], filter_list_of_coordinates))

#*****************************************************************************
#                       Основной код
#*****************************************************************************
#Создание экземпляров классов
create_window = CreateWindow()
level = Level()
create_window.background_settings()
gamer = Gamer()
gamer.name_request()
space_ship = SpaceShip()
aliens = Aliens()
interface = Interface()

#команда для экстренного закрытия окна
create_window.root.bind("<Escape>", lambda x: create_window.root.destroy())


create_window.root.mainloop()