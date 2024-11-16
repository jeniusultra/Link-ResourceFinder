#JeniusUltra's Link&ResourceFinder
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup
import threading
import webbrowser
import urllib.parse
import re

class LinkResourceFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Link & Resource Finder")
        self.root.geometry("1200x800")
        
        self.create_interface()
    
    def create_interface(self):
        # Search Frame
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        # Search Entry
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame, 
            textvariable=self.search_var, 
            font=('Arial', 14), 
            width=50
        )
        search_entry.pack(side='left', expand=True, fill='x', padx=5)
        search_entry.bind('<Return>', lambda event: self.start_resource_search())
        
        # Search Button
        search_btn = tk.Button(
            search_frame, 
            text="Find Resources", 
            command=self.start_resource_search
        )
        search_btn.pack(side='right', padx=5)
        
        # Results Text Area
        self.results_text = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD, 
            font=('Courier', 10)
        )
        self.results_text.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Make text read-only and add link detection
        self.results_text.tag_config('link', foreground='blue', underline=True)
        self.results_text.bind('<Button-1>', self.handle_link_click)
    
    def start_resource_search(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Error", "Please enter a search query")
            return
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        
        # Start threaded search
        threading.Thread(
            target=self.comprehensive_resource_search, 
            args=(query,), 
            daemon=True
        ).start()
    
    def comprehensive_resource_search(self, query):
        results = []
        
        # Multiple search strategies
        search_methods = [
            self.google_search,
            self.scholarly_search,
            self.github_search
        ]
        
        for method in search_methods:
            try:
                method_results = method(query)
                results.extend(method_results)
            except Exception as e:
                print(f"Search method error: {method.__name__}: {e}")
        
        # Update results in main thread
        self.root.after(0, self.display_results, results)
    
    def google_search(self, query):
        # Encode the query for URL
        encoded_query = urllib.parse.quote(query)
        
        # Construct search URL
        url = f"https://www.google.com/search?q={encoded_query}+filetype:pdf+OR+site:academia.edu"
        
        try:
            # Send request with user agent to mimic browser
            response = requests.get(
                url, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                }
            )
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract links
            results = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Filter and clean links
                if href.startswith('/url?q='):
                    clean_link = href.split('/url?q=')[1].split('&sa=')[0]
                    if any(ext in clean_link.lower() for ext in ['.pdf', 'academia.edu']):
                        results.append(clean_link)
            
            return list(set(results))[:20]
        
        except Exception as e:
            print(f"Google search error: {e}")
            return []
    
    def scholarly_search(self, query):
        # Encode the query for URL
        encoded_query = urllib.parse.quote(query)
        
        # Construct search URL for Google Scholar
        url = f"https://scholar.google.com/scholar?q={encoded_query}"
        
        try:
            # Send request with user agent to mimic browser
            response = requests.get(
                url, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                }
            )
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract links to scholarly articles
            results = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Filter links to scholarly sources
                if href.startswith('http') and ('scholar.google' in href or '.pdf' in href):
                    results.append(href)
            
            return list(set(results))[:20]
        
        except Exception as e:
            print(f"Scholarly search error: {e}")
            return []
    
    def github_search(self, query):
        # Encode the query for URL
        encoded_query = urllib.parse.quote(query)
        
        # Construct GitHub search URL
        url = f"https://github.com/search?q={encoded_query}+extension:pdf"
        
        try:
            # Send request with user agent to mimic browser
            response = requests.get(
                url, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                }
            )
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract repository links
            results = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Filter GitHub links
                if href.startswith('/') and href.count('/') == 2:
                    full_link = f"https://github.com{href}"
                    results.append(full_link)
            
            return list(set(results))[:20]
        
        except Exception as e:
            print(f"GitHub search error: {e}")
            return []
    
    def display_results(self, results):
        if not results:
            self.results_text.insert(tk.END, "No resources found. Try a different search.")
            return
        
        # Deduplicate and limit results
        unique_results = list(set(results))[:50]
        
        # Display results with clickable links
        for link in unique_results:
            # Truncate long links
            display_link = link[:100] + '...' if len(link) > 100 else link
            
            # Insert link with tag for clickability
            self.results_text.insert(tk.END, display_link + '\n', 'link')
    
    def handle_link_click(self, event):
        # Get the index of the clicked position
        index = self.results_text.index(f"@{event.x},{event.y}")
        
        # Get the tags at that index
        tags = self.results_text.tag_names(index)
        
        # If the link tag is present, open the link
        if 'link' in tags:
            # Get the text of the link
            line_start = self.results_text.index(f"{index} linestart")
            line_end = self.results_text.index(f"{index} lineend")
            link = self.results_text.get(line_start, line_end).strip()
            
            try:
                webbrowser.open(link)
            except Exception as e:
                print(f"Error opening link: {e}")

def main():
    root = tk.Tk()
    app = LinkResourceFinder(root)
    root.mainloop()

if __name__ == "__main__":
    main()
