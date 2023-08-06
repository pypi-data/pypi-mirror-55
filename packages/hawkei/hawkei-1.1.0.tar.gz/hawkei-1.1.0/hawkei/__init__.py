import logging

from hawkei.message import message_base, message_extended

from hawkei.utils import merge
from hawkei.config import config
from hawkei.processor.asynchronous import Async

_TRACK_EVENTS_CREATE = 'track_events:create'
_IDENTIFY_EVENTS_CREATE = 'identify_events:create'
_GROUP_EVENTS_CREATE = 'group_events:create'
_IDENTITIES_UPDATE = 'identities:update'
_WATCHERS_CREATE = 'watchers:create'

_processor = None

def init(user_config=None):
    config.build(user_config)

    global _processor # pylint: disable=global-statement
    _processor = Async()

def track(name, payload=None, options=None):
    if not config.active(): return False

    payload = payload or {}
    options = options or {}

    payload['name'] = name
    payload['type'] = 'track'

    _processor.enqueue({
        'action': _TRACK_EVENTS_CREATE,
        'payload': merge(message_extended(), payload),
        'options': options,
    })
    return True

def identify(user_id, payload=None, options=None):
    if not config.active(): return False

    payload = payload or {}
    options = options or {}

    payload['user_id'] = user_id

    _processor.enqueue({
        'action': _IDENTIFY_EVENTS_CREATE,
        'payload': merge(message_extended(), payload),
        'options': options,
    })
    return True

def group(group_id, payload=None, options=None):
    if not config.active(): return False

    payload = payload or {}
    options = options or {}

    payload['group_id'] = group_id

    _processor.enqueue({
        'action': _GROUP_EVENTS_CREATE,
        'payload': merge(message_base(), payload),
        'options': options,
    })
    return True

def watch(flow, payload=None, options=None):
    if not config.active(): return False

    payload = payload or {}
    options = options or {}

    payload['template_flow'] = flow

    _processor.enqueue({
        'action': _WATCHERS_CREATE,
        'payload': merge(message_base(), payload),
        'options': options,
    })
    return True

def flush():
    if not config.active(): return False
    _processor.flush()
    return True

def shutdown():
    if not config.active(): return False
    _processor.shutdown()
    return True
