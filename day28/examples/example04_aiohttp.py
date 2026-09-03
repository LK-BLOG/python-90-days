"""示例4：aiohttp 异步 HTTP"""
import asyncio

try:
    import aiohttp
    
    async def fetch_url(session, url):
        """获取单个 URL"""
        async with session.get(url) as response:
            return response.status, await response.text()
    
    async def main():
        urls = [
            "https://httpbin.org/get",
            "https://httpbin.org/ip",
            "https://httpbin.org/user-agent",
        ]
        
        async with aiohttp.ClientSession() as session:
            # 并发请求
            tasks = [fetch_url(session, url) for url in urls]
            results = await asyncio.gather(*tasks)
            
            for url, (status, data) in zip(urls, results):
                print(f"{url}: {status}")
    
    if __name__ == "__main__":
        asyncio.run(main())

except ImportError:
    print("aiohttp 未安装，跳过此示例")
    print("安装命令: pip install aiohttp")
