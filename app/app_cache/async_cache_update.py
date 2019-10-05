from threading import Thread

from app.utils import logger


class AsyncCacheUpdate(Thread):
    """
    A seperate Thread instance to update cache asyncronously to avoid data serialization overhead upon API calls
    and also to plug into application logger for better interpretability.
    """
    def __init__(self, func_ref, func_args):
        Thread.__init__(self)
        self.func = func_ref
        self.args = func_args
        self.result = None

        logger.info('Thread {0}({1})'.format(func_ref.__name__, *func_args), ' initialized')

    def run(self):
        try:
            self.result = self.func(*self.args)  # unwrap the arguments
            logger.info(str(self.func), "returned => ", self.result)
        except Exception as e:
            logger.exception(e)
            self.result = -1

    def join(self):
        Thread.join(self)
        return self.result