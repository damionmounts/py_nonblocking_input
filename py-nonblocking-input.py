import copy
import threading
import time
from typing import Union, List


class __NonBlocking:

    def __init__(self):
        self.__paused = False
        self.__lines = []

        collector = threading.Thread(target=self.collect_input)
        collector.start()

    def collect_input(self) -> None:
        while True:
            line = input()
            while self.__paused:
                pass
            self.__lines.append(line)

    def input(self) -> Union[str, None]:
        self.__paused = True

        if len(self.__lines) == 0:
            line = None
        else:
            line = self.__lines.pop(0)

        self.__paused = False
        return line

    def available_lines(self) -> int:
        self.__paused = True
        amount = len(self.__lines)
        self.__paused = False
        return amount

    def get_all_input(self) -> Union[List[str], None]:
        self.__paused = True

        if len(self.__lines) == 0:
            lines = None
        else:
            lines = copy.deepcopy(self.__lines)

        self.__paused = False
        return lines


if __name__ == '__main__':
    u = __NonBlocking()

    cnt = 0
    while True:
        time.sleep(0.5)
        print('u: ' + str(u.get_all_input()))
