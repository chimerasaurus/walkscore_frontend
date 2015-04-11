class WsLocation:
    """Represents a location helf in the Walkscore website."""
    def __init__(self, *init_data, **kwargs):
        for dictionary in init_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class City(WsLocation):
    """Represents a city from the Walkscore website."""
    def __init__(self, *init_data, **kwargs):
        WsLocation.__init__(self, *init_data, **kwargs)

    @property
    def neighborhoods(self):
        """Get a list of neighborhoods for the city."""
        nh_list = []
        for nh in self._neighborhoods:
            nh['city'] = self.name
            nh['state'] = self.state
            new_neighborhood = Neighborhood(nh)
            nh_list.append(new_neighborhood)
        return nh_list

    @neighborhoods.setter
    def neighborhoods(self, value):
        """Set the list of neighborhoods for the city."""
        self._neighborhoods = value


class Neighborhood(WsLocation):
    """Represents a neighborhood from the Walkscore website."""
    def __init__(self, *init_data, **kwargs):
        WsLocation.__init__(self, *init_data, **kwargs)