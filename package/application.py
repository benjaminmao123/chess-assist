from package.core.chess_engine_handler import ChessEngineHandler
from package.core.state_manager import StateManager
from package.core.state import *
from package.utils import selector_constants

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import keyboard
import os
import sys
import json


class Application:
    def __init__(self, settings: dict) -> None:
        self.__settings = settings

        keyboard.on_press_key(self.__settings["automaticModeHotkey"], self.__on_automatic_mode_key_pressed)

    def run(self) -> None:
        chess_engine_handler = ChessEngineHandler(self.__settings)
        state_manager = StateManager()

        os.environ["WDM_LOG_LEVEL"] = "0"
        options = Options()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = Chrome(options)
        driver.get("https://www.chess.com/")

        while True:
            self.__update(driver, state_manager, chess_engine_handler)

    def __update(self, driver: Chrome, state_manager: StateManager, chess_engine_handler: ChessEngineHandler):
        if not self.__is_browser_open(driver):
            self.__quit(driver)

        self.__handle_user_input(driver, state_manager, chess_engine_handler)
        state_manager.update()

    def __handle_user_input(
        self, driver: Chrome, state_manager: StateManager, chess_engine_handler: ChessEngineHandler
    ) -> None:
        resign_element = driver.find_elements(By.XPATH, selector_constants.RESIGN)

        if state_manager.get_state().get_state_value() != State.PLAYING and resign_element:
            state_manager.set_state(
                StatePlaying(
                    self.__settings,
                    driver=driver,
                    chess_engine_handler=chess_engine_handler,
                    chess_board=ChessBoard(driver),
                )
            )
        if state_manager.get_state().get_state_value != State.NOT_PLAYING and not resign_element:
            state_manager.set_state(StateNotPlaying())

    def __quit(self, driver: Chrome) -> None:
        self.__serialize_settings()
        sys.exit()

    def __is_browser_open(self, driver: Chrome) -> bool:
        if not driver:
            return False

        try:
            if driver.window_handles:
                return True
        except:
            return False

    def __on_automatic_mode_key_pressed(self, event: keyboard.KeyboardEvent) -> None:
        self.__settings["automaticModeEnabled"] = not self.__settings["automaticModeEnabled"]
        print("Automatic mode: " + str(self.__settings["automaticModeEnabled"]))

    def __serialize_settings(self) -> None:
        json_object = json.dumps(self.__settings, indent=4)

        with open(self.__settings["settingsPath"], "w") as outfile:
            outfile.write(json_object)
