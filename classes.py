import random
from enum import Enum


# класс-перечисление для типов игроков
class PlayerType(Enum):
    HUMAN = 0
    CPU = 1


# класс Player моделирует поведение игрока и хранит все его данные
class Player:

    def __init__(self, player_type, player_num):
        self._type = player_type
        self._card = []
        self._alias = ("Игрок " if player_type == PlayerType.HUMAN else "Комп ") + str(player_num)
        self._lost = False
        self._dash_count = 0

    def __str__(self):
        return self._alias

    def __eq__(self, other):
        # в рамках нашей программы можно сравнивать только алиасы, но, вообще говоря, нужны какие-то уникальные ID
        return self._alias == str(other)

    @property
    def type(self):
        return self._type

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, card):
        self._card = card

    #def set_alias(self, alias):
    #    self.alias = alias

    # вместо свойства alias у нас теперь __str__, потому что логика та же
    #@property
    #def alias(self):
    #    return self._alias

    @property
    def lost(self):
        return self._lost

    @property
    def dash_count(self):
        return self._dash_count

    def check(self, number, check_by_hand=False):
        if self._type == PlayerType.CPU:
            for i in range(3):
                if number in self._card[i]:
                    self._card[i][self._card[i].index(number)] = 99
                    self._dash_count += 1
                    return
        else:
            for i in range(3):
                if number in self._card[i]:
                    if check_by_hand:
                        self._card[i][self._card[i].index(number)] = 99
                        self._dash_count += 1
                    else:
                        self._lost = True
                    return
            if check_by_hand:
                self._lost = True


#  класс Session реализует основной функционал игры и обеспечивает взаимодействие
#  между игроками, а также пользовательский интерфейс. Объект класса соответствует одной игровой сессии
class Session:

    def __init__(self, ID, players_list):

        self._num_of_lost = 0
        self._ID = ID

        self._players = players_list
        for p in players_list:
            p.card = self.generate_card()

    def __str__(self):
        return "Игровая сессия " + str(self._ID) + ". Игроки: " + str([str(p) for p in self._players])

    def __eq__(self, other):
        if self._ID != other.id:
            return False
        # сравниваем по набору игроков
        for player in self._players:
            if player not in other.players:
                return False
        return True

    # поскольку Session - это контейнер, добавим вычисление длины, проверку принадлежности и получение значения
    # по индексу

    def __len__(self):
        return len(self.players)

    def __contains__(self, item):
        return item in self.players

    def __getitem__(self, item):
        return self.players[item]

    @property
    def id(self):
        return self._ID

    @property
    def players(self):
        return self._players

    def run(self):
        App.print_start()
        bag_of_nums = [i+1 for i in range(90)]

        while True:
            num = random.sample(bag_of_nums, 1)[0]
            bag_of_nums.remove(num)
            App.print_new_num(num, len(bag_of_nums))
            for player in self._players:
                if not player.lost:
                    App.print_card(str(player), player.card)
            for player in self._players:
                if not player.lost:
                    self.player_turn(player, num)
                    if player.lost:
                        App.print_lose(str(player))
                        self._num_of_lost += 1
                        if self._num_of_lost == len(self._players) - 1:
                            for p in self._players:
                                if not p.lost:
                                    App.print_win(str(p))
                                    return

                if player.dash_count == 15:
                    App.print_win(str(player))
                    return

    @staticmethod
    def player_turn(player, num):
        if player.type == PlayerType.HUMAN:
            move = App.input_move(str(player))
            player.check(num, True if move == "y" or move == "Y" else False)
        else:
            player.check(num)

    @staticmethod
    def generate_card():
        card = []
        nums_d = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        nums_u = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # генерируем 3 ряда с цифрами, которые будут означать разряд десятков (в каждом ряду они не повторяются)
        for i in range(3):
            card.append(sorted(random.sample(nums_d, 5)))

        # добавляем к десяткам в каждом ряду разряд единиц (числа не будут повторяться, поскольку для каждого
        # десятка выбираем три разные цифры)
        for i in reversed(nums_d):
            digits = random.sample(nums_u, 3)
            for j in range(3):
                try:
                    ind = card[j].index(i)
                except ValueError:
                    continue
                else:
                    card[j][ind] = i * 10 + digits[j]

        # в реальной жизни число в карточке всегда стояло бы на позиции n + 1, где n - это цифра в разряде десятков
        # но тогда совсем неинтересно будет играть, поэтому генерируем промежутки между числами случайным образом
        for i in range(3):
            zero_pos = random.sample(nums_d, 4)
            for p in zero_pos:
                card[i].insert(p, 0)

        return card

    #def start(self):
        #end = False
        #while not end:


