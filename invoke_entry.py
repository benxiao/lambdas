from requests import Session
import base64
import sys
import json

from util import encode_base64string_from

URL = "https://jukjr9f6ic.execute-api.ap-southeast-2.amazonaws.com/entry_test/entry"
AUTHENTICATION = {"x-api-key": "fpYXQK6i0W94igcygJYLx2ocInmWwZLJ6qvZm5Zv"}
session = Session()


def create_event(fn: str)->dict:
    fn_has_extension = len(fn.rsplit(".")) == 2
    return {
        "file_name": fn,
        "file": encode_base64string_from(fn),
        "file_type": fn.rsplit(".")[-1] if fn_has_extension else ""
    }


def configure_session(session: Session):
    session.headers.update(AUTHENTICATION)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError()
    fn = sys.argv[1]
    configure_session(session)
    event = create_event(fn)
    resp = session.post(URL, data=json.dumps(event))
    print(resp.headers)
    print(resp.content)
