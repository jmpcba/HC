class ObjectNotFoundError(Exception):
    def __init__(self):
        # Call the base class constructor with the parameters it needs
        super().__init__(f"No Objects were found in the database")


class IllegalIDError(Exception):
    def __init__(self, id):
        super().__init__(f"the ID provided: {id},  is not a valid type. It must be int")


class InvalidParameter(Exception):
    def __init__(self, parameters):
        super().__init__(f"the parameters provided\n: {str(parameters)}\n are not valid")