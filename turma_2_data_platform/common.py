from enum import Enum

from aws_cdk import core
from aws_cdk import (
    aws_rds as rds,
    aws_ec2 as ec2
)


class Environment(Enum):
    PRODUCTION = 'production'
    STAGING = 'staging'
    DEV = 'dev'
