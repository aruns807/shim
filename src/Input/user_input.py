import interaction_manager

# parses keyboard input for meaningful instructions
# sends "completed" instructions to interaction_manager router
class user_input():
    def __init__(self):
        self.graphics = None
        self.char_buf = []

    def key(self, event):
        print 'in key down'
        print event.keysym

    def control_f(self, event):
        # drop on floor for now
        a = 1

    def control_b(self, event):
        # drop on floor for now
        a = 1
