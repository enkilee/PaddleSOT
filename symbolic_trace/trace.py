import contextlib
import paddle
from .opcode_translator import eval_frame_callback
from .symbolic_trace import SymbolicTraceContext
from .proxy_tensor import clear_runtime_proxytensor

def symbolic_trace(func, with_log=False):
    def wrapped(*args, **kw):
        clear_runtime_proxytensor()
        with SymbolicTraceContext() as ctx:
            paddle.fluid.core.set_eval_frame(eval_frame_callback)
            func(*args, **kw)
            paddle.fluid.core.set_eval_frame(None)
        SymbolicTraceContext().start_compile()
    return wrapped
