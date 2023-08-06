import backoff
import requests


class ArchiveSession(requests.Session):
    def __init__(self, root_url="https://archive.cnx.org"):
        super(ArchiveSession, self).__init__()

        self.headers.update(
            {
                # Only accept UTF-8 encoded data
                "Accept-Charset": "utf-8",
                # Set our own custom User-Agent string
                "User-Agent": "OpenStax Archive API Client",
            }
        )
        self.root_url = root_url
        self.request_counter = 0

    def build_url(self, *args, **kwargs):
        parts = [kwargs.get("root_url") or self.root_url]
        parts.extend(args)
        parts = [str(p) for p in parts]

        return '/'.join(parts)

    @backoff.on_exception(backoff.expo, requests.exceptions.ConnectionError)
    def request(self, *args, **kwargs):
        response = super(ArchiveSession, self).request(*args, **kwargs)
        self.request_counter += 1
        return response
