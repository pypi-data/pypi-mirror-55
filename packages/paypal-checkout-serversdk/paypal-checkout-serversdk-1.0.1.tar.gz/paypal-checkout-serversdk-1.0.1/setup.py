from setuptools import setup, find_packages;

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setup(
    name="paypal-checkout-serversdk",
    version="1.0.1",
    author="https://developer.paypal.com",
    author_email="dl-paypal-checkout-api@paypal.com",
    description="Python Rest SDK for PayPal Checkout",
    long_description="Python Rest SDK for PayPal Checkout",
    long_description_content_type="text/markdown",
    url="https://github.com/paypal/Checkout-Python-SDK/",
    packages=find_packages(exclude=["tests","sample"]),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["paypalhttp"],
)
