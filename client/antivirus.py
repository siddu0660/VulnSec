import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk, Pango
import os
import subprocess
import threading


class AntivirusScanWindow(Gtk.Window):
    def __init__(self, parent=None):
        super().__init__(title="VULNSEC - Antivirus Scanner")
        self.parent = parent
        self.set_default_size(800, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        main_box.set_border_width(20)
        self.add(main_box)
        
        header_label = Gtk.Label(label="Antivirus Scanner")
        header_label.override_font(Pango.FontDescription("Sans Bold 18"))
        header_label.get_style_context().add_class("options-title")
        main_box.pack_start(header_label, False, False, 10)
        
        scanner_frame = Gtk.Frame(label="Scanner Type")
        scanner_frame.get_style_context().add_class("scan-frame")
        main_box.pack_start(scanner_frame, False, False, 10)
        
        scanner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        scanner_box.set_border_width(10)
        scanner_frame.add(scanner_box)
        
        self.clamscan_radio = Gtk.RadioButton.new_with_label_from_widget(None, "ClamScan (Standard)")
        scanner_box.pack_start(self.clamscan_radio, False, False, 0)
        
        self.clamd_radio = Gtk.RadioButton.new_with_label_from_widget(self.clamscan_radio, "ClamD (Daemon-based, faster)")
        scanner_box.pack_start(self.clamd_radio, False, False, 0)
        
        dir_frame = Gtk.Frame(label="Scan Location")
        dir_frame.get_style_context().add_class("scan-frame")
        main_box.pack_start(dir_frame, False, False, 10)
        
        dir_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        dir_box.set_border_width(10)
        dir_frame.add(dir_box)
        
        self.dir_entry = Gtk.Entry()
        self.dir_entry.set_text(os.path.expanduser("~"))
        dir_box.pack_start(self.dir_entry, True, True, 0)
        
        browse_button = Gtk.Button(label="Browse")
        browse_button.connect("clicked", self.on_browse_clicked)
        dir_box.pack_start(browse_button, False, False, 0)
        
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.TOP)
        main_box.pack_start(notebook, False, False, 0)
        
        general_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        general_box.set_border_width(10)
        general_label = Gtk.Label(label="General")
        notebook.append_page(general_box, general_label)
        
        self.recursive_check = Gtk.CheckButton(label="Recursive Scan (-r)")
        self.recursive_check.set_active(True)
        general_box.pack_start(self.recursive_check, False, False, 0)
        
        self.infected_only_check = Gtk.CheckButton(label="Show Only Infected Files (-i)")
        general_box.pack_start(self.infected_only_check, False, False, 0)
        
        self.scan_archive_check = Gtk.CheckButton(label="Scan Archives (--scan-archive)")
        self.scan_archive_check.set_active(True)
        general_box.pack_start(self.scan_archive_check, False, False, 0)
        
        self.scan_mail_check = Gtk.CheckButton(label="Scan Emails (--scan-mail)")
        general_box.pack_start(self.scan_mail_check, False, False, 0)
        
        self.scan_pdf_check = Gtk.CheckButton(label="Scan PDFs (--scan-pdf)")
        general_box.pack_start(self.scan_pdf_check, False, False, 0)
        
        self.scan_html_check = Gtk.CheckButton(label="Scan HTML (--scan-html)")
        general_box.pack_start(self.scan_html_check, False, False, 0)
        
        file_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        file_box.set_border_width(10)
        file_label = Gtk.Label(label="File Handling")
        notebook.append_page(file_box, file_label)
        
        self.remove_check = Gtk.CheckButton(label="Delete Infected Files (--remove)")
        file_box.pack_start(self.remove_check, False, False, 0)
        
        move_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.move_check = Gtk.CheckButton(label="Move Infected Files (--move=)")
        move_box.pack_start(self.move_check, False, False, 0)
        self.move_entry = Gtk.Entry()
        move_box.pack_start(self.move_entry, True, True, 0)
        file_box.pack_start(move_box, False, False, 0)
        
        copy_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.copy_check = Gtk.CheckButton(label="Copy Infected Files (--copy=)")
        copy_box.pack_start(self.copy_check, False, False, 0)
        self.copy_entry = Gtk.Entry()
        copy_box.pack_start(self.copy_entry, True, True, 0)
        file_box.pack_start(copy_box, False, False, 0)
        
        exclude_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.exclude_check = Gtk.CheckButton(label="Exclude Files (--exclude=)")
        exclude_box.pack_start(self.exclude_check, False, False, 0)
        self.exclude_entry = Gtk.Entry()
        exclude_box.pack_start(self.exclude_entry, True, True, 0)
        file_box.pack_start(exclude_box, False, False, 0)
        
        exclude_dir_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.exclude_dir_check = Gtk.CheckButton(label="Exclude Directories (--exclude-dir=)")
        exclude_dir_box.pack_start(self.exclude_dir_check, False, False, 0)
        self.exclude_dir_entry = Gtk.Entry()
        exclude_dir_box.pack_start(self.exclude_dir_entry, True, True, 0)
        file_box.pack_start(exclude_dir_box, False, False, 0)
        
        perf_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        perf_box.set_border_width(10)
        perf_label = Gtk.Label(label="Performance")
        notebook.append_page(perf_box, perf_label)
        
        filesize_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.filesize_check = Gtk.CheckButton(label="Max File Size (--max-filesize=)")
        filesize_box.pack_start(self.filesize_check, False, False, 0)
        self.filesize_entry = Gtk.Entry()
        self.filesize_entry.set_placeholder_text("e.g., 10M")
        filesize_box.pack_start(self.filesize_entry, True, True, 0)
        perf_box.pack_start(filesize_box, False, False, 0)
        
        scansize_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.scansize_check = Gtk.CheckButton(label="Max Scan Size (--max-scansize=)")
        scansize_box.pack_start(self.scansize_check, False, False, 0)
        self.scansize_entry = Gtk.Entry()
        self.scansize_entry.set_placeholder_text("e.g., 100M")
        scansize_box.pack_start(self.scansize_entry, True, True, 0)
        perf_box.pack_start(scansize_box, False, False, 0)
        
        recursion_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.recursion_check = Gtk.CheckButton(label="Max Recursion Depth (--max-recursion=)")
        recursion_box.pack_start(self.recursion_check, False, False, 0)
        self.recursion_entry = Gtk.Entry()
        self.recursion_entry.set_placeholder_text("e.g., 15")
        recursion_box.pack_start(self.recursion_entry, True, True, 0)
        perf_box.pack_start(recursion_box, False, False, 0)
        
        maxfiles_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.maxfiles_check = Gtk.CheckButton(label="Max Number of Files (--max-files=)")
        maxfiles_box.pack_start(self.maxfiles_check, False, False, 0)
        self.maxfiles_entry = Gtk.Entry()
        self.maxfiles_entry.set_placeholder_text("e.g., 1000")
        maxfiles_box.pack_start(self.maxfiles_entry, True, True, 0)
        perf_box.pack_start(maxfiles_box, False, False, 0)
        
        self.quiet_check = Gtk.CheckButton(label="Quiet Mode (--quiet)")
        perf_box.pack_start(self.quiet_check, False, False, 0)
        
        heur_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        heur_box.set_border_width(10)
        heur_label = Gtk.Label(label="Heuristics")
        notebook.append_page(heur_box, heur_label)
        
        self.heuristic_check = Gtk.CheckButton(label="Enable Heuristic Alerts (--heuristic-alerts)")
        heur_box.pack_start(self.heuristic_check, False, False, 0)
        
        self.detect_pua_check = Gtk.CheckButton(label="Detect Potentially Unwanted Apps (--detect-pua)")
        heur_box.pack_start(self.detect_pua_check, False, False, 0)
        
        self.phishing_check = Gtk.CheckButton(label="Detect Phishing (--phishing-sigs)")
        heur_box.pack_start(self.phishing_check, False, False, 0)
        
        self.phishing_ssl_check = Gtk.CheckButton(label="Detect Phishing via SSL (--phishing-ssl)")
        heur_box.pack_start(self.phishing_ssl_check, False, False, 0)
        
        self.phishing_cloak_check = Gtk.CheckButton(label="Detect Phishing Cloaks (--phishing-cloak)")
        heur_box.pack_start(self.phishing_cloak_check, False, False, 0)
        
        self.block_encrypted_check = Gtk.CheckButton(label="Block Encrypted Archives (--block-encrypted)")
        heur_box.pack_start(self.block_encrypted_check, False, False, 0)
        
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
    
    def on_browse_clicked(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Select Directory to Scan",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.dir_entry.set_text(dialog.get_filename())
        
        dialog.destroy()
    
    def on_close_clicked(self, button):
        self.destroy()
    
    def on_scan_clicked(self, button):
        scan_dir = self.dir_entry.get_text()
        
        if not os.path.isdir(scan_dir):
            self.append_result(f"Error: Directory does not exist: {scan_dir}", "error")
            return
        
        self.scan_button.set_sensitive(False)
        self.close_button.set_sensitive(False)
        
        self.results_buffer.set_text("")
        self.append_result(f"Starting scan of: {scan_dir}", "normal")
        self.append_result("Please wait, this may take some time...\n", "normal")
        
        threading.Thread(target=self.run_scan, args=(scan_dir,), daemon=True).start()
    
    def append_result(self, text, tag_name="normal"):
        end_iter = self.results_buffer.get_end_iter()
        self.results_buffer.insert_with_tags_by_name(end_iter, text + "\n", tag_name)

        self.results_view.scroll_to_iter(self.results_buffer.get_end_iter(), 0.0, False, 0.0, 0.0)
        
    def process_results_queue(self, queue, stop_event):
        infected_count = 0
        total_files = 0
        
        while not stop_event.is_set() or not queue.empty():
            try:
                result, is_error = queue.get(timeout=0.1)
                
                tag = "error" if is_error else "normal"
                if "FOUND" in result:
                    tag = "error"
                    infected_count += 1
                elif "Error" in result or "WARNING" in result:
                    tag = "warning"
                
                if "Scanned files:" in result:
                    try:
                        parts = result.split(":")
                        if len(parts) > 1:
                            total_files += int(parts[1].strip())
                    except:
                        pass
                
                GLib.idle_add(self.append_result, result, tag)
                
                GLib.idle_add(self.update_progress)
                
                queue.task_done()
            except queue.empty:
                pass
        
        if infected_count > 0:
            GLib.idle_add(self.append_result, f"Total infected files found: {infected_count}", "error")
        else:
            GLib.idle_add(self.append_result, f"No infected files found in {total_files} scanned files", "success")


    def run_scan(self, scan_dir):
        GLib.idle_add(self.status_bar.set_fraction, 0.0)
        GLib.idle_add(self.status_bar.set_text, "Initializing scan...")
        
        import multiprocessing
        thread_count = min(multiprocessing.cpu_count(), 16)  # Use up to 16 threads
        GLib.idle_add(self.append_result, f"Using {thread_count} threads for scanning", "normal")
        
        if self.clamscan_radio.get_active():
            base_command = ["clamscan"]
        else:
            base_command = ["clamdscan"]
            
            try:
                result = subprocess.run(["systemctl", "is-active", "clamav-daemon"], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                    universal_newlines=True)
                if result.stdout.strip() != "active":
                    GLib.idle_add(self.append_result, "Error: ClamAV daemon (clamd) is not running!", "error")
                    GLib.idle_add(self.append_result, "Start it using: sudo systemctl start clamav-daemon", "normal")
                    GLib.idle_add(self.scan_complete, False)
                    return
            except Exception as e:
                GLib.idle_add(self.append_result, f"Error checking ClamAV daemon status: {str(e)}", "error")
                GLib.idle_add(self.scan_complete, False)
                return
        
        if self.recursive_check.get_active():
            base_command.append("-r")
        
        if self.infected_only_check.get_active():
            base_command.append("-i")
        
        if base_command[0] == "clamscan":
            if self.scan_archive_check.get_active():
                base_command.append("--scan-archive=yes")
            else:
                base_command.append("--scan-archive=no")
            
            if self.scan_mail_check.get_active():
                base_command.append("--scan-mail=yes")
            
            if self.scan_pdf_check.get_active():
                base_command.append("--scan-pdf=yes")
            
            if self.scan_html_check.get_active():
                base_command.append("--scan-html=yes")
        
        if hasattr(self, 'remove_check') and self.remove_check.get_active():
            base_command.append("--remove=yes")
        
        if hasattr(self, 'move_check') and self.move_check.get_active() and self.move_entry.get_text():
            move_dir = self.move_entry.get_text()
            if not os.path.exists(move_dir):
                try:
                    os.makedirs(move_dir)
                    GLib.idle_add(self.append_result, f"Created directory for infected files: {move_dir}", "normal")
                except Exception as e:
                    GLib.idle_add(self.append_result, f"Error creating move directory: {str(e)}", "error")
            base_command.append(f"--move={move_dir}")
        
        if hasattr(self, 'copy_check') and self.copy_check.get_active() and self.copy_entry.get_text():
            copy_dir = self.copy_entry.get_text()
            if not os.path.exists(copy_dir):
                try:
                    os.makedirs(copy_dir)
                    GLib.idle_add(self.append_result, f"Created directory for copying infected files: {copy_dir}", "normal")
                except Exception as e:
                    GLib.idle_add(self.append_result, f"Error creating copy directory: {str(e)}", "error")
            base_command.append(f"--copy={copy_dir}")
        
        if hasattr(self, 'exclude_check') and self.exclude_check.get_active() and self.exclude_entry.get_text():
            base_command.append(f"--exclude={self.exclude_entry.get_text()}")
        
        if hasattr(self, 'exclude_dir_check') and self.exclude_dir_check.get_active() and self.exclude_dir_entry.get_text():
            base_command.append(f"--exclude-dir={self.exclude_dir_entry.get_text()}")
        
        if hasattr(self, 'filesize_check') and self.filesize_check.get_active() and self.filesize_entry.get_text():
            base_command.append(f"--max-filesize={self.filesize_entry.get_text()}")
        
        if hasattr(self, 'scansize_check') and self.scansize_check.get_active() and self.scansize_entry.get_text():
            base_command.append(f"--max-scansize={self.scansize_entry.get_text()}")
        
        if hasattr(self, 'recursion_check') and self.recursion_check.get_active() and self.recursion_entry.get_text():
            base_command.append(f"--max-recursion={self.recursion_entry.get_text()}")
        
        if hasattr(self, 'maxfiles_check') and self.maxfiles_check.get_active() and self.maxfiles_entry.get_text():
            base_command.append(f"--max-files={self.maxfiles_entry.get_text()}")
        
        if hasattr(self, 'quiet_check') and self.quiet_check.get_active():
            base_command.append("--quiet")
        
        if hasattr(self, 'heuristic_check') and self.heuristic_check.get_active():
            base_command.append("--heuristic-alerts=yes")
        
        if hasattr(self, 'detect_pua_check') and self.detect_pua_check.get_active():
            base_command.append("--detect-pua=yes")
        
        if hasattr(self, 'phishing_check') and self.phishing_check.get_active():
            base_command.append("--phishing-sigs=yes")
        
        if hasattr(self, 'phishing_ssl_check') and self.phishing_ssl_check.get_active():
            base_command.append("--phishing-ssl=yes")
        
        if hasattr(self, 'phishing_cloak_check') and self.phishing_cloak_check.get_active():
            base_command.append("--phishing-cloak=yes")
        
        if hasattr(self, 'block_encrypted_check') and self.block_encrypted_check.get_active():
            base_command.append("--block-encrypted=yes")
        
        GLib.idle_add(self.append_result, f"Running command: {' '.join(base_command)} {scan_dir}", "normal")
        
        try:
            all_dirs = [scan_dir]
            
            if self.recursive_check.get_active():
                GLib.idle_add(self.append_result, "Finding subdirectories for parallel scanning...", "normal")
                for root, dirs, files in os.walk(scan_dir, topdown=True):
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    
                    depth = root.count(os.sep) - scan_dir.count(os.sep)
                    if depth <= 1 and dirs:
                        all_dirs.extend([os.path.join(root, d) for d in dirs])
                        
                    if len(all_dirs) >= thread_count * 4:
                        break
            
            if len(all_dirs) < thread_count:
                all_dirs = [scan_dir]
            
            from concurrent.futures import ThreadPoolExecutor
            import queue
            
            result_queue = queue.Queue()
            
            import threading
            output_lock = threading.Lock()
            
            stop_processing = threading.Event()
            results_thread = threading.Thread(
                target=self.process_results_queue, 
                args=(result_queue, stop_processing),
                daemon=True
            )
            results_thread.start()
            
            def scan_directory(directory, command):
                try:
                    cmd = command.copy()
                    cmd.append(directory)
                    
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
                            result_queue.put((output.strip(), "FOUND" in output))
                    
                    stdout, stderr = process.communicate()
                    if stdout:
                        for line in stdout.strip().split('\n'):
                            if line:
                                result_queue.put((line, "FOUND" in line))
                    if stderr:
                        for line in stderr.strip().split('\n'):
                            if line:
                                result_queue.put((line, True))
                    
                    return process.returncode
                except Exception as e:
                    result_queue.put((f"Error scanning {directory}: {str(e)}", True))
                    return 1
            
            GLib.idle_add(self.append_result, f"Starting scan with {len(all_dirs)} directories using {thread_count} threads", "normal")
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                future_to_dir = {executor.submit(scan_directory, d, base_command): d for d in all_dirs}
                
                from concurrent.futures import as_completed
                return_codes = []
                
                for future in as_completed(future_to_dir):
                    directory = future_to_dir[future]
                    try:
                        return_code = future.result()
                        return_codes.append(return_code)
                        GLib.idle_add(self.append_result, f"Completed scan of: {directory}", "normal")
                    except Exception as e:
                        GLib.idle_add(self.append_result, f"Error scanning {directory}: {str(e)}", "error")
                        return_codes.append(1)
            
            stop_processing.set()
            results_thread.join(timeout=2.0)
            
            success = all(code <= 1 for code in return_codes)
            GLib.idle_add(self.scan_complete, success)
            
        except Exception as e:
            GLib.idle_add(self.append_result, f"Error setting up scan: {str(e)}", "error")
            GLib.idle_add(self.scan_complete, False)

    def update_progress_from_output(self, total_files):
        if total_files > 0:
            current = self.status_bar.get_fraction()
            if current < 0.9:
                new_value = min(current + 0.01, 0.9)
                self.status_bar.set_fraction(new_value)
                self.status_bar.set_text(f"Scanning... {int(new_value * 100)}%")
        else:
            current = self.status_bar.get_fraction()
            if current < 0.9:
                new_value = min(current + 0.005, 0.9)
                self.status_bar.set_fraction(new_value)
                self.status_bar.set_text("Scanning...")
        return False
    
    def scan_complete(self, success):
        self.scan_button.set_sensitive(True)
        self.close_button.set_sensitive(True)
        
        if success:
            self.status_bar.set_fraction(1.0)
            self.status_bar.set_text("Scan completed successfully")
        else:
            self.status_bar.set_fraction(0.0)
            self.status_bar.set_text("Scan failed")