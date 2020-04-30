from typing import Union, List  # Makes for expressive signatures
import threading  # Allows input() to block a thread that isn't main

import time  # Used in testing


# Spawns a thread on creation that automatically pulls and stores input
# Allows for a non-blocking input method that returns None when no content

# Must be killed before another instance is created - otherwise downfall ensues
# Singleton facilities may be implemented
class NonBlockingStdIn:

    # line_limit is None by default (infinity)
    # This sets the max amount of lines to be stored in lines[] at once
    def __init__(self, line_limit: Union[int, None] = None) -> None:

        # Attributes are private to prevent severe turmoil
        self.__line_limit = line_limit
        self.__running = True
        self.__paused = False
        self.__lines = []
        self.__thread = threading.Thread(target=self.__input_collector)
        self.__thread.daemon = True
        self.__thread.start()

    # Private process used by thread - collects input continuously
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

    # Non-blocking input method, pulls line from buffer, None when empty
    def input(self) -> Union[str, None]:
        self.__paused = True

        if len(self.__lines) == 0:
            line = None
        else:
            line = self.__lines.pop(0)

        self.__paused = False
        return line

    # Returns number of lines buffered
    def num_available_lines(self) -> int:
        self.__paused = True
        amount = len(self.__lines)
        self.__paused = False
        return amount

    # Returns all buffered lines and clears buffer
    def get_all_lines(self) -> List[str]:
        self.__paused = True

        lines = self.__lines
        self.__lines = []

        self.__paused = False
        return lines

    # Necessary to shutdown thread properly and restore input() method
    # Sadly requires user to place line into stdin to free-up the blocking input()
    def kill(self):
        self.__running = False
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
