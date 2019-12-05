import time
import json
import random
import pytest
from datetime import datetime, timezone

from aiohttp import ClientSession


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S%z")


async def delete_record(record):
    custodian_url = "http://127.0.0.1:8080/custodian/data/tbl/"
    async with ClientSession() as session:
        response = await session.delete(custodian_url + str(record["id"]))
        if response.status != 200:
            assert False, f"{response.status}: record not deleted"


async def check(index, word, count, record):
    search_url = "http://127.0.0.1:8000/search/?index={index}&match={match}"
    async with ClientSession() as session:
        url = search_url.format(index=index, match=word)
        response = await session.get(url)
        if response.status != 200:
            await delete_record(record)
            assert False, f"{response.status}: {index} search error"

        data = await response.json()

    if len(data["matches"]) != count:
        await delete_record(record)
        assert len(data["matches"]) == count, f"{index} search {word} fail."


@pytest.mark.asyncio
async def test_rt_index(big_text):
    custodian_url = "http://127.0.0.1:8080/custodian/data/tbl/"
    # Create record
    async with ClientSession() as session:
        response = await session.post(custodian_url, json={"text": big_text})
        if response.status != 200:
            assert False, f"{response.status}: record not created"

        data = await response.json()

    record = data["data"]
    search_word = "understanding"
    new_search_word = search_word[::-1]
    new_text = big_text.replace(search_word, new_search_word)
    index = "tbl_index"
    rt_index = f"rt_{index}"
    # Check record in distributed index
    await check(index, search_word, 1, record)
    # Check record in rt index
    await check(rt_index, search_word, 1, record)

    # Update record
    async with ClientSession() as session:
        response = await session.patch(
            custodian_url + str(record["id"]),
            json={"text": new_text, "edited": now()},
        )
        if response.status != 200:
            await delete_record(record)
            assert False, f"{response.status}: record not updated"

    # Check previous record not in distributed index
    await check(index, search_word, 0, record)
    await check(index, new_search_word, 1, record)
    # Check previous record not in rt index
    await check(rt_index, search_word, 0, record)
    await check(rt_index, new_search_word, 1, record)

    # Delete record
    await delete_record(record)

    # Check record not in distributed index
    await check(index, new_search_word, 0, record)
    # Check record not in rt index
    await check(rt_index, new_search_word, 0, record)
