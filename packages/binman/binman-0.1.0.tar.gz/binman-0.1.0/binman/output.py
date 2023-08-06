from colorama import Back, Fore, Style, init

init()


class OutputManager:
    def __init__(self, verbose: bool = False):
        self._verbose = verbose

    def _msg(self, message: str, prefix_marker: str, color: str, padding: int):
        pad = ""
        if padding > 0:
            pad = "|" + "  " * padding

        print(pad + color + f"{prefix_marker} {message}" + Style.RESET_ALL)

    def step(self, message: str, prefix_marker: str = "+", padding: int = 0) -> None:
        self._msg(message, prefix_marker, Fore.YELLOW, padding)

    def progress(self, message: str, prefix_marker: str = "", padding: int = 0) -> None:
        self._msg(message, prefix_marker, "", padding)

    def info(self, message: str, prefix_marker: str = "+", padding: int = 0) -> None:
        self._msg(message, prefix_marker, Fore.GREEN, padding)

    def debug(self, message: str, prefix_marker: str = "-", padding: int = 0) -> None:
        if self._verbose:
            self._msg(message, prefix_marker, Fore.BLUE, padding)

    def error(self, message: str, prefix_marker: str = "!", padding: int = 0) -> None:
        self._msg(message, prefix_marker, Fore.RED, padding)
