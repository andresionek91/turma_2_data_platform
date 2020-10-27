#!/usr/bin/env python3

from aws_cdk import core

from turma_2_data_platform.turma_2_data_platform_stack import Turma2DataPlatformStack


app = core.App()
Turma2DataPlatformStack(app, "turma-2-data-platform")

app.synth()
