import xml.etree.ElementTree as ET


class Player:

    def __init__(self, name, age, country, overall):
        Player.counter += 1
        self._id = Player.counter
        self._name = name
        self._age = age
        self._country = country
        self._overall = overall

    def to_xml(self):
        el = ET.Element("Player")
        el.set("id", str(self._id))
        el.set("name", self._name)
        el.set("age", self._age)
        el.set("country_ref", str(self._country.get_id()))
        el.set("overall", self._overall)
        return el

    def __str__(self):
        return f"{self._name}, age:{self._age}, country:{self._country}, overall:{self._overall}"


Player.counter = 0
