class ObjectNotFoundError(Exception):
    def __init__(self, id):
        # Call the base class constructor with the parameters it needs
        super().__init__(f"No Object with id: {id} was found")


class IllegalIDError(Exception):
    def __init__(self, id):
        super().__init__(f"the ID provided: {id},  is not a valid type. It must be int")


class InvalidParameter(Exception):
    def __init__(self, parameters):
        super().__init__(f"the paramters: {str(parameters)} are not valid")