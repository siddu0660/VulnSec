import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk, Pango
import os
import subprocess
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue


class NetworkScanWindow(Gtk.Window):
    def __init__(self, parent=None):
        super().__init__(title="VULNSEC - Network Security Scanner")
        self.parent = parent
        self.set_default_size(800, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        main_box.set_border_width(20)
        self.add(main_box)
        
        header_label = Gtk.Label(label="Network Security Scanner")
        header_label.override_font(Pango.FontDescription("Sans Bold 18"))
        header_label.get_style_context().add_class("options-title")
        main_box.pack_start(header_label, False, False, 10)
        
        scan_frame = Gtk.Frame(label="Scan Type")
        scan_frame.get_style_context().add_class("scan-frame")
        main_box.pack_start(scan_frame, False, False, 10)
        
        scan_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        scan_box.set_border_width(10)
        scan_frame.add(scan_box)
        
        self.web_security_radio = Gtk.RadioButton.new_with_label_from_widget(None, "Web Security Scan (Nikto + Sucridata)")
        scan_box.pack_start(self.web_security_radio, False, False, 0)
        
        self.network_security_radio = Gtk.RadioButton.new_with_label_from_widget(self.web_security_radio, "Full Network Security Audit (OpenVAS + Zeek + Snort)")
        scan_box.pack_start(self.network_security_radio, False, False, 0)
        
        self.vpn_analysis_radio = Gtk.RadioButton.new_with_label_from_widget(self.web_security_radio, "VPN & Firewall Analysis (Snort + Zeek)")
        scan_box.pack_start(self.vpn_analysis_radio, False, False, 0)
        
        self.custom_radio = Gtk.RadioButton.new_with_label_from_widget(self.web_security_radio, "Custom Selection")
        scan_box.pack_start(self.custom_radio, False, False, 0)
        
        custom_frame = Gtk.Frame(label="Custom Tool Selection")
        custom_frame.get_style_context().add_class("scan-frame")
        main_box.pack_start(custom_frame, False, False, 10)
        
        custom_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        custom_box.set_border_width(10)
        custom_frame.add(custom_box)
        
        self.nikto_check = Gtk.CheckButton(label="Nikto (Web Server Scanner)")
        custom_box.pack_start(self.nikto_check, False, False, 0)
        
        self.sucridata_check = Gtk.CheckButton(label="Sucridata (Web Security Scanner)")
        custom_box.pack_start(self.sucridata_check, False, False, 0)
        
        self.openvas_check = Gtk.CheckButton(label="OpenVAS (Vulnerability Scanner)")
        custom_box.pack_start(self.openvas_check, False, False, 0)
        
        self.zeek_check = Gtk.CheckButton(label="Zeek (Network Traffic Analysis)")
        custom_box.pack_start(self.zeek_check, False, False, 0)
        
        self.snort_check = Gtk.CheckButton(label="Snort (Intrusion Detection)")
        custom_box.pack_start(self.snort_check, False, False, 0)
        
        target_frame = Gtk.Frame(label="Target Configuration")
        target_frame.get_style_context().add_class("scan-frame")
        main_box.pack_start(target_frame, False, False, 10)
        
        target_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        target_box.set_border_width(10)
        target_frame.add(target_box)
        
        host_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        host_label = Gtk.Label(label="Target Host:")
        host_label.set_width_chars(15)
        host_box.pack_start(host_label, False, False, 0)
        
        self.host_entry = Gtk.Entry()
        self.host_entry.set_text("localhost")
        host_box.pack_start(self.host_entry, True, True, 0)
        target_box.pack_start(host_box, False, False, 0)
        
        pcap_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        pcap_label = Gtk.Label(label="PCAP File Path:")
        pcap_label.set_width_chars(15)
        pcap_box.pack_start(pcap_label, False, False, 0)
        
        self.pcap_entry = Gtk.Entry()
        self.pcap_entry.set_text("/var/log/pcap/*.pcap")
        pcap_box.pack_start(self.pcap_entry, True, True, 0)
        
        pcap_browse = Gtk.Button(label="Browse")
        pcap_browse.connect("clicked", self.on_pcap_browse_clicked)
        pcap_box.pack_start(pcap_browse, False, False, 0)
        target_box.pack_start(pcap_box, False, False, 0)
        
        snort_conf_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        snort_conf_label = Gtk.Label(label="Snort Config:")
        snort_conf_label.set_width_chars(15)
        snort_conf_box.pack_start(snort_conf_label, False, False, 0)
        
        self.snort_conf_entry = Gtk.Entry()
        self.snort_conf_entry.set_text("/etc/snort/snort.conf")
        snort_conf_box.pack_start(self.snort_conf_entry, True, True, 0)
        
        snort_conf_browse = Gtk.Button(label="Browse")
        snort_conf_browse.connect("clicked", self.on_snort_conf_browse_clicked)
        snort_conf_box.pack_start(snort_conf_browse, False, False, 0)
        target_box.pack_start(snort_conf_box, False, False, 0)
        
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        main_box.pack_start(button_box, False, False, 10)
        
        self.scan_button = Gtk.Button(label="Start Scan")
        self.scan_button.connect("clicked", self.on_scan_clicked)
        self.scan_button.get_style_context().add_class("start-button")
        button_box.pack_end(self.scan_button, False, False, 0)
        
        self.close_button = Gtk.Button(label="Close")
        self.close_button.connect("clicked", self.on_close_clicked)
        button_box.pack_start(self.close_button, False, False, 0)
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_min_content_height(200)
        main_box.pack_start(scrolled_window, True, True, 0)
        
        self.results_view = Gtk.TextView()
        self.results_view.set_editable(False)
        self.results_view.set_cursor_visible(False)
        self.results_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.results_view.override_font(Pango.FontDescription("monospace 10"))
        
        self.results_buffer = self.results_view.get_buffer()
        self.results_buffer.set_text("Scan results will appear here...")
        
        self.results_buffer.create_tag("normal", foreground="#FFFFFF")
        self.results_buffer.create_tag("warning", foreground="#FFCC00")
        self.results_buffer.create_tag("error", foreground="#FF0000")
        self.results_buffer.create_tag("success", foreground="#00FF00")
        
        scrolled_window.add(self.results_view)
        
        self.status_bar = Gtk.ProgressBar()
        self.status_bar.set_show_text(True)
        self.status_bar.set_text("Ready")
        main_box.pack_start(self.status_bar, False, False, 0)
        
        self.apply_css()
        
        self.custom_radio.connect("toggled", self.on_custom_toggled)
        self.on_custom_toggled(self.custom_radio)
    
    def apply_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
        .scan-frame {
            border: 1px solid #336699;
            border-radius: 5px;
        }
        
        .scan-frame > label {
            color: #FFCC00;
            font-weight: bold;
        }
        
        .start-button {
            background-color: #336699;
            color: white;
            font-weight: bold;
            border-radius: 3px;
            padding: 5px 15px;
        }
        
        .options-title {
            color: #FF0000;
            font-size: 18px;
        }
        """)
        
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def on_custom_toggled(self, button):
        is_custom = self.custom_radio.get_active()
        self.nikto_check.set_sensitive(is_custom)
        self.sucridata_check.set_sensitive(is_custom)
        self.openvas_check.set_sensitive(is_custom)
        self.zeek_check.set_sensitive(is_custom)
        self.snort_check.set_sensitive(is_custom)
    
    def on_pcap_browse_clicked(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Select PCAP File",
            parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        
        filter_pcap = Gtk.FileFilter()
        filter_pcap.set_name("PCAP files")
        filter_pcap.add_pattern("*.pcap")
        dialog.add_filter(filter_pcap)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.pcap_entry.set_text(dialog.get_filename())
        
        dialog.destroy()
    
    def on_snort_conf_browse_clicked(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Select Snort Configuration File",
            parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        
        filter_conf = Gtk.FileFilter()
        filter_conf.set_name("Configuration files")
        filter_conf.add_pattern("*.conf")
        dialog.add_filter(filter_conf)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.snort_conf_entry.set_text(dialog.get_filename())
        
        dialog.destroy()
    
    def on_close_clicked(self, button):
        self.destroy()
    
    def on_scan_clicked(self, button):
        self.scan_button.set_sensitive(False)
        self.close_button.set_sensitive(False)
        self.results_buffer.set_text("")
        
        tools_to_run = []
        
        if self.web_security_radio.get_active():
            tools_to_run = ["nikto", "sucridata"]
        elif self.network_security_radio.get_active():
            tools_to_run = ["openvas", "zeek", "snort"]
        elif self.vpn_analysis_radio.get_active():
            tools_to_run = ["snort", "zeek"]
        elif self.custom_radio.get_active():
            if self.nikto_check.get_active():
                tools_to_run.append("nikto")
            if self.sucridata_check.get_active():
                tools_to_run.append("sucridata")
            if self.openvas_check.get_active():
                tools_to_run.append("openvas")
            if self.zeek_check.get_active():
                tools_to_run.append("zeek")
            if self.snort_check.get_active():
                tools_to_run.append("snort")
        
        if not tools_to_run:
            self.append_result("Error: No tools selected for scanning", "error")
            self.scan_complete(False)
            return
        
        self.append_result(f"Starting security scan with: {', '.join(tools_to_run)}", "normal")
        self.append_result("Please wait, this may take some time...\n", "normal")
        
        threading.Thread(target=self.run_scan, args=(tools_to_run,), daemon=True).start()
    
    def append_result(self, text, tag_name="normal"):
        end_iter = self.results_buffer.get_end_iter()
        self.results_buffer.insert_with_tags_by_name(end_iter, text + "\n", tag_name)
        self.results_view.scroll_to_iter(self.results_buffer.get_end_iter(), 0.0, False, 0.0, 0.0)
    
    def run_scan(self, tools):
        GLib.idle_add(self.status_bar.set_fraction, 0.0)
        GLib.idle_add(self.status_bar.set_text, "Initializing scan...")
        
        result_queue = queue.Queue()
        stop_processing = threading.Event()
        
        results_thread = threading.Thread(
            target=self.process_results_queue,
            args=(result_queue, stop_processing),
            daemon=True
        )
        results_thread.start()
        
        try:
            with ThreadPoolExecutor(max_workers=len(tools)) as executor:
                future_to_tool = {executor.submit(self.run_tool, tool, result_queue): tool for tool in tools}
                
                completed = 0
                total = len(tools)
                
                for future in as_completed(future_to_tool):
                    tool = future_to_tool[future]
                    try:
                        success = future.result()
                        completed += 1
                        progress = completed / total
                        GLib.idle_add(self.status_bar.set_fraction, progress)
                        GLib.idle_add(self.status_bar.set_text, f"Progress: {int(progress * 100)}%")
                    except Exception as e:
                        GLib.idle_add(self.append_result, f"Error running {tool}: {str(e)}", "error")
            
            stop_processing.set()
            results_thread.join(timeout=2.0)
            GLib.idle_add(self.scan_complete, True)
            
        except Exception as e:
            GLib.idle_add(self.append_result, f"Error setting up scan: {str(e)}", "error")
            GLib.idle_add(self.scan_complete, False)
    
    def process_results_queue(self, queue, stop_event):
        while not stop_event.is_set() or not queue.empty():
            try:
                result, tag = queue.get(timeout=0.1)
                GLib.idle_add(self.append_result, result, tag)
                queue.task_done()
            except:
                pass
    
    def run_tool(self, tool, result_queue):
        result_queue.put((f"🔍 Running {tool.upper()} scan...", "normal"))
        
        try:
            if tool == "nikto":
                target = self.host_entry.get_text() or "localhost"
                cmd = ["nikto", "-h", f"http://{target}"]
                self.execute_command(cmd, result_queue)
                
            elif tool == "sucridata":
                target = self.host_entry.get_text() or "localhost"
                cmd = ["sucridata", "--scan", f"http://{target}"]
                self.execute_command(cmd, result_queue)
                
            elif tool == "openvas":
                cmd = ["greenbone-nvt-sync"]
                self.execute_command(cmd, result_queue)
                
                cmd = ["openvas-start"]
                self.execute_command(cmd, result_queue)
                
            elif tool == "zeek":
                pcap_path = self.pcap_entry.get_text() or "/var/log/pcap/*.pcap"
                cmd = ["zeek", "-r", pcap_path]
                self.execute_command(cmd, result_queue)
                
            elif tool == "snort":
                snort_conf = self.snort_conf_entry.get_text() or "/etc/snort/snort.conf"
                cmd = ["snort", "-c", snort_conf, "-A", "console"]
                self.execute_command(cmd, result_queue)
            
            result_queue.put((f"✅ {tool.upper()} scan completed successfully", "success"))
            return True
            
        except Exception as e:
            result_queue.put((f"❌ Error running {tool}: {str(e)}", "error"))
            return False
    
    def execute_command(self, cmd, result_queue):
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    result_queue.put((output.strip(), False))
            
            stdout, stderr = process.communicate()
            
            if stdout:
                for line in stdout.strip().split('\n'):
                    if line:
                        result_queue.put((line, False))
            
            if stderr:
                for line in stderr.strip().split('\n'):
                    if line:
                        result_queue.put((line, True))
                        
            return process.returncode == 0
        except Exception as e:
            result_queue.put((f"Error executing command {' '.join(cmd)}: {str(e)}", True))
            return False
    
    def update_progress(self):
        current = self.status_bar.get_fraction()
        if current < 0.9:
            new_value = min(current + 0.01, 0.9)
            self.status_bar.set_fraction(new_value)
            self.status_bar.set_text(f"Scanning... {int(new_value * 100)}%")
        return False
    
    def scan_complete(self, success):
        self.scan_button.set_sensitive(True)
        self.close_button.set_sensitive(True)
        
        if success:
            self.status_bar.set_fraction(1.0)
            self.status_bar.set_text("Scan completed successfully")
            self.append_result("\n✅ Security scan completed successfully!", "success")
        else:
            self.status_bar.set_fraction(0.0)
            self.status_bar.set_text("Scan failed")
            self.append_result("\n❌ Security scan encountered errors!", "error")