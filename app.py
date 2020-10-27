#!/usr/bin/env python3

from aws_cdk import core
from common import Environment, Common
from turma_2_data_platform.turma_2_data_platform_stack import DataLake
import os

environment = Environment[os.environ['ENVIRONMENT']]

app = core.App()
common = Common(app, environment=environment)
DataLake(app, environment=environment)
app.synth()
