import json as jsonlib

import dateutil.parser
import requests
from bs4 import BeautifulSoup

from .session import ArchiveSession


class ClientCore(object):
    def __init__(self, json, session=None):
        self.session = getattr(session, "session", session)
        self.soup = BeautifulSoup

        self._json_data = json
        try:
            self._update_attributes(json)
        except KeyError as kerr:
            raise Exception("Incomplete Response")

    def _update_attributes(self, json):
        pass

    def __getattr__(self, attribute):
        """Proxy access to stored JSON."""
        if attribute not in self._json_data:
            raise AttributeError(attribute)
        value = self._json_data.get(attribute)
        setattr(self, attribute, value)
        return value

    def as_dict(self):
        """Return the attributes for this object as a dictionary.

        This is equivalent to calling::

            json.loads(obj.as_json())

        :returns: this object's attributes serialized to a dictionary
        :rtype: dict
        """
        return self._json_data

    def as_json(self):
        """Return the json data for this object.

        This is equivalent to calling::

            json.dumps(obj.as_dict())

        :returns: this object's attributes as a JSON string
        :rtype: str
        """
        return jsonlib.dumps(self._json_data)

    def _strptime(cls, time_str):
        """Convert an ISO 8601 formatted string to a datetime object.

        We assume that the ISO 8601 formatted string is in UTC and we create
        the datetime object so that it is timezone-aware.

        :param str time_str: ISO 8601 formatted string
        :returns: timezone-aware datetime object
        :rtype: datetime or None
        """
        if time_str:
            return dateutil.parser.parse(time_str)
        return None

    def request(self, method, *args, **kwargs):
        request_method = getattr(self.session, method)
        return request_method(*args, **kwargs)

    def get(self, url, **kwargs):
        """Sends a get request"""
        return self.request('get', url, **kwargs)

    def __repr__(self):
        repr_string = self._repr()
        if requests.compat.is_py2:
            return repr_string.encode("utf-8")
        return repr_string

    @classmethod
    def from_dict(cls, json_dict):
        """Return an instance of this class formed from ``json_dict``."""
        return cls(json_dict)

    @classmethod
    def from_json(cls, json):
        """Return an instance of this class formed from ``json``."""
        return cls(jsonlib.loads(json))

    def _repr(self):
        return "<basemodel at 0x{0:x}>".format(id(self))

    def new_session(self):
        """Generate a new session.

        :returns:
            A brand new session
        """
        return ArchiveSession()


class Collection(ClientCore):
    """ <Better Describe Collections here>

    """
    _class_name = "Collection"

    def _update_attributes(self, json):
        self.version = json["version"]
        self.id = f'{json["id"]}@{json["version"]}'
        self.title = json["title"]
        self.legacy_id = json["legacy_id"]
        self.tree = json["tree"]
        self.baked = self._strptime(json["baked"])
        self.json_url = self.session.build_url(
            "contents", f"{self.id}@{self.version}.json")
        self.html_url = self.session.build_url(
            "contents", f"{self.id}@{self.version}.html")
        self.slug = self.tree["slug"]
        self.license = License(json["license"])
        self.table_of_contents = TableOfContents(self.tree, self.id, self.session)
        self.history = [History(item, self.session) for item in json["history"]]

    def _repr(self):
        return f"<{self._class_name} [{self.title}]>"


class SubCollection(ClientCore):
    _class_name = "SubCollection"

    def __init__(self, json, collection_id, session=None, parent_id=None):
        self.collection_id = collection_id
        self.parent_id = parent_id
        super(SubCollection, self).__init__(json, session)

    def _update_attributes(self, json):
        self.id = json["id"]
        self.slug = json["slug"]
        self.html_title = json["title"]
        self.short_id = json["shortId"]
        self.title = self.soup(
            json["title"], "html.parser").find('span', attrs={"class": "os-text"}).text
        self.html_url = self.session.build_url("contents", f"{self.collection_id}:{self.id}.html")
        self.json_url = self.session.build_url("contents", f"{self.collection_id}:{self.id}.json")

        if "contents" in json and json["contents"]:
            self.contents = [
                SubCollection(
                    node, self.collection_id, session=self.session)
                if "contents" in node and node["contents"] else Module(
                    node, self.collection_id, session=self.session) for node in json["contents"]]

    def _repr(self):
        return f"<{self._class_name} [{self.title}]>"


class TableOfContents(ClientCore):
    _class_name = "_TableOfContents"

    def __init__(self, json, collection_id, session=None):
        self.collection_id = collection_id
        super(TableOfContents, self).__init__(json, session)

    def _update_attributes(self, json):
        self.contents = [
            SubCollection(
                node, self.collection_id, session=self.session)
            if "contents" in node and node["contents"] else Module(
                node, self.collection_id, session=self.session) for node in json["contents"]]

    def _repr(self):
        return f"<{self._class_name} {[module.title for module in self.contents[:3]]}>"


class Module(ClientCore):
    _class_name = "Module"

    def __init__(self, json, collection_id, session=None):
        self.collection_id = collection_id
        super(Module, self).__init__(json, session)

    def _update_attributes(self, json):
        self.id = json["id"]
        self.slug = json["slug"]
        self.html_title = json["title"]
        self.short_id = json["shortId"]
        self.title = self.soup(
            json["title"], "html.parser").find('span', attrs={"class": "os-text"}).text
        self.html_url = self.session.build_url("contents", f"{self.collection_id}:{self.id}.html")
        self.json_url = self.session.build_url("contents", f"{self.collection_id}:{self.id}.json")

    def _repr(self):
        return f"<{self._class_name} [{self.title}]>"

    def get_html(self):
        response = self.session.get(self.html_url)
        return response.text

    def get_json(self):
        response = self.session.get(self.json_url)
        return response.json()

    @property
    def section_num(self):
        section_num = self.soup(
            self.html_title, "html.parser").find('span', attrs={"class": "os-number"})
        if section_num:
            return section_num.text
        else:
            return None


class License(ClientCore):
    _class_name = "License"

    def _update_attributes(self, json):
        self.url = json["url"]
        self.code = json["code"]
        self.version = json["version"]
        self.name = json["name"]

    def _repr(self):
        return f"<{self._class_name} [{self.name} {self.version}]>"


class History(ClientCore):
    _class_name = "History"

    def _update_attributes(self, json):
        self.changes = json["changes"]
        self.version = json["version"]
        self.revised = self._strptime(json["revised"])
        self.publisher = Publisher(json["publisher"], session=self.session)

    def _repr(self):
        return f"<{self._class_name} [{self.version}]>"


class Publisher(ClientCore):
    _class_name = "Publisher"

    def _update_attributes(self, json):
        self.surname = json["surname"]
        self.suffix = json["suffix"]
        self.firstname = json["firstname"]
        self.title = json["title"]
        self.fullname = json["fullname"]
        self.id = json["id"]

    def _repr(self):
        return f"<{self._class_name} [{self.id}]>"
