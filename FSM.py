from state import State
from random import random, choice

class DayHour:
    def __init__(self):
        self.hour = 12

    def next(self):
        self.hour += 1
        self._check_limits()

    def _check_limits(self):
        if self.hour >= 24:
            self.hour %= 24

    def __iter__(self):
        return self.__next__()

    def __next__(self):
        while True:
            yield self.hour
            self.hour += 1
            self._check_limits()

    def __str__(self):
        if self.hour < 10:
            return f'0{self.hour}'
        return f'{self.hour}'


class LifeFSM:
    def __init__(self, states: dict):
        self.start_state = None
        self.states = states
        self.time = DayHour()

    def set_start(self, state):
        if state in self.states:
            self.start_state = self.states[state]
        else:
            raise KeyError(f'Key [{state}] not in {self.states.__name__()}')

    def connect_states(self, from_state: State, to_state: State, value=True):
        from_state.set_exit(to_state, value)

    def run(self):
        current_state = self.start_state
        while True:
            print(f'Current hour is {str(self.time)}. Present state is {current_state.name}.')
            input('Press to change hour...')
            current_state = current_state.check_condition(self.time.hour)
            self.time.next()

def main():
    states = {'SLEEP': lambda x: x >= 23 or x <= 7,
              'EAT': lambda x: 12 <= x <= 14,
              'WORK': lambda x: 8 <= x <= 23 and random() <= 0.3, # random is a chance, that i'm not lazy
              'RELAX': lambda x: (x >= 14 or x <= 12) and random() <= 0.5,
              'BEERTIME': lambda x: 18 <= x <= 23 and random() <= 0.6}
    states = {key: State(name=key, condition=states[key]) for key in states}
    for state in states.values():
        state.set_exit(state, value=True)
    # bad code goes here |
    #                    V
    states['SLEEP'].set_exit(states['WORK'], value=False)
    states['WORK'].set_exit(states['RELAX'], value=False)
    states['RELAX'].set_exit(states['EAT'], value=False)
    states['EAT'].set_exit(states['BEERTIME'], value=False)
    states['BEERTIME'].set_exit(states['SLEEP'], value=False)
    fsm = LifeFSM(states)
    fsm.set_start('SLEEP')
    fsm.run()


if __name__ == '__main__':
    main()