from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from bookFinder import BookFinder as bf
from courseFinder import CourseFinder as cf


class ResourceFinder():
    def __init__(self, master):
        # Window settings
        master.title("Link&RescourceFinder")
        master.configure(background="#80ffff")
        master.option_add('*tearOff', False)
        master.geometry("1000x700")

        # Menubar Declaration
        self.menubar = Menu(master)
        master.config(menu=self.menubar)

        # Max Results Menu
        self.maxRslts = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.maxRslts, label="Max Results")

        self.maxR_choice = IntVar()
        self.maxRslts.add_radiobutton(
            label='10', variable=self.maxR_choice, value=10)
        self.maxRslts.add_radiobutton(
            label='20', variable=self.maxR_choice, value=20)
        self.maxRslts.add_radiobutton(
            label='30', variable=self.maxR_choice, value=30)

        # Help menu
        self.help_ = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.help_, label="Help")

        self.help_.add_command(
            label="About", command=lambda: self.help_about())

        self.help_.add_command(
            label="Tutorial", command=lambda: self.help_tutorial())

        # First Frame w/ widgets
        self.frame_first = ttk.Frame(master, padding=(15.45, 10))
        self.frame_first.pack()

        # Frame will be 2 rows with 3 columns
        # (     Blank    )(   Exampletxt )(    Blank     )
        # (   Entrytxt   )(   Entry      )(    Entertxt  )

        ttk.Label(self.frame_first, text="Example: topic OR cheese,butter").grid(
            row=0, column=1, padx=5, sticky='w')
        ttk.Label(self.frame_first, text="Enter Your Topic(s):").grid(
            row=1, column=0, padx=5, sticky='w')
        self.topic_entry = ttk.Entry(self.frame_first, width=50)
        self.topic_entry.grid(row=1, column=1, padx=5, sticky='w')

        # Button to start search
        ttk.Button(self.frame_first, text="Search", command=lambda: self.startSearch(self.maxR_choice, self.topic_entry, self.sortOpt, self.searchType)).grid(
            row=1, column=2, padx=5)

        # Second Frame w/ Widgets
        self.frame_second = ttk.Frame(master, padding=(5, 10))
        self.frame_second.pack()

        # Frame will be 1 rows with 3 columns
        # (   STtxt    )(    SearchType   )(   SOtxt   )(    Sortoption    )

        ttk.Label(self.frame_second, text="Search Type:").grid(
            row=0, column=0, padx=5, pady=5)

        # Use this variable to determine what to search for
        self.searchType = StringVar()
        self.searchTypeCBox = ttk.Combobox(
            self.frame_second, textvariable=self.searchType, values=('Books', 'Courses'))
        self.searchTypeCBox.current(newindex=0)
        self.searchTypeCBox.grid(row=0, column=1)

        ttk.Label(self.frame_second, text="Sort By:").grid(
            row=0, column=2, padx=5, pady=5)

        # Use this variable to search for most frequent or most recent items
        self.sortOpt = StringVar()
        self.sortOptCBox = ttk.Combobox(
            self.frame_second, textvariable=self.sortOpt, values=('Relevance', 'Newest'))
        self.sortOptCBox.current(newindex=0)
        self.sortOptCBox.grid(row=0, column=3)

        # Paned window with two frames
        self.rsltPWindow = ttk.PanedWindow(master, orient=HORIZONTAL)
        self.rsltPWindow.pack(fill=BOTH, expand=True)

        # Paned window will have two frames
        # Left will be list of results, right will be options
        # (  results    )(  open   )
        # (             )( download)
        # (             )(         )
        # (             )(         )

        self.frame_third = ttk.Frame(
            self.rsltPWindow, width=200, height=100, relief=SUNKEN)
        self.frame_fourth = ttk.Frame(
            self.rsltPWindow, width=100, height=100)
        self.rsltPWindow.add(self.frame_third, weight=2)
        self.rsltPWindow.add(self.frame_fourth, weight=1)

        ttk.Button(self.frame_fourth, text="Open",
                   command=lambda: self.openLink(self.resultsList.get(
                       0, 'end').index(self.resultsList.get(ACTIVE)))).pack(pady=10)

        ttk.Button(self.frame_fourth, text="Download",
                   command=lambda: self.downloadBook(self.resultsList.get(
                       0, 'end').index(self.resultsList.get(ACTIVE)))).pack(pady=10)

        self.resultsList = Listbox(
            self.frame_third, selectmode=SINGLE, width=100, height=30)
        self.resultsList.pack(fill=BOTH)

        # List of links and titles for the results
        self.listlinks = []
        self.listTitles = []

        # Progress bar for processes
        self.progressbar = ttk.Progressbar(
            master, orient=HORIZONTAL, length=300, mode='indeterminate')
        self.progressbar.pack(fill=X)

    # Help menu About option command
    def help_about(self):
        about_window = Toplevel()
        about_window.title('About')
        about_window.geometry("700x50")

        ttk.Label(about_window,
                  text="This application was created by David Llanio in order" +
                  " to reduce the time spent googling for books and courses for new topics.").pack()

    # Help menu Tutorial option command
    def help_tutorial(self):
        tutorial_window = Toplevel()
        tutorial_window.title('Tutorial')
        tutorial_window.geometry("700x200")

        frame_tutorial = ttk.Frame(tutorial_window)
        frame_tutorial.pack()

        ttk.Label(frame_tutorial, text="1. Select the max number of results from the Max numbers Menu on the menubar." +
                  "\n\n2. Enter your topic or topics seperated by commas or spaces.\n\n3. Choose books or courses from dropdown." +
                  "\n\n4. Press enter to begin search." +
                  "\n\n5. Click on a book from the list and then click either open or download.").pack()

    # Search for content
    def startSearch(self, maxResults, topics, orderType, searchType):
        # Check to see if max results was selected
        if maxResults.get() == 0:
            messagebox.showerror(title="No Max Results Selected", message="You have not chosen the max number of results.\n" +
                                 "Go to Max Results menu and choose")
        # Search for search type selected
        else:
            if searchType.get() == "Books":

                # Search results object
                resultsobj = bf.searchRequest(
                    topics.get(), maxResults.get(), orderType.get())

                self.populateBookResultsList(resultsobj["items"])

            elif searchType.get() == "Courses":
                cf.searchCourses(topics.get())

    # Populate the listbox with results
    def populateBookResultsList(self, results):
        self.resultsList.delete(0, 'end')
        booktitles = []
        bookauthors = []
        booklinks = []

        for item in results:
            booktitles.append(item["volumeInfo"]["title"])
            bookauthors.append(item["volumeInfo"]["authors"])
            booklinks.append(item["volumeInfo"]["infoLink"])

        listItems = []
        for title in booktitles:
            listItems.append(title)

        for i in range(0, len(bookauthors)):
            listItems[i] += " by: " + "/".join(bookauthors[i])

        for i in range(0, len(listItems)):
            self.resultsList.insert(i, listItems[i])

        self.listlinks = booklinks
        self.listTitles = booktitles

    # Open book link in web browser
    def openLink(self, indexlinkToOpen):
        linkToOpen = self.listlinks[indexlinkToOpen]
        bf.openBookInfo(linkToOpen)

    # Download book
    def downloadBook(self, indexBookName):
        bookName = self.listTitles[indexBookName]
        bf.downloadRequest(bookName)


def main():
    root = Tk()
    resourcefinder = ResourceFinder(root)
    root.mainloop()


if __name__ == '__main__':
    main()
