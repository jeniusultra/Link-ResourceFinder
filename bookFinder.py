import json
import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
from urllib import request, parse
import threading

class BookFinder:
    def __init__(self):
        self.api_key = "YOUR_GOOGLE_BOOKS_API_KEY"  # Optional: Add your API key for more requests
        self.base_url = "https://www.googleapis.com/books/v1/volumes"
        
        # Predefined download sources
        self.download_sources = {
            "Project Gutenberg": "https://www.gutenberg.org/ebooks/search/?query=",
            "Open Library": "https://openlibrary.org/search?q=",
            "PDF Drive": "https://www.pdfdrive.com/search?q=",
            "Z-Library": "https://z-lib.org/",  # Requires careful use
        }

    def search_books(self, topics, max_results=20, order_by='relevance'):
        """
        Search for books using Google Books API
        
        Args:
            topics (str): Search query
            max_results (int): Maximum number of results
            order_by (str): Sorting method (relevance, newest)
        
        Returns:
            dict: Book search results
        """
        try:
            # URL encode the search query
            encoded_topics = parse.quote(topics.lower().strip())
            
            # Construct query parameters
            params = {
                'q': encoded_topics,
                'filter': 'ebooks',
                'langRestrict': 'en',
                'maxResults': max_results,
                'orderBy': order_by,
                'printType': 'BOOKS',
                'projection': 'LITE'
            }
            
            # Add API key if available
            if self.api_key:
                params['key'] = self.api_key
            
            # Construct full URL
            full_url = f"{self.base_url}?{parse.urlencode(params)}"
            
            # Perform the request
            with request.urlopen(full_url) as response:
                data = response.read().decode('utf-8')
                return json.loads(data)
        
        except Exception as e:
            messagebox.showerror("Search Error", f"An error occurred: {str(e)}")
            return None

    def open_book_info(self, book_link):
        """
        Open book information in default web browser
        
        Args:
            book_link (str): URL to book details
        """
        if book_link:
            webbrowser.open(book_link)
        else:
            messagebox.showwarning("Warning", "No link available")

    def download_book(self, book_name, source=None):
        """
        Open download sources for a book
        
        Args:
            book_name (str): Name of the book to download
            source (str, optional): Specific download source
        """
        if source and source in self.download_sources:
            search_url = self.download_sources[source] + parse.quote(book_name)
            webbrowser.open(search_url)
        else:
            # Open all sources if no specific source is selected
            for url in self.download_sources.values():
                webbrowser.open(url + parse.quote(book_name))

    def create_gui(self):
        """
        Create a GUI for book searching
        """
        root = tk.Tk()
        root.title("Book Finder")
        root.geometry("600x500")
        root.configure(bg='black')

        # Search Frame
        search_frame = tk.Frame(root, bg='black')
        search_frame.pack(pady=10)

        # Search Label and Entry
        tk.Label(search_frame, text="Search Books:", bg='black', fg='white').pack(side=tk.LEFT)
        search_entry = tk.Entry(search_frame, width=40)
        search_entry.pack(side=tk.LEFT, padx=10)

        # Results Treeview
        results_tree = ttk.Treeview(root, columns=('Title', 'Author', 'Year'), show='headings')
        results_tree.heading('Title', text='Title')
        results_tree.heading('Author', text='Author')
        results_tree.heading('Year', text='Year')
        results_tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Download Source Dropdown
        tk.Label(root, text="Download Source:", bg='black', fg='white').pack()
        download_var = tk.StringVar(root)
        download_var.set("All Sources")
        download_dropdown = tk.OptionMenu(root, download_var, "All Sources", *self.download_sources.keys())
        download_dropdown.pack(pady=5)

        def perform_search():
            # Clear previous results
            for i in results_tree.get_children():
                results_tree.delete(i)
            
            # Perform search
            query = search_entry.get()
            if not query:
                messagebox.showwarning("Warning", "Please enter a search query")
                return
            
            # Use threading to prevent GUI freezing
            def search_thread():
                results = self.search_books(query)
                if results and 'items' in results:
                    for book in results['items']:
                        try:
                            title = book['volumeInfo'].get('title', 'Unknown Title')
                            authors = ', '.join(book['volumeInfo'].get('authors', ['Unknown Author']))
                            year = book['volumeInfo'].get('publishedDate', 'Unknown Year')[:4]
                            
                            results_tree.insert('', 'end', values=(title, authors, year))
                        except Exception as e:
                            print(f"Error processing book: {e}")
            
            threading.Thread(target=search_thread, daemon=True).start()

        def download_selected():
            selected_item = results_tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a book")
                return
            
            book_name = results_tree.item(selected_item)['values'][0]
            source = download_var.get() if download_var.get() != "All Sources" else None
            self.download_book(book_name, source)

        # Search Button
        search_button = tk.Button(root, text="Search", command=perform_search)
        search_button.pack(pady=5)

        # Download Button
        download_button = tk.Button(root, text="Download", command=download_selected)
        download_button.pack(pady=5)

        root.mainloop()

def main():
    book_finder = BookFinder()
    book_finder.create_gui()

if __name__ == "__main__":
    main()
