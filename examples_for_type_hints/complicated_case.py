import json
import os
import uuid
from datetime import datetime

# IDE don't know about type which will be returned
# we can fix it:
# def _generate_tracking_event(fingerprint, event, parent_fingerprint, annotations)->bytes:
def _generate_tracking_event(fingerprint, event, parent_fingerprint, annotations):
    if annotations is None:
        annotations = {}

    if parent_fingerprint is None or parent_fingerprint == '':
        links = []
    else:
        links = [{"fingerprint": parent_fingerprint, "rel": "parent"}]

    return json.dumps({
        'id': str(uuid.uuid1()),
        'ts': datetime.utcnow().isoformat() + 'Z',
        'host': '{}/{}'.format(os.getenv('AWS_LAMBDA_FUNCTION_NAME'), os.getenv('AWS_LAMBDA_LOG_STREAM_NAME')),
        'source': os.getenv('SERVICE_NAME', 'Comms2.0'),
        'fingerprint': fingerprint,
        'annotations': annotations,
        'event': event,
        'links': links
    })


def get_event_id():
    event = _generate_tracking_event(str(uuid.uuid1()), None, None, {})
    return event['id']
