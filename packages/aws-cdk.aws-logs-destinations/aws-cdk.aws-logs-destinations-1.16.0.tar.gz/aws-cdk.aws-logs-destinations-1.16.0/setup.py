import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-logs-destinations",
    "version": "1.16.0",
    "description": "Log Destinations for AWS CloudWatch Logs",
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
        "aws_cdk.aws_logs_destinations",
        "aws_cdk.aws_logs_destinations._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_logs_destinations._jsii": [
            "aws-logs-destinations@1.16.0.jsii.tgz"
        ],
        "aws_cdk.aws_logs_destinations": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.20.2",
        "publication>=0.0.3",
        "aws-cdk.aws-iam~=1.16,>=1.16.0",
        "aws-cdk.aws-kinesis~=1.16,>=1.16.0",
        "aws-cdk.aws-lambda~=1.16,>=1.16.0",
        "aws-cdk.aws-logs~=1.16,>=1.16.0",
        "aws-cdk.core~=1.16,>=1.16.0"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
