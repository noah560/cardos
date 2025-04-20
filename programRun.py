import sys
import io
import os

def run(x, cardos):
    try:
        os.chdir("/sd/")
        exec(x, {"cardos": cardos})
        return None
    except Exception as e:
        buffer = io.StringIO()
        sys.print_exception(e, buffer)
        return buffer.getvalue()


