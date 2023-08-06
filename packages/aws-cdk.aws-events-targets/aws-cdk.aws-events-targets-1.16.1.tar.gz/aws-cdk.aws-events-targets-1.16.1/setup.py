import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-events-targets",
    "version": "1.16.1",
    "description": "Event targets for AWS CloudWatch Events",
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
        "aws_cdk.aws_events_targets",
        "aws_cdk.aws_events_targets._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_events_targets._jsii": [
            "aws-events-targets@1.16.1.jsii.tgz"
        ],
        "aws_cdk.aws_events_targets": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.20.3",
        "publication>=0.0.3",
        "aws-cdk.aws-cloudformation~=1.16,>=1.16.1",
        "aws-cdk.aws-codebuild~=1.16,>=1.16.1",
        "aws-cdk.aws-codepipeline~=1.16,>=1.16.1",
        "aws-cdk.aws-ec2~=1.16,>=1.16.1",
        "aws-cdk.aws-ecs~=1.16,>=1.16.1",
        "aws-cdk.aws-events~=1.16,>=1.16.1",
        "aws-cdk.aws-iam~=1.16,>=1.16.1",
        "aws-cdk.aws-lambda~=1.16,>=1.16.1",
        "aws-cdk.aws-sns~=1.16,>=1.16.1",
        "aws-cdk.aws-sns-subscriptions~=1.16,>=1.16.1",
        "aws-cdk.aws-sqs~=1.16,>=1.16.1",
        "aws-cdk.aws-stepfunctions~=1.16,>=1.16.1",
        "aws-cdk.core~=1.16,>=1.16.1"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
