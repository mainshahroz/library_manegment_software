from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

# Sample data for books and users
books = [
    {"id": 1, "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "status": "Available"},
    {"id": 2, "title": "1984", "author": "George Orwell", "genre": "Dystopian", "status": "Checked Out"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction", "status": "Available"}
]

users = [
    {"id": 1, "name": "loki", "borrowed_books": []},
    {"id": 2, "name": "Bob", "borrowed_books": []}
]


class LibraryApp(App):

    def build(self):
        self.title = "Library Management System"
        self.layout = BoxLayout(orientation='vertical')

        # Title Label
        self.layout.add_widget(Label(text="Welcome to the Community Library System", font_size=24, size_hint_y=0.1))

        # Input for User ID
        self.user_id_input = TextInput(hint_text="Enter your User ID", multiline=False, size_hint_y=0.1)
        self.layout.add_widget(self.user_id_input)

        # Input for Book ID
        self.book_id_input = TextInput(hint_text="Enter Book ID", multiline=False, size_hint_y=0.1)
        self.layout.add_widget(self.book_id_input)

        # Borrow Book Button
        borrow_btn = Button(text="Borrow Book", size_hint_y=0.1)
        borrow_btn.bind(on_press=self.borrow_book)
        self.layout.add_widget(borrow_btn)

        # Return Book Button
        return_btn = Button(text="Return Book", size_hint_y=0.1)
        return_btn.bind(on_press=self.return_book)
        self.layout.add_widget(return_btn)

        # View All Books Button
        view_books_btn = Button(text="View All Books", size_hint_y=0.1)
        view_books_btn.bind(on_press=self.view_books)
        self.layout.add_widget(view_books_btn)

        # Search Books Button
        search_btn = Button(text="Search Book", size_hint_y=0.1)
        search_btn.bind(on_press=self.search_books)
        self.layout.add_widget(search_btn)

        return self.layout

    # Function to Borrow a Book
    def borrow_book(self, instance):
        user_id = self.user_id_input.text
        book_id = self.book_id_input.text

        if not user_id.isdigit() or not book_id.isdigit():
            self.show_popup("Error", "Please enter valid User ID and Book ID.")
            return

        user_id = int(user_id)
        book_id = int(book_id)

        user = next((user for user in users if user['id'] == user_id), None)
        book = next((book for book in books if book['id'] == book_id), None)

        if user and book:
            if book['status'] == "Available":
                book['status'] = "Checked Out"
                user['borrowed_books'].append(book)
                self.show_popup("Success", f"Book '{book['title']}' borrowed successfully!")
            else:
                self.show_popup("Error", f"Book '{book['title']}' is already checked out.")
        else:
            self.show_popup("Error", "Invalid User ID or Book ID.")

    # Function to Return a Book
    def return_book(self, instance):
        user_id = self.user_id_input.text
        book_id = self.book_id_input.text

        if not user_id.isdigit() or not book_id.isdigit():
            self.show_popup("Error", "Please enter valid User ID and Book ID.")
            return

        user_id = int(user_id)
        book_id = int(book_id)

        user = next((user for user in users if user['id'] == user_id), None)
        book = next((book for book in books if book['id'] == book_id), None)

        if user and book:
            if book in user['borrowed_books']:
                book['status'] = "Available"
                user['borrowed_books'].remove(book)
                self.show_popup("Success", f"Book '{book['title']}' returned successfully!")
            else:
                self.show_popup("Error", f"User {user['name']} hasn't borrowed '{book['title']}'.")
        else:
            self.show_popup("Error", "Invalid User ID or Book ID.")

    # Function to View All Books
    def view_books(self, instance):
        book_list = "\n".join([f"{book['id']}. {book['title']} ({book['status']})" for book in books])
        self.show_popup("All Books", book_list)

    # Function to Search Books
    def search_books(self, instance):
        keyword = self.book_id_input.text.lower()
        results = [f"{book['id']}. {book['title']} ({book['status']})"
                   for book in books if keyword in book['title'].lower() or keyword in book['author'].lower()]
        if results:
            self.show_popup("Search Results", "\n".join(results))
        else:
            self.show_popup("Search Results", "No books found.")

    # Function to show Popup messages
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        close_btn = Button(text="Close", size_hint=(1, 0.25))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()


# Run the application
if __name__ == "__main__":
    LibraryApp().run()