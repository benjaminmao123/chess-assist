from package.utils import parser_constants
from package.utils import selector_constants

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import chess
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


def get_piece_color_from_node_element(element: WebElement) -> chess.Color:
    if not element:
        return None

    try:
        color_text = element.get_attribute("class").split(" ")[0]
    except StaleElementReferenceException:
        return None

    return parser_constants.NODE_COLOR_TO_CHESS_PIECE_COLOR[color_text]


def convert_uci_to_board_squares_as_int(uci: str) -> tuple:
    if not uci:
        return None

    return {
        "src": {"col": parser_constants.COLUMN_LETTER_TO_NUMBER[uci[0]], "row": int(uci[1])},
        "dst": {"col": parser_constants.COLUMN_LETTER_TO_NUMBER[uci[2]], "row": int(uci[3])},
    }


def get_promo_piece_element_from_uci(uci: str, promo_elements: list) -> WebElement:
    if not uci:
        return None

    piece_to_promote_to = uci[-1]

    try:
        for element in promo_elements:
            piece_name = element.get_attribute("class").split(" ")[1]

            if piece_to_promote_to.lower() in piece_name.lower():
                return element
    except StaleElementReferenceException:
        return None

    return None


def get_san_from_figurine(element: WebElement) -> str:
    if not element:
        return None

    try:
        span_element = element.find_element(By.CSS_SELECTOR, selector_constants.FIGURINE_SPAN)
    except NoSuchElementException:
        return element.text
    except StaleElementReferenceException:
        return None

    figurine_text = span_element.get_attribute("data-figurine")

    if not figurine_text:
        return element.text

    return figurine_text + element.text
