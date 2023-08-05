# -*- coding: utf-8 -*-

"""Console script for mlbench_cli."""
from mlbench_core.api import ApiClient

import click
from kubernetes import client, config
import os
import sys



BENCHMARK_IMAGES = ['pytorch-cifar10-resnet-scaling', 'tensorflow-cifar10-resnet']


@click.group()
def cli(args=None):
    """Console script for mlbench_cli."""
    return 0


@cli.command()
@click.argument('benchmark', type=click.Choice(BENCHMARK_IMAGES))
@click.argument('name', type=str)
@click.argument('num_workers', nargs=-1, type=int)
@click.option('--dashboard-url', '--u', default=None, type=str)
def run(benchmark, name, num_workers, dashboard_url):
    client = ApiClient(in_cluster=False, url=dashboard_url)

    print(client.endpoint)



if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
