from package.utils import parser
from package.utils import selector_constants

import chess
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


class Player:
    def __init__(self, color: chess.Color, driver: Chrome) -> None:
        self.__color = color
        self.__driver = driver

    def get_color(self) -> chess.Color:
        return self.__color

    def is_turn(self) -> bool:
        selected_node = self.__driver.find_elements(By.CSS_SELECTOR, selector_constants.NODE_SELECTED)

        if selected_node:
            selected_node = selected_node[0]
            selected_node_color = parser.get_piece_color_from_node_element(selected_node)

            return selected_node_color != self.get_color()

        if self.get_color() is chess.WHITE:
            return True

        return False
