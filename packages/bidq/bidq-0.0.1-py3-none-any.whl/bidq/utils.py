import json
from asyncio import Queue
from enum import Enum
from typing import Optional, Tuple, Any


class JobState:
    def __init__(self):
        self.state = None
        self.q = Queue()

    def mark_success(self, value):
        self.state = (True, value)
        self.q.put_nowait(self.state)

    def mark_failure(self, reason):
        self.state = (False, reason)
        self.q.put_nowait(self.state)

    async def wait_for_value(self):
        return await self.q.get()


class MessageType(Enum):
    Submit = "SUBMIT"
    SubmitAck = "SUBMIT_ACK"
    Bid = "BID"
    BidAck = "BID_ACK"
    BidReject = "BID_REJECT"
    JobSuccess = "JOB_SUCCESS"
    JobFailure = "JOB_FAILURE"
    Cancel = "CANCEL"


class Message:
    def __init__(self, **attrs):
        if "type" in attrs and isinstance(attrs["type"], MessageType):
            attrs["type"] = attrs["type"].value
        self.__raw = attrs
        for k, v in attrs.items():
            setattr(self, k, v)

    def is_a(self, message_type: MessageType):
        return hasattr(self, "type") and self.type == message_type.value

    def get(self, attr, default):
        return getattr(self, attr, default)

    @classmethod
    def decode(cls, raw):
        return Message(**json.loads(raw))

    def encode(self):
        return json.dumps(self.__raw)
