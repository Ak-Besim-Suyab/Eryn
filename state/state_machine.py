class StateMachine:
    def __init__(self):
        self.states = {}

    def register(self, state_name, cls):
        self.states[state_name] = cls
        print(f"[StateMachine] Registered state: {state_name}")

    def get(self, state_name):
        return self.states.get(state_name)

    def create(self, state_name, *args, **kwargs):
        state = self.get(state_name)
        if state:
            return state(*args, **kwargs) # it will return implemented object State()
        raise ValueError(f"State '{state_name}' not registered.")