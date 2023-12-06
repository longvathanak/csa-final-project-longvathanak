import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3 as sql

def add_task():
    task_string = task_field.get()
    due_date_string = due_date_field.get()
    priority_string = priority_var.get()

    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Task field is empty.')
    else:
        tasks.append((task_string, due_date_string, priority_string))
        the_cursor.execute('insert into tasks (title, due_date, priority) values (?, ?, ?)',
                           (task_string, due_date_string, priority_string))
        list_update()
        clear_fields()

def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', f"{task[0]} - Due: {task[1]}, Priority: {task[2]}")

def delete_task():
    try:
        selected_index = task_listbox.curselection()[0]
        the_value = task_listbox.get(selected_index)
        task_string = the_value.split(" - ")[0]

        for task in tasks:
            if task[0] == task_string:
                tasks.remove(task)
                the_cursor.execute('delete from tasks where title = ?', (task_string,))
                the_connection.commit()
                list_update()
                break
    except IndexError:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')




def delete_all_tasks():
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')
    if message_box:
        tasks.clear()
        the_cursor.execute('delete from tasks')
        list_update()

def clear_list():
    task_listbox.delete(0, 'end')

def clear_fields():
    task_field.delete(0, 'end')
    due_date_field.delete(0, 'end')
    priority_combobox.set('Low')

def edit_task():
    try:
        selected_index = task_listbox.curselection()[0]
        task_to_edit = tasks[selected_index]
        task_field.delete(0, 'end')
        due_date_field.delete(0, 'end')
        priority_combobox.set('Low')

        task_field.insert(0, task_to_edit[0])
        due_date_field.insert(0, task_to_edit[1])
        priority_combobox.set(task_to_edit[2])
    except IndexError:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Edit.')

def update_task():
    try:
        selected_index = task_listbox.curselection()[0]
        the_value = tasks[selected_index][0]

        new_task_string = task_field.get()
        new_due_date_string = due_date_field.get()
        new_priority_string = priority_var.get()

        tasks[selected_index] = (new_task_string, new_due_date_string, new_priority_string)
        the_cursor.execute('update tasks set title=?, due_date=?, priority=? where title=?',
                           (new_task_string, new_due_date_string, new_priority_string, the_value))
        list_update()
        clear_fields()
    except IndexError:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Update.')

def close():
    guiWindow.destroy()

def retrieve_database():
    tasks.clear()
    the_cursor.execute('PRAGMA table_info(tasks)')
    columns = [column[1] for column in the_cursor.fetchall()]
    if 'due_date' not in columns:
        the_cursor.execute('ALTER TABLE tasks ADD COLUMN due_date TEXT')
    if 'priority' not in columns:
        the_cursor.execute('ALTER TABLE tasks ADD COLUMN priority TEXT')
    for row in the_cursor.execute('SELECT title, due_date, priority FROM tasks'):
        tasks.append(row)
    list_update()

if __name__ == "__main__":
    guiWindow = tk.Tk()
    guiWindow.title("To-Do List Manager - JAVATPOINT")
    guiWindow.geometry("1000x400+500+200")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#FAEBD7")

    the_connection = sql.connect('listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('create table if not exists tasks (title text, due_date text, priority text)')

    tasks = []

    header_frame = tk.Frame(guiWindow, bg="#FAEBD7")
    functions_frame = tk.Frame(guiWindow, bg="#FAEBD7")
    listbox_frame = tk.Frame(guiWindow, bg="#FAEBD7")

    header_frame.pack(fill="both")
    functions_frame.pack(side="left", expand=True, fill="both")
    listbox_frame.pack(side="right", expand=True, fill="both")

    header_label = ttk.Label(
        header_frame,
        text="The To-Do List",
        font=("Brush Script MT", "30"),
        background="#FAEBD7",
        foreground="#8B4513"
    )
    header_label.pack(padx=20, pady=20)

    task_label = ttk.Label(
        functions_frame,
        text="Enter the Task:",
        font=("Consolas", "11", "bold"),
        background="#FAEBD7",
        foreground="#FFFFFF"
    )
    task_label.grid(row=0, column=0, padx=30, pady=10)

    task_field = ttk.Entry(
        functions_frame,
        font=("Consolas", "12"),
        width=18,
        background="#FFF8DC",
        foreground="#f5bfbf"
    )
    task_field.grid(row=0, column=1, pady=10)

    due_date_label = ttk.Label(
        functions_frame,
        text="Due Date:",
        font=("Consolas", "11", "bold"),
        background="#FAEBD7",
        foreground="#FFFFFF"
    )
    due_date_label.grid(row=1, column=0, padx=30, pady=10)

    due_date_field = ttk.Entry(
        functions_frame,
        font=("Consolas", "12"),
        width=18,
        background="#FFF8DC",
        foreground="#f5bfbf"
    )
    due_date_field.grid(row=1, column=1, pady=10)

    priority_label = ttk.Label(
        functions_frame,
        text="Priority:",
        font=("Consolas", "11", "bold"),
        background="#FAEBD7",
        foreground="#FFFFFF"
    )
    priority_label.grid(row=2, column=0, padx=30, pady=10)

    priority_var = tk.StringVar()
    priority_combobox = ttk.Combobox(
        functions_frame,
        textvariable=priority_var,
        values=['Low', 'Medium', 'High'],
        font=("Consolas", "12"),
        width=16,
        state="readonly"
    )
    priority_combobox.grid(row=2, column=1, pady=10)
    priority_combobox.set('Low')

    add_button = ttk.Button(
        functions_frame,
        text="Add Task",
        width=24,
        command=add_task
    )
    del_button = ttk.Button(
        functions_frame,
        text="Delete Task",
        width=24,
        command=delete_task
    )
    edit_button = ttk.Button(
        functions_frame,
        text="Edit Task",
        width=24,
        command=edit_task
    )
    update_button = ttk.Button(
        functions_frame,
        text="Update Task",
        width=24,
        command=update_task
    )
    del_all_button = ttk.Button(
        functions_frame,
        text="Delete All Tasks",
        width=24,
        command=delete_all_tasks
    )
    exit_button = ttk.Button(
        functions_frame,
        text="Exit",
        width=24,
        command=close
    )
    add_button.grid(row=3, column=0, pady=10)
    del_button.grid(row=3, column=1, pady=10)
    edit_button.grid(row=4, column=0, pady=10)
    update_button.grid(row=4, column=1, pady=10)
    del_all_button.grid(row=5, column=0, pady=10)
    exit_button.grid(row=5, column=1, pady=10)

    task_listbox = tk.Listbox(
        listbox_frame,
        width=45,
        height=15,
        selectmode='SINGLE',
        background="#FFFFFF",
        foreground="#000000",
        selectbackground="#CD853F",
        selectforeground="#FFFFFF"
    )
    task_listbox.grid(row=0, column=0, padx=10, pady=10, rowspan=5)

    retrieve_database()
    guiWindow.mainloop()
    the_connection.commit()
    the_cursor.close()
