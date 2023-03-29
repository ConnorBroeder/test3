import subprocess
import tkinter as tk

class WifiScanner:
    def __init__(self, master):
        self.master = master
        self.master.title("Wi-Fi Scanner")
        self.networks = []
        self.password_required = False
        self.selected_network = tk.StringVar()
        self.password = tk.StringVar()

        # Create the UI elements
        self.network_label = tk.Label(self.master, text="Select a network to connect to:")
        self.network_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.network_listbox = tk.Listbox(self.master, width=50, height=10)
        self.network_listbox.grid(row=1, column=0, padx=10, pady=10)

        self.password_label = tk.Label(self.master, text="Password:")
        self.password_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        self.password_entry = tk.Entry(self.master, show="*", textvariable=self.password, width=50)
        self.password_entry.grid(row=3, column=0, padx=10, pady=10)

        self.connect_button = tk.Button(self.master, text="Connect", command=self.connect_to_network)
        self.connect_button.grid(row=4, column=0, padx=10, pady=10)

        # Populate the listbox with available networks
        self.update_networks()

    def update_networks(self):
        try:
            # Run the command to get the available networks
            output = subprocess.run(["netsh", "wlan", "show", "networks"], capture_output=True, text=True, encoding="latin-1")

            # Parse the output and add each network to the list
            self.networks = []
            for line in output.stdout.split("\n"):
                if "SSID" not in line:
                    continue
                ssid = line.split(":")[1].strip()
                self.networks.append(ssid)

            # Update the listbox with the available networks
            self.network_listbox.delete(0, tk.END)
            for network in self.networks:
                self.network_listbox.insert(tk.END, network)

        except Exception as e:
            print(f"Error: {e}")
            self.network_label.config(text="Error: Could not get available networks")

    def connect_to_network(self):
        # Get the selected network and password
        self.selected_network = self.network_listbox.get(tk.ACTIVE)
        self.password = self.password_entry.get()

        # Check if the selected network requires a password
        self.password_required = "security key" in subprocess.run(["netsh", "wlan", "show", "networks", "mode=ssid", "name=" + self.selected_network], capture_output=True, text=True, encoding="latin-1").stdout

        # Show an error message if no network is selected
        if not self.selected_network:
            self.network_label.config(text="Error: Please select a network to connect to")
            return

        # Attempt to connect to the selected network
        try:
            if self.password_required:
                output = subprocess.run(["netsh", "wlan", "connect", "name=" + self.selected_network, "keyMaterial=" + self.password], capture_output=True, text=True, encoding="latin-1")
            else:
                output = subprocess.run(["netsh", "wlan", "connect", "name=" + self.selected_network], capture_output=True, text=True, encoding="latin-1")

            # Check if the connection was successful
            if "successfully" in output.stdout:
                self.network_label.config(text="Successfully connected to " + self.selected_network)
            else:
                self.network_label.config(text="Error: Could not connect to " + self.selected_network)

        except Exception as e:
            print(f"Error: {e}")
            self.network_label.config(text="Error: Could not connect to " + self.selected_network)

def main():
    root = tk.Tk()
    scanner = WifiScanner(root)
    root.mainloop()

if __name__ == "__main__":
    main()