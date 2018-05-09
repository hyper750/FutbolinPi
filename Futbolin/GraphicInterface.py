import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import os

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_name("mainWindow")
        self.set_title("Futbolin")
        self.set_icon_from_file("Image/icon64.png")
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(600, 800)
        #self.set_position(Gtk.WIN_POS_CENTER)
        self.fullscreen()

        styleProvider = Gtk.CssProvider()
        cssPath = "Style/Main.css"
        if os.path.exists(cssPath):
            with open(cssPath, "r") as file:
                css = file.read()
        else:
            css = ""

        styleProvider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), styleProvider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        #Layout
        layout = Gtk.Grid()
        self.add(layout)

        #Widgets
        #Scoreboard
        self.scoreLabel = Gtk.Label("0 - 0")
        self.scoreLabel.set_name("scoreLabel")
        self.scoreLabel.set_hexpand(True)
        layout.attach(self.scoreLabel, 0, 0, 1, 1)


        #Gif widgets
        self.gifViewer = Gtk.Image()
        self.gifViewer.set_name("gifViewer")
        #self.gifViewer.set_from_file("Gif/propia.gif")
        self.gifViewer.set_hexpand(True)
        layout.attach(self.gifViewer, 0, 1, 1, 1)
        Gdk.threads_init()
        self.show_all()


        #X Column, Y Row, Width, Height
        '''layout.attach(gtk.Button("Hola"), 0, 0, 1, 1)
        adeu = gtk.Button("Adeu")
        adeu.set_property("width-request", 1235)
        layout.attach(adeu, 1, 0, 1, 1)
        layout.attach(gtk.Button("ASD"), 0, 1, 2, 1)'''

        '''scoreText = gtk.Label("0 - 0", justify=gtk.Justification.RIGHT)
        #scoreText.set_justify(gtk.JUSTIFY.RIGHT)
        layout.attach(scoreText, 0, 0, 1, 1)'''

        '''self.button = Gtk.Button(label="Click Here")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        print("Hello World")'''

    def setText(self, text):
        #glib.idle_add(self.scoreLabel.set_text, text)
        Gdk.threads_enter()
        self.scoreLabel.set_text(text)
        Gdk.threads_leave()

    def setGif(self, gif):
        #glib.idle_add(self.gifViewer.set_from_file, gif)
        Gdk.threads_enter()
        #self.gifViewer.set_from_file(gif)
        self.gifViewer.set_from_animation(gif)
        Gdk.threads_leave()

    def visibleGifView(self, boolean):
        #glib.idle_add(self.gifViewer.set_visible, boolean)
        Gdk.threads_enter()
        self.gifViewer.set_visible(boolean)
        Gdk.threads_leave()




'''if __name__ == '__main__':
    win = MainWindow("")
    Gtk.main()'''