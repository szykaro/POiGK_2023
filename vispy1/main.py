from vispy import app


class Apka(app.Canvas):
    def __init__(self):
        super().__init__(title='Hello world!',
                         size=(800, 800))
        self.show()


apka = Apka()
app.run()
