"""
Multi-Browser Profile Generator - Core Engine
Developed by Mr.Rahul Scripts
Supports Google Chrome, Microsoft Edge, Opera, Opera GX, Brave, Vivaldi, and Custom Browsers.
"""

import os
import sys
import glob
import subprocess
import winreg
import win32com.client


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller bundle."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


SUPPORTED_BROWSERS = {
    "chrome": {
        "id": "chrome",
        "name": "Google Chrome",
        "icon": "🌐",
        "default_prefix": "Chrome",
        "candidates": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe"),
        ],
        "reg_key": r"Software\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe",
        "mode_type": "standard",
    },
    "edge": {
        "id": "edge",
        "name": "Microsoft Edge",
        "icon": "🌊",
        "default_prefix": "Edge",
        "candidates": [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
            os.path.expandvars(r"%PROGRAMFILES(X86)%\Microsoft\Edge\Application\msedge.exe"),
            os.path.expandvars(r"%PROGRAMFILES%\Microsoft\Edge\Application\msedge.exe"),
        ],
        "reg_key": r"Software\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe",
        "mode_type": "standard",
    },
    "opera": {
        "id": "opera",
        "name": "Opera Browser",
        "icon": "🔴",
        "default_prefix": "Opera",
        "candidates": [
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Opera\launcher.exe"),
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Opera\opera.exe"),
            r"C:\Program Files\Opera\launcher.exe",
            r"C:\Program Files (x86)\Opera\launcher.exe",
            os.path.expandvars(r"%APPDATA%\Opera Software\Opera Stable\launcher.exe"),
            os.path.expandvars(r"%PROGRAMFILES%\Opera\launcher.exe"),
            os.path.expandvars(r"%PROGRAMFILES(X86)%\Opera\launcher.exe"),
        ],
        "reg_key": r"Software\Microsoft\Windows\CurrentVersion\App Paths\opera.exe",
        "mode_type": "isolated_auto",
    },
    "operagx": {
        "id": "operagx",
        "name": "Opera GX",
        "icon": "🎮",
        "default_prefix": "OperaGX",
        "candidates": [
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Opera GX\launcher.exe"),
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Opera GX\opera.exe"),
            r"C:\Program Files\Opera GX\launcher.exe",
            os.path.expandvars(r"%APPDATA%\Opera Software\Opera GX Stable\launcher.exe"),
        ],
        "reg_key": r"Software\Microsoft\Windows\CurrentVersion\App Paths\operagx.exe",
        "mode_type": "isolated_auto",
    },
    "brave": {
        "id": "brave",
        "name": "Brave Browser",
        "icon": "🦁",
        "default_prefix": "Brave",
        "candidates": [
            r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"),
            os.path.expandvars(r"%PROGRAMFILES%\BraveSoftware\Brave-Browser\Application\brave.exe"),
        ],
        "reg_key": r"Software\Microsoft\Windows\CurrentVersion\App Paths\brave.exe",
        "mode_type": "standard",
    },
    "vivaldi": {
        "id": "vivaldi",
        "name": "Vivaldi",
        "icon": "🔺",
        "default_prefix": "Vivaldi",
        "candidates": [
            os.path.expandvars(r"%LOCALAPPDATA%\Vivaldi\Application\vivaldi.exe"),
            r"C:\Program Files\Vivaldi\Application\vivaldi.exe",
            r"C:\Program Files (x86)\Vivaldi\Application\vivaldi.exe",
        ],
        "reg_key": r"Software\Microsoft\Windows\CurrentVersion\App Paths\vivaldi.exe",
        "mode_type": "standard",
    }
}


def find_browser_path(browser_id):
    """Locate the executable path for a given browser id."""
    if browser_id not in SUPPORTED_BROWSERS:
        return None
    b_info = SUPPORTED_BROWSERS[browser_id]

    # 1. Candidate paths
    for path in b_info["candidates"]:
        if os.path.isfile(path):
            return path

    # 2. Registry paths
    if "reg_key" in b_info:
        for rk in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
            try:
                with winreg.OpenKey(rk, b_info["reg_key"]) as key:
                    val, _ = winreg.QueryValueEx(key, "")
                    if val and os.path.isfile(val):
                        return val
            except Exception:
                pass

    return None


def detect_all_browsers():
    """Detect all installed browsers on the machine."""
    detected = {}
    for b_id, b_info in SUPPORTED_BROWSERS.items():
        found_path = find_browser_path(b_id)
        detected[b_id] = {
            "id": b_id,
            "name": b_info["name"],
            "icon": b_info["icon"],
            "default_prefix": b_info["default_prefix"],
            "mode_type": b_info["mode_type"],
            "path": found_path,
            "found": (found_path is not None)
        }
    return detected


def find_chrome_path():
    """Backwards compatibility for finding Chrome."""
    return find_browser_path("chrome")


def get_desktop_path():
    """Retrieve the Windows Desktop path."""
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        return shell.SpecialFolders("Desktop")
    except Exception:
        return os.path.expanduser(r"~\Desktop")


