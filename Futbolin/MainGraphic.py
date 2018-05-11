from GameController import GameController
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

if __name__ == "__main__":
    gameController = GameController()
    Gtk.main()

    '''while len(threading.enumerate()) > 1:
        for t in threading.enumerate():
            print(t)

        time.sleep(2)
        print("-----------------")'''