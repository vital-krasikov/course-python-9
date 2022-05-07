import sys

from classes import PlayerType, Player, Session, App


class TestPlayer:
    def test_init(self):
        # игрок-человек
        player = Player(PlayerType.HUMAN, 1)
        assert player is not None and player._type == PlayerType.HUMAN \
               and player._card == [] and player._alias == "Игрок 1" and player._lost is False \
               and player._dash_count == 0
       # игрок-компьютер
        player = Player(PlayerType.CPU, 1)
        assert player is not None and player._type == PlayerType.CPU \
               and player._card == [] and player._alias == "Комп 1" and player._lost is False \
               and player._dash_count == 0

    def test_type(self):
        player = Player(PlayerType.HUMAN, 1)
        assert player.type == PlayerType.HUMAN

    def test_card(self):
        player = Player(PlayerType.HUMAN, 1)
        assert player.card == []

    def test_card_setter(self):
        player = Player(PlayerType.HUMAN, 1)
        player.card = [1, 2, 3, 4, 5]  # вообще говоря, не карточка, но нам неважно, мы сеттер тестируем
        assert player.card == [1, 2, 3, 4, 5]

    def test_alias(self):
        player = Player(PlayerType.HUMAN, 1)
        assert player.alias == "Игрок 1"

    def test_lost(self):
        player = Player(PlayerType.HUMAN, 1)
        assert player.lost is False

    def test_dash_count(self):
        player = Player(PlayerType.HUMAN, 1)
        assert player.dash_count == 0

    def test_check(self):
        player = Player(PlayerType.HUMAN, 1)

        player.card = [[2, 17, 0, 0, 41, 0, 60, 74, 83], [0, 0, 23, 0, 47, 50, 0, 77, 0],
                       [7, 18, 0, 0, 0, 55, 67, 0, 88]]
        player.check(17, True)
        assert player.card == [[2, 99, 0, 0, 41, 0, 60, 74, 83], [0, 0, 23, 0, 47, 50, 0, 77, 0],
                               [7, 18, 0, 0, 0, 55, 67, 0, 88]] and player.lost is False

        player.check(41, False)
        assert player.lost is True

        player = Player(PlayerType.HUMAN, 1)
        player.card = [[2, 17, 0, 0, 41, 0, 60, 74, 83], [0, 0, 23, 0, 47, 50, 0, 77, 0],
                       [7, 18, 0, 0, 0, 55, 67, 0, 88]]
        player.check(90, False)
        assert player.card == [[2, 17, 0, 0, 41, 0, 60, 74, 83], [0, 0, 23, 0, 47, 50, 0, 77, 0],
                       [7, 18, 0, 0, 0, 55, 67, 0, 88]] and player.lost is False
        player.check(90, True)
        assert player.lost is True

        player = Player(PlayerType.CPU, 1)

        player.card = [[2, 17, 0, 0, 41, 0, 60, 74, 83], [0, 0, 23, 0, 47, 50, 0, 77, 0],
                       [7, 18, 0, 0, 0, 55, 67, 0, 88]]
        player.check(17)
        assert player.card == [[2, 99, 0, 0, 41, 0, 60, 74, 83], [0, 0, 23, 0, 47, 50, 0, 77, 0],
                               [7, 18, 0, 0, 0, 55, 67, 0, 88]]
        player.check(40)
        assert player.card == [[2, 99, 0, 0, 41, 0, 60, 74, 83], [0, 0, 23, 0, 47, 50, 0, 77, 0],
                               [7, 18, 0, 0, 0, 55, 67, 0, 88]]


class TestSession:
    def test_init(self):
        player1 = Player(PlayerType.HUMAN, 1)
        player2 = Player(PlayerType.CPU, 2)

        session = Session([player1, player2])
        assert session is not None and session._num_of_lost == 0 and session._players == [player1, player2]

    # тестить run сложно, поскольку придется лезть в стандартные потоки ввода-вывода, не знаю, имеет ли это смысл
    # аналогичная ситуация с player_turn

    def test_player_alias(self):
        player1 = Player(PlayerType.HUMAN, 1)
        player2 = Player(PlayerType.CPU, 2)

        assert Session.player_alias(player1) == "Игрок" and Session.player_alias(player2) == "Компьютер"

    def test_generate_card(self):
        card = Session.generate_card()

        assert card is not None and len(card) == 3 and len(card[0]) == 9

        for row in card:
            for elem in row:
                assert 0 <= elem <= 99


class TestApp:
    def test_init(self):
        app = App()

        assert app is not None and app._num_of_players == 2 and app._players == [PlayerType.HUMAN, PlayerType.CPU]

    # Не знаю, как протестировать вывод в консоль, тот код, который закомментирован ниже - не работает!
    # def test_print_start(self):
    #     App.print_start()
    #     for line in sys.stdout:
    #         assert line == "Началась новая игра!"
