import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd

from .samples import ALL_SAMPLES

# Simple configs
RATE_LIMIT = 2 # requests per s
EXCLUDE_CRITERIA = ['#', '<strong>', 'ID']
BASE_URL = "https://www.ncbi.nlm.nih.gov/"
SAMPLE_BASE_URL = "geo/query/acc.cgi?acc="

# Semaphore for rate limiting
semaphore = asyncio.Semaphore(RATE_LIMIT)


def should_include_line(line):
    return line and not any(line.startswith(criterion) for criterion in EXCLUDE_CRITERIA)


async def fetch(session, url):
    async with semaphore:
        async with session.get(url) as response:
            return await response.text()
    

async def async_samples_iter(samples):
    for sample in samples:
        yield sample


async def extract_tissue_full_table_link(session, url):
    html_content = await fetch(session, url)
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the input tag with the onclick attribute
    input_tag = soup.find('input', {'name': 'fulltable'})

    if input_tag:
        onclick_value = input_tag.get('onclick')

        # Extract the URL from the onclick value
        start = onclick_value.find("'") + 1
        end = onclick_value.find("'", start)
        url = onclick_value[start:end]
        print(url)

        return url
    else:
        return "Link not found"


async def parse_full_table(session, url, sample):
    html_content = await fetch(session, url)
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract text within <pre> tag
    pre_content = soup.find('pre').get_text()

    # Split the content into lines and parse each line
    lines = pre_content.split('\n')
    parsed_data = parsed_data = [line.split('\t') for line in lines if should_include_line(line)]

    # Create DataFrame
    df = pd.DataFrame(parsed_data, columns=['ID_REF', 'VALUE'])
    df['VALUE'] = pd.to_numeric(df['VALUE'], errors='coerce')
    df['TISSUE_SAMPLE'] = sample

    # Drop nans values
    mask_notna = df['VALUE'].notna()
    df = df[mask_notna]
    print(f"Saving data {sample}")
    df.to_parquet(f"./data/tissue_sample_{sample}.parquet", index=True)

    return df


async def parse_samples(samples):
    print(f"Begin parsing.\n# of samples: {len(samples)}")
    async with aiohttp.ClientSession() as session:
        tasks = []
        async for sample in async_samples_iter(samples):
            url_tissue = f"{BASE_URL}{SAMPLE_BASE_URL}{sample}"
            print(f"Tissue sample url: {url_tissue}")

            full_table_path = await extract_tissue_full_table_link(session, url_tissue)
            url_full_table = f"{BASE_URL}{full_table_path}"

            print(f"Parsing: {url_full_table}")
            if full_table_path != "Link not found":
                task = parse_full_table(session, url_full_table, sample)
                tasks.append(task)

        dataframes = await asyncio.gather(*tasks)

        if dataframes:
            combined_df = pd.concat(dataframes, ignore_index=True)
            return combined_df
        else:
            print("No dataframes to concatenate")
            return pd.DataFrame()


def main():
    samples_ = list(ALL_SAMPLES.keys())
    df = asyncio.run(parse_samples(samples_[160::]))
    df.to_parquet("./data/tissue_samples.parquet", index=False)


if __name__ == "__main__":
    main()
