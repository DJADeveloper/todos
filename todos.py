import tkinter as tk
from tkinter import simpledialog, messagebox, Listbox, END
import speech_recognition as sr

filename = 'tasks.txt'

def read_tasks():
    tasks = []
    try:
        with open(filename, 'r') as file:
            tasks = file.readlines()
        tasks = [task.strip() for task in tasks]
    except FileNotFoundError:
        open(filename, 'a').close()  # Creates the file if it does not exist
    return tasks

def write_tasks(tasks):
    with open(filename, 'w') as file:
        for task in tasks:
            file.write(f"{task}\n")

def refresh_task_list():
    tasks = read_tasks()
    listbox.delete(0, END)
    for task in tasks:
        listbox.insert(END, task)

def add_task_by_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Info", "Please speak now. Waiting for task...")
        audio = r.listen(source)
        try:
            task = r.recognize_google(audio)
            tasks = read_tasks()
            tasks.append(task)
            write_tasks(tasks)
            refresh_task_list()
            messagebox.showinfo("Info", f"Task added: {task}")
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Could not request results from Google Speech Recognition service; {e}")

def main():
    global listbox
    root = tk.Tk()
    root.title("To-Do List App")

    frame = tk.Frame(root)
    frame.pack(pady=10, padx=10)

    listbox = Listbox(frame, width=50, height=15)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    add_button = tk.Button(root, text="Add Task", command=lambda: add_task_by_voice())
    add_button.pack(fill=tk.X, expand=True)

    refresh_task_list()

    root.mainloop()

if __name__ == '__main__':
    main()