from fastapi import FastAPI, Response, status
import asyncio
import aiohttp

app = FastAPI()


async def get(
    session: aiohttp.ClientSession,
    service: str,
    url: str,
    **kwargs,
) -> bool:
    try:
        resp = await session.request('GET', url=url, **kwargs)
        data = await resp.text()
        if resp.status != 200:
            print(f"{service}@{url} [HTTP {resp.status}]: {data}")
            return False
    except Exception as e:
        print(f"{service}@{url} [Error]: {e}")
        return False

    return True


@app.get("/healthz", status_code=200)
async def healthz(response: Response):
    async with aiohttp.ClientSession() as session:
        tasks = [
            get(session, "localstack",
                "http://localhost:4566/_localstack/health", timeout=2),
            get(session, "proxy",
                "http://localhost:8080/_proxy/health", timeout=2)
        ]

        statuses = await asyncio.gather(*tasks, return_exceptions=False)

        success = all(statuses)
        if not success:
            response.status_code = 503

        return success