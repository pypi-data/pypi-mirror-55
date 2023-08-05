# pybidq
Python SDK for bidq

# Usage
```python
import asyncio
from bidq import BidQ


async def setup_worker():
    client = await BidQ.create()

    @client.worker("add")
    def add(x, y):
        return x + y

    await client.serve()


async def send_job():
    client = await BidQ.create()
    jid = await client.submit("add", {"x": 1, "y": 2}, 0.2)
    try:
        print(await client.get(jid))
    except Exception as e:
        print(e)
    await client.close()


# asyncio.run(send_job())
asyncio.run(setup_worker())

```