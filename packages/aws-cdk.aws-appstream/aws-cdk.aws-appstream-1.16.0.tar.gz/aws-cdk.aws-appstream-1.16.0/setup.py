import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-appstream",
    "version": "1.16.0",
    "description": "The CDK Construct Library for AWS::AppStream",
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
        "aws_cdk.aws_appstream",
        "aws_cdk.aws_appstream._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_appstream._jsii": [
            "aws-appstream@1.16.0.jsii.tgz"
        ],
        "aws_cdk.aws_appstream": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.20.2",
        "publication>=0.0.3",
        "aws-cdk.core~=1.16,>=1.16.0"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
