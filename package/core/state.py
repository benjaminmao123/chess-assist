from package.core.chess_board import ChessBoard
from package.core.chess_engine_handler import ChessEngineHandler
from package.core.player import Player
from package.utils import web_interaction
from package.utils import parser
from package.utils import selector_constants

from abc import ABC
import chess
from selenium.webdriver import Chrome
import keyboard
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


class State(ABC):
    NONE = 0
    PLAYING = 1
    NOT_PLAYING = 2

    def __init__(
        self,
        settings: dict = None,
        state: int = NONE,
        driver: Chrome = None,
        chess_engine_handler: ChessEngineHandler = None,
        chess_board: ChessBoard = None,
    ) -> None:
        self._settings = settings
        self._state = state
        self._driver = driver
        self._chess_engine_handler = chess_engine_handler
        self._chess_board = chess_board
        self._player = None

    def update(self) -> None:
        pass

    def get_state_value(self) -> int:
        return self._state


class StateNotPlaying(State):
    def __init__(
        self,
        settings: dict = None,
        state: int = State.NOT_PLAYING,
        driver: Chrome = None,
        chess_engine_handler: ChessEngineHandler = None,
        chess_board: ChessBoard = None,
    ) -> None:
        super().__init__(settings, state, driver, chess_engine_handler, chess_board)

    def update(self) -> None:
        super().update()


class StatePlaying(State):
    def __init__(
        self,
        settings: dict = None,
        state: int = State.PLAYING,
        driver: Chrome = None,
        chess_engine_handler: ChessEngineHandler = None,
        chess_board: ChessBoard = None,
    ) -> None:
        super().__init__(settings, state, driver, chess_engine_handler, chess_board)

        if self._chess_board.is_flipped():
            self._player = Player(chess.BLACK, self._driver)
        else:
            self._player = Player(chess.WHITE, self._driver)

        keyboard.on_press_key(self._settings["playNextMoveHotkey"], self.__update_manual_mode)

    def update(self) -> None:
        self.__update_automatic_mode()

    def __update_automatic_mode(self) -> None:
        if self._settings["automaticModeEnabled"]:
            self.__compute_and_play_best_move()

    def __update_manual_mode(self, event: keyboard.KeyboardEvent) -> None:
        if not self._settings["automaticModeEnabled"]:
            self.__compute_and_play_best_move()

    def __compute_and_play_best_move(self) -> None:
        if not self._player.is_turn():
            return

        self._chess_board.update_board()

        self._chess_engine_handler.set_fen(self._chess_board.get_fen())
        uci = self._chess_engine_handler.get_next_move()

        try:
            self._chess_board.push_uci(uci)
        except ValueError:
            return

        squares = parser.convert_uci_to_board_squares_as_int(uci)
        src_square = self._chess_board.get_square(squares["src"]["row"], squares["src"]["col"])
        dst_square = self._chess_board.get_square(squares["dst"]["row"], squares["dst"]["col"])

        ac = ActionChains(self._driver)
        ac.w3c_actions.pointer_action._duration = 0

        promotion_pieces = self._driver.find_elements(By.CSS_SELECTOR, selector_constants.PROMOTION_PIECE)

        if not promotion_pieces:
            web_interaction.perform_move(ac, self._chess_board.get_board_element(), src_square, dst_square)
            return

        promo_element = parser.get_promo_piece_element_from_uci(uci, promotion_pieces)

        if promo_element:
            web_interaction.perform_promotion(ac, promo_element)
        else:
            web_interaction.perform_move(ac, self._chess_board.get_board_element(), src_square, dst_square)
