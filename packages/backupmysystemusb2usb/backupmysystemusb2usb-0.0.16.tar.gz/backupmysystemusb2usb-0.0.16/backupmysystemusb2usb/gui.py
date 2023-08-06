"""
    This software is a part of backupmystemusb2usb and its functionality is to
    backup one usb key to another usb with the same space disk
    Author: Stéphane Bressani <s.bressani@bluewin.ch>
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk  # noqa: E402

GUI_TITLE = 'Backup my system usb to usb'
GUI_HBOX_SPACING = 5
GUI_BUTTON_CANCEL = 'Cancel operation [Ctrl + c]'

log_list = [('1'), ('2'), ('3')]
"""
https://python-gtk-3-tutorial.readthedocs.io/en/latest/treeview.html#the-view
"""


class LogWindow(Gtk.Window):
    def __init__(self, log_file):
        self.log_file = log_file
        """log_list = [('blabla'), ('2'), (self.log_file)]"""

        Gtk.Window.__init__(self, title=GUI_TITLE)
        self.set_border_width(10)

        # Setting up the self.grid in wich the element are to be positione
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        # Creating the ListStore model
        self.log_list_liststore = Gtk.ListStore(str)
        for l in log_list:
            self.log_list_liststore.append(list(l))
        self.current_filter = None
        # Creating the treeview, making it use the filter as a model,
        # and adding the columns
        self.filter = self.log_list_liststore.filter_new()
        # Setting the filter
        self.filter.set_visible_func(self.filter_func)

        # Crating the treeview, making it use the filter as a model, and adding
        # columns
        self.treeview = Gtk.TreeView.new_with_model(self.filter)
        for i, column_title in enumerate(['Log']):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        hbox = Gtk.Box(spacing=GUI_HBOX_SPACING)

        button = Gtk.Button.new_with_label(GUI_BUTTON_CANCEL)
        button.connect('clicked', self.on_click_cancel)
        hbox.pack_start(button, True, True, 0)

        # Setting up the layout, putting the treeview in scrollwindow, and
        # the button in
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.grid.attach_next_to(hbox, self.scrollable_treelist,
                                 Gtk.PositionType.BOTTOM, 1, 1)
        self.scrollable_treelist.add(self.treeview)

        self.grid.connect('key-release-event', self.on_key_release)

        self.show_all()

    def on_click_cancel(self, button):
        """
        Cancel execution
        """
        self.__cancel_execution()

    def on_key_release(self, widget, ev, data=None):
        """
        Key release
        """
        if ev.keyval in [Gdk.KEY_Control_L, Gdk.KEY_c]:
            self.__cancel_execution()
        if ev.keyval in [Gdk.KEY_Control_R, Gdk.KEY_c]:
            self.__cancel_execution()

    def __cancel_execution(self):
        """
        Cancel execution
        """
        Gtk.main_quit()

    def filter_func(self, model, iter, data):
        return True


class gui:
    def __init__(self, log_file):
        self.log_file = log_file

    def run(self):
        """
        Run gui
        """
        win = LogWindow(self.log_file)
        win.connect('destroy', Gtk.main_quit)
        win.show_all()
        Gtk.main()
