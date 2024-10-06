def get_linux_distro():
    try:
        with open("/etc/os-release") as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith("PRETTY_NAME"):
                return line.split("=")[1].strip().replace('"', '')
    except FileNotFoundError:
        return "No se pudo determinar la distribuciÃ³n de Linux"


def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])

    uptime_days = uptime_seconds // (24 * 3600)
    uptime_hours = (uptime_seconds % (24 * 3600)) // 3600
    uptime_minutes = (uptime_seconds % 3600) // 60
    uptime_seconds = uptime_seconds % 60

    return int(uptime_days), int(uptime_hours), int(uptime_minutes), int(uptime_seconds)
