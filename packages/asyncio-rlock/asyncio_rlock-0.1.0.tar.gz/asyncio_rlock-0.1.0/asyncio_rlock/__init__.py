import asyncio


class RLock(asyncio.Lock):
    """
    A reentrant lock for Python coroutines.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._task = None
        self._depth = 0

    async def acquire(self):
        if self._task is None or self._task != asyncio.current_task():
            await super().acquire()
            self._task = asyncio.current_task()
            assert self._depth == 0
        self._depth += 1

    def release(self):
        if self._depth > 0:
            self._depth -= 1
        if self._depth == 0:
            super().release()
            self._task = None
