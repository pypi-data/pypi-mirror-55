import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-stepfunctions-tasks",
    "version": "1.16.2",
    "description": "Task integrations for AWS StepFunctions",
    "url": "https://github.com/aws/aws-cdk",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "project_urls": {
        "Source": "https://github.com/aws/aws-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.aws_stepfunctions_tasks",
        "aws_cdk.aws_stepfunctions_tasks._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_stepfunctions_tasks._jsii": [
            "aws-stepfunctions-tasks@1.16.2.jsii.tgz"
        ],
        "aws_cdk.aws_stepfunctions_tasks": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.20.4",
        "publication>=0.0.3",
        "aws-cdk.assets~=1.16,>=1.16.2",
        "aws-cdk.aws-cloudwatch~=1.16,>=1.16.2",
        "aws-cdk.aws-ec2~=1.16,>=1.16.2",
        "aws-cdk.aws-ecr~=1.16,>=1.16.2",
        "aws-cdk.aws-ecr-assets~=1.16,>=1.16.2",
        "aws-cdk.aws-ecs~=1.16,>=1.16.2",
        "aws-cdk.aws-iam~=1.16,>=1.16.2",
        "aws-cdk.aws-kms~=1.16,>=1.16.2",
        "aws-cdk.aws-lambda~=1.16,>=1.16.2",
        "aws-cdk.aws-s3~=1.16,>=1.16.2",
        "aws-cdk.aws-sns~=1.16,>=1.16.2",
        "aws-cdk.aws-sqs~=1.16,>=1.16.2",
        "aws-cdk.aws-stepfunctions~=1.16,>=1.16.2",
        "aws-cdk.core~=1.16,>=1.16.2"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
