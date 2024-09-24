import os
import psutil
import tkinter as tk
from tkinter import ttk
from threading import Thread, Event
from multiprocessing import Process
import glob

processes = {}
threads = {}
thread_stop_flags = {}

class CommandLineApp:
    def __init__(self, parent):
        self.parent = parent
        self.command_label = ttk.Label(parent, text="Enter command:")
        self.command_label.pack(pady=5)

        self.command_entry = ttk.Entry(parent)
        self.command_entry.pack(pady=5)

        self.execute_button = ttk.Button(parent, text="Execute", command=self.execute_command)
        self.execute_button.pack(pady=5)

        self.output_text = tk.Text(parent, height=10, width=50)
        self.output_text.pack(pady=5)

    def execute_command(self):
        command = self.command_entry.get()
        output = self.run_command(command)
        self.output_text.insert(tk.END, output + "\n")

    def run_command(self, command):
        global processes, threads, thread_stop_flags

        command_parts = command.split()
        cmd = command_parts[0]

        if cmd == "ps":
            return self.ps()
        elif cmd == "kill":
            return self.kill(command_parts)
        elif cmd == "top":
            return self.top()
        elif cmd == "thread-start":
            return self.thread_start(command_parts)
        elif cmd == "thread-stop":
            return self.thread_stop(command_parts)
        elif cmd == "proc-start":
            return self.proc_start(command_parts)
        elif cmd == "proc-stop":
            return self.proc_stop(command_parts)
        elif cmd == "proc-status":
            return self.proc_status(command_parts)
        elif cmd == "proc-priority":
            return self.proc_priority(command_parts)
        elif cmd == "find":
            return self.find(command_parts)
        else:
            return f"Unknown command: {cmd}"

    def ps(self):
        return "\n".join([f"PID: {p.pid}, Name: {p.name()}" for p in psutil.process_iter()])

    def kill(self, args):
        if len(args) < 2:
            return "Usage: kill <pid>"
        pid = int(args[1])
        try:
            psutil.Process(pid).terminate()
            return f"Process {pid} terminated."
        except psutil.NoSuchProcess:
            return f"No such process with PID {pid}."

    def top(self):
        processes = [(p.pid, p.name(), p.cpu_percent(), p.memory_percent()) for p in psutil.process_iter()]
        processes.sort(key=lambda x: x[2], reverse=True)
        output = "PID    Name    CPU%    Mem%\n"
        for p in processes[:10]:
            output += f"{p[0]}    {p[1]}    {p[2]:.1f}    {p[3]:.1f}\n"
        return output

    def thread_start(self, args):
        if len(args) < 2:
            return "Usage: thread-start <name>"
        name = args[1]
        stop_flag = Event()
        thread = Thread(target=self.dummy_thread, args=(name, stop_flag))
        thread.start()
        threads[name] = thread
        thread_stop_flags[name] = stop_flag
        return f"Thread {name} started."

    def thread_stop(self, args):
        if len(args) < 2:
            return "Usage: thread-stop <name>"
        name = args[1]
        if name in threads:
            thread_stop_flags[name].set()
            threads[name].join()
            del threads[name]
            del thread_stop_flags[name]
            return f"Thread {name} stopped."
        return f"No thread with name {name}."

    def dummy_thread(self, name, stop_flag):
        while not stop_flag.is_set():
            print(f"Thread {name} is running...")
            time.sleep(1)

    def proc_start(self, args):
        if len(args) < 2:
            return "Usage: proc-start <name>"
        name = args[1]
        process = Process(target=self.dummy_process, args=(name,))
        process.start()
        processes[process.pid] = process
        return f"Process {name} started with PID {process.pid}."

    def proc_stop(self, args):
        if len(args) < 2:
            return "Usage: proc-stop <pid>"
        pid = int(args[1])
        if pid in processes:
            processes[pid].terminate()
            return f"Process {pid} stopped."
        return f"No process with PID {pid}."

    def dummy_process(self, name):
        while True:
            print(f"Process {name} is running...")
            time.sleep(1)

    def proc_status(self, args):
        if len(args) < 2:
            return "Usage: proc-status <pid>"
        pid = int(args[1])
        if pid in processes:
            return f"Process {pid} is running."
        return f"No process with PID {pid}."

    def proc_priority(self, args):
        if len(args) < 3:
            return "Usage: proc-priority <pid> <priority>"
        pid = int(args[1])
        priority = int(args[2])
        if pid in processes:
            os.nice(priority)
            return f"Priority of process {pid} set to {priority}."
        return f"No process with PID {pid}."

    def find(self, args):
        if len(args) < 2:
            return "Usage: find <file_name>"
        file_name = args[1]
        files = glob.glob(f"**/{file_name}", recursive=True)
        return "\n".join(files) if files else f"No files found with name {file_name}."
