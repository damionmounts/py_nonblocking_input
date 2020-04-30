from typing import Union, List  # Makes for expressive signatures
import threading  # Allows input() to block a thread that isn't main

import time  # Used in testing


# Spawns a thread on creation that automatically pulls and stores input
# Allows for a non-blocking input method that returns None when no content

# Must be killed before another instance is created - otherwise downfall ensues
# Singleton facilities may be implemented
class NonBlockingStdIn:

    # This sets the max amount of lines to be stored in lines[] at once
    def __init__(self, line_limit: int = 0) -> None:
        # Attributes are private to prevent severe turmoil
        self.__line_limit = abs(line_limit) or float('inf')
        self.__kill_flag = threading.Event()
        self.__lines = []
        self.__lines_lock = threading.Lock()
        self.__thread = threading.Thread(target=self.__input_collector)
        self.__thread.start()

    # Private process used by thread - collects input continuously
    def __input_collector(self) -> None:
        while True:
            if self.__kill_flag.is_set():
                return
            elif len(self.__lines) < self.__line_limit:
                try:
                    line = input()
                except EOFError:
                    continue
                self.__lines_lock.acquire()
                self.__lines.append(line)
                self.__lines_lock.release()

    # Non-blocking input method, pulls line from buffer, None when empty
    def input(self) -> Union[str, None]:
        self.__lines_lock.acquire()
        line = None
        if len(self.__lines) > 0:
            line = self.__lines.pop(0)
        self.__lines_lock.release()
        return line

    # Returns number of lines buffered
    def num_available_lines(self) -> int:
        self.__lines_lock.acquire()
        amount = len(self.__lines)
        self.__lines_lock.release()
        return amount

    # Returns all buffered lines and clears buffer
    def get_all_lines(self) -> List[str]:
        self.__lines_lock.acquire()
        lines = self.__lines
        self.__lines = []
        self.__lines_lock.release()
        return lines

    # Necessary to shutdown thread properly and restore input() method
    # Sadly requires user to place line into stdin to free-up the blocking input()
    def kill(self):
        self.__kill_flag.set()
        print('Please hit [ENTER]')
        self.__thread.join()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Usage example entry point
if __name__ == '__main__':

    # Setup non-blocking input at start of program
    u = NonBlockingStdIn()

    # 10s Demo
    # Prints array of lines collected each second
    cnt = 0
    while True:
        time.sleep(1)
        cnt = cnt + 1
        print('u: ' + str(u.get_all_lines()))
        if cnt == 10:
            break

    # Kill non-blocking input to free input()
    u.kill()
    exit(0)
