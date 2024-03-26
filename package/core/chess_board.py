from package.utils import selector_constants
from package.utils import parser

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Chrome
import chess


class ChessBoardSquare:
    def __init__(self, size: tuple, position: tuple) -> None:
        self.__size = size
        self.__position = position

    def get_size(self) -> tuple:
        return self.__size

    def get_width(self) -> int:
        return self.__size[0]

    def get_height(self) -> int:
        return self.__size[1]

    def get_position(self) -> tuple:
        return self.__position


class ChessBoard:
    def __init__(self, driver: Chrome) -> None:
        self.__driver = driver
        self.__board = chess.Board()
        self.__init_board()

    def __init_board(self) -> None:
        self.__board.reset()

        if self.is_flipped():
            self.__board_element = self.__driver.find_elements(By.CSS_SELECTOR, selector_constants.BOARD_FLIPPED)[0]
        else:
            self.__board_element = self.__driver.find_elements(By.CSS_SELECTOR, selector_constants.BOARD)[0]

        self.__init_board_squares()
        self.__update_nodes()

    def __init_board_squares(self) -> None:
        square_size = (self.__board_element.size["width"] / 8, self.__board_element.size["height"] / 8)
        self.__board_mapping = [[None] * 9 for _ in range(9)]

        for row, row_index in zip(
            range(
                self.__range_params["row_start"], self.__range_params["row_end"], self.__range_params["row_increment"]
            ),
            range(1, 9),
        ):
            for col, col_index in zip(
                range(
                    self.__range_params["col_start"],
                    self.__range_params["col_end"],
                    self.__range_params["col_increment"],
                ),
                range(1, 9),
            ):
                x = col * square_size[0]
                y = row * square_size[1]

                self.__board_mapping[row_index][col_index] = ChessBoardSquare(square_size, (x, y))

    def update_board(self) -> None:
        if self.__is_board_dirty():
            self.__init_board()

    def get_board_element(self) -> WebElement:
        return self.__board_element

    def is_flipped(self) -> bool:
        if self.__driver.find_elements(By.CSS_SELECTOR, selector_constants.BOARD_FLIPPED):
            self.__range_params = {
                "row_start": 0,
                "row_end": 8,
                "col_start": 7,
                "col_end": -1,
                "row_increment": 1,
                "col_increment": -1,
            }
            return True

        self.__range_params = {
            "row_start": 7,
            "row_end": -1,
            "col_start": 0,
            "col_end": 8,
            "row_increment": -1,
            "col_increment": 1,
        }
        return False

    def push_san(self, san: str) -> str:
        return self.__board.push_san(san).uci()

    def push_uci(self, uci: str) -> str:
        return self.__board.push_uci(uci)

    def get_fen(self) -> str:
        return self.__board.fen()

    def get_square(self, row: int, column: int) -> ChessBoardSquare:
        return self.__board_mapping[row][column]

    def print_board(self) -> None:
        print(self.__board)

    def __is_board_dirty(self) -> bool:
        self.__nodes = self.__driver.find_elements(By.CSS_SELECTOR, selector_constants.NODES)

        return len(self.__previous_nodes) != len(self.__nodes)

    def __update_nodes(self) -> None:
        self.__nodes = self.__driver.find_elements(By.CSS_SELECTOR, selector_constants.NODES)
        self.__previous_nodes = self.__nodes

        try:
            for node in self.__nodes:
                self.push_san(parser.get_san_from_figurine(node))
        except (ValueError, TypeError):
            pass
