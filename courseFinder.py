import webbrowser
import tkinter as tk
from tkinter import messagebox, simpledialog

class CourseFinder:
    def __init__(self):
        self.platforms = {
            "LinkedIn Learning": "https://www.linkedin.com/learning/search?entityType=COURSE&keywords=",
            "Udemy": "https://www.udemy.com/courses/search/?q=",
            "Coursera": "https://www.coursera.org/courses?query=",
            "edX": "https://www.edx.org/find-your-course?search_query=",
            "Pluralsight": "https://www.pluralsight.com/search?q=",
            "Skillshare": "https://www.skillshare.com/browse?query="
        }

    def search_courses(self, topics, platform=None):
        """
        Search courses on specified platform or all platforms
        
        Args:
            topics (str): Search keywords
            platform (str, optional): Specific platform to search. Defaults to None.
        """
        # Validate input
        if not topics:
            messagebox.showwarning("Warning", "Please enter search topics")
            return

        # URL encode the topics
        encoded_topics = topics.replace(" ", "+")

        # If no specific platform is chosen, open all platforms
        if platform is None:
            for url in self.platforms.values():
                webbrowser.open(url + encoded_topics)
        else:
            # Check if platform exists
            if platform in self.platforms:
                webbrowser.open(self.platforms[platform] + encoded_topics)
            else:
                messagebox.showerror("Error", f"Platform {platform} not found")

    def interactive_search(self):
        """
        Interactive GUI for course search
        """
        root = tk.Tk()
        root.title("Course Finder")
        root.geometry("400x300")
        root.configure(bg='black')

        # Topics Entry
        tk.Label(root, text="Enter Course Topics:", bg='black', fg='white').pack(pady=10)
        topics_entry = tk.Entry(root, width=40)
        topics_entry.pack(pady=10)

        # Platform Selection
        tk.Label(root, text="Select Platform (Optional):", bg='black', fg='white').pack(pady=5)
        platform_var = tk.StringVar(root)
        platform_var.set("All Platforms")  # default value
        platform_dropdown = tk.OptionMenu(root, platform_var, "All Platforms", *self.platforms.keys())
        platform_dropdown.pack(pady=10)

        def search_action():
            topics = topics_entry.get()
            platform = platform_var.get() if platform_var.get() != "All Platforms" else None
            self.search_courses(topics, platform)

        # Search Button
        search_button = tk.Button(root, text="Search Courses", command=search_action)
        search_button.pack(pady=20)

        root.mainloop()

    def add_platform(self, name, url):
        """
        Add a new learning platform
        
        Args:
            name (str): Name of the platform
            url (str): Base search URL for the platform
        """
        self.platforms[name] = url

    def remove_platform(self, name):
        """
        Remove a learning platform
        
        Args:
            name (str): Name of the platform to remove
        """
        if name in self.platforms:
            del self.platforms[name]
        else:
            print(f"Platform {name} not found")

    def list_platforms(self):
        """
        List all available platforms
        
        Returns:
            list: List of platform names
        """
        return list(self.platforms.keys())

# Example usage
def main():
    course_finder = CourseFinder()
    
    # Option 1: Direct search
    course_finder.search_courses("Python Programming")
    
    # Option 2: Interactive search
    course_finder.interactive_search()
    
    # Option 3: Search on specific platform
    course_finder.search_courses("Machine Learning", "Coursera")
    
    # Option 4: Add and remove platforms
    course_finder.add_platform("Udacity", "https://www.udacity.com/courses?search=")
    course_finder.remove_platform("Skillshare")
    
    # List available platforms
    print(course_finder.list_platforms())

if __name__ == "__main__":
    main()
