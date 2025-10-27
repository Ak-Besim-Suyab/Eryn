from state.state import State

class LevelState(State):
    async def start(self):
        # check level here.
        # if level up, invoke level up function.
        # if not, invoke end().
        pass

    async def end(self):
        pass