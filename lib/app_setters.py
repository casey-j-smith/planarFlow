def set_fullscreen(window, platform_type):
    if platform_type == "Linux":
        window.attributes("-zoomed", True)
    if platform_type == "Darwin":
        window.state("zoomed")
    if platform_type == "Windows":
        from ctypes import windll

        window.state("zoomed")
        windll.shcore.SetProcessDpiAwareness(1)  # This is necessary if the Scale and Layout settings in not 100%.


def set_icon(window, logo_path, platform_type):
    if platform_type == "Linux":
        return
    if platform_type == "Darwin":
        return
    if platform_type == "Windows":
        window.iconbitmap(logo_path)
