import ipaddress
import random
import tkinter as tk

def calculate_prefix_for_hosts(hosts):
    """Calculate the smallest prefix that can accommodate the given number of hosts."""
    for prefix in range(32, 0, -1):
        if (2 ** (32 - prefix)) - 2 >= hosts:
            return prefix
    return None

def generate_base_network():
    """Generate a random base network with a CIDR between /8 and /24."""
    base_ip = ipaddress.IPv4Address(random.randint(0x0A000000, 0xDF000000))  # Random IP
    prefix = random.randint(8, 24)
    return ipaddress.IPv4Network(f"{base_ip}/{prefix}", strict=False)

def align_to_subnet_boundary(ip, prefix):
    """Align the given IP to the correct subnet boundary."""
    subnet_size = 2 ** (32 - prefix)
    aligned_ip_int = int(ip) + (subnet_size - (int(ip) % subnet_size)) % subnet_size
    return ipaddress.IPv4Address(aligned_ip_int)

def generate_subnet_plan(base_network, num_subnets=5):
    """Generate a list of subnets with random host requirements, ensuring no overlaps."""
    subnets = []
    current_ip = base_network.network_address
    for _ in range(num_subnets):
        required_hosts = random.randint(10, 500)
        prefix = calculate_prefix_for_hosts(required_hosts)
        if prefix is None:
            continue
        aligned_ip = align_to_subnet_boundary(current_ip, prefix)
        try:
            subnet = ipaddress.IPv4Network(f"{aligned_ip}/{prefix}", strict=True)
            if subnet.network_address < base_network.network_address or subnet.broadcast_address > base_network.broadcast_address:
                break
            subnets.append((subnet, required_hosts))
            current_ip = subnet.broadcast_address + 1
        except ValueError:
            break
    return subnets

def check_answers():
    for i, (subnet, _) in enumerate(current_subnets):
        user_input = entries[i].get().strip()
        correct = str(subnet)
        if user_input == correct:
            entries[i].config(bg='lightgreen')
        else:
            entries[i].config(bg='lightcoral')

def show_correct_answers():
    for i, (subnet, _) in enumerate(current_subnets):
        correct_entries[i].config(state='normal')
        correct_entries[i].delete(0, tk.END)
        correct_entries[i].insert(0, str(subnet))
        correct_entries[i].config(state='readonly')

def regenerate_problem():
    global current_subnets, entries, correct_entries, base_network
    for widget in frame.winfo_children():
        widget.destroy()
    entries = []
    correct_entries = []
    base_network = generate_base_network()
    base_label.config(text=f"Base Network: {base_network}")
    current_subnets = generate_subnet_plan(base_network)
    for i, (subnet, hosts) in enumerate(current_subnets):
        tk.Label(frame, text=f"Subnet {i+1} - Required Hosts: {hosts}").grid(row=i, column=0, padx=5, pady=5, sticky='w')
        entry = tk.Entry(frame, width=25)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)
        correct_entry = tk.Entry(frame, width=25, state='readonly')
        correct_entry.grid(row=i, column=2, padx=5, pady=5)
        correct_entries.append(correct_entry)

# GUI setup
root = tk.Tk()
root.title("Subnetting Practice Tool")

base_network = generate_base_network()
base_label = tk.Label(root, text=f"Base Network: {base_network}")
base_label.pack(pady=10)

frame = tk.Frame(root)
frame.pack()

entries = []
correct_entries = []
current_subnets = []

regenerate_problem()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Check Answers", command=check_answers).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Show Correct Answers", command=show_correct_answers).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="New Problem", command=regenerate_problem).grid(row=0, column=2, padx=5)

root.mainloop()
