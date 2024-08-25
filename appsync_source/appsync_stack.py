from aws_cdk import (
    Stack,
    aws_appsync as appsync,
    aws_iam,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_ssm as ssm,
)
from constructs import Construct


class AppSyncApiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stack = Stack.of(self)

        api = appsync.GraphqlApi(
            self,
            "ExampleAPI",
            name="ExampleAPI",
            definition=appsync.Definition.from_file("appsync_source/schema.graphql"),
        )

        rds_secret = rds.Credentials.from_generated_secret(username="clusteradmin")

        vpc = ec2.Vpc(self, "AuroraVpc")

        rds_cluster = rds.ServerlessCluster(
            self,
            "AuroraCluster",
            engine=rds.DatabaseClusterEngine.AURORA_MYSQL,
            vpc=vpc,
            credentials=rds_secret,
            cluster_identifier="db-endpoint-test2",
            default_database_name="demos",
            enable_data_api=True,
        )

        api.add_rds_data_source(
            "rds-datasource",
            rds_cluster,
            secret_store=rds_cluster.secret,
        )

        merged_api = appsync.GraphqlApi.from_graphql_api_attributes(
            self,
            "merged_api",
            graphql_api_id=ssm.StringParameter.value_from_lookup(
                self, "/appsync/merged-api-id"
            ),
        )


        merged_api_role = aws_iam.Role.from_role_name(
            self,
            "merged_api_role",
            role_name=ssm.StringParameter.value_from_lookup(self, "/appsync/merged-api-role-name"),
        )


        association = appsync.SourceApiAssociation(
            self,
            "ApiAssociation",
            source_api=api,
            merged_api=merged_api,
            merge_type=appsync.MergeType.AUTO_MERGE,
            merged_api_execution_role=merged_api_role,
        )
