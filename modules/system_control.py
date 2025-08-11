
import os
import subprocess
import platform
import psutil
import datetime
import json

class SystemController:
    def __init__(self):
        self.system = platform.system()
        self.system_info = self.get_system_info()
    
    def get_system_info(self):
        """Get basic system information"""
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": psutil.cpu_count(),
            "memory": psutil.virtual_memory().total // (1024**3)  # GB
        }
    
    def execute_command(self, command):
        """Execute system commands based on user input"""
        command_lower = command.lower()
        
        if "open calculator" in command_lower or "launch calculator" in command_lower:
            return self.open_calculator()
        elif "open notepad" in command_lower or "launch notepad" in command_lower:
            return self.open_notepad()
        elif "open browser" in command_lower:
            return self.open_browser()
        elif "system info" in command_lower or "system status" in command_lower:
            return self.get_system_status()
        else:
            return f"Command '{command}' not recognized or not implemented in demo mode"
    
    def open_calculator(self):
        """Open system calculator"""
        try:
            if self.system == "Windows":
                subprocess.Popen("calc.exe")
                return "Calculator opened successfully"
            elif self.system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", "Calculator"])
                return "Calculator opened successfully"
            elif self.system == "Linux":
                subprocess.Popen(["gnome-calculator"])
                return "Calculator opened successfully"
            else:
                return "Calculator not available for this system"
        except Exception as e:
            return f"Could not open calculator: {str(e)}"
    
    def open_notepad(self):
        """Open system text editor"""
        try:
            if self.system == "Windows":
                subprocess.Popen("notepad.exe")
                return "Notepad opened successfully"
            elif self.system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", "TextEdit"])
                return "TextEdit opened successfully"
            elif self.system == "Linux":
                subprocess.Popen(["gedit"])
                return "Text editor opened successfully"
            else:
                return "Text editor not available for this system"
        except Exception as e:
            return f"Could not open text editor: {str(e)}"
    
    def open_browser(self):
        """Open default web browser"""
        try:
            if self.system == "Windows":
                subprocess.Popen(["start", "chrome"], shell=True)
                return "Browser opened successfully"
            elif self.system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", "Google Chrome"])
                return "Browser opened successfully"
            elif self.system == "Linux":
                subprocess.Popen(["google-chrome"])
                return "Browser opened successfully"
            else:
                return "Browser not available for this system"
        except Exception as e:
            return f"Could not open browser: {str(e)}"
    
    def get_system_status(self):
        """Get current system status"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            status = f"""System Status Report:
            
🖥️ System: {self.system_info['system']} {self.system_info['release']}
💻 Processor: {self.system_info['processor']}
🧮 CPU Usage: {cpu_percent}%
🧠 Memory: {memory.percent}% used ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)
💾 Disk Usage: {disk.percent}% used ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)
⚡ CPU Cores: {self.system_info['cpu_count']}
🕒 Boot Time: {datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}
            """
            return status
        except Exception as e:
            return f"Could not retrieve system status: {str(e)}"
    
    def get_running_processes(self):
        """Get list of running processes"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                processes.append(proc.info)
            return processes[:10]  # Return top 10 processes
        except Exception as e:
            return f"Could not retrieve process list: {str(e)}"
