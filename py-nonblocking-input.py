from typing import Union, List
import threading
import time


# Spawns a thread on creation that automatically pulls and stores input
class NonBlockingStdIn:

    def __init__(self, line_limit: Union[int, None] = None) -> None:
        self.__line_limit = line_limit
        self.__running = True
        self.__paused = False
        self.__lines = []
        self.__thread = threading.Thread(target=self.__input_collector)
        self.__thread.daemon = True
        self.__thread.start()

    def __input_collector(self) -> None:
        while self.__running:
            if len(self.__lines) < (self.__line_limit or float('inf')):
                try:
                    line = input()
                except EOFError:
                    continue
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

    def num_available_lines(self) -> int:
        self.__paused = True
        amount = len(self.__lines)
        self.__paused = False
        return amount

    def get_all_input(self) -> Union[List[str], None]:
        self.__paused = True

        if len(self.__lines) == 0:
            lines = None
        else:
            lines = self.__lines
            self.__lines = []

        self.__paused = False
        return lines

    #
    def kill(self):
        self.__running = False
        print('Please hit [ENTER]')
        self.__thread.join()


# Main entry point
if __name__ == '__main__':
    u = NonBlockingStdIn(line_limit=4)

    cnt = 0
    while True:
        time.sleep(0.5)
        cnt = cnt + 1
        print('u: ' + str(u.get_all_input()))
        if cnt == 55:
            break

    u.kill()
