import time
import os
import json
import random
import pytest
from datetime import datetime, timezone

from aiohttp import ClientSession


@pytest.fixture
def custodian_url():
    return os.environ.get(
        "CUSTODIAN_URL", "http://127.0.0.1:8080/custodian/data/tbl/"
    )


@pytest.fixture
def search_url():
    return os.environ.get(
        "SEARCH_URL",
        "http://127.0.0.1:8000/?index={index}&match=eq(text,{match})",
    )


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S%z")


async def delete_record(url, record):
    async with ClientSession() as session:
        response = await session.delete(url + str(record["id"]))
        if response.status != 200:
            assert False, f"{response.status}: record not deleted"


async def check(search_url, index, word, count, custodian_url, record):
    async with ClientSession() as session:
        url = search_url.format(index=index, match=word)
        response = await session.get(url)
        if response.status != 200:
            await delete_record(custodian_url, record)
            assert False, f"{response.status}: {index} search error"

        data = await response.json()

    if len(data["matches"]) != count:
        await delete_record(custodian_url, record)
        assert len(data["matches"]) == count, f"{index} search {word} fail."


@pytest.mark.asyncio
async def test_rt_index(big_text, search_url, custodian_url):
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
    await check(search_url, index, search_word, 1, custodian_url, record)
    # Check record in rt index
    await check(search_url, rt_index, search_word, 1, custodian_url, record)

    # Update record
    async with ClientSession() as session:
        response = await session.patch(
            custodian_url + str(record["id"]),
            json={"text": new_text, "edited": now()},
        )
        if response.status != 200:
            await delete_record(custodian_url, record)
            assert False, f"{response.status}: record not updated"

    # Check previous record not in distributed index
    await check(search_url, index, search_word, 0, custodian_url, record)
    await check(search_url, index, new_search_word, 1, custodian_url, record)
    # Check previous record not in rt index
    await check(search_url, rt_index, search_word, 0, custodian_url, record)
    await check(
        search_url, rt_index, new_search_word, 1, custodian_url, record
    )

    # Delete record
    await delete_record(custodian_url, record)

    # Check record not in distributed index
    await check(search_url, index, new_search_word, 0, custodian_url, record)
    # Check record not in rt index
    await check(
        search_url, rt_index, new_search_word, 0, custodian_url, record
    )
