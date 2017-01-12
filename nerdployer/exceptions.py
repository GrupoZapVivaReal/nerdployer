

class StepExecutionException(Exception):
    def __init__(self, step, message):
        self.message = message
        self.step = step

    def __str__(self):
        return self.message

class FlowException(Exception):
    def __init__(self, step, message):
        self.message = message
        self.step = step

    def __str__(self):
        return self.message