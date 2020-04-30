import time
# Required so that the demo function will run if demo.py
# is imported via py_nonblock_input.demo or ran directly
try:
    # Accessed via py_nonblocking_input.demo
    from . import NonBlockingStdIn
except ImportError:
    # Accessed via directly running demo.py
    from __init__ import NonBlockingStdIn


def run_demo(seconds=10):
    """Run a demo of py_nonblocking_input.

    Keyword arguments:
    seconds -- how long the demo will run for (default 10)"""
	# Setup non-blocking input at start of program
    u = NonBlockingStdIn()
    # Print array of lines collected each second
    for i in range(seconds):
        time.sleep(1)
        print(f'u: {str(u.get_all_lines())}')
    # Kill non-blocking input to free stdin
    u.kill()


if __name__ == '__main__':
	run_demo()