from package.core.chess_board import *
from package.utils import web_interaction_constants

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement


def click_on_element(
    ac: ActionChains, element: WebElement, click_type: int = web_interaction_constants.LEFT_CLICK
) -> None:
    ac.move_to_element(element)

    if click_type == web_interaction_constants.LEFT_CLICK:
        ac.click()
    elif click_type == web_interaction_constants.RIGHT_CLICK:
        ac.context_click()


def click_on_square(
    ac: ActionChains,
    board_element: WebElement,
    square: ChessBoardSquare,
    click_type: int = web_interaction_constants.LEFT_CLICK,
) -> None:
    x = square.get_position()[0] + (square.get_width() // 2)
    y = square.get_position()[1] + (square.get_height() // 2)

    ac.move_to_element_with_offset(board_element, -board_element.size["width"] // 2, -board_element.size["height"] // 2)
    ac.move_by_offset(x, y)

    if click_type == web_interaction_constants.LEFT_CLICK:
        ac.click()
    elif click_type == web_interaction_constants.RIGHT_CLICK:
        ac.context_click()


def perform_move(
    ac: ActionChains,
    board_element: WebElement,
    src_square: ChessBoardSquare,
    dst_square: ChessBoardSquare,
) -> None:
    click_on_square(ac, board_element, src_square)
    click_on_square(ac, board_element, dst_square)
    ac.perform()


def perform_promotion(ac: ActionChains, promo_element: WebElement) -> None:
    click_on_element(ac, promo_element)
    ac.perform()
