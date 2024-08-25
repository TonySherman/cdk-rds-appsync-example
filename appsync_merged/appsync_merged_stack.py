from aws_cdk import Stack, aws_appsync as appsync, aws_iam as iam, aws_ssm as ssm
from constructs import Construct


class MergedAppSyncApiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        appsync_role = iam.Role(
            self,
            "RootGraphApiRole",
            assumed_by=iam.ServicePrincipal("appsync.amazonaws.com"),
        )

        appsync_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "appsync:SourceGraphQL",
                    "appsync:StartSchemaMerge",
                    "lambda:InvokeFunction",
                ],
                resources=["*"],
            )
        )

        merged_api = appsync.GraphqlApi(
            self,
            construct_id,
            name="merged-graph-api",
            definition=appsync.Definition.from_source_apis(
                source_apis=[], merged_api_execution_role=appsync_role
            ),
        )

        ssm.StringParameter(
            self,
            "SSMRootGraphRoleName",
            parameter_name="/appsync/merged-api-role-name",
            string_value=appsync_role.role_name,
        )

        ssm.StringParameter(
            self,
            "SSMRootGraphID",
            parameter_name="/appsync/merged-api-id",
            string_value=merged_api.api_id,
        )
