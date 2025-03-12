import os
import sys
import psutil
import asyncio
import requests
from xml.etree import ElementTree
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import hashlib

# Define output directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs_agno")

def extract_urls_from_xml_file(xml_file_path: str) -> List[str]:
    """Extract URLs from local XML file"""
    try:
        with open(xml_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        root = ElementTree.fromstring(content)
        
        # Extract all URLs from the sitemap
        urls = []
        for url in root.findall('.//loc'):
            if url.text:  # Check if URL text exists
                urls.append(url.text.strip())
        
        return urls
    except Exception as e:
        print(f"Error reading XML file: {e}")
        return []

async def crawl_parallel(urls: List[str], max_concurrent: int = 3):
    print("\n=== Parallel Crawling with Browser Reuse + Memory Check ===")
    
    peak_memory = 0
    process = psutil.Process(os.getpid())

    def log_memory(prefix: str = ""):
        nonlocal peak_memory
        current_mem = process.memory_info().rss
        if current_mem > peak_memory:
            peak_memory = current_mem
        print(f"{prefix} Current Memory: {current_mem // (1024 * 1024)} MB, Peak: {peak_memory // (1024 * 1024)} MB")

    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
        extra_args=[
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-web-security",  # Add this
            "--ignore-certificate-errors",  # Add this
        ],
    )
    
    # Modified crawl config with markdown generator and correct wait_until value
    crawl_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        markdown_generator=DefaultMarkdownGenerator(),
        page_timeout=60000,  # 60 seconds
        wait_until="networkidle"  # Changed from "networkidle0" to "networkidle"
    )
    
    # Add delay between batches
    async def process_batch(batch, session_offset):
        tasks = []
        for j, url in enumerate(batch):
            session_id = f"parallel_session_{session_offset + j}"
            task = crawler.arun(url=url, config=crawl_config, session_id=session_id)
            tasks.append(task)
            await asyncio.sleep(0.5)  # Add small delay between requests
        return await asyncio.gather(*tasks, return_exceptions=True)

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    try:
        success_count = 0
        fail_count = 0
        
        for i in range(0, len(urls), max_concurrent):
            batch = urls[i : i + max_concurrent]
            
            log_memory(prefix=f"Before batch {i//max_concurrent + 1}: ")
            results = await process_batch(batch, i)
            log_memory(prefix=f"After batch {i//max_concurrent + 1}: ")
            
            for url, result in zip(batch, results):
                if isinstance(result, Exception):
                    print(f"Error crawling {url}: {result}")
                    fail_count += 1
                elif result.success:
                    success_count += 1
                    # Create subdirectories based on URL path
                    url_path = url.replace("https://docs.agno.com/", "").replace("/", "\\")
                    filename = f"{url_path}.md"
                    filepath = os.path.join(OUTPUT_DIR, filename)
                    
                    # Create subdirectories if they don't exist
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(result.markdown.raw_markdown)  # Changed from markdown_v2 to markdown
                    print(f"Successfully crawled and saved: {url} -> {filepath}")
                else:
                    fail_count += 1

        print(f"\nSummary:")
        print(f"  - Successfully crawled: {success_count}")
        print(f"  - Failed: {fail_count}")

    finally:
        print("\nClosing crawler...")
        await crawler.close()
        log_memory(prefix="Final: ")
        print(f"\nPeak memory usage (MB): {peak_memory // (1024 * 1024)}")

async def main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    xml_file_path = os.path.join(current_dir, "text.md")
    
    urls = extract_urls_from_xml_file(xml_file_path)
    
    if urls:
        print(f"Found {len(urls)} URLs to crawl")
        batch_size = int(input("Enter batch size for parallel crawling (default 10): ") or 10)
        await crawl_parallel(urls, max_concurrent=batch_size)
    else:
        print("No URLs found to crawl")

if __name__ == "__main__":
    asyncio.run(main())