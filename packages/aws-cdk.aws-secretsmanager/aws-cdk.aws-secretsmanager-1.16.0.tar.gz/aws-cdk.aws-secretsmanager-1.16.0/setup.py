import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-secretsmanager",
    "version": "1.16.0",
    "description": "The CDK Construct Library for AWS::SecretsManager",
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
        "aws_cdk.aws_secretsmanager",
        "aws_cdk.aws_secretsmanager._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_secretsmanager._jsii": [
            "aws-secretsmanager@1.16.0.jsii.tgz"
        ],
        "aws_cdk.aws_secretsmanager": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.20.2",
        "publication>=0.0.3",
        "aws-cdk.aws-ec2~=1.16,>=1.16.0",
        "aws-cdk.aws-iam~=1.16,>=1.16.0",
        "aws-cdk.aws-kms~=1.16,>=1.16.0",
        "aws-cdk.aws-lambda~=1.16,>=1.16.0",
        "aws-cdk.core~=1.16,>=1.16.0"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
