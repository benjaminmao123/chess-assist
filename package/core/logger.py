import logging
from datetime import datetime
from pathlib import Path


def init(logs_path: str, is_debug: bool) -> None:
    log_path = Path(logs_path)
    
    if not log_path.exists():
        log_path.mkdir()
    
    if is_debug:
        logging.basicConfig(
            filename=f"{logs_path}/log_{datetime.now().strftime("%Y-%m-%d_%H%M%S")}.txt",
            encoding="utf-8",
            level=logging.DEBUG,
        )
    else:
        logging.basicConfig(
            filename=f"{logs_path}/log_{datetime.now().strftime("%Y-%m-%d_%H%M%S")}.txt",
            encoding="utf-8",
            level=logging.INFO,
        )
        
_logger = logging.getLogger()    
    
def debug(msg: str) -> logging.Logger:
    _logger.debug(msg)
            

def info(msg: str) -> logging.Logger:
    _logger.info(msg)        
    

def warn(msg: str) -> logging.Logger:
    _logger.warn(msg)
    

def error(msg: str) -> logging.Logger:
    _logger.error(msg)        
    

def critical(msg: str) -> logging.Logger:
    _logger.critical(msg)        


def set_log_level(level: int) -> None:
    _logger.setLevel(level)
            
    
