from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    CfnOutput,
    aws_iam as iam
)
from constructs import Construct

class HelloCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        existing_role = iam.Role.from_role_arn(
            self, "ExistingRole",
            "arn:aws:iam::891377180652:role/nuv-test-LambdaS3ExecutionRole"
        )

        my_function = _lambda.Function(
            self, "HelloWorldFunction",
            runtime = _lambda.Runtime.NODEJS_20_X,
            handler = "index.handler",
            role = existing_role,
            code = _lambda.Code.from_inline(
                """
                exports.handler = async function(event) {
                    return {
                        statusCode: 200,
                        body: JSON.stringify('Hello CDK!'),
                    };
                };
                """
            ),
        )

        my_function_url = my_function.add_function_url(
            auth_type = _lambda.FunctionUrlAuthType.NONE,
        )

        CfnOutput(self, "myFunctionUrlOutput", value=my_function_url.url)
