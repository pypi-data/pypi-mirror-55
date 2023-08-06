import setuptools


setuptools.setup(
    name="hypersRedisCluster", 
    version="0.0.1",
    author="yingzhe.zhang",
    author_email="yingzhe.zhang@mail.hypers.com",
    description="support redis cluster",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["redis-py-cluster", "django-redis"],
    zip_safe=False
)
