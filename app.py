#!/usr/bin/env python3
import os

import aws_cdk as cdk
from appsync_source.appsync_stack import AppSyncApiStack
from appsync_merged.appsync_merged_stack import MergedAppSyncApiStack


app = cdk.App()

env = cdk.Environment(
    account=os.getenv("CDK_ACCOUNT"),
    region="us-east-1",
)


AppSyncApiStack(app, "AppSyncApiStack", env=env)

MergedAppSyncApiStack(app, "MergedAppSyncApiStack", env=env)

app.synth()
