class Labeler():
    def __init__(self):
        self.count = 0

    def generate_label(self):
        label = str(self.count)
        self.count += 1
        return label
