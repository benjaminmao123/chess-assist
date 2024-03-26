from stockfish import Stockfish


class ChessEngineHandler:
    def __init__(self, settings: dict) -> None:
        self.__engine = Stockfish(
            settings["stockfishPath"], settings["stockfishDepth"], settings["stockfishParameters"]
        )

    def get_next_move(self) -> str:
        return self.__engine.get_best_move()

    def set_fen(self, fen: str) -> None:
        self.__engine.set_fen_position(fen)
