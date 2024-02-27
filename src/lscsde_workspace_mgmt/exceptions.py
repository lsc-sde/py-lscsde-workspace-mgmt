class NoAssignedValidWorkspaces(Exception):
    def __init__(self, user):
        self.user = user
        self.message = f"User {user} does not have any valid workspaces assigned"
        super().__init__(self.message)
