import asyncio
from typing import AsyncIterator, Iterable, TypeVar

T = TypeVar("T")


class SDKIterator(AsyncIterator[T]):
    def __init__(self, obj: Iterable[T]):
        self.obj = obj
        self.index = 0
        self.lock = asyncio.Lock()

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        async with self.lock:
            if self.index >= len(self.obj):
                raise StopAsyncIteration

            next_obj = self.obj[self.index]
            self.index += 1
            return next_obj
