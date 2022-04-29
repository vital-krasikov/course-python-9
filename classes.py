import random
from enum import Enum

# класс-перечисление для типов игроков
class PlayerType(Enum):
    HUMAN = 0
    CPU = 1


# класс Player моделирует поведение игрока и хранит все его данные
class Player:

    def __init__(self, player_type, player_num):
        self.type = player_type
        self.card = []
        self.alias = ("Игрок " if player_type == PlayerType.HUMAN else "Комп ") + str(player_num)
        self.lost = False
        self.dash_count = 0

    def get_type(self):
        return self.type

    def set_card(self, card):
        self.card = card

    def get_card(self):
        return self.card

    #def set_alias(self, alias):
    #    self.alias = alias

    def get_alias(self):
        return self.alias

    # get lost XD
    def get_lost(self):
        return self.lost

    def get_dash_count(self):
        return self.dash_count

    def check(self, number, check_by_hand=False):
        if self.type == PlayerType.CPU:
            for i in range(3):
                if number in self.card[i]:
                    self.card[i][self.card[i].index(number)] = 99
                    self.dash_count += 1
                    return
        else:
            for i in range(3):
                if number in self.card[i]:
                    if check_by_hand:
                        self.card[i][self.card[i].index(number)] = 99
                        self.dash_count += 1
                    else:
                        self.lost = True
                    return
            if check_by_hand:
                self.lost = True


#  класс Session реализует основной функционал игры и обеспечивает взаимодействие
#  между игроками, а также пользовательский интерфейс. Объект класса соответствует одной игровой сессии
class Session:

    def __init__(self, players_list):

        self.num_of_lost = 0

        self.players = players_list
        for p in players_list:
            p.set_card(self.generate_card())

    def run(self):
        App.print_start()
        bag_of_nums = [i+1 for i in range(90)]

        while True:
            num = random.sample(bag_of_nums, 1)[0]
            bag_of_nums.remove(num)
            App.print_new_num(num, len(bag_of_nums))
            for player in self.players:
                if not player.get_lost():
                    App.print_card(player.get_alias(), player.get_card())
            for player in self.players:
                if not player.get_lost():
                    self.player_turn(player, num)
                    if player.get_lost():
                        App.print_lose(player.get_alias())
                        self.num_of_lost += 1
                        if self.num_of_lost == len(self.players) - 1:
                            for p in self.players:
                                if not p.get_lost():
                                    App.print_win(p.get_alias())
                                    return

                if player.get_dash_count() == 15:
                    App.print_win(player.get_alias())
                    return

    @staticmethod
    def player_turn(player, num):
        if player.get_type() == PlayerType.HUMAN:
            move = App.input_move(player.get_alias())
            player.check(num, True if move == "y" or move == "Y" else False)
        else:
            player.check(num)

    @staticmethod
    def player_alias(player):
        if player.get_type() == PlayerType.HUMAN:
            return "Игрок"
        else:
            return "Компьютер"

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
        self.num_of_players = 2
        self.players = [PlayerType.HUMAN, PlayerType.CPU]

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
            print("1. Изменить количество игроков (текущее: "+str(self.num_of_players)+")")
            print("2. Изменить тип игрока (текущие: " + "".join([str(i+1) + " - " +
                ("чел; " if self.players[i] == PlayerType.HUMAN else "комп; ") for i in range(self.num_of_players)]) + ")")
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
                elif quantity > self.num_of_players:
                    for i in range(quantity - self.num_of_players):
                        self.players.append(PlayerType.CPU)
                self.num_of_players = quantity

            elif option == 2:
                try:
                    num = int(input("Тип какого игрока изменить? (введите номер) "))
                except ValueError:
                    print("Введите число от 1 до " + str(self.num_of_players) + "!")
                if 0 < num <= self.num_of_players:
                    self.players[num-1] = (PlayerType.HUMAN if self.players[num-1] == PlayerType.CPU else PlayerType.CPU)
                else:
                    print("Введите число от 1 до " + str(self.num_of_players) + "!")
            elif option == 3:
                players_list = []
                for i in range(self.num_of_players):
                    players_list.append(Player(self.players[i], i+1))
                session = Session(players_list[:self.num_of_players])
                session.run()
            elif option != 4:
                print("Введите число от 1 до 4!")





