"""
Defines a basic CLI for exposing Searcher
"""
import json
import logging

import fire

# pylint: disable=import-error
from searcher import Searcher

# pylint: disable=too-many-arguments, bad-continuation
def main(
    email,
    api_key=None,
    query=None,
    mongo_url=None,
    download_all=False,
    limit=None,
    **kwargs,
):
    """
    Given an e-mail and API key, searches for Human RNA and outputs the result
    """
    logging.basicConfig(level=logging.INFO)
    searcher = Searcher(email, api_key=api_key, mongo_url=mongo_url)

    if query and query != "human":
        searcher.search(query, limit=limit, **kwargs)
    else:
        logging.info("No query supplied, searching for Human RNA")
        searcher.search_human_rna(limit=limit)

    if download_all:
        assert searcher.cached, "Searcher is not cached."

        logging.info(f"Found {len(searcher)} results")
        logging.info("Downloading all results")
        searcher.download_all()
    else:
        for result in searcher:
            print(json.dumps(result, indent=4, sort_keys=True))


if __name__ == "__main__":
    fire.Fire(main)
