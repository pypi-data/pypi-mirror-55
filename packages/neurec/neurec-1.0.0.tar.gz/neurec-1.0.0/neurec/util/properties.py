import logging
from neurec.util.singleton import Singleton
from neurec.util import reader
from neurec.data.properties import types

class Properties(metaclass=Singleton):
    """A class to handle property settings."""
    def __init__(self, properties="", section="DEFAULT"):
        """Setups the class with an empty properties dictionary."""
        self.logger = logging.getLogger(__name__)
        self.__section = section
        self.__properties = self.setProperties(properties) if properties else {}

    def setSection(self, name):
        """Sets the section of the property file to read from.

        name -- name of the section
        """
        self.__section = name

    def setProperties(self, path):
        """Reads a properties file to load the property values.

        path -- path to properties file
        """
        self.__properties = reader.file(path)

    def getProperty(self, name):
        """Returns the value for a property."""
        try:
            value = self.__properties[self.__section][name]
        except KeyError:
            raise KeyError('Key ' + str(name) + ' not found in properties. Add to your properties')

        return self.__convertProperty(name, value)

    def getProperties(self, names):
        """Returns a dictionary of values for the properties names.

        names -- list of property names
        """
        values = {}

        for name in names:
            values[name] = self.getProperty(name)

        return values

    def __convertProperty(self, name, value):
        """Casts a property's value to its required type.

        name -- name of property
        value -- value to convert
        """
        try:
            return types[name](value)
        except KeyError:
            raise KeyError("Could not convert property " + str(name) + ". Key not found in types. Add to neurec.data.properties.types")
        except ValueError:
            raise ValueError("Could not covert the value of " + str(name) + '. ' + str(value) + " does not match type set in neurec.data.properties.types")
