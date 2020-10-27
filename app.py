#!/usr/bin/env python3

from aws_cdk import core
from common import Environment, Common
from turma_2_data_platform.turma_2_data_platform_stack import DataLake
from turma_2_data_platform.ingestion import RawIngestion
import os

environment = Environment[os.environ['ENVIRONMENT']]

app = core.App()
common = Common(app, environment=environment)
data_lake = DataLake(app, environment=environment)
raw_ingestion = RawIngestion(app, data_lake=data_lake, common=common)
app.synth()
