
"""
Subnetting Practice Tool
Author: Thomas Kunchick
Email: brag.aces.8k@icloud.com
Date: August 2025
Description: GUI tool for practicing subnetting with adjustable font size.
"""


import ipaddress
import random
import tkinter as tk
from tkinter import ttk

def generate_random_ip_and_cidr():
    ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    cidr = random.randint(8, 30)
    return f"{ip}/{cidr}"

def calculate_subnet_info(ip_cidr):
    network = ipaddress.ip_network(ip_cidr, strict=False)
    first_host = network.network_address + 1
    last_host = network.broadcast_address - 1
    broadcast = network.broadcast_address
    next_subnet = ipaddress.ip_network((int(network.network_address) + network.num_addresses, network.prefixlen))
    return {
        'Network': str(network.network_address),
        'First Host': str(first_host),
        'Last Host': str(last_host),
        'Broadcast': str(broadcast),
        'Next Subnet': str(next_subnet.network_address)
    }

def update_font_size(event=None):
    selected_size = int(font_size_var.get())
    font_settings = ("Helvetica", selected_size)
    ip_label.config(font=font_settings)
    for field in fields:
        labels[field].config(font=font_settings)
        answer_entries[field].config(font=font_settings)
        correct_entries[field].config(font=font_settings)
    for button in buttons:
        button.config(font=font_settings)

def check_answers():
    for key in answer_entries:
        user_input = answer_entries[key].get().strip()
        correct_answer = correct_answers[key]
        if user_input == correct_answer:
            answer_entries[key].config(bg='lightgreen')
        else:
            answer_entries[key].config(bg='lightcoral')

def show_correct_answers():
    for key in correct_entries:
        correct_entries[key].config(state='normal')
        correct_entries[key].delete(0, tk.END)
        correct_entries[key].insert(0, correct_answers[key])
        correct_entries[key].config(state='readonly')

def populate_problem():
    global correct_answers
    ip_cidr = generate_random_ip_and_cidr()
    ip_label.config(text=f"IP/CIDR: {ip_cidr}")
    correct_answers = calculate_subnet_info(ip_cidr)
    for key in answer_entries:
        answer_entries[key].delete(0, tk.END)
        answer_entries[key].config(bg='white')
    for key in correct_entries:
        correct_entries[key].config(state='normal')
        correct_entries[key].delete(0, tk.END)
        correct_entries[key].config(state='readonly')

root = tk.Tk()
root.title("Subnetting Practice Tool")

font_size_var = tk.StringVar(value="14")
font_size_dropdown = ttk.Combobox(root, textvariable=font_size_var, values=[10, 12, 14, 16, 18, 20], state="readonly", width=5)
font_size_dropdown.grid(row=0, column=3, padx=5, pady=5)
font_size_dropdown.bind("<<ComboboxSelected>>", update_font_size)
tk.Label(root, text="Font Size:").grid(row=0, column=2, padx=5, pady=5, sticky='e')

ip_label = tk.Label(root, text="IP/CIDR: ")
ip_label.grid(row=1, column=0, columnspan=3, pady=10)

fields = ['Network', 'First Host', 'Last Host', 'Broadcast', 'Next Subnet']
answer_entries = {}
correct_entries = {}
labels = {}

for i, field in enumerate(fields, start=2):
    label = tk.Label(root, text=field)
    label.grid(row=i, column=0, padx=5, pady=5, sticky='e')
    labels[field] = label

    entry = tk.Entry(root, width=20)
    entry.grid(row=i, column=1, padx=5, pady=5)
    answer_entries[field] = entry

    correct_entry = tk.Entry(root, width=20, state='readonly')
    correct_entry.grid(row=i, column=2, padx=5, pady=5)
    correct_entries[field] = correct_entry

btn_check = tk.Button(root, text="Check Answers", command=check_answers)
btn_check.grid(row=8, column=0, pady=10)

btn_show = tk.Button(root, text="Show Correct Answers", command=show_correct_answers)
btn_show.grid(row=8, column=1, pady=10)

btn_new = tk.Button(root, text="New Problem", command=populate_problem)
btn_new.grid(row=8, column=2, pady=10)

buttons = [btn_check, btn_show, btn_new]

populate_problem()
update_font_size()
root.mainloop()
