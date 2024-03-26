from package.core.state import State
from package.core.state import StateNotPlaying


class StateManager:
    def __init__(self) -> None:
        self.set_state(StateNotPlaying())

    def update(self) -> None:
        self.__state.update()

    def get_state(self) -> State:
        return self.__state

    def set_state(self, state: State) -> None:
        self.__state = state
