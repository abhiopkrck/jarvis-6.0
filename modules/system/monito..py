import platform
import time

class SystemMonitor:
    def __init__(self):
        self.psutil_available = False
        self.speedtest_available = False
        self._check_dependencies()
    
    def _check_dependencies(self):
        try:
            import psutil
            self.psutil_available = True
        except ImportError:
            print("⚠️ psutil not available")
        
        try:
            import speedtest
            self.speedtest_available = True
        except ImportError:
            print("⚠️ speedtest not available")

    def get_cpu_temperature(self):
        if not self.psutil_available:
            return "N/A"
            
        try:
            import psutil
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        for entry in entries:
                            if 'core' in entry.label.lower():
                                return f"{entry.current}°C"
            return "N/A"
        except:
            return "N/A"

    def get_cpu_usage(self):
        if self.psutil_available:
            import psutil
            return f"{psutil.cpu_percent(interval=0.5)}%"
        return "N/A"

    def get_ram_usage(self):
        if self.psutil_available:
            import psutil
            memory = psutil.virtual_memory()
            return f"{memory.percent}%"
        return "N/A"

    def get_network_status(self):
        try:
            if self.speedtest_available:
                import speedtest
                st = speedtest.Speedtest()
                st.get_best_server()
                return "🟢 ONLINE"
            
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return "🟢 ONLINE"
        except:
            return "🔴 OFFLINE"

    def get_disk_usage(self):
        if self.psutil_available:
            import psutil
            try:
                disk = psutil.disk_usage('/' if platform.system() != "Windows" else 'C:\\')
                return f"{disk.percent}%"
            except:
                return "N/A"
        return "N/A"

    def get_battery_status(self):
        if self.psutil_available:
            import psutil
            try:
                battery = psutil.sensors_battery()
                if battery:
                    return f"{int(battery.percent)}%"
                return "N/A"
            except:
                return "N/A"
        return "N/A"