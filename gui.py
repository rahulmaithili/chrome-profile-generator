"""
All-In-One Browser Profile Generator - Modern Tkinter GUI
Developed by Mr.Rahul Scripts
Supports Google Chrome, Microsoft Edge, Opera, Opera GX, Brave, Vivaldi, and Custom Browsers.
"""

import os
import sys
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import profile_generator


class BrowserProfileGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("All-In-One Browser Profile Generator - Developed by Mr.Rahul Scripts")
        self.root.geometry("820x820")
        self.root.minsize(760, 720)

        # Multi-Browser Detection
        self.browsers = profile_generator.detect_all_browsers()
        self.desktop_path = profile_generator.get_desktop_path()

        # Variables
        self.var_browser = tk.StringVar(value="chrome")
        self.var_custom_exe = tk.StringVar(value="")
        self.custom_folder_path = None
        self.user_manually_edited_prefix = False

        # Color scheme - Modern Dark Theme
        self.c_bg = "#0f172a"          # slate 900
        self.c_card = "#1e293b"        # slate 800
        self.c_card_border = "#334155" # slate 700
        self.c_accent = "#38bdf8"      # sky 400
        self.c_accent_hover = "#0284c7"# sky 600
        self.c_btn_success = "#10b981" # emerald 500
        self.c_btn_success_hover = "#059669"
        self.c_btn_danger = "#f43f5e"  # rose 500
        self.c_btn_danger_hover = "#e11d48"
        self.c_btn_secondary = "#475569" # slate 600
        self.c_text = "#f8fafc"        # slate 50
        self.c_text_muted = "#94a3b8"  # slate 400
        self.c_input_bg = "#0f172a"
        self.c_input_fg = "#ffffff"

        self.root.configure(bg=self.c_bg)

        # Set Window Icon
        self.set_window_icon()

        # Configure ttk styles
        self.setup_styles()

        # Build UI layout
        self.build_ui()

    def set_window_icon(self):
        icon_path = profile_generator.get_resource_path(os.path.join("assets", "icon.ico"))
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Custom ttk progressbar
        style.configure(
            "Horizontal.TProgressbar",
            troughcolor=self.c_card_border,
            background=self.c_accent,
            bordercolor=self.c_card,
            lightcolor=self.c_accent,
            darkcolor=self.c_accent
        )

        style.configure(
            "TCombobox",
            fieldbackground=self.c_input_bg,
            background=self.c_card,
            foreground="#ffffff",
            darkcolor=self.c_card,
            lightcolor=self.c_card,
            arrowcolor="#ffffff"
        )

    def build_ui(self):
        # Outer container with canvas for smooth scrolling if needed on smaller displays
        canvas = tk.Canvas(self.root, bg=self.c_bg, highlightthickness=0)
        v_scroll = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        
        main_container = tk.Frame(canvas, bg=self.c_bg)
        main_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas_window = canvas.create_window((0, 0), window=main_container, anchor="nw")

        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", on_canvas_configure)
        canvas.configure(yscrollcommand=v_scroll.set)

        # Mouse wheel support
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(15, 0), pady=10)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # ================= 1. HEADER =================
        header_frame = tk.Frame(main_container, bg=self.c_bg)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # Right-side: RS Rahul Scripts Logo Card
        self.logo_img = None
        logo_path = profile_generator.get_resource_path(os.path.join("assets", "logo_header.png"))
        if os.path.exists(logo_path):
            try:
                self.logo_img = tk.PhotoImage(file=logo_path)
                logo_box = tk.Frame(
                    header_frame,
                    bg="#ffffff",
                    highlightbackground=self.c_card_border,
                    highlightthickness=1,
                    padx=6,
                    pady=4
                )
                logo_box.pack(side=tk.RIGHT, padx=(12, 15), anchor="ne")

                logo_lbl = tk.Label(
                    logo_box,
                    image=self.logo_img,
                    bg="#ffffff"
                )
                logo_lbl.pack()
            except Exception:
                pass

        # Left-side: Titles & Branding
        left_header = tk.Frame(header_frame, bg=self.c_bg)
        left_header.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        title_lbl = tk.Label(
            left_header,
            text="⚡ All-In-One Browser Profile Generator",
            font=("Segoe UI", 17, "bold"),
            fg=self.c_text,
            bg=self.c_bg
        )
        title_lbl.pack(anchor="w")

        dev_row = tk.Frame(left_header, bg=self.c_bg)
        dev_row.pack(anchor="w", pady=(2, 3))

        dev_lbl = tk.Label(
            dev_row,
            text="🔥 Developed by Mr.Rahul Scripts",
            font=("Segoe UI", 9, "bold"),
            fg="#38bdf8",
            bg=self.c_bg
        )
        dev_lbl.pack(side=tk.LEFT)

        tagline_lbl = tk.Label(
            dev_row,
            text=" • BUILD • AUTOMATE • GROW",
            font=("Segoe UI", 8, "bold"),
            fg="#f97316",
            bg=self.c_bg
        )
        tagline_lbl.pack(side=tk.LEFT)

        subtitle_lbl = tk.Label(
            left_header,
            text="Unlimited profiles for Chrome, Edge, Opera, Opera GX, Brave, Vivaldi & custom browsers.",
            font=("Segoe UI", 9),
            fg=self.c_text_muted,
            bg=self.c_bg
        )
        subtitle_lbl.pack(anchor="w")

        # ================= 2. BROWSER SELECTION CARD =================
        browser_card = tk.LabelFrame(
            main_container,
            text=" 🌐 Select Browser (ब्राउज़र चुनें) ",
            font=("Segoe UI", 10, "bold"),
            fg=self.c_accent,
            bg=self.c_card,
            bd=1,
            relief=tk.SOLID,
            padx=14,
            pady=10
        )
        browser_card.pack(fill=tk.X, padx=(0, 15), pady=(0, 8))

        b_row = tk.Frame(browser_card, bg=self.c_card)
        b_row.pack(fill=tk.X, pady=(0, 6))

        tk.Label(
            b_row,
            text="Choose Target Browser:",
            font=("Segoe UI", 9, "bold"),
            fg=self.c_text,
            bg=self.c_card,
            width=22,
            anchor="w"
        ).pack(side=tk.LEFT)

        # Build dropdown options with detection status
        self.browser_options = self.get_browser_dropdown_list()
        self.cb_browser = ttk.Combobox(
            b_row,
            values=[opt[0] for opt in self.browser_options],
            state="readonly",
            font=("Segoe UI", 9, "bold"),
            width=36
        )
        self.cb_browser.current(0)
        self.cb_browser.pack(side=tk.LEFT, padx=(0, 8))
        self.cb_browser.bind("<<ComboboxSelected>>", self.on_browser_changed)

        btn_rescan = tk.Button(
            b_row,
            text="🔄 Re-Scan",
            font=("Segoe UI", 8, "bold"),
            bg=self.c_btn_secondary,
            fg="#ffffff",
            activebackground=self.c_card_border,
            relief=tk.FLAT,
            cursor="hand2",
            padx=8,
            pady=2,
            command=self.rescan_browsers
        )
        btn_rescan.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_browse_exe = tk.Button(
            b_row,
            text="📂 Browse .EXE",
            font=("Segoe UI", 8, "bold"),
            bg=self.c_card_border,
            fg="#ffffff",
            activebackground=self.c_btn_secondary,
            relief=tk.FLAT,
            cursor="hand2",
            padx=8,
            pady=2,
            command=self.browse_custom_exe
        )
        self.btn_browse_exe.pack(side=tk.LEFT)

        # Status Badge for selected browser
        self.lbl_browser_status = tk.Label(
            browser_card,
            text="",
            font=("Consolas", 8),
            fg="#34d399",
            bg=self.c_card,
            anchor="w"
        )
        self.lbl_browser_status.pack(fill=tk.X, pady=(2, 0))

        # ================= 3. CONFIGURATION CARD =================
        config_card = tk.LabelFrame(
            main_container,
            text=" Profile Configuration (प्रोफाइल सेटिंग्स) ",
            font=("Segoe UI", 10, "bold"),
            fg=self.c_accent,
            bg=self.c_card,
            bd=1,
            relief=tk.SOLID,
            padx=14,
            pady=10
        )
        config_card.pack(fill=tk.X, padx=(0, 15), pady=(0, 8))

        # Row 1: Count
        r1 = tk.Frame(config_card, bg=self.c_card)
        r1.pack(fill=tk.X, pady=3)

        tk.Label(
            r1,
            text="Profiles Count (Kitne Profile Banane Hai?):",
            font=("Segoe UI", 9, "bold"),
            fg=self.c_text,
            bg=self.c_card,
            width=36,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.var_count = tk.StringVar(value="10")
        self.entry_count = tk.Entry(
            r1,
            textvariable=self.var_count,
            font=("Segoe UI", 10, "bold"),
            width=10,
            bg=self.c_input_bg,
            fg=self.c_accent,
            insertbackground="white",
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.c_card_border,
            justify="center"
        )
        self.entry_count.pack(side=tk.LEFT, padx=(0, 10))

        count_presets = [("5", "5"), ("10", "10"), ("25", "25"), ("50", "50"), ("100", "100")]
        for label, val in count_presets:
            btn = tk.Button(
                r1,
                text=label,
                font=("Segoe UI", 8),
                bg=self.c_card_border,
                fg=self.c_text,
                activebackground=self.c_accent,
                activeforeground="#000000",
                relief=tk.FLAT,
                cursor="hand2",
                padx=6,
                pady=1,
                command=lambda v=val: self.var_count.set(v)
            )
            btn.pack(side=tk.LEFT, padx=2)

        # Row 2: Prefix
        r2 = tk.Frame(config_card, bg=self.c_card)
        r2.pack(fill=tk.X, pady=4)

        tk.Label(
            r2,
            text="Name Prefix (Shortcut Ka Naam):",
            font=("Segoe UI", 9),
            fg=self.c_text,
            bg=self.c_card,
            width=36,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.var_prefix = tk.StringVar(value="Chrome")
        self.entry_prefix = tk.Entry(
            r2,
            textvariable=self.var_prefix,
            font=("Segoe UI", 9),
            width=18,
            bg=self.c_input_bg,
            fg=self.c_text,
            insertbackground="white",
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.c_card_border
        )
        self.entry_prefix.pack(side=tk.LEFT, padx=(0, 8))
        self.entry_prefix.bind("<KeyRelease>", self.on_prefix_manual_edit)

        prefix_presets = ["Chrome", "Edge", "Opera", "Work", "Bot", "User"]
        for p in prefix_presets:
            btn = tk.Button(
                r2,
                text=p,
                font=("Segoe UI", 8),
                bg=self.c_card_border,
                fg=self.c_text_muted,
                relief=tk.FLAT,
                cursor="hand2",
                padx=4,
                pady=1,
                command=lambda val=p: self.set_prefix_preset(val)
            )
            btn.pack(side=tk.LEFT, padx=2)

        # Row 3: Start Number & Padding
        r3 = tk.Frame(config_card, bg=self.c_card)
        r3.pack(fill=tk.X, pady=4)

        tk.Label(
            r3,
            text="Start Index (Shuruwat Kahan Se Ho?):",
            font=("Segoe UI", 9),
            fg=self.c_text,
            bg=self.c_card,
            width=36,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.var_start_num = tk.StringVar(value="1")
        tk.Entry(
            r3,
            textvariable=self.var_start_num,
            font=("Segoe UI", 9),
            width=6,
            bg=self.c_input_bg,
            fg=self.c_text,
            insertbackground="white",
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.c_card_border,
            justify="center"
        ).pack(side=tk.LEFT, padx=(0, 15))

        tk.Label(
            r3,
            text="Zero Padding:",
            font=("Segoe UI", 9),
            fg=self.c_text,
            bg=self.c_card
        ).pack(side=tk.LEFT, padx=(0, 6))

        self.var_pad = tk.StringVar(value="none")
        pad_options = [("1, 2, 3...", "none"), ("01, 02...", "2"), ("001, 002...", "3")]
        for text, val in pad_options:
            rb = tk.Radiobutton(
                r3,
                text=text,
                variable=self.var_pad,
                value=val,
                font=("Segoe UI", 8),
                fg=self.c_text,
                bg=self.c_card,
                selectcolor=self.c_input_bg,
                activebackground=self.c_card,
                activeforeground=self.c_text
            )
            rb.pack(side=tk.LEFT, padx=3)

        # Row 4: Mode (Standard vs Isolated)
        r4 = tk.Frame(config_card, bg=self.c_card)
        r4.pack(fill=tk.X, pady=4)

        tk.Label(
            r4,
            text="Profile Mode:",
            font=("Segoe UI", 9),
            fg=self.c_text,
            bg=self.c_card,
            width=20,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.var_mode = tk.StringVar(value="standard")
        rb_mode1 = tk.Radiobutton(
            r4,
            text="Standard (--profile-directory) - Recommended for Chrome/Edge/Brave",
            variable=self.var_mode,
            value="standard",
            font=("Segoe UI", 8),
            fg=self.c_text,
            bg=self.c_card,
            selectcolor=self.c_input_bg,
            activebackground=self.c_card,
            activeforeground=self.c_text
        )
        rb_mode1.pack(side=tk.LEFT, padx=(0, 10))

        rb_mode2 = tk.Radiobutton(
            r4,
            text="Isolated Folder (--user-data-dir)",
            variable=self.var_mode,
            value="isolated",
            font=("Segoe UI", 8),
            fg=self.c_text,
            bg=self.c_card,
            selectcolor=self.c_input_bg,
            activebackground=self.c_card,
            activeforeground=self.c_text
        )
        rb_mode2.pack(side=tk.LEFT)

        # Row 5: Auto URL
        r5 = tk.Frame(config_card, bg=self.c_card)
        r5.pack(fill=tk.X, pady=4)

        tk.Label(
            r5,
            text="Auto-Open URL (Optional):",
            font=("Segoe UI", 9),
            fg=self.c_text,
            bg=self.c_card,
            width=20,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.var_url = tk.StringVar(value="")
        self.entry_url = tk.Entry(
            r5,
            textvariable=self.var_url,
            font=("Segoe UI", 9),
            bg=self.c_input_bg,
            fg=self.c_text,
            insertbackground="white",
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.c_card_border
        )
        self.entry_url.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Label(
            r5,
            text="e.g. google.com or blank",
            font=("Segoe UI", 8),
            fg=self.c_text_muted,
            bg=self.c_card
        ).pack(side=tk.LEFT)

        # ================= 4. DESTINATION LOCATION CARD =================
        loc_card = tk.LabelFrame(
            main_container,
            text=" Destination Location (Shortcuts Kahan Banayein?) ",
            font=("Segoe UI", 10, "bold"),
            fg=self.c_accent,
            bg=self.c_card,
            bd=1,
            relief=tk.SOLID,
            padx=14,
            pady=8
        )
        loc_card.pack(fill=tk.X, padx=(0, 15), pady=(0, 8))

        self.var_loc_type = tk.StringVar(value="desktop_direct")
        loc_row = tk.Frame(loc_card, bg=self.c_card)
        loc_row.pack(fill=tk.X)

        tk.Radiobutton(
            loc_row,
            text="🖥️ Directly on Desktop",
            variable=self.var_loc_type,
            value="desktop_direct",
            font=("Segoe UI", 9),
            fg=self.c_text,
            bg=self.c_card,
            selectcolor=self.c_input_bg,
            activebackground=self.c_card,
            activeforeground=self.c_text,
            command=self.update_loc_preview
        ).pack(side=tk.LEFT, padx=(0, 12))

        tk.Radiobutton(
            loc_row,
            text="📁 Desktop Folder ('My Browser Profiles')",
            variable=self.var_loc_type,
            value="desktop_folder",
            font=("Segoe UI", 9),
            fg=self.c_text,
            bg=self.c_card,
            selectcolor=self.c_input_bg,
            activebackground=self.c_card,
            activeforeground=self.c_text,
            command=self.update_loc_preview
        ).pack(side=tk.LEFT, padx=(0, 12))

        tk.Radiobutton(
            loc_row,
            text="📂 Choose Custom Folder...",
            variable=self.var_loc_type,
            value="custom",
            font=("Segoe UI", 9),
            fg=self.c_text,
            bg=self.c_card,
            selectcolor=self.c_input_bg,
            activebackground=self.c_card,
            activeforeground=self.c_text,
            command=self.choose_custom_folder
        ).pack(side=tk.LEFT)

        # ================= 5. ACTION BUTTONS =================
        btn_bar = tk.Frame(main_container, bg=self.c_bg)
        btn_bar.pack(fill=tk.X, padx=(0, 15), pady=(0, 8))

        self.btn_generate = tk.Button(
            btn_bar,
            text="🚀 GENERATE PROFILES NOW",
            font=("Segoe UI", 11, "bold"),
            bg=self.c_btn_success,
            fg="#ffffff",
            activebackground=self.c_btn_success_hover,
            activeforeground="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=9,
            command=self.start_generation
        )
        self.btn_generate.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        self.btn_clean = tk.Button(
            btn_bar,
            text="🗑️ Delete Generated",
            font=("Segoe UI", 9, "bold"),
            bg=self.c_btn_danger,
            fg="#ffffff",
            activebackground=self.c_btn_danger_hover,
            activeforeground="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            padx=14,
            pady=9,
            command=self.confirm_cleanup
        )
        self.btn_clean.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_open_folder = tk.Button(
            btn_bar,
            text="📂 Open Desktop / Folder",
            font=("Segoe UI", 9, "bold"),
            bg=self.c_btn_secondary,
            fg="#ffffff",
            activebackground=self.c_card_border,
            activeforeground="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            padx=14,
            pady=9,
            command=self.open_target_folder
        )
        self.btn_open_folder.pack(side=tk.LEFT)

        # ================= 6. PROGRESS & ACTIVITY LOG =================
        log_card = tk.LabelFrame(
            main_container,
            text=" Activity & Generation Status ",
            font=("Segoe UI", 10, "bold"),
            fg=self.c_accent,
            bg=self.c_card,
            bd=1,
            relief=tk.SOLID,
            padx=12,
            pady=8
        )
        log_card.pack(fill=tk.BOTH, expand=True, padx=(0, 15))

        prog_frame = tk.Frame(log_card, bg=self.c_card)
        prog_frame.pack(fill=tk.X, pady=(0, 6))

        self.prog_bar = ttk.Progressbar(
            prog_frame,
            style="Horizontal.TProgressbar",
            orient="horizontal",
            mode="determinate"
        )
        self.prog_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.lbl_percent = tk.Label(
            prog_frame,
            text="0%",
            font=("Segoe UI", 9, "bold"),
            fg=self.c_accent,
            bg=self.c_card,
            width=5
        )
        self.lbl_percent.pack(side=tk.RIGHT)

        self.txt_log = tk.Text(
            log_card,
            font=("Consolas", 9),
            bg=self.c_input_bg,
            fg="#e2e8f0",
            insertbackground="white",
            relief=tk.FLAT,
            height=9,
            wrap=tk.WORD
        )
        self.txt_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(log_card, command=self.txt_log.yview, bg=self.c_card)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_log.config(yscrollcommand=scrollbar.set)

        # ================= 7. FOOTER =================
        footer_frame = tk.Frame(main_container, bg=self.c_bg)
        footer_frame.pack(fill=tk.X, padx=(0, 15), pady=(6, 0))

        lbl_footer_dev = tk.Label(
            footer_frame,
            text="Developed by Mr.Rahul Scripts  |  BUILD • AUTOMATE • GROW",
            font=("Segoe UI", 8, "bold"),
            fg="#38bdf8",
            bg=self.c_bg
        )
        lbl_footer_dev.pack(side=tk.RIGHT)

        lbl_footer_info = tk.Label(
            footer_frame,
            text="⚡ All-In-One Multi-Browser Profile Generator v2.0",
            font=("Segoe UI", 8),
            fg=self.c_text_muted,
            bg=self.c_bg
        )
        lbl_footer_info.pack(side=tk.LEFT)

        # Initial Setup & Logs
        self.update_browser_status_display()
        self.log("=" * 60)
        self.log("⚡ All-In-One Multi-Browser Profile Generator")
        self.log("🛠️ Developed by Mr.Rahul Scripts")
        self.log("=" * 60)
        self.log("✅ Tool Ready.")
        for b_id, b in self.browsers.items():
            if b["found"]:
                self.log(f"   {b['icon']} {b['name']}: Detected ({b['path']})")
        self.log(f"📁 Desktop Target: {self.desktop_path}")
        self.log("ℹ️ Select your browser, enter count, and click 'GENERATE PROFILES NOW'.")

    # ================= LOGIC METHODS =================
    def get_browser_dropdown_list(self):
        """Build the list of dropdown options (label, browser_id)."""
        options = []
        # Individual browsers
        for b_id, b in self.browsers.items():
            status = " [Detected]" if b["found"] else " [Not Found]"
            label = f"{b['icon']} {b['name']}{status}"
            options.append((label, b_id))

        # Batch mode
        detected_names = [b["name"] for b in self.browsers.values() if b["found"]]
        detected_summary = ", ".join(detected_names) if detected_names else "None"
        options.append((f"⚡ ALL Detected Browsers ({detected_summary})", "all"))

        # Custom
        options.append(("📁 Custom Browser Executable (.exe)...", "custom"))
        return options

    def rescan_browsers(self):
        self.browsers = profile_generator.detect_all_browsers()
        self.browser_options = self.get_browser_dropdown_list()
        self.cb_browser["values"] = [opt[0] for opt in self.browser_options]
        self.update_browser_status_display()
        self.log("🔄 Browser scan refreshed.")
        for b_id, b in self.browsers.items():
            if b["found"]:
                self.log(f"   ● {b['name']}: {b['path']}")

    def on_browser_changed(self, event=None):
        idx = self.cb_browser.current()
        if 0 <= idx < len(self.browser_options):
            b_id = self.browser_options[idx][1]
            self.var_browser.set(b_id)

            # Auto-update prefix if user hasn't manually entered a custom prefix
            if not self.user_manually_edited_prefix:
                if b_id in self.browsers:
                    self.var_prefix.set(self.browsers[b_id]["default_prefix"])
                elif b_id == "all":
                    self.var_prefix.set("Browser")
                elif b_id == "custom":
                    self.var_prefix.set("Custom")

            # If user selected custom, prompt browse if not yet set
            if b_id == "custom" and not self.var_custom_exe.get():
                self.browse_custom_exe()

            self.update_browser_status_display()

    def update_browser_status_display(self):
        b_id = self.var_browser.get()
        if b_id == "all":
            detected = [b["name"] for b in self.browsers.values() if b["found"]]
            if detected:
                self.lbl_browser_status.config(
                    text=f"⚡ Batch Mode Active: Will create profiles for {len(detected)} browsers ({', '.join(detected)})",
                    fg="#38bdf8"
                )
            else:
                self.lbl_browser_status.config(
                    text="⚠️ No supported browsers detected automatically. Please specify a custom browser .exe",
                    fg="#f43f5e"
                )
        elif b_id == "custom":
            exe = self.var_custom_exe.get()
            if exe and os.path.isfile(exe):
                self.lbl_browser_status.config(text=f"● Custom Executable: {exe}", fg="#34d399")
            else:
                self.lbl_browser_status.config(text="⚠️ Please click 'Browse .EXE' to choose your browser executable.", fg="#fbbf24")
        else:
            b = self.browsers.get(b_id)
            if b and b["found"]:
                self.lbl_browser_status.config(
                    text=f"● {b['name']} Detected: {b['path']}",
                    fg="#34d399"
                )
            else:
                b_name = b["name"] if b else "Selected browser"
                self.lbl_browser_status.config(
                    text=f"⚠️ {b_name} not detected in standard location. Click 'Browse .EXE' to select manually.",
                    fg="#fbbf24"
                )

    def browse_custom_exe(self):
        f = filedialog.askopenfilename(
            title="Select Browser Executable (chrome.exe, msedge.exe, opera.exe, etc.)",
            filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")]
        )
        if f:
            self.var_custom_exe.set(f)
            # Switch combobox to custom
            for i, opt in enumerate(self.browser_options):
                if opt[1] == "custom":
                    self.cb_browser.current(i)
                    self.var_browser.set("custom")
                    break
            self.update_browser_status_display()
            self.log(f"Custom browser selected: {f}")

    def on_prefix_manual_edit(self, event=None):
        self.user_manually_edited_prefix = True

    def set_prefix_preset(self, val):
        self.var_prefix.set(val)
        self.user_manually_edited_prefix = True

    def update_loc_preview(self):
        loc = self.get_target_directory()
        self.log(f"Target location set to: {loc}")

    def choose_custom_folder(self):
        f = filedialog.askdirectory(title="Select Destination Folder for Shortcuts")
        if f:
            self.custom_folder_path = f
            self.log(f"Custom folder selected: {f}")
        else:
            self.var_loc_type.set("desktop_direct")

    def get_target_directory(self):
        t = self.var_loc_type.get()
        if t == "desktop_direct":
            return self.desktop_path
        elif t == "desktop_folder":
            return os.path.join(self.desktop_path, "My Browser Profiles")
        elif t == "custom":
            return self.custom_folder_path if self.custom_folder_path else self.desktop_path
        return self.desktop_path

    def log(self, msg):
        self.txt_log.insert(tk.END, msg + "\n")
        self.txt_log.see(tk.END)

    def start_generation(self):
        # Validate count
        raw_count = self.var_count.get().strip()
        try:
            count = int(raw_count)
            if count <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Invalid Count", "Please enter a valid positive number of profiles (e.g., 10).")
            self.entry_count.focus_set()
            return

        if count > 1000:
            if not messagebox.askyesno("Large Batch Warning", f"Are you sure you want to generate {count} profiles?"):
                return

        raw_start = self.var_start_num.get().strip()
        try:
            start_num = int(raw_start)
            if start_num < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Invalid Start Index", "Please enter a valid start number (e.g., 1).")
            return

        prefix = self.var_prefix.get().strip()
        mode = self.var_mode.get()
        url = self.var_url.get().strip()
        target_dir = self.get_target_directory()
        browser_id = self.var_browser.get()
        custom_exe = self.var_custom_exe.get()

        pad_setting = self.var_pad.get()
        padding = 0 if pad_setting == "none" else int(pad_setting)

        # Check if browser is present
        if browser_id == "custom":
            if not custom_exe or not os.path.isfile(custom_exe):
                messagebox.showerror("Missing Browser EXE", "Please click 'Browse .EXE' to select the browser executable.")
                return
        elif browser_id != "all":
            b_info = self.browsers.get(browser_id)
            if not b_info or not b_info["found"]:
                res = messagebox.askyesno(
                    "Browser Not Detected",
                    f"{b_info['name'] if b_info else browser_id} was not detected automatically in standard folders.\n\n"
                    "Would you like to browse and locate the .exe file manually now?"
                )
                if res:
                    self.browse_custom_exe()
                return

        # Disable buttons while generating
        self.btn_generate.config(state=tk.DISABLED, text="⏳ Generating...")
        self.btn_clean.config(state=tk.DISABLED)
        self.prog_bar["value"] = 0
        self.lbl_percent.config(text="0%")

        self.log("-" * 60)
        self.log(f"🚀 Starting Profile Generation...")
        self.log(f"   Target Browser : {browser_id.upper()}")
        self.log(f"   Count          : {count} profiles")
        self.log(f"   Prefix         : '{prefix}'")
        self.log(f"   Directory      : {target_dir}")
        self.log(f"   Mode           : {mode}")

        def worker():
            try:
                def progress(current, total, name):
                    pct = int((current / total) * 100)
                    self.root.after(0, lambda: self.update_progress(pct, f"Created [{current}/{total}]: {name}.lnk"))

                created = profile_generator.create_profile_shortcuts(
                    count=count,
                    prefix=prefix,
                    start_num=start_num,
                    pad_digits=padding,
                    target_dir=target_dir,
                    mode=mode,
                    open_url=url,
                    browser=browser_id,
                    custom_exe_path=custom_exe,
                    progress_callback=progress
                )

                self.root.after(0, lambda: self.finish_generation(len(created), target_dir))
            except Exception as e:
                self.root.after(0, lambda: self.handle_error(str(e)))

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def update_progress(self, pct, msg):
        self.prog_bar["value"] = pct
        self.lbl_percent.config(text=f"{pct}%")
        self.log(msg)

    def finish_generation(self, count, target_dir):
        self.btn_generate.config(state=tk.NORMAL, text="🚀 GENERATE PROFILES NOW")
        self.btn_clean.config(state=tk.NORMAL)
        self.prog_bar["value"] = 100
        self.lbl_percent.config(text="100%")
        self.log(f"🎉 SUCCESS: Successfully created {count} profile shortcuts!")
        self.log("=" * 60)

        res = messagebox.askyesno(
            "Generation Completed!",
            f"Successfully created {count} profile shortcuts!\n\nLocation: {target_dir}\n\nWould you like to open the folder now?"
        )
        if res:
            self.open_target_folder()

    def handle_error(self, err_msg):
        self.btn_generate.config(state=tk.NORMAL, text="🚀 GENERATE PROFILES NOW")
        self.btn_clean.config(state=tk.NORMAL)
        self.log(f"❌ ERROR: {err_msg}")
        messagebox.showerror("Error", f"Failed to generate profiles:\n{err_msg}")

    def confirm_cleanup(self):
        prefix = self.var_prefix.get().strip() or "Profile"
        target_dir = self.get_target_directory()

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete all '{prefix} *.lnk' shortcuts from:\n{target_dir}?\n\nThis will only remove desktop shortcuts, not your browsing history or data."
        )
        if not confirm:
            return

        deleted = profile_generator.delete_generated_shortcuts(
            target_dir=target_dir,
            prefix=prefix
        )
        self.log(f"🧹 Cleaned up {len(deleted)} shortcuts matching '{prefix} *.lnk'.")
        messagebox.showinfo("Cleanup Finished", f"Removed {len(deleted)} shortcut(s).")

    def open_target_folder(self):
        target_dir = self.get_target_directory()
        if os.path.exists(target_dir):
            os.startfile(target_dir)
        else:
            os.startfile(self.desktop_path)


def main():
    root = tk.Tk()
    app = BrowserProfileGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
