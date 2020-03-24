class Label:
    def __init__(self, text, aa, c, s, x, y):
        self.text = text
        self.aa = aa
        self.c = c
        self.s = s
        self.x = x
        self.y = y

    def draw(self, win, font):
        if self.text is not None:
            text = font.render(self.text, self.aa, self.c)
            win.blit(text, (self.x, self.y))

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y