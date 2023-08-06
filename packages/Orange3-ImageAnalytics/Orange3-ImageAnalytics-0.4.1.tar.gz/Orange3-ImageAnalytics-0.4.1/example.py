import asyncio
import pickle

import httpx


class SendRequests:
    num_parallel_requests = 0
    MAX_PARALLEL = 100

    async def embedd_batch(self):
        requests = []
        async with httpx.AsyncClient(
                timeout=httpx.TimeoutConfig(timeout=60),
                base_url="https://api.garaza.io/") as client:
            for i in range(1000):
                requests.append(self._send_to_server(client))

            embeddings = await asyncio.gather(*requests)

        return embeddings

    async def __wait_until_released(self):
        while self.num_parallel_requests >= self.MAX_PARALLEL:
            await asyncio.sleep(0.1)

    async def _send_to_server(self, client):
        await self.__wait_until_released()

        self.num_parallel_requests += 1
        # simplified image loading
        with open("image.pkl", "rb") as f:
            im = pickle.load(f)
        # it just shows the part of the code for loading image from the cache
        # it is not required for the example but it is the reason why we made
        # a custom limitation of number of images - if image not in cache
        # send to server otherwise not
        # cache_key = self._cache.md5_hash(im)
        # emb = self._cache.get_cached_result_or_none(cache_key)
        # if emb is None:
            # gather responses
        url = "/image/inception-v3?machine=1&session=1&retry=0"
        emb = await self._send_request(client, im, url)
        self.num_parallel_requests -= 1
        return emb

    async def _send_request(self, client, image, url):
        headers = {'Content-Type': 'image/jpeg',
                   'Content-Length': str(len(image))}
        response = await client.post(url, headers=headers, data=image)
        print(response.content)
        return response


if __name__ == "__main__":
    cl = SendRequests()
    asyncio.get_event_loop().run_until_complete(cl.embedd_batch())