def create_profile_shortcuts(
    count: int,
    prefix: str = None,
    start_num: int = 1,
    pad_digits: int = 0,
    target_dir: str = None,
    mode: str = "standard",  # 'standard' or 'isolated'
    open_url: str = "",
    isolated_base_dir: str = None,
    browser: str = "chrome",  # browser id, 'all', or 'custom'
    custom_exe_path: str = None,
    progress_callback=None
):
    """
    Generate browser profile shortcuts for Chrome, Edge, Opera, Brave, Vivaldi, or All.
    """
    if not target_dir:
        target_dir = get_desktop_path()

    os.makedirs(target_dir, exist_ok=True)
    shell = win32com.client.Dispatch("WScript.Shell")

    # If browser is 'all', generate for all installed browsers
    if browser == "all":
        detected = detect_all_browsers()
        installed = [b for b in detected.values() if b["found"]]
        if not installed:
            raise FileNotFoundError("No supported browsers detected on this system.")

        all_created = []
        total_items = count * len(installed)
        current_overall = 0

        for b in installed:
            b_prefix = f"{b['default_prefix']}" if not prefix else f"{prefix}_{b['default_prefix']}"
            created_sub = _create_single_browser_shortcuts(
                shell=shell,
                exe_path=b["path"],
                browser_id=b["id"],
                browser_name=b["name"],
                count=count,
                prefix=b_prefix,
                start_num=start_num,
                pad_digits=pad_digits,
                target_dir=target_dir,
                mode=mode,
                open_url=open_url,
                isolated_base_dir=isolated_base_dir,
                mode_type=b["mode_type"],
                progress_callback=progress_callback,
                overall_offset=current_overall,
                overall_total=total_items
            )
            all_created.extend(created_sub)
            current_overall += count

        return all_created

    # Single browser execution
    if browser == "custom":
        if not custom_exe_path or not os.path.isfile(custom_exe_path):
            raise FileNotFoundError(f"Custom browser executable not found: {custom_exe_path}")
        exe_path = custom_exe_path
        browser_name = os.path.splitext(os.path.basename(custom_exe_path))[0].title()
        eff_prefix = prefix if prefix else browser_name
        mode_type = "standard"
    else:
        b_info = SUPPORTED_BROWSERS.get(browser)
        if not b_info:
            raise ValueError(f"Unknown browser identifier: {browser}")

        exe_path = find_browser_path(browser)
        if not exe_path:
            raise FileNotFoundError(f"{b_info['name']} could not be found on this system.")

        browser_name = b_info["name"]
        eff_prefix = prefix if prefix else b_info["default_prefix"]
        mode_type = b_info["mode_type"]

    return _create_single_browser_shortcuts(
        shell=shell,
        exe_path=exe_path,
        browser_id=browser,
        browser_name=browser_name,
        count=count,
        prefix=eff_prefix,
        start_num=start_num,
        pad_digits=pad_digits,
        target_dir=target_dir,
        mode=mode,
        open_url=open_url,
        isolated_base_dir=isolated_base_dir,
        mode_type=mode_type,
        progress_callback=progress_callback,
        overall_offset=0,
        overall_total=count
    )


def _create_single_browser_shortcuts(
    shell,
    exe_path,
    browser_id,
    browser_name,
    count,
    prefix,
    start_num,
    pad_digits,
    target_dir,
    mode,
    open_url,
    isolated_base_dir,
    mode_type,
    progress_callback=None,
    overall_offset=0,
    overall_total=1
):
    created = []

    # Isolated base dir
    if not isolated_base_dir:
        isolated_base_dir = os.path.join(os.path.expanduser("~"), f"{prefix}_Profiles")

    for i in range(count):
        idx = start_num + i
        if pad_digits > 0:
            formatted_num = str(idx).zfill(pad_digits)
        else:
            formatted_num = str(idx)

        shortcut_name = f"{prefix} {formatted_num}".strip()
        shortcut_file = os.path.join(target_dir, f"{shortcut_name}.lnk")

        # Determine CLI Arguments according to browser behavior
        if mode == "isolated" or mode_type == "isolated_auto":
            profile_data_path = os.path.join(isolated_base_dir, f"Profile_{formatted_num}")
            os.makedirs(profile_data_path, exist_ok=True)
            arguments = f'--user-data-dir="{profile_data_path}"'
        else:
            profile_dir_name = f"Profile {formatted_num}"
            arguments = f'--profile-directory="{profile_dir_name}"'

        # Optional URL to open on launch
        if open_url and open_url.strip():
            url = open_url.strip()
            if not (url.startswith("http://") or url.startswith("https://")):
                url = "https://" + url
            arguments += f' "{url}"'

        shortcut = shell.CreateShortcut(shortcut_file)
        shortcut.TargetPath = exe_path
        shortcut.Arguments = arguments
        shortcut.IconLocation = f"{exe_path},0"
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.Description = f"{browser_name} Profile {formatted_num} - Developed by Mr.Rahul Scripts"
        shortcut.Save()

        created.append(shortcut_file)

        if progress_callback:
            current_num = overall_offset + i + 1
            progress_callback(current_num, overall_total, shortcut_name)

    return created


def delete_generated_shortcuts(
    target_dir: str = None,
    prefix: str = "Chrome",
    start_num: int = 1,
    count: int = None
):
    """
    Remove generated shortcuts. If count is None, removes all matching prefix '*.lnk'.
    """
    if not target_dir:
        target_dir = get_desktop_path()

    deleted = []
    if count is None:
        pattern = os.path.join(target_dir, f"{prefix} *.lnk")
        for f in glob.glob(pattern):
            try:
                os.remove(f)
                deleted.append(f)
            except Exception:
                pass
    else:
        for i in range(count):
            idx = start_num + i
            candidates = [
                os.path.join(target_dir, f"{prefix} {idx}.lnk"),
                os.path.join(target_dir, f"{prefix} {str(idx).zfill(2)}.lnk"),
                os.path.join(target_dir, f"{prefix} {str(idx).zfill(3)}.lnk"),
                os.path.join(target_dir, f"{prefix} {str(idx).zfill(4)}.lnk"),
            ]
            for c in candidates:
                if os.path.isfile(c):
                    try:
                        os.remove(c)
                        deleted.append(c)
                    except Exception:
                        pass
    return deleted
