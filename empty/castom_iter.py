class TumbochkaIterator:
		def __init__(self, some_objects):
				self.some_objects = some_objects
        self.current = 0

    def to_start(self):
        self.current = 0

    def to_current(self, val):
        if val >= len(self.some_objects) or val < 0:
            print("Неверное значение для курсора!")
        else:
            self.current = val

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < len(self.some_objects):
            result = self.some_objects[self.current]
            self.current += 1
            return result
        raise StopIteration