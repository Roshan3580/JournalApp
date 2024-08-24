# ROSHAN RAJ
# 90439894
# roshar1@uci.edu

# Tkinter.py

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from typing import Dict, List
import json, time
from ds_messenger import DirectMessenger
from ds_client import send
from Profile import Profile


class Body(tk.Frame):
    """Represents the main body of the GUI.

        Attributes:
            root: The root Tkinter frame.
            _contacts: A list of contact usernames.
            _select_callback: Callback function for when a recipient is selected.
        """
    def __init__(self, root, recipient_selected_callback=None):
        """Initialize the Body instance.

                Args:
                    root: The root Tkinter frame.
                    recipient_selected_callback: Callback function for recipient selection.
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event):
        """Callback function for when a node is selected in the Treeview."""
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        """Inserts a new contact into the contact list.

                Args:
                    contact: The username of the contact.
                """
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        """Inserts a contact into the Treeview widget.

                Args:
                    id: The ID of the contact.
                    contact: The username of the contact.
                """
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message: str):
        """Inserts a message sent by the user into the text editor.

                Args:
                    message: The message to be inserted.
                """
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        """Inserts a message received from a contact into the text editor.

                Args:
                    message: The message to be inserted.
                """
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        """Gets the text entry from the message editor.

                Returns:
                    The text entry.
                """
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        """Sets the text entry in the message editor.

                Args:
                    text: The text to be set.
                """
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        """Draws the body components."""
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """Represents the footer of the GUI.

        Attributes:
            root: The root Tkinter frame.
            _send_callback: Callback function for sending messages.
            _refresh_callback: Callback function for refreshing feed.
        """
    def __init__(self, root, send_callback=None, refresh_callback=None):
        """Initialize the Footer instance.

                Args:
                    root: The root Tkinter frame.
                    send_callback: Callback function for sending messages.
                    refresh_callback: Callback function for refreshing feed.
                """
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._refresh_callback = refresh_callback
        self._draw()

    def send_click(self):
        """Callback function for the send button click."""
        if self._send_callback is not None:
            self._send_callback()

    def refresh_click(self):
        """Callback function for the refresh button click."""
        if self._refresh_callback is not None:
            self._refresh_callback()


    def _draw(self):
        """Draws the footer components."""
        save_button = tk.Button(master=self, text="Send", width=20, command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        refresh_button = tk.Button(master=self, text="Refresh", width=20, command=self.refresh_click)
        refresh_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)




class NewContactDialog(tk.simpledialog.Dialog):
    """Represents a dialog window for adding new contacts."""
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        """Initialize the NewContactDialog instance."""
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        """Creates the body of the dialog window."""
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, str(self.server) if self.server is not None else "")
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, str(self.user) if self.user is not None else "")
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30, show='*')
        self.password_entry.insert(tk.END, str(self.pwd) if self.user is not None else "")
        self.password_entry.pack()


    def apply(self):
        """Applies the changes made in the dialog window."""
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        """Initialize the MainApp instance."""
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.direct_messenger = DirectMessenger()
        self.profile = Profile()
        self._draw()
        self.body.insert_contact("studentexw23")
        publish_button = tk.Button(master=self.footer, text="Publish", width=20, command=self.publish)
        publish_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)
        refresh_button = tk.Button(master=self.footer, text="Refresh", width=20, command=self.refresh)
        refresh_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)

    def send_message(self):
        """Sends a message."""
        message = self.body.get_text_entry()
        if self.recipient is None:
            messagebox.showerror("Error", "No recipient selected.")
            return

        if message and self.recipient:
            success = self.direct_messenger.send(message, self.recipient)
            if success:
                self.add_recipient(self.username, self.recipient, f"{self.username}_recipients.json")
                self.body.insert_user_message(message)
                self.add_message(username=self.username, recipient=self.recipient, message=message)
                self.body.set_text_entry("")
            else:
                messagebox.showerror("Error", "Failed to send message.")

    def add_contact(self):
        """Adds a new contact."""
        new_contact = simpledialog.askstring("Add Contact", "Enter the username of the new contact:")
        if new_contact:
            self.body.insert_contact(new_contact)

    def recipient_selected(self, recipient):
        """Callback function for when a recipient is selected."""
        self.recipient = recipient

        self.retrieve_messages(self.username, DirectMessenger(self.server, self.username, self.password))

        self.body.entry_editor.delete(1.0, tk.END)

        messages = self.load_messages(self.username, self.recipient)
        if messages:
            for timestamp, message in messages.items():
                if message.startswith(f"You:"):
                    self.body.insert_user_message(f"{message}\n")

                if message.startswith(f"{self.recipient}:"):
                    self.body.insert_contact_message(f"{message}\n")

        else:
            print("No messages with this recipient.")

    def refresh(self):
        """Refreshes the message feed for the currently selected recipient."""
        if self.recipient:
            self.body.entry_editor.delete(1.0, tk.END)
            self.recipient_selected(self.recipient)


    def configure_server(self):
        """Configures the DS server."""
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        try:
            self.direct_messenger = DirectMessenger(self.server, self.username, self.password)
            self.check_new()
            self.load_and_display_recipients()
        except Exception as e:
            print(f"Failed to configure DirectMessenger: {e}")
            self.direct_messenger = None

    def publish(self):
        """Publishes a message to the server."""
        publish_option = messagebox.askyesno("Publish", "Do you want to publish something on the ICS 32 DS Server?")
        if publish_option:
            message = simpledialog.askstring("Publish", "Enter what you want to post:")
            if message is not None:
                self.publish_to_server(message)

    def publish_to_server(self, message: str):
        """Publishes a message to the server.

            Args:
                message (str): The message to publish.
            """
        try:
            send(server="168.235.86.101", port=3021, username=self.username, password=self.password, message=message)
            messagebox.showinfo("Publish", "Message published successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to publish message: {e}")


    @staticmethod
    def add_message(username, recipient: str, message: str):
        """Adds a message to the sent messages history.

            Args:
                username (str): The username of the sender.
                recipient (str): The username of the recipient.
                message (str): The message to add.
            """
        timestamp = int(time.time())
        try:
            with open(f"{username}_sent_messages.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"sent_messages": {}}

        if recipient not in data["sent_messages"]:
            data["sent_messages"][recipient] = []

        data["sent_messages"][recipient].append({"timestamp": str(timestamp), "message": message})

        with open(f"{username}_sent_messages.json", "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def retrieve_messages(username: str, messenger: DirectMessenger) -> None:
        """Retrieves messages from the server.

            Args:
                username (str): The username of the user.
                messenger (DirectMessenger): The messenger object for communication.
            """
        new_messages = messenger.retrieve_new()
        all_messages = messenger.retrieve_all()
        received_messages = {"received_messages": {}}

        for message in new_messages:
            recipient = message.recipient
            if recipient not in received_messages["received_messages"]:
                received_messages["received_messages"][recipient] = {"new": [], "old": []}
            received_messages["received_messages"][recipient]["new"].append(
                {"timestamp": message.timestamp, "message": message.message})

        for message in all_messages:
            recipient = message.recipient
            if recipient not in received_messages["received_messages"]:
                received_messages["received_messages"][recipient] = {"new": [], "old": []}

            if not any(msg["message"] == message.message for msg in
                       received_messages["received_messages"][recipient]["new"]):
                received_messages["received_messages"][recipient]["old"].append(
                    {"timestamp": message.timestamp, "message": message.message})

        with open(f"{username}_received_messages.json", "w") as file:
            json.dump(received_messages, file, indent=4)

    @staticmethod
    def load_messages(username: str, recipient: str) -> dict:
        """Loads messages from the message history.

            Args:
                username (str): The username of the user.
                recipient (str): The username of the recipient.

            Returns:
                dict: A dictionary containing the loaded messages.
            """
        messages = {}

        file_path = f"{username}_sent_messages.json"

        try:
            with open(file_path, "r") as file:
                sent_messages_data = json.load(file)
                if recipient in sent_messages_data["sent_messages"]:
                    messages_data = sent_messages_data["sent_messages"][recipient]
                    for msg in messages_data:
                        timestamp = msg["timestamp"]
                        message = msg["message"]
                        messages[timestamp] = f"You: {message}"
        except FileNotFoundError:
            print(f"File '{file_path}' not found. Creating a new file.")
            with open(file_path, "w") as file:
                json.dump({"sent_messages": {}}, file)
        except Exception as e:
            print(f"ERROR {e}")

        try:
            with open(f"{username}_received_messages.json", "r") as file:
                received_messages_data = json.load(file)
                for recipient in received_messages_data["received_messages"]:
                    if recipient in received_messages_data["received_messages"]:
                        data = received_messages_data["received_messages"][recipient]
                        for msg in data["new"]:
                            timestamp = msg["timestamp"]
                            message = msg["message"]
                            messages[timestamp] = f"{recipient}: {message}"
                        for msg in data["old"]:
                            timestamp = msg["timestamp"]
                            message = msg["message"]
                            messages[timestamp] = f"{recipient}: {message}"
        except FileNotFoundError:
            print("ERROR")

        sorted_messages = {float(k): v for k, v in sorted(messages.items(), key=lambda item: float(item[0]))}

        return sorted_messages


    @staticmethod
    def add_recipient(username: str, recipient: str, file_path: str) -> None:
        """Adds a recipient to the recipient list.

            Args:
                username (str): The username of the user.
                recipient (str): The username of the recipient to add.
                file_path (str): The file path to the recipient list.
            """
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        if username in data:
            if recipient not in data[username]:
                data[username].append(recipient)
        else:
            data[username] = [recipient]

        with open(file_path, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def load_recipients(file_path: str) -> Dict[str, List[str]]:
        """Loads recipients from the recipient list.

            Args:
                file_path (str): The file path to the recipient list.

            Returns:
                Dict[str, List[str]]: A dictionary containing the loaded recipients.
            """
        try:
            with open(file_path, 'r') as file:
                recipients = json.load(file)
        except FileNotFoundError:
            recipients = {}
        return recipients

    def load_and_display_recipients(self) -> None:
        """Loads and displays recipients."""
        file_path = f"{self.username}_recipients.json"
        recipients = self.load_recipients(file_path)
        if self.username in recipients:
            self.body.posts_tree.delete(*self.body.posts_tree.get_children())
            for recipient in recipients[self.username]:
                self.body.insert_contact(recipient)
        else:
            messagebox.showinfo("Info", "This user has no saved contacts. Add your first one!")

    def check_new(self):
        """Checks for new recipients."""
        if not self.direct_messenger:
            print("DirectMessenger is not configured.")
            return

        all_messages = self.direct_messenger.retrieve_all()

        if not all_messages:
            print("No messages found.")
            return

        recipients = set()
        for message in all_messages:
            recipients.add(message.recipient)

        self.update_recipients_file(recipients)

    def update_recipients_file(self, recipients):
        """Updates the recipient list file.

            Args:
                recipients: The recipient list to update.
            """
        file_path = f"{self.username}_recipients.json"

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        if self.username in data:
            data[self.username] += list(recipients - set(data[self.username]))
        else:
            data[self.username] = list(recipients)

        with open(file_path, 'w') as file:
            json.dump(data, file)



    def _draw(self):
        """Draws the menu bar, settings menu, body, and footer of the application."""
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message, refresh_callback=self.refresh)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)
