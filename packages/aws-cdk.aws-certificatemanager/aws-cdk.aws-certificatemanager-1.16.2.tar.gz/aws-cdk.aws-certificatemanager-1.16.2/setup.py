import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-certificatemanager",
    "version": "1.16.2",
    "description": "The CDK Construct Library for AWS::CertificateManager",
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
        "aws_cdk.aws_certificatemanager",
        "aws_cdk.aws_certificatemanager._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_certificatemanager._jsii": [
            "aws-certificatemanager@1.16.2.jsii.tgz"
        ],
        "aws_cdk.aws_certificatemanager": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.20.4",
        "publication>=0.0.3",
        "aws-cdk.aws-cloudformation~=1.16,>=1.16.2",
        "aws-cdk.aws-iam~=1.16,>=1.16.2",
        "aws-cdk.aws-lambda~=1.16,>=1.16.2",
        "aws-cdk.aws-route53~=1.16,>=1.16.2",
        "aws-cdk.core~=1.16,>=1.16.2"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
