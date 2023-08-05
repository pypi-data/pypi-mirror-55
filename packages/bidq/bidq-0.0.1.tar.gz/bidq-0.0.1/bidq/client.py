import asyncio
import uuid
from inspect import iscoroutinefunction
from .exceptions import BidqException
from .utils import JobState, MessageType, Message


lock = True


class BidQ:
    @classmethod
    async def create(cls, host="127.0.0.1", port=8888):
        global lock
        reader, writer = await asyncio.open_connection(host, port)
        lock = False
        self = cls(reader, writer)
        task = asyncio.create_task(self._handler())
        self._task = task
        lock = True
        return self

    def __init__(self, reader, writer):
        if lock:
            raise BidqException("Use BidQ.creaet(...) to get an instance")
        self.reader = reader
        self.writer = writer
        self._q = asyncio.Queue()
        self._jobs = {}
        self._workers = {}
        self._bids = {}

    async def _handle_message(self, message: Message):
        if message.is_a(MessageType.JobFailure):
            jid = message.id
            if jid in self._jobs:
                self._jobs[jid].mark_failure(message.reason)
        elif message.is_a(MessageType.JobSuccess):
            jid = message.id
            if jid in self._jobs:
                self._jobs[jid].mark_success(message.get("value", None))
        elif message.is_a(MessageType.Submit):
            if message.get("topic", None) in self._workers:
                self._bids[message.id] = message
                await self._send(Message(type=MessageType.Bid.value, id=message.id))
        elif message.is_a(MessageType.BidAck) or message.is_a(MessageType.BidReject):
            msg = self._bids[message.id]
            del self._bids[message.id]
            if message.is_a(MessageType.BidReject):
                return
            worker = self._workers[msg.get("topic", None)]
            task = worker() if not msg.get("payload", None) else worker(**msg.payload)
            try:
                value = (await task) if iscoroutinefunction(worker) else task
                return await self._send(
                    Message(type=MessageType.JobSuccess, id=message.id, value=value)
                )
            except Exception as e:
                return await self._send(
                    Message(type=MessageType.JobFailure, id=message.id, reason=str(e))
                )

    async def _handler(self):
        while True:
            try:
                data = await self.reader.read(1500)
                msg = Message.decode(data)
                self._q.put_nowait(msg)
                await self._handle_message(msg)
            except asyncio.CancelledError:
                return

    async def _send(self, message: Message):
        self.writer.write(message.encode().encode())
        await self.writer.drain()

    async def _set_timeout_for(self, jid, timeout):
        await asyncio.sleep(timeout)
        if jid in self._jobs and self._jobs[jid].state is None:
            await self.cancel(jid)

    async def cancel(self, jid):
        if jid not in self._jobs:
            raise BidqException("Job does not exist")
        if self._jobs[jid].state is not None:
            raise BidqException("Job already done")
        await self._send(Message(type=MessageType.Cancel, id=jid))
        return self._handle_message(
            Message(type=MessageType.JobFailure, id=jid, reason="Client Timeout")
        )

    async def submit(self, topic, payload=None, timeout=0):
        jid = str(uuid.uuid4())
        await self._send(
            Message(type=MessageType.Submit, id=jid, topic=topic, payload=payload)
        )
        while True:
            msg = await self._q.get()
            if msg.is_a(MessageType.SubmitAck) and msg.clientId == jid:
                jid = msg.id
                self._jobs[jid] = JobState()
                if timeout != 0:
                    asyncio.create_task(self._set_timeout_for(jid, timeout))
                return jid

    async def get(self, jid):
        if jid in self._jobs:
            job = self._jobs[jid]
            result = job.state
            if job.state is None:
                result = await job.wait_for_value()
            success, value = result
            if not success:
                raise BidqException(value)
            return value
        raise BidqException(f"Job not found: {jid}")

    async def close(self):
        self.writer.close()
        self._task.cancel()
        await self.writer.wait_closed()

    def worker(self, topic=None):
        def outer(f):
            self._workers[topic] = f
            return f

        return outer

    def serve(self):
        return self._task

