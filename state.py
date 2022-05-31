from typing import Callable

class _BaseState:
    def __init__(self, name):
        self.name = name
        self._exit_states = {True: None,
                             False: None}

    def set_exit(self, exit_state, value: bool = True):
        if not isinstance(value, bool):
            raise KeyError('Non boolean key')
        self._exit_states[value] = exit_state


class State(_BaseState):
    def __init__(self, name: str, condition: Callable):
        self._condition = condition
        super(State, self).__init__(name)

    def check_condition(self, hour):
        if self._condition(hour):
            return self._exit_states[True]
        else:
            return self._exit_states[False]

