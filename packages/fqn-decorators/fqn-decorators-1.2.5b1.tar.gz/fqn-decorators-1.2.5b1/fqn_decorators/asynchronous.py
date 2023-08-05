"""This module implements an async-aware decorator.

For backwards compatibility with Python 2.x, it needs to remain separate from
the rest of the codebase, since it uses Python 3.5 syntax (``async def``, ``await``).
"""
import sys

from .decorators import Decorator


class AsyncDecorator(Decorator):
    # __call__ should be sync to return a decorator class object, not a coroutine
    def __call__(self, *args, **kwargs):
        if not self.func:
            # Decorator initialized without providing the function (parametrised decorator)
            return self.__class__(args[0], **self.params)

        self.fqn = self.get_fqn()
        self.args = args
        self.kwargs = kwargs

        async def async_wrapper(*args, **kwargs):
            self.before()
            try:
                self.result = await self.func(*self.args, **self.kwargs)
            except:
                self.exc_info = sys.exc_info()
                self.exception()
                raise
            finally:
                self.after()
            return self.result
        return async_wrapper(*args, **kwargs)
