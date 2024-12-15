import random
import robot.api.logger as logger
import time
import concurrent.futures
import queue
from robot.libraries.BuiltIn import BuiltIn

def _start_guess_number_1_to_100(nr, _loginfoQueue):
    """
    This is a toy example of a long running task which can be executed in parallel.
    """
    trials = 0
    try:
        _loginfoQueue.put((logger.console, f"Start guess number {nr}",))
        while True:
            gues = random.randint(1,100)
            _loginfoQueue.put(lambda: BuiltIn().set_global_variable("${LAST_GUESSED_NUMBER}", gues))
            trials += 1
            if gues == nr:
                break
            _loginfoQueue.put((logger.console, f"Guess {gues} is wrong, should be {nr}",))
            time.sleep(gues/100)
        _loginfoQueue.put((logger.console, f"Guess {gues} is correct",))
    except Exception as e:
        _loginfoQueue.put((logger.console, f"Guessing terminated with exception {e} of type {type(e)}",))
    finally:
        _loginfoQueue.put((logger.console, f"End guess number {nr}",))
    return trials


class parallel_execution_keyword(object):
    def __init__(self):
        self._loginfoQueue = queue.Queue()
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        self._futures = []

    def start_guess_number_1_to_100_parallel(self, nr: int):
        future = self._executor.submit(_start_guess_number_1_to_100, nr, self._loginfoQueue)
        future.add_done_callback(lambda _: self._loginfoQueue.put("End"))
        self._futures.append(future)

    def wait_for_completion_of_parallel_tasks(self):
        while True:
            fromParallels = self._loginfoQueue.get(block=True)
            match fromParallels:
                case "End":
                    if all(future.done() for future in self._futures):
                        logger.console("All tasks completed")
                        logger.info("All tasks completed")
                        return [future.result() for future in self._futures]
                case (logTarget, logMessage,):
                    # This is the most usefull and least dangerous use case
                    logTarget(logMessage)
                case toRunInMainThread:
                    # This is a bad idea, way to powerfull and dangerous, just to present the idea
                    toRunInMainThread()              
            


