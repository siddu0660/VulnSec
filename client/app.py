import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk, Pango
import os
import time
from threading import Thread


class BannerWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="VULNSEC")
        self.set_default_size(900, 550)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 1))

        home_dir = os.path.expanduser("~/.vulnsec")
        if not os.path.exists(home_dir):
            os.makedirs(home_dir)
            self.project_status = "\nProject initiated at .vulnsec"
        else:
            self.project_status = ""

        self.banner_text = """
██╗   ██╗██╗   ██╗██╗     ███╗   ██╗███████╗███████╗ ██████╗
██║   ██║██║   ██║██║     ████╗  ██║██╔════╝██╔════╝██╔════╝
██║   ██║██║   ██║██║     ██╔██╗ ██║███████╗█████╗  ██║     
╚██╗ ██╔╝██║   ██║██║     ██║╚██╗██║╚════██║██╔══╝  ██║     
 ╚████╔╝ ╚██████╔╝███████╗██║ ╚████║███████║███████╗╚██████╗
  ╚═══╝   ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚═════╝"""

        self.tagline = "The place where you need no more security....."
        self.typed_text = ""
        self.index = 0

        self.banner_text_view = Gtk.TextView()
        self.banner_text_view.get_buffer().set_text(self.banner_text)
        self.banner_text_view.override_font(Pango.FontDescription("monospace 14"))
        self.banner_text_view.set_editable(False)
        self.banner_text_view.set_cursor_visible(False)
        self.banner_text_view.set_justification(Gtk.Justification.CENTER)
        self.banner_text_view.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 1))
        self.banner_text_view.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 0, 0, 1)) 

        self.typing_label = Gtk.Label()
        self.typing_label.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("red"))

        self.status_label = Gtk.Label(label=self.project_status)
        self.status_label.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("red"))

        banner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        banner_box.pack_start(self.banner_text_view, False, False, 0)
        banner_box.pack_start(self.typing_label, False, False, 0)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        main_box.set_valign(Gtk.Align.CENTER)
        main_box.set_halign(Gtk.Align.CENTER)
        main_box.pack_start(banner_box, False, False, 0)
        main_box.pack_start(self.status_label, False, False, 0)

        padding_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        padding_box.set_border_width(20)
        padding_box.pack_start(main_box, True, True, 0)

        self.add(padding_box)

        Thread(target=self.animate_typing, daemon=True).start()

    def animate_typing(self):
        for char in self.tagline:
            self.typed_text += char
            GLib.idle_add(self.typing_label.set_text, self.typed_text)
            time.sleep(0.1)

        time.sleep(1)
        GLib.idle_add(self.switch_to_main)

    def switch_to_main(self):
        main_app = MainAppWindow()
        main_app.show_all()
        self.hide()


class MainAppWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="VULNSEC")
        self.set_default_size(1000, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("destroy", Gtk.main_quit)

        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(paned)

        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        sidebar.set_size_request(220, -1)
        sidebar.set_border_width(10)
        sidebar.get_style_context().add_class("sidebar")

        title_label = Gtk.Label(label="VULNSEC")
        title_label.override_font(Pango.FontDescription("Sans Bold 22"))
        title_label.get_style_context().add_class("title-label")

        btn_configs = Gtk.Button(label="Configs")
        btn_logs = Gtk.Button(label="Logs")

        for btn in [btn_configs, btn_logs]:
            btn.set_size_request(-1, 40)
            btn.get_style_context().add_class("sidebar-button")
            
        btn_configs.connect("clicked", self.on_configs_clicked)

        sidebar.pack_start(title_label, False, False, 0)
        sidebar.pack_start(btn_configs, False, False, 0)
        sidebar.pack_start(btn_logs, False, False, 0)

        self.content_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.content_area.set_border_width(20)
        self.content_area.get_style_context().add_class("content-area")

        paned.pack1(sidebar, False, False)
        paned.pack2(self.content_area, True, False)
        
        self.show_default_options()

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            window, .sidebar, .content-area, list, listbox {
                background-color: #000000;
                padding : 10px;
            }
            .sidebar-button {
                background-image: none;
                background-color: #336699;
                color: white;
                border-radius: 5px;
                padding: 10px 15px;
                margin: 5px 0;
            }
            .sidebar-button:active {
                background-color: #1a3d5c;
            }
            .title-label {
                color: #ff0000;
            }
            .directory-label {
                color: #ffcc00;
                font-weight: bold;
                font-size: 16px;
                margin-top: 20px;
                margin-bottom: 10px;
                padding-left: 5px;
            }
            .file-row {
                padding: 10px;
                border-radius: 3px;
            }
            .file-row:hover {
                background-color: #2a2a2a;
            }
            .file-row:selected {
                background-color: #1a3d5c;
            }
            .file-label {
                color: #ffffff;
            }
            .arrow-label {
                color: #336699;
                font-weight: bold;
                margin-right: 10px;
            }
            .options-title {
                color: #ff0000;
                margin-bottom: 20px;
            }
            .option-button {
                background-image: none;
                background-color: #336699;
                color: white;
                border-radius: 5px;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
            }
            .option-button:hover {
                background-color: #4477aa;
            }
            .option-button:active {
                background-color: #1a3d5c;
            }
        """)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def on_configs_clicked(self, widget):
        for child in self.content_area.get_children():
            self.content_area.remove(child)

        config_files = self.get_config_files()

        if not config_files:
            label = Gtk.Label(label="No config files found.")
            label.get_style_context().add_class("file-label")
            self.content_area.pack_start(label, False, False, 0)
        else:
            scrolled_window = Gtk.ScrolledWindow()
            scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            
            listbox = Gtk.ListBox()
            listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
            listbox.connect("row-activated", self.on_file_selected)
            listbox.get_style_context().add_class("list")
            
            current_dir = None
            for file_path in sorted(config_files):
                dir_name = os.path.dirname(file_path)
                if dir_name != current_dir:
                    current_dir = dir_name
                    dir_label = Gtk.Label(label=f"Directory: {os.path.basename(dir_name)}")
                    dir_label.get_style_context().add_class("directory-label")
                    dir_label.set_halign(Gtk.Align.START)
                    listbox.add(dir_label)

                row = Gtk.ListBoxRow()
                row.get_style_context().add_class("file-row")
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
                row.add(hbox)

                arrow_label = Gtk.Label(label=">")
                arrow_label.get_style_context().add_class("arrow-label")
                hbox.pack_start(arrow_label, False, False, 0)

                file_label = Gtk.Label(label=os.path.basename(file_path))
                file_label.get_style_context().add_class("file-label")
                file_label.set_halign(Gtk.Align.START)
                hbox.pack_start(file_label, True, True, 0)

                listbox.add(row)

            scrolled_window.add(listbox)
            self.content_area.pack_start(scrolled_window, True, True, 0)

        self.content_area.show_all()

    def get_config_files(self):
        base_dir = os.path.expanduser("~/.vulnsec/configs")
        file_list = []
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list

    def on_file_selected(self, listbox, row):
        if isinstance(row.get_child(), Gtk.Label):
            return
        file_name = row.get_child().get_children()[1].get_text()
        print(f"Selected file: {file_name}")
        
    def show_default_options(self):
        for child in self.content_area.get_children():
            self.content_area.remove(child)
        
        options_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        options_box.set_valign(Gtk.Align.CENTER)
        options_box.set_halign(Gtk.Align.CENTER)
        
        title = Gtk.Label(label="Security Options")
        title.override_font(Pango.FontDescription("Sans Bold 18"))
        title.get_style_context().add_class("options-title")
        options_box.pack_start(title, False, False, 10)
        
        options = [
            {"label": "Antivirus Scans", "callback": self.on_antivirus_clicked},
            {"label": "Network Scans", "callback": self.on_network_clicked},
            {"label": "Firewall", "callback": self.on_firewall_clicked},
            {"label": "VPN", "callback": self.on_vpn_clicked}
        ]
        
        for option in options:
            button = Gtk.Button(label=option["label"])
            button.set_size_request(200, 60)
            button.get_style_context().add_class("option-button")
            button.connect("clicked", option["callback"])
            options_box.pack_start(button, False, False, 10)
        
        self.content_area.pack_start(options_box, True, True, 0)
        self.content_area.show_all()

    def on_antivirus_clicked(self, widget):
        from antivirus import AntivirusScanWindow
        scan_window = AntivirusScanWindow(self)
        scan_window.show_all()
        # TODO : Check for errors
        
    def on_network_clicked(self, widget):
        from networkSec import NetworkScanWindow
        scan_window = NetworkScanWindow(self)
        scan_window.show_all()
        # TODO : Check for errors
        
    def on_firewall_clicked(self, widget):
        print("Firewall option selected")
        # TODO : Call your firewall script here
        
    def on_vpn_clicked(self, widget):
        print("VPN option selected")
        # TODO : Call your VPN script here


win = MainAppWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()