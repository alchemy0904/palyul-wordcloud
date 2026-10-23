from controller import Controller
from view import App
from ttkbootstrap.utility import enable_high_dpi_awareness

if __name__ == '__main__':
    controller = Controller()
    enable_high_dpi_awareness()
    app = App(controller)
    controller.view = app
    app.mainloop()