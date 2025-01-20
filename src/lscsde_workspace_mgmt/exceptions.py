class NoAssignedValidWorkspaces(Exception):
    """
    Represents an error where a user is not assigned any valid workspaces
    """
    
    def __init__(self, user):
        self.user = user
        self.message = f"User {user} does not have any valid workspaces assigned"
        super().__init__(self.message)

class InvalidParameterException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidLabelFormatException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class WorkspaceNotFoundException(Exception):
    """
    Represents an exception where a workspace is not found in the labels from jupyterhub
    """
    def __init__(self, namespace, name):
        self.name = name
        self.namespace = namespace
        self.message = f"workspace label is not populated for pod/{name} on {namespace} namespace"
        super().__init__(self.message)
