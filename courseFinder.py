import webbrowser


class CourseFinder:
    def searchCourses(topics):
        link = f"https://www.linkedin.com/learning/search?entityType=COURSE&keywords={topics}"
        webbrowser.open(link)
