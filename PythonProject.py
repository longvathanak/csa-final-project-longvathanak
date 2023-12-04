import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from datetime import datetime
import json

class ToDoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Enhanced To-Do List")

        self.tasks = []

        self.task_entry = tk.Text(self.master, height=5, width=30)
        self.task_entry.pack(pady=10)

        self.priority_var = tk.StringVar(self.master)
        self.priority_var.set("Low")
        priority_options = ["High", "Medium", "Low"]
        priority_menu = tk.OptionMenu(self.master, self.priority_var, *priority_options)
        priority_menu.pack()

        self.due_date_var = tk.StringVar(self.master)
        self.due_date_var.set("No Due Date")
        due_date_label = tk.Label(self.master, text="Due Date:")
        due_date_label.pack()

        # Entry for manual due date input
        due_date_entry = tk.Entry(self.master, textvariable=self.due_date_var)
        due_date_entry.pack()

        add_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        add_button.pack()

        self.task_list = tk.Listbox(self.master, height=10, width=50)
        self.task_list.pack()

        # Buttons for additional features
        details_button = tk.Button(self.master, text="Task Details", command=self.show_task_details)
        details_button.pack()

        delete_button = tk.Button(self.master, text="Delete Task", command=self.delete_task)
        delete_button.pack()

        save_button = tk.Button(self.master, text="Save Tasks", command=self.save_tasks)
        save_button.pack()

        load_button = tk.Button(self.master, text="Load Tasks", command=self.load_tasks)
        load_button.pack()

        self.update_task_list()

    def add_task(self):
        task_text = self.task_entry.get("1.0", "end-1c")
        priority = self.priority_var.get()
        due_date = self.due_date_var.get()

        if task_text:
            task_info = {"Task": task_text, "Priority": priority, "Due Date": due_date, "Completed": False}
            self.tasks.append(task_info)
            self.update_task_list()
            self.clear_entry_fields()
        else:
            messagebox.showwarning("Warning", "Task text cannot be empty.")

    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        for i, task_info in enumerate(self.tasks, start=1):
            task_str = f"{i}. {task_info['Task']} - Priority: {task_info['Priority']} - Due Date: {task_info['Due Date']} - Completed: {task_info['Completed']}"
            self.task_list.insert(tk.END, task_str)

    def delete_task(self):
        selected_task_index = self.task_list.curselection()
        if selected_task_index:
            confirm = messagebox.askokcancel("Confirmation", "Are you sure you want to delete this task?")
            if confirm:
                del self.tasks[selected_task_index[0]]
                self.update_task_list()

    def clear_entry_fields(self):
        self.task_entry.delete("1.0", tk.END)
        self.priority_var.set("Low")
        self.due_date_var.set("No Due Date")

    def show_task_details(self):
        selected_task_index = self.task_list.curselection()
        if selected_task_index:
            task_info = self.tasks[selected_task_index[0]]
            details_window = tk.Toplevel(self.master)
            details_window.title("Task Details")

            details_label = tk.Label(details_window, text=f"Task: {task_info['Task']}\nPriority: {task_info['Priority']}\nDue Date: {task_info['Due Date']}\nCompleted: {task_info['Completed']}")
            details_label.pack()

            mark_completed_button = tk.Button(details_window, text="Mark as Completed", command=lambda: self.mark_task_completed(selected_task_index[0]))
            mark_completed_button.pack()

    def mark_task_completed(self, index):
        self.tasks[index]["Completed"] = not self.tasks[index]["Completed"]
        self.update_task_list()

    def save_tasks(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as file:
                json.dump(self.tasks, file)
            messagebox.showinfo("Save Successful", "Tasks saved successfully.")

    def load_tasks(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    self.tasks = json.load(file)
                self.update_task_list()
                messagebox.showinfo("Load Successful", "Tasks loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading tasks: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