# класс App со статическими методами для пользовательского интерфейса - не знаю пока, как это положено делать в Python,
# поэтому пока так
class App:

    def __init__(self):
        self._num_of_players = 2
        self._players = [PlayerType.HUMAN, PlayerType.CPU]
        self._session_num = 0

    def __str__(self):
        return "Игра Лото. Текущая сессия - " + str(self._session_num)

    def __eq__(self, other):
        return self._num_of_players == other.num_of_players and self._players == other.players and \
               self._session_num == other.session_num

    @property
    def num_of_players(self):
        return self._num_of_players

    @property
    def players(self):
        return self._players

    @property
    def session_num(self):
        return self._session_num

    @staticmethod
    def print_start():
        print("Началась новая игра!")

    @staticmethod
    def print_card(alias, card):
        print("-"*(8-len(alias)//2)+" Карточка игрока "+alias+" " + "-"*(7-len(alias)//2))

        for i in range(3):
            s = ''
            for j in range(9):
                if card[i][j] == 0:
                    s += ' \t'
                elif card[i][j] == 99:
                    s += '-\t'
                else:
                    s += str(card[i][j])+'\t'
            print(s)
        print("----------------------------------")

    @staticmethod
    def print_new_num(num, remains):
        print("Новый бочонок: " + str(num) + " (осталось " + str(remains) + ")")

    @staticmethod
    def input_move(alias):
        return input(alias + " - зачеркнуть число? (y/n) ")

    @staticmethod
    def print_lose(alias):
        input(alias + " проиграл!")

    @staticmethod
    def print_win(alias):
        input("Игра окончена! " + alias + " победил")

    def run(self):
        option = 0
        while option != 4:
            print("1. Изменить количество игроков (текущее: "+str(self._num_of_players)+")")
            print("2. Изменить тип игрока (текущие: " + "".join([str(i+1) + " - " +
                ("чел; " if self._players[i] == PlayerType.HUMAN else "комп; ") for i in range(self._num_of_players)]) + ")")
            print("3. Начать игру")
            print("4. Выход")
            try:
                option = int(input("> "))
            except ValueError:
                print("Введите число от 1 до 4!")
                continue
            if option == 1:
                try:
                    quantity = int(input("Введите новое количество игроков (> 1) "))
                except ValueError:
                    print("Число игроков должно быть больше 1!")
                    continue
                if quantity <= 1:
                    print("Число игроков должно быть больше 1!")
                    continue
                elif quantity > self._num_of_players:
                    for i in range(quantity - self._num_of_players):
                        self._players.append(PlayerType.CPU)
                self._num_of_players = quantity

            elif option == 2:
                try:
                    num = int(input("Тип какого игрока изменить? (введите номер) "))
                except ValueError:
                    print("Введите число от 1 до " + str(self._num_of_players) + "!")
                if 0 < num <= self._num_of_players:
                    self._players[num-1] = (PlayerType.HUMAN if self._players[num-1] == PlayerType.CPU else PlayerType.CPU)
                else:
                    print("Введите число от 1 до " + str(self._num_of_players) + "!")
            elif option == 3:
                players_list = []
                for i in range(self._num_of_players):
                    players_list.append(Player(self._players[i], i+1))
                self._session_num += 1
                session = Session(self._session_num, players_list[:self._num_of_players])
                print(session)
                session.run()
            elif option != 4:
                print("Введите число от 1 до 4!")





