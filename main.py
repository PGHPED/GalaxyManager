import psutil
import os
import time
from datetime import datetime
import platform
import shutil

class Colors:
    RESET = '\033[0m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    CLEAR_LINE = '\033[K'
    HIDE_CURSOR = '\033[?25l'
    SHOW_CURSOR = '\033[?25h'

def move_cursor(row, col):
    return f'\033[{row};{col}H'

class GalaxyManager:
    def __init__(self):
        self.running = True
        self.terminal_width = shutil.get_terminal_size().columns
        self.terminal_height = shutil.get_terminal_size().lines
        self.last_net_io = psutil.net_io_counters()
        self.last_disk_io = psutil.disk_io_counters()
        self.last_time = time.time()
        self.first_draw = True
        
        if platform.system() == 'Windows':
            os.system('color')
            os.system('')
        print(Colors.HIDE_CURSOR, end='')

    def clear_screen_once(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')

    def update_at(self, row, col, content):
        print(f"{move_cursor(row, col)}{content}", end='', flush=True)

    def clear_at(self, row, col, width):
        print(f"{move_cursor(row, col)}{' ' * width}", end='', flush=True)

    def get_cpu_temp(self):
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                return None
            
            if 'coretemp' in temps:
                return temps['coretemp'][0].current
            elif 'cpu_thermal' in temps:
                return temps['cpu_thermal'][0].current
            elif 'acpitz' in temps:
                return temps['acpitz'][0].current
            else:
                for name, entries in temps.items():
                    if entries:
                        return entries[0].current
        except:
            pass
        return None

    def draw_bar(self, percentage, width=20):
        filled = int(width * percentage / 100)
        bar = "█" * filled + "░" * (width - filled)
        
        if percentage > 80:
            color = Colors.RED
        elif percentage > 60:
            color = Colors.YELLOW
        else:
            color = Colors.GREEN
        
        return f"[{color}{bar}{Colors.RESET}] {Colors.MAGENTA}{percentage:5.1f}%{Colors.RESET}"

    def draw_static_layout(self):
        center_col = (self.terminal_width - 60) // 2
        
        logo = [
            f"{Colors.CYAN}{Colors.BOLD} _____     _                _____                         {Colors.RESET}",
            f"{Colors.CYAN}{Colors.BOLD}|   __|___| |___ _ _ _ _   |     |___ ___ ___ ___ ___ ___ {Colors.RESET}",
            f"{Colors.CYAN}{Colors.BOLD}|  |  | .'| | .'|_'_| | |  | | | | .'|   | .'| . | -_|  _|{Colors.RESET}",
            f"{Colors.CYAN}{Colors.BOLD}|_____|__,|_|__,|_,_|_  |  |_|_|_|__,|_|_|__,|_  |___|_|  {Colors.RESET}",
            f"{Colors.CYAN}{Colors.BOLD}                    |___|                    |___|         {Colors.RESET}"
        ]
        
        for i, line in enumerate(logo):
            self.update_at(1 + i, center_col, line)
        
        self.update_at(7, (self.terminal_width - 26) // 2, f"{Colors.DIM}Professional Edition v2.0{Colors.RESET}")
        
        col1 = 2
        row = 9
        
        self.update_at(row, col1, f"{Colors.CYAN}╔═══ SYSTEM OVERVIEW ═══════════════════════════╗{Colors.RESET}")
        self.update_at(row + 1, col1, f"{Colors.CYAN}║{Colors.RESET} {Colors.WHITE}OS:{Colors.RESET}")
        self.update_at(row + 2, col1, f"{Colors.CYAN}║{Colors.RESET} {Colors.WHITE}Uptime:{Colors.RESET}")
        self.update_at(row + 3, col1, f"{Colors.CYAN}║{Colors.RESET} {Colors.WHITE}CPU Load:{Colors.RESET}")
        self.update_at(row + 4, col1, f"{Colors.CYAN}║{Colors.RESET} {Colors.WHITE}Memory:{Colors.RESET}")
        
        try:
            battery = psutil.sensors_battery()
            if battery:
                self.update_at(row + 5, col1, f"{Colors.CYAN}║{Colors.RESET} {Colors.WHITE}Battery:{Colors.RESET}")
                self.update_at(row + 6, col1, f"{Colors.CYAN}╚═══════════════════════════════════════════════╝{Colors.RESET}")
            else:
                self.update_at(row + 5, col1, f"{Colors.CYAN}╚═══════════════════════════════════════════════╝{Colors.RESET}")
        except:
            self.update_at(row + 5, col1, f"{Colors.CYAN}╚═══════════════════════════════════════════════╝{Colors.RESET}")
        
        col2 = self.terminal_width - 52
        row = 9
        
        self.update_at(row, col2, f"{Colors.BLUE}╔═══ CPU DETAILS ═══════════════════════════════╗{Colors.RESET}")
        self.update_at(row + 1, col2, f"{Colors.BLUE}║{Colors.RESET} {Colors.WHITE}Physical Cores:{Colors.RESET}")
        self.update_at(row + 2, col2, f"{Colors.BLUE}║{Colors.RESET} {Colors.WHITE}Logical Cores:{Colors.RESET}")
        self.update_at(row + 3, col2, f"{Colors.BLUE}║{Colors.RESET} {Colors.WHITE}Frequency:{Colors.RESET}")
        self.update_at(row + 4, col2, f"{Colors.BLUE}║{Colors.RESET} {Colors.WHITE}Max Frequency:{Colors.RESET}")
        self.update_at(row + 5, col2, f"{Colors.BLUE}║{Colors.RESET} {Colors.WHITE}Ctx Switches:{Colors.RESET}")
        self.update_at(row + 6, col2, f"{Colors.BLUE}║{Colors.RESET} {Colors.WHITE}Interrupts:{Colors.RESET}")
        self.update_at(row + 7, col2, f"{Colors.BLUE}║{Colors.RESET} {Colors.WHITE}Temperature:{Colors.RESET}")
        self.update_at(row + 8, col2, f"{Colors.BLUE}╚═══════════════════════════════════════════════╝{Colors.RESET}")
        
        start_row = 18
        col = 2
        
        self.update_at(start_row, col, f"{Colors.MAGENTA}╔═══ CPU CORES ═════════════════════════════════╗{Colors.RESET}")
        
        cpu_count = psutil.cpu_count()
        for i in range(min(cpu_count, 16)):
            self.update_at(start_row + 1 + i, col, f"{Colors.MAGENTA}║{Colors.RESET} {Colors.WHITE}Core {i:2d}:{Colors.RESET}")
        
        self.update_at(start_row + 1 + min(cpu_count, 16), col, f"{Colors.MAGENTA}╚═══════════════════════════════════════════════╝{Colors.RESET}")
        
        col = self.terminal_width - 52
        row = 18
        
        self.update_at(row, col, f"{Colors.GREEN}╔═══ MEMORY & SWAP ═════════════════════════════╗{Colors.RESET}")
        self.update_at(row + 1, col, f"{Colors.GREEN}║{Colors.RESET} {Colors.WHITE}RAM Total:{Colors.RESET}")
        self.update_at(row + 2, col, f"{Colors.GREEN}║{Colors.RESET} {Colors.WHITE}RAM Used:{Colors.RESET}")
        self.update_at(row + 3, col, f"{Colors.GREEN}║{Colors.RESET} {Colors.WHITE}RAM Free:{Colors.RESET}")
        self.update_at(row + 4, col, f"{Colors.GREEN}║{Colors.RESET} {Colors.WHITE}Available:{Colors.RESET}")
        self.update_at(row + 5, col, f"{Colors.GREEN}║{Colors.RESET} {Colors.WHITE}Cached:{Colors.RESET}")
        self.update_at(row + 6, col, f"{Colors.GREEN}║{Colors.RESET} {Colors.WHITE}Buffers:{Colors.RESET}")
        self.update_at(row + 7, col, f"{Colors.GREEN}║{Colors.RESET}")
        self.update_at(row + 8, col, f"{Colors.GREEN}║{Colors.RESET} {Colors.WHITE}SWAP Total:{Colors.RESET}")
        self.update_at(row + 9, col, f"{Colors.GREEN}║{Colors.RESET} {Colors.WHITE}SWAP Used:{Colors.RESET}")
        self.update_at(row + 10, col, f"{Colors.GREEN}╚═══════════════════════════════════════════════╝{Colors.RESET}")
        
        row = self.terminal_height - 18
        col = 2
        
        self.update_at(row, col, f"{Colors.YELLOW}╔═══ NETWORK I/O ═══════════════════════════════╗{Colors.RESET}")
        self.update_at(row + 1, col, f"{Colors.YELLOW}║{Colors.RESET} {Colors.WHITE}↑ Upload:{Colors.RESET}")
        self.update_at(row + 2, col, f"{Colors.YELLOW}║{Colors.RESET} {Colors.WHITE}↓ Download:{Colors.RESET}")
        self.update_at(row + 3, col, f"{Colors.YELLOW}║{Colors.RESET} {Colors.WHITE}Total Sent:{Colors.RESET}")
        self.update_at(row + 4, col, f"{Colors.YELLOW}║{Colors.RESET} {Colors.WHITE}Total Recv:{Colors.RESET}")
        self.update_at(row + 5, col, f"{Colors.YELLOW}║{Colors.RESET} {Colors.WHITE}Packets Sent:{Colors.RESET}")
        self.update_at(row + 6, col, f"{Colors.YELLOW}║{Colors.RESET} {Colors.WHITE}Packets Recv:{Colors.RESET}")
        self.update_at(row + 7, col, f"{Colors.YELLOW}║{Colors.RESET} {Colors.WHITE}Errors:{Colors.RESET}")
        self.update_at(row + 8, col, f"{Colors.YELLOW}╚═══════════════════════════════════════════════╝{Colors.RESET}")
        
        row = self.terminal_height - 18
        col = self.terminal_width - 52
        
        self.update_at(row, col, f"{Colors.RED}╔═══ DISK I/O ══════════════════════════════════╗{Colors.RESET}")
        self.update_at(row + 1, col, f"{Colors.RED}║{Colors.RESET} {Colors.WHITE}📖 Read Speed:{Colors.RESET}")
        self.update_at(row + 2, col, f"{Colors.RED}║{Colors.RESET} {Colors.WHITE}📝 Write Speed:{Colors.RESET}")
        self.update_at(row + 3, col, f"{Colors.RED}║{Colors.RESET} {Colors.WHITE}Total Read:{Colors.RESET}")
        self.update_at(row + 4, col, f"{Colors.RED}║{Colors.RESET} {Colors.WHITE}Total Write:{Colors.RESET}")
        self.update_at(row + 5, col, f"{Colors.RED}║{Colors.RESET} {Colors.WHITE}Read Ops:{Colors.RESET}")
        self.update_at(row + 6, col, f"{Colors.RED}║{Colors.RESET} {Colors.WHITE}Write Ops:{Colors.RESET}")
        self.update_at(row + 7, col, f"{Colors.RED}╚═══════════════════════════════════════════════╝{Colors.RESET}")
        
        center_col = (self.terminal_width - 100) // 2
        row = self.terminal_height - 9
        
        self.update_at(row, center_col, f"{Colors.CYAN}{Colors.BOLD}╔═══ TOP PROCESSES ═══════════════════════════════════════════════════════════════════════╗{Colors.RESET}")
        header = f"║ {Colors.BOLD}{'PID':<8} {'NAME':<32} {'CPU%':<8} {'MEM%':<8} {'THREADS':<9} {'STATUS':<10}{Colors.RESET} ║"
        self.update_at(row + 1, center_col, header)
        self.update_at(row + 7, center_col, f"{Colors.CYAN}╚═════════════════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")

    def update_dynamic_data(self):
        col1 = 2
        row = 9
        
        uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        uptime_str = str(uptime).split('.')[0]
        
        self.clear_at(row + 1, col1 + 15, 35)
        self.update_at(row + 1, col1 + 15, f"{Colors.GREEN}{platform.system()} {platform.release()}{Colors.RESET}")
        
        self.clear_at(row + 2, col1 + 15, 35)
        self.update_at(row + 2, col1 + 15, f"{Colors.GREEN}{uptime_str}{Colors.RESET}")
        
        cpu_percent = psutil.cpu_percent(interval=0.1)
        self.clear_at(row + 3, col1 + 15, 35)
        self.update_at(row + 3, col1 + 15, self.draw_bar(cpu_percent, 20))
        
        mem = psutil.virtual_memory()
        self.clear_at(row + 4, col1 + 15, 35)
        self.update_at(row + 4, col1 + 15, self.draw_bar(mem.percent, 20))
        
        try:
            battery = psutil.sensors_battery()
            if battery:
                bat_status = "⚡" if battery.power_plugged else "🔋"
                self.clear_at(row + 5, col1 + 15, 35)
                self.update_at(row + 5, col1 + 15, f"{bat_status} {self.draw_bar(battery.percent, 18)}")
        except:
            pass
        
        col2 = self.terminal_width - 52
        row = 9
        
        cpu_count_physical = psutil.cpu_count(logical=False)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        cpu_stats = psutil.cpu_stats()
        
        self.clear_at(row + 1, col2 + 25, 25)
        self.update_at(row + 1, col2 + 25, f"{Colors.GREEN}{cpu_count_physical}{Colors.RESET}")
        
        self.clear_at(row + 2, col2 + 25, 25)
        self.update_at(row + 2, col2 + 25, f"{Colors.GREEN}{cpu_count_logical}{Colors.RESET}")
        
        self.clear_at(row + 3, col2 + 25, 25)
        self.update_at(row + 3, col2 + 25, f"{Colors.GREEN}{cpu_freq.current:.0f} MHz{Colors.RESET}")
        
        self.clear_at(row + 4, col2 + 25, 25)
        self.update_at(row + 4, col2 + 25, f"{Colors.GREEN}{cpu_freq.max:.0f} MHz{Colors.RESET}")
        
        self.clear_at(row + 5, col2 + 25, 25)
        self.update_at(row + 5, col2 + 25, f"{Colors.YELLOW}{cpu_stats.ctx_switches:,}{Colors.RESET}")
        
        self.clear_at(row + 6, col2 + 25, 25)
        self.update_at(row + 6, col2 + 25, f"{Colors.YELLOW}{cpu_stats.interrupts:,}{Colors.RESET}")
        
        temp = self.get_cpu_temp()
        if temp:
            temp_color = Colors.GREEN if temp < 60 else (Colors.YELLOW if temp < 80 else Colors.RED)
            self.clear_at(row + 7, col2 + 25, 25)
            self.update_at(row + 7, col2 + 25, f"{temp_color}{temp:.1f}°C{Colors.RESET}")
        else:
            self.clear_at(row + 7, col2 + 25, 25)
            self.update_at(row + 7, col2 + 25, f"{Colors.YELLOW}N/A{Colors.RESET}")
        
        start_row = 18
        col = 2
        
        cpu_percents = psutil.cpu_percent(interval=0, percpu=True)
        for i, percent in enumerate(cpu_percents[:16]):
            self.clear_at(start_row + 1 + i, col + 15, 35)
            self.update_at(start_row + 1 + i, col + 15, self.draw_bar(percent, 20))
        
        col = self.terminal_width - 52
        row = 18
        
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        self.clear_at(row + 1, col + 20, 30)
        self.update_at(row + 1, col + 20, f"{Colors.CYAN}{mem.total / (1024**3):.2f} GB{Colors.RESET}")
        
        self.clear_at(row + 2, col + 20, 30)
        self.update_at(row + 2, col + 20, f"{Colors.YELLOW}{mem.used / (1024**3):.2f} GB{Colors.RESET}")
        
        self.clear_at(row + 3, col + 20, 30)
        self.update_at(row + 3, col + 20, f"{Colors.GREEN}{mem.free / (1024**3):.2f} GB{Colors.RESET}")
        
        self.clear_at(row + 4, col + 20, 30)
        self.update_at(row + 4, col + 20, f"{Colors.GREEN}{mem.available / (1024**3):.2f} GB{Colors.RESET}")
        
        cached = mem.cached / (1024**3) if hasattr(mem, 'cached') else 0
        buffers = mem.buffers / (1024**3) if hasattr(mem, 'buffers') else 0
        
        self.clear_at(row + 5, col + 20, 30)
        self.update_at(row + 5, col + 20, f"{Colors.BLUE}{cached:.2f} GB{Colors.RESET}")
        
        self.clear_at(row + 6, col + 20, 30)
        self.update_at(row + 6, col + 20, f"{Colors.BLUE}{buffers:.2f} GB{Colors.RESET}")
        
        self.clear_at(row + 8, col + 20, 30)
        self.update_at(row + 8, col + 20, f"{Colors.CYAN}{swap.total / (1024**3):.2f} GB{Colors.RESET}")
        
        self.clear_at(row + 9, col + 20, 30)
        self.update_at(row + 9, col + 20, f"{Colors.YELLOW}{swap.used / (1024**3):.2f} GB{Colors.RESET}")
        
        row = self.terminal_height - 18
        col = 2
        
        current_net_io = psutil.net_io_counters()
        current_time = time.time()
        time_delta = current_time - self.last_time
        
        if time_delta > 0:
            upload_speed = (current_net_io.bytes_sent - self.last_net_io.bytes_sent) / time_delta / 1024
            download_speed = (current_net_io.bytes_recv - self.last_net_io.bytes_recv) / time_delta / 1024
        else:
            upload_speed = 0
            download_speed = 0
        
        self.last_net_io = current_net_io
        self.last_time = current_time
        
        self.clear_at(row + 1, col + 20, 30)
        self.update_at(row + 1, col + 20, f"{Colors.GREEN}{upload_speed:.2f} KB/s{Colors.RESET}")
        
        self.clear_at(row + 2, col + 20, 30)
        self.update_at(row + 2, col + 20, f"{Colors.GREEN}{download_speed:.2f} KB/s{Colors.RESET}")
        
        self.clear_at(row + 3, col + 20, 30)
        self.update_at(row + 3, col + 20, f"{Colors.CYAN}{current_net_io.bytes_sent / (1024**3):.2f} GB{Colors.RESET}")
        
        self.clear_at(row + 4, col + 20, 30)
        self.update_at(row + 4, col + 20, f"{Colors.CYAN}{current_net_io.bytes_recv / (1024**3):.2f} GB{Colors.RESET}")
        
        self.clear_at(row + 5, col + 20, 30)
        self.update_at(row + 5, col + 20, f"{Colors.MAGENTA}{current_net_io.packets_sent:,}{Colors.RESET}")
        
        self.clear_at(row + 6, col + 20, 30)
        self.update_at(row + 6, col + 20, f"{Colors.MAGENTA}{current_net_io.packets_recv:,}{Colors.RESET}")
        
        self.clear_at(row + 7, col + 20, 30)
        self.update_at(row + 7, col + 20, f"{Colors.RED}In:{current_net_io.errin} Out:{current_net_io.errout}{Colors.RESET}")
        
        row = self.terminal_height - 18
        col = self.terminal_width - 52
        
        try:
            current_disk_io = psutil.disk_io_counters()
            
            if time_delta > 0 and self.last_disk_io:
                read_speed = (current_disk_io.read_bytes - self.last_disk_io.read_bytes) / time_delta / (1024**2)
                write_speed = (current_disk_io.write_bytes - self.last_disk_io.write_bytes) / time_delta / (1024**2)
            else:
                read_speed = 0
                write_speed = 0
            
            self.last_disk_io = current_disk_io
            
            self.clear_at(row + 1, col + 25, 25)
            self.update_at(row + 1, col + 25, f"{Colors.GREEN}{read_speed:.2f} MB/s{Colors.RESET}")
            
            self.clear_at(row + 2, col + 25, 25)
            self.update_at(row + 2, col + 25, f"{Colors.GREEN}{write_speed:.2f} MB/s{Colors.RESET}")
            
            self.clear_at(row + 3, col + 25, 25)
            self.update_at(row + 3, col + 25, f"{Colors.CYAN}{current_disk_io.read_bytes / (1024**3):.2f} GB{Colors.RESET}")
            
            self.clear_at(row + 4, col + 25, 25)
            self.update_at(row + 4, col + 25, f"{Colors.CYAN}{current_disk_io.write_bytes / (1024**3):.2f} GB{Colors.RESET}")
            
            self.clear_at(row + 5, col + 25, 25)
            self.update_at(row + 5, col + 25, f"{Colors.MAGENTA}{current_disk_io.read_count:,}{Colors.RESET}")
            
            self.clear_at(row + 6, col + 25, 25)
            self.update_at(row + 6, col + 25, f"{Colors.MAGENTA}{current_disk_io.write_count:,}{Colors.RESET}")
        except:
            pass
        
        center_col = (self.terminal_width - 100) // 2
        row = self.terminal_height - 9
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'num_threads', 'status']):
            try:
                info = proc.info
                if info['name'] and 'System Idle Process' not in info['name']:
                    processes.append(info)
            except:
                pass
        
        processes = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)
        
        for i in range(5):
            if i < len(processes):
                proc = processes[i]
                pid = str(proc['pid'])[:7]
                name = (proc['name'] or "N/A")[:31]
                cpu = proc['cpu_percent'] or 0
                mem = proc['memory_percent'] or 0
                threads = proc['num_threads'] or 0
                status = (proc['status'] or "N/A")[:9]
                
                if cpu > 50:
                    color = Colors.RED
                elif cpu > 25:
                    color = Colors.YELLOW
                else:
                    color = Colors.GREEN
                
                line = f"║ {color}{pid:<8} {name:<32} {cpu:>6.1f}%  {mem:>6.2f}%  {threads:>8}  {status:<10}{Colors.RESET} ║"
            else:
                line = f"║{' ' * 88}║"
            
            self.clear_at(row + 2 + i, center_col, 100)
            self.update_at(row + 2 + i, center_col, line)
        
        footer = f"{Colors.YELLOW}[Ctrl+C]{Colors.RESET} Exit  •  {Colors.CYAN}Refresh: 1s{Colors.RESET}  •  {Colors.GREEN}{datetime.now().strftime('%H:%M:%S')}{Colors.RESET}"
        footer_col = (self.terminal_width - 50) // 2
        self.clear_at(self.terminal_height, footer_col, 50)
        self.update_at(self.terminal_height, footer_col, footer)

    def run(self):
        self.clear_screen_once()
        print(f"{Colors.GREEN}Initializing Galaxy Manager...{Colors.RESET}")
        time.sleep(1)
        self.clear_screen_once()
        
        self.draw_static_layout()
        
        while self.running:
            try:
                self.update_dynamic_data()
                time.sleep(1)
                
            except KeyboardInterrupt:
                self.running = False
                print(f"\n\n{Colors.SHOW_CURSOR}{Colors.CYAN}Galaxy Manager terminated.{Colors.RESET}\n")
                break
            except Exception as e:
                print(f"\n{Colors.SHOW_CURSOR}{Colors.RED}Error: {e}{Colors.RESET}")
                time.sleep(2)

def setup_console():
    if platform.system() == 'Windows':
        os.system('chcp 65001 > nul')
        os.system('mode con: cols=120 lines=40')
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleTitleW("Galaxy Manager - System Monitor")

def main():
    setup_console()
    
    try:
        app = GalaxyManager()
        app.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.SHOW_CURSOR}{Colors.CYAN}Goodbye!{Colors.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.SHOW_CURSOR}{Colors.RED}Critical Error: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()