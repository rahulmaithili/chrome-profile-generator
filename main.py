"""
All-In-One Browser Profile Generator - Entry Point
Supports both GUI and CLI modes.
Developed by Mr.Rahul Scripts
"""

import os
import sys
import argparse
import profile_generator


# Ensure UTF-8 output encoding for Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def cli_mode(args):
    print("=" * 65)
    print(" ⚡ All-In-One Browser Profile Generator (CLI Mode)")
    print(" 🛠️ Developed by Mr.Rahul Scripts")
    print("=" * 65)

    desktop = profile_generator.get_desktop_path()
    target_dir = args.dir if args.dir else desktop

    print(f"[*] Target Browser: {args.browser.upper()}")
    print(f"[*] Target Dir    : {target_dir}")
    print(f"[*] Count         : {args.count}")
    print(f"[*] Prefix        : {args.prefix or '(Auto by browser)'}")
    print(f"[*] Start Index   : {args.start}")
    print(f"[*] Mode          : {args.mode}")
    if args.url:
        print(f"[*] Auto URL      : {args.url}")
    print("-" * 65)

    if args.delete:
        eff_prefix = args.prefix if args.prefix else "Chrome"
        print(f"[*] Deleting shortcuts matching '{eff_prefix} *.lnk'...")
        deleted = profile_generator.delete_generated_shortcuts(
            target_dir=target_dir,
            prefix=eff_prefix
        )
        print(f"[OK] Deleted {len(deleted)} shortcut(s).")
        return

    def print_progress(cur, total, name):
        pct = int((cur / total) * 100)
        sys.stdout.write(f"\rGenerating: [{cur}/{total}] ({pct}%) -> {name}.lnk")
        sys.stdout.flush()

    try:
        created = profile_generator.create_profile_shortcuts(
            count=args.count,
            prefix=args.prefix,
            start_num=args.start,
            pad_digits=args.pad,
            target_dir=target_dir,
            mode=args.mode,
            open_url=args.url or "",
            browser=args.browser,
            custom_exe_path=args.exe,
            progress_callback=print_progress
        )
        print()
        print(f"\n[OK] Successfully created {len(created)} profile shortcuts!")
    except Exception as e:
        print(f"\n[!] ERROR: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="All-In-One Multi-Browser Profile Generator - Mr.Rahul Scripts")
    parser.add_argument("--count", type=int, default=0, help="Number of profiles to generate")
    parser.add_argument("--browser", type=str, default="chrome", choices=["chrome", "edge", "opera", "operagx", "brave", "vivaldi", "all", "custom"], help="Target browser (default: chrome)")
    parser.add_argument("--exe", type=str, default="", help="Path to custom browser executable if --browser custom")
    parser.add_argument("--prefix", type=str, default="", help="Shortcut prefix name (e.g. Chrome, Edge, Work)")
    parser.add_argument("--start", type=int, default=1, help="Starting index (default: 1)")
    parser.add_argument("--pad", type=int, default=0, help="Zero padding digits (e.g. 2 for 01, 3 for 001)")
    parser.add_argument("--dir", type=str, default="", help="Custom output directory")
    parser.add_argument("--mode", type=str, default="standard", choices=["standard", "isolated"], help="Profile mode")
    parser.add_argument("--url", type=str, default="", help="Optional URL to open on launch")
    parser.add_argument("--delete", action="store_true", help="Delete shortcuts matching prefix")

    args = parser.parse_args()

    # If count > 0 or delete flag specified, run CLI mode
    if args.count > 0 or args.delete:
        cli_mode(args)
    else:
        # Launch GUI
        import gui
        gui.main()


if __name__ == "__main__":
    main()
