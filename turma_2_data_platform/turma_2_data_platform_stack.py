from aws_cdk import core
from aws_cdk import (
    aws_s3 as s3,
    aws_glue as glue,
    aws_iam as iam,
    aws_athena as athena
)
from data_lake_core import Layer, S3Defaults
from common import Environment


class DataLakeBucket(s3.Bucket):

    def __init__(self, scope: core.Construct, environment: Environment, layer: Layer, **kwargs):
        name = f's3-belisco-{environment.value}-data-lake-{layer.value}'
        self.environment = environment
        self.layer = layer

        super().__init__(
            scope,
            name,
            bucket_name=name,
            removal_policy=core.RemovalPolicy.DESTROY,
            block_public_access=S3Defaults.block_public_access(),
            encryption=S3Defaults.encryption(),
            versioned=True,
            **kwargs
        )

        S3Defaults.lifecycle_rules(self)


class DataLakeDatabase(glue.Database):

    def __init__(self, scope: core.Construct, bucket: DataLakeBucket, **kwargs) -> None:
        name = f'glue-belisco-{bucket.environment.value}-data-lake-{bucket.layer.value}'

        super().__init__(
            scope,
            name,
            database_name=name,
            location_uri=f's3://{bucket.bucket_name}'
        )


class DataLake(core.Stack):

    def __init__(self, scope: core.Construct, environment: Environment, **kwargs) -> None:
        self.env = environment
        super().__init__(scope, id=f'{self.env.value}-data-lake', **kwargs)

        self.data_lake_raw_bucket, self.data_lake_raw_database = self.get_data_lake_raw()
        self.data_lake_processed_bucket, self.data_lake_processed_database = self.get_data_lake_processed()
        self.data_lake_curated_bucket, self.data_lake_curated_database = self.get_data_lake_curated()


    def get_data_lake_raw(self):
        bucket = DataLakeBucket(
            self,
            environment=self.env,
            layer=Layer.RAW
        )

        bucket.add_lifecycle_rule(
            transitions=[
                s3.Transition(
                    storage_class=s3.StorageClass.INTELLIGENT_TIERING,
                    transition_after=core.Duration.days(90)
                ),
                s3.Transition(
                    storage_class=s3.StorageClass.GLACIER,
                    transition_after=core.Duration.days(360)
                )
            ],
            enabled=True)

        database = DataLakeDatabase(self, bucket=bucket)

        return bucket, database

    def get_data_lake_processed(self):
        bucket = DataLakeBucket(
            self,
            environment=self.env,
            layer=Layer.PROCESSED
        )

        database = DataLakeDatabase(self, bucket=bucket)

        return bucket, database

    def get_data_lake_curated(self):
        bucket = DataLakeBucket(
            self,
            environment=self.env,
            layer=Layer.CURATED
        )

        database = DataLakeDatabase(self, bucket=bucket)

        return bucket, database

