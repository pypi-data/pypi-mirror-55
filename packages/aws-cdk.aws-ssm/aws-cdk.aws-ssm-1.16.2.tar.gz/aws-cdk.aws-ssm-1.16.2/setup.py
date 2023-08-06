import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-ssm",
    "version": "1.16.2",
    "description": "The CDK Construct Library for AWS::SSM",
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
        "aws_cdk.aws_ssm",
        "aws_cdk.aws_ssm._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_ssm._jsii": [
            "aws-ssm@1.16.2.jsii.tgz"
        ],
        "aws_cdk.aws_ssm": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.20.4",
        "publication>=0.0.3",
        "aws-cdk.aws-iam~=1.16,>=1.16.2",
        "aws-cdk.aws-kms~=1.16,>=1.16.2",
        "aws-cdk.core~=1.16,>=1.16.2",
        "aws-cdk.cx-api~=1.16,>=1.16.2"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
