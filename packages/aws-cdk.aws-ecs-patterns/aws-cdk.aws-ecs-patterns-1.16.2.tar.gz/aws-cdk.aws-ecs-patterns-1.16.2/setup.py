import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-ecs-patterns",
    "version": "1.16.2",
    "description": "CDK Constructs for AWS ECS",
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
        "aws_cdk.aws_ecs_patterns",
        "aws_cdk.aws_ecs_patterns._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_ecs_patterns._jsii": [
            "aws-ecs-patterns@1.16.2.jsii.tgz"
        ],
        "aws_cdk.aws_ecs_patterns": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.20.4",
        "publication>=0.0.3",
        "aws-cdk.aws-applicationautoscaling~=1.16,>=1.16.2",
        "aws-cdk.aws-certificatemanager~=1.16,>=1.16.2",
        "aws-cdk.aws-ec2~=1.16,>=1.16.2",
        "aws-cdk.aws-ecs~=1.16,>=1.16.2",
        "aws-cdk.aws-elasticloadbalancingv2~=1.16,>=1.16.2",
        "aws-cdk.aws-events~=1.16,>=1.16.2",
        "aws-cdk.aws-events-targets~=1.16,>=1.16.2",
        "aws-cdk.aws-iam~=1.16,>=1.16.2",
        "aws-cdk.aws-route53~=1.16,>=1.16.2",
        "aws-cdk.aws-route53-targets~=1.16,>=1.16.2",
        "aws-cdk.aws-servicediscovery~=1.16,>=1.16.2",
        "aws-cdk.aws-sqs~=1.16,>=1.16.2",
        "aws-cdk.core~=1.16,>=1.16.2"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
