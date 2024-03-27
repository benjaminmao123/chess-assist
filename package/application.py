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
from consoledraw import Console


class Application:
    def __init__(self, settings: dict) -> None:
        self.__settings = settings
        self.__console = Console()
        self.__chess_engine_handler = ChessEngineHandler(self.__settings)
        self.__state_manager = StateManager()
        self.__driver = None
        self.__chess_board = None

        keyboard.on_press_key(self.__settings["automaticModeHotkey"], self.__on_automatic_mode_key_pressed)
        keyboard.on_press_key(self.__settings["resetHotkey"], self.__on_automatic_mode_key_pressed)

    def run(self) -> None:
        os.environ["WDM_LOG_LEVEL"] = "0"
        options = Options()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.__driver = Chrome(options)
        self.__driver.get("https://www.chess.com/")

        while True:
            self.__update()

    def __update(self):
        if not self.__is_browser_open():
            self.__quit()

        self.__handle_user_input()
        self.__state_manager.update()
        self.__update_ui()

    def __handle_user_input(
        self
    ) -> None:
        resign_element = self.__driver.find_elements(By.XPATH, selector_constants.RESIGN)

        if self.__state_manager.get_state().get_state_value() != State.PLAYING and resign_element:
            self.__set_playing_state()
        if self.__state_manager.get_state().get_state_value != State.NOT_PLAYING and not resign_element:
            self.__state_manager.set_state(StateNotPlaying())
            
    def __set_playing_state(self) -> None:
        self.__chess_board = ChessBoard(self.__driver)
        self.__state_manager.set_state(
            StatePlaying(self.__settings,
                        driver=self.__driver,
                        chess_engine_handler=self.__chess_engine_handler,
                        chess_board=self.__chess_board))

    def __quit(self) -> None:
        self.__serialize_settings()

        if not self.__is_browser_open():
            self.__driver.quit()

        sys.exit()

    def __is_browser_open(self) -> bool:
        if not self.__driver:
            return False

        try:
            if self.__driver.window_handles:
                return True
        except:
            return False

    def __on_automatic_mode_key_pressed(self, event: keyboard.KeyboardEvent) -> None:
        self.__settings["automaticModeEnabled"] = not self.__settings["automaticModeEnabled"]
        
    def _on_reset_key_pressed(self, event: keyboard.KeyboardEvent) -> None:
        if self.__state_manager.get_state().get_state_value() == State.PLAYING:
            self.__set_playing_state()  

    def __serialize_settings(self) -> None:
        json_object = json.dumps(self.__settings, indent=4)

        with open(self.__settings["settingsPath"], "w") as outfile:
            outfile.write(json_object)

    def __update_ui(self) -> None:
        with self.__console:
            self.__console.print(f"{self.__settings["automaticModeHotkey"]} - Toggle Automatic Mode")
            self.__console.print(f"{self.__settings['playNextMoveHotkey']} - Play Next Move (Autoplay must be disabled)")
            self.__console.print(f"{self.__settings["resetHotkey"]} - Reset")
            enabled = "Enabled" if self.__settings["automaticModeEnabled"] else "Disabled"
            self.__console.print(f"Automatic Mode: {enabled}\n")
            
            if self.__state_manager.get_state().get_state_value() == State.PLAYING:
                eval = self.__chess_engine_handler.get_evaluation()
                eval_value = eval["value"] - 1 if eval["type"] == "mate" else eval["value"] / 100
                self.__console.print(f"Evaluation: {eval["type"]}: {eval_value}")
                
                move = "None"
                try:
                    move = self.__chess_board.get_last_move()
                except IndexError:
                    pass
                self.__console.print(f"Last Move: {move}")
