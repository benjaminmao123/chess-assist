from package.utils import parser_constants
from package.utils import selector_constants

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import chess
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


def get_square_number_as_string(element: WebElement) -> tuple:
    if not element:
        return None

    try:
        square_number = element.get_attribute("class").split(" ")[2].split("-")[1]
    except StaleElementReferenceException:
        return None

    return {"col": square_number[0], "row": square_number[1]}


def get_square_number_as_int(element: WebElement) -> tuple:
    if not element:
        return None

    square_number = get_square_number_as_string(element)

    return {"col": int(square_number["col"]), "row": int(square_number["row"])}


def get_piece_name_from_element(element: WebElement) -> chess.PieceType:
    if not element:
        return None

    try:
        piece_name = element.get_attribute("class").split(" ")[1][1]
    except StaleElementReferenceException:
        return None

    return parser_constants.ELEMENT_PIECE_NAME_TO_CHESS_PIECE_NAME[piece_name]


def get_piece_color_from_element(element: WebElement) -> chess.Color:
    if not element:
        return None

    try:
        color_text = element.get_attribute("class").split(" ")[1][0]
    except StaleElementReferenceException:
        return None

    return parser_constants.ELEMENT_PIECE_COLOR_TO_CHESS_PIECE_COLOR[color_text]


def get_piece_from_element(element: WebElement) -> chess.Piece:
    if not element:
        return None

    return chess.Piece(get_piece_name_from_element(element), get_piece_color_from_element(element))


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
