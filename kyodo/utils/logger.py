import logging
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

class Logger:
    def __init__(self, level=logging.INFO, log_to_file=False, log_file='kyodo.log'):
        self.logger = logging.getLogger("Logger")
        self.logger.setLevel(level)
        self.logger.propagate = False

        self.log_to_file = log_to_file
        self.log_file = log_file

        self.COLORS = {
            logging.DEBUG: Fore.GREEN,
            logging.INFO: Fore.CYAN,
            logging.WARNING: Fore.YELLOW,
            logging.ERROR: Fore.RED,
            logging.CRITICAL: Fore.RED
        }

        self.LEVEL_COLORS = {
            logging.DEBUG: Fore.GREEN + Style.BRIGHT,
            logging.INFO: Fore.CYAN + Style.BRIGHT,
            logging.WARNING: Fore.YELLOW + Style.BRIGHT,
            logging.ERROR: Fore.RED + Style.BRIGHT,
            logging.CRITICAL: Fore.RED + Style.BRIGHT
        }

        self.DATE_COLOR = Fore.LIGHTBLACK_EX

        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(self.console_handler)

        if self.log_to_file:
            self._add_file_handler()

    def _add_file_handler(self):
        self.file_handler = logging.FileHandler(self.log_file)
        self.file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"))
        self.logger.addHandler(self.file_handler)

    def _colorize(self, message, level):
        level_name = logging.getLevelName(level)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        colored_timestamp = self.DATE_COLOR + timestamp + Style.RESET_ALL
        colored_level = self.LEVEL_COLORS.get(level, Fore.WHITE) + level_name + Style.RESET_ALL
        colored_message = self.COLORS.get(level, Fore.WHITE) + message + Style.RESET_ALL
        return f"{colored_timestamp} - {colored_level} - {colored_message}"

    def _log(self, level, message):
        if self.logger.level > level: return
        colored_message = self._colorize(message, level)
        self.console_handler.emit(logging.LogRecord("Logger", level, "", 0, colored_message, None, None))

        if self.log_to_file:
            plain_record = logging.LogRecord("Logger", level, "", 0, message, None, None)
            self.file_handler.emit(plain_record)

    def debug(self, message):    self._log(logging.DEBUG, message)
    def info(self, message):     self._log(logging.INFO, message)
    def warning(self, message):  self._log(logging.WARNING, message)
    def error(self, message):    self._log(logging.ERROR, message)
    def critical(self, message): self._log(logging.CRITICAL, message)

    def set_level(self, level):
        self.logger.setLevel(level)

    def enable_file_logging(self, log_file='kyodo.log'):
        if not self.log_to_file:
            self.log_to_file = True
            self.log_file = log_file
            self._add_file_handler()

    def disable_file_logging(self):
        if self.log_to_file:
            self.log_to_file = False
            self.logger.removeHandler(self.file_handler)
