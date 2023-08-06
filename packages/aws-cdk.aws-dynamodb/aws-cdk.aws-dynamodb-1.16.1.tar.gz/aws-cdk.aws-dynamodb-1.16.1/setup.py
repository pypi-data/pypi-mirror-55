import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-dynamodb",
    "version": "1.16.1",
    "description": "CDK Constructs for AWS DynamoDB",
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
        "aws_cdk.aws_dynamodb",
        "aws_cdk.aws_dynamodb._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_dynamodb._jsii": [
            "aws-dynamodb@1.16.1.jsii.tgz"
        ],
        "aws_cdk.aws_dynamodb": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.20.3",
        "publication>=0.0.3",
        "aws-cdk.aws-applicationautoscaling~=1.16,>=1.16.1",
        "aws-cdk.aws-iam~=1.16,>=1.16.1",
        "aws-cdk.core~=1.16,>=1.16.1"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
