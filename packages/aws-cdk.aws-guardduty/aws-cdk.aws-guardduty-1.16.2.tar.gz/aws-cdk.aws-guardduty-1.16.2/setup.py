import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-guardduty",
    "version": "1.16.2",
    "description": "The CDK Construct Library for AWS::GuardDuty",
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
        "aws_cdk.aws_guardduty",
        "aws_cdk.aws_guardduty._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_guardduty._jsii": [
            "aws-guardduty@1.16.2.jsii.tgz"
        ],
        "aws_cdk.aws_guardduty": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.20.4",
        "publication>=0.0.3",
        "aws-cdk.core~=1.16,>=1.16.2"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
