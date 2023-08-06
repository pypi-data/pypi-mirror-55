"""Prophetess entry point"""

import os
import sys
import yaml
import logging
import asyncio
from pathlib import Path

from prophetess.pipeline import build_pipelines

log = logging.getLogger()


async def run():
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[logging.StreamHandler(sys.stdout)],
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    )

    here = Path(__file__).parent.parent

    with open(here / 'config' / 'pipeline.yaml') as f:
       cfg = yaml.safe_load(f.read())

    p = build_pipelines(cfg)

    for pipeline_name, pipeline in p.items():
       log.debug('>> Pipeline: {}'.format(pipeline_name))
       await pipeline.run()
