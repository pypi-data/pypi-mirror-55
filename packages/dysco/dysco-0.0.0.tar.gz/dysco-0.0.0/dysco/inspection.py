"""Utilities related to inspection."""
import inspect
from types import FrameType


def get_calling_frame(depth: int = 0) -> FrameType:
    stack = inspect.stack()
    if len(stack) < depth + 1:
        raise ValueError(f'No frame found at {depth} levels up the stack.')
    return stack[depth + 1].frame
