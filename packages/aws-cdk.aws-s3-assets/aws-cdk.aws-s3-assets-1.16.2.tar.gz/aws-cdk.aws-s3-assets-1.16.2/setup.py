import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-s3-assets",
    "version": "1.16.2",
    "description": "Deploy local files and directories to S3",
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
        "aws_cdk.aws_s3_assets",
        "aws_cdk.aws_s3_assets._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_s3_assets._jsii": [
            "aws-s3-assets@1.16.2.jsii.tgz"
        ],
        "aws_cdk.aws_s3_assets": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.20.4",
        "publication>=0.0.3",
        "aws-cdk.assets~=1.16,>=1.16.2",
        "aws-cdk.aws-iam~=1.16,>=1.16.2",
        "aws-cdk.aws-s3~=1.16,>=1.16.2",
        "aws-cdk.core~=1.16,>=1.16.2",
        "aws-cdk.cx-api~=1.16,>=1.16.2"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
