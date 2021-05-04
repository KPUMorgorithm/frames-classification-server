from collections.abc import Callable

class Task:
    def __init__(self, id, runnable : Callable):
        self.id = id
        self.runnable : Callable = runnable
    
    def run(self):
        self.runnable()