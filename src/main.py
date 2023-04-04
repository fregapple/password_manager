import os
import string
import secrets
import webbrowser

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button



def generate_password(length=12):
    characters = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    password = ''.join(secrets.choice(characters) for i in range(length))
    while not rule_check(password):
        password = ''.join(secrets.choice(characters) for i in range(length))
    return password

def rule_check(password):
    w = 0
    x = 0
    y = 0
    z = 0
    for char in password:
        if char in string.ascii_letters:
            if char == char.upper():
                x += 1
            else:
                w += 1
        elif char in string.digits:
            y += 1
        elif char in string.punctuation:
            z += 1

    return w >= 2 and x >= 2 and y >= 2 and z >= 2

class PasswordManagerApp(App):
    def build(self):
        self.root_layout = BoxLayout(orientation='vertical')
        self.main_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.9))
        self.navbar_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.new_password_button = Button(text='Create New Password')
        self.new_password_button.bind(on_press=self.show_new_password_screen)
        self.view_passwords_button = Button(text='View Saved Passwords')
        self.view_passwords_button.bind(on_press=self.show_saved_passwords)
        self.navbar_layout.add_widget(self.new_password_button)
        self.navbar_layout.add_widget(self.view_passwords_button)
        self.root_layout.add_widget(self.main_layout)
        self.root_layout.add_widget(self.navbar_layout)
        return self.root_layout

    def show_new_password_screen(self, instance):
        self.main_layout.clear_widgets()
        self.title_label = Label(text='Enter a title for the password:')
        self.title_input = TextInput(multiline=False)
        self.generate_button = Button(text='Generate Password')
        self.generate_button.bind(on_press=self.generate_password)
        self.password_label = Label(text='')
        self.main_layout.add_widget(self.title_label)
        self.main_layout.add_widget(self.title_input)
        self.main_layout.add_widget(self.generate_button)
        self.main_layout.add_widget(self.password_label)

    def show_saved_passwords(self, instance):
        self.main_layout.clear_widgets()
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'passwords.txt')
        with open(file_path, 'r') as f:
            passwords = f.read()
            passwords_label = Label(text=passwords)
            self.main_layout.add_widget(passwords_label)

    def generate_password(self, instance):
        title = self.title_input.text
        password = generate_password()
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'passwords.txt')
        with open(file_path, 'a') as f:
            f.write(f'{title}: {password}\n')
        self.password_label.text = f'Your password has been saved to passwords.txt with the title: {title}'

if __name__ == '__main__':
    PasswordManagerApp().run()