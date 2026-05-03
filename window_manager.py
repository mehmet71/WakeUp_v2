import time

try:
    import win32api
    import win32gui
    import win32con
    import win32process
    import psutil
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

_positioning_warned = False

_PRESETS = {
    "full":             (0,     0,     1,     1),
    "left-half":        (0,     0,     0.5,   1),
    "right-half":       (0.5,   0,     0.5,   1),
    "top-half":         (0,     0,     1,     0.5),
    "bottom-half":      (0,     0.5,   1,     0.5),
    "top-left":         (0,     0,     0.5,   0.5),
    "top-right":        (0.5,   0,     0.5,   0.5),
    "bottom-left":      (0,     0.5,   0.5,   0.5),
    "bottom-right":     (0.5,   0.5,   0.5,   0.5),
    "left-third":       (0,     0,     1/3,   1),
    "center-third":     (1/3,   0,     1/3,   1),
    "right-third":      (2/3,   0,     1/3,   1),
    "left-two-thirds":  (0,     0,     2/3,   1),
    "right-two-thirds": (1/3,   0,     2/3,   1),
}


# Returns work-area rects as (x, y, w, h): primary monitor first, then others sorted by left x-coord.
def _get_monitors() -> list[tuple[int, int, int, int]]:
    primary = []
    others = []
    for hmon, _, _ in win32api.EnumDisplayMonitors():
        info = win32api.GetMonitorInfo(hmon)
        work = info["Work"]
        rect = (work[0], work[1], work[2] - work[0], work[3] - work[1])
        if info["Flags"] & win32con.MONITORINFOF_PRIMARY:
            primary.append(rect)
        else:
            others.append(rect)
    others.sort(key=lambda r: r[0])
    return primary + others


# Maps a named preset to an absolute (x, y, w, h) rect within the given monitor rect.
def _calc_preset_rect(monitor: tuple[int, int, int, int], preset: str) -> tuple[int, int, int, int]:
    mx, my, mw, mh = monitor
    rx, ry, rw, rh = _PRESETS[preset]
    return (mx + int(mw * rx), my + int(mh * ry), int(mw * rw), int(mh * rh))


# Resolves window_cfg to a target (x, y, w, h) rect; warns and clamps if monitor index is out of range.
def _resolve_target_rect(
    window_cfg: dict,
    monitors: list[tuple[int, int, int, int]],
) -> tuple[int, int, int, int] | None:
    idx = window_cfg.get("monitor", 0)
    if idx >= len(monitors):
        print(f"[wakeup] warning: monitor {idx} not found, clamping to monitor {len(monitors) - 1}")
        idx = len(monitors) - 1
    mon = monitors[idx]

    if all(k in window_cfg for k in ("x", "y", "w", "h")):
        return (mon[0] + window_cfg["x"], mon[1] + window_cfg["y"], window_cfg["w"], window_cfg["h"])

    preset = window_cfg.get("preset")
    if preset not in _PRESETS:
        print(f"[wakeup] warning: unknown preset '{preset}'")
        return None
    return _calc_preset_rect(mon, preset)


# Searches all visible top-level windows for one owned by pid; falls back to matching by exe_name.
def _find_hwnd_for_pid(pid: int, exe_name: str) -> int | None:
    result = []

    def callback(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return
        _, owner_pid = win32process.GetWindowThreadProcessId(hwnd)
        matched = owner_pid == pid
        if not matched and exe_name:
            try:
                matched = psutil.Process(owner_pid).name().lower() == exe_name.lower()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        if matched:
            result.append(hwnd)

    win32gui.EnumWindows(callback, None)
    return result[0] if result else None


# Un-maximizes the window, moves/resizes it to rect, then re-maximizes if requested.
def _apply_position(hwnd: int, rect: tuple[int, int, int, int], maximize: bool) -> None:
    x, y, w, h = rect
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, w, h, win32con.SWP_NOZORDER)
    if maximize:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)


# Polls all (pid, window_cfg, exe_name) targets simultaneously until each window appears or 10s elapses.
def position_all(targets: list[tuple[int, dict, str]]) -> None:
    if not HAS_WIN32:
        print("[wakeup] warning: pywin32/psutil not installed — window positioning disabled")
        return

    monitors = _get_monitors()
    pending = []
    for pid, window_cfg, exe_name in targets:
        rect = _resolve_target_rect(window_cfg, monitors)
        if rect is not None:
            pending.append((pid, rect, window_cfg.get("maximize", False), exe_name))

    deadline = time.monotonic() + 10.0
    while pending and time.monotonic() < deadline:
        still_waiting = []
        for pid, rect, maximize, exe_name in pending:
            hwnd = _find_hwnd_for_pid(pid, exe_name)
            if hwnd:
                _apply_position(hwnd, rect, maximize)
            else:
                still_waiting.append((pid, rect, maximize, exe_name))
        pending = still_waiting
        if pending:
            time.sleep(0.01)

    for pid, _, _, exe_name in pending:
        print(f"[wakeup] warning: window for pid {pid} ({exe_name}) did not appear within 10s")
