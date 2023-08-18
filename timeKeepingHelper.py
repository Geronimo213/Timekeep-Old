class Project(object):
    name = ""
    start_date = None
    completion_date = None
    total_hours = 0.0
    client = ""

    def __init__(self, name, start_date, client):
        self.name = name
        self.start_date = start_date
        self.total_hours = 0.0
        self.client = client


def createProject(projects, name, start_date, client):
    project = Project(name, start_date, client)
    projects.append(project)
    return projects

