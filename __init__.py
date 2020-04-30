from typing import Union, List  # Makes for expressive signatures
import threading  # Allows input() to block a thread that isn't main


class NonBlockingStdIn:
    """NonBlockingStdIn
    Spawns a thread on creation that automatically reads and buffers stdin.
    This allows for a non-blocking line-buffered stdin.
    In the event of nothing being buffered None is returned.

    Sidenote: If stdin is read by anything else eternal suffering may ensue.
    Singleton facilities may be implemented soon(tm)."""

    def __init__(self, line_limit: int = 0) -> None:
        """Create a NonBlockingStdIn instance.

        Keyword arguments:
        line_limit -- max buffered lines (default 0 [infinite])"""

        # Attributes are private to prevent severe turmoil
        self.__line_limit = abs(line_limit) or float('inf')
        self.__kill_flag = threading.Event()
        self.__lines = []
        self.__lines_lock = threading.Lock()
        self.__thread = threading.Thread(target=self.__input_collector)
        self.__thread.start()

    def __input_collector(self) -> None:
        """Input thread target. Continuously collects stdin into __lines."""
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

    def input(self) -> Union[str, None]:
        """Pop one line from the buffer. Returns None when the buffer is empty."""
        self.__lines_lock.acquire()
        line = None
        if len(self.__lines) > 0:
            line = self.__lines.pop(0)
        self.__lines_lock.release()
        return line

    def num_available_lines(self) -> int:
        """Return number of lines buffered."""
        self.__lines_lock.acquire()
        amount = len(self.__lines)
        self.__lines_lock.release()
        return amount

    def get_all_lines(self) -> List[str]:
        """Return all buffered lines and clear buffer."""
        self.__lines_lock.acquire()
        lines = self.__lines
        self.__lines = []
        self.__lines_lock.release()
        return lines

    def kill(self):
        """Kill input thread to restore predictable useage of input().
        
        Note: Currently requires input to stdin to stop the thread being blocked.
        """
        self.__kill_flag.set()
        print('Please hit [ENTER]')
        self.__thread.join()