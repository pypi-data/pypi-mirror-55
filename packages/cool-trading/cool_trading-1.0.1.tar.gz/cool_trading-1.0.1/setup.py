# coding:utf-8

from setuptools import Extension, find_packages, setup
# or
# from distutils.core import setup  

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name='cool_trading',     # 包名字
        version='1.0.1',           # 包版本
        author="ipqhjjybj",
        author_email='250657661@qq.com',  # 作者邮箱
        license="AGPL v3",
        url='https://www.8btc.com/',      # 包的主页
        description='One trading system ',   # 简单描述
        long_description=long_description,
        include_package_data=True,
        #packages=['cool_trading'],
        packages=find_packages(exclude=["test"]),                 # 包
        install_requires=[
            'redis>=2.10.5',
            'pika>=1.1.0',
        ],
        classifiers = [
            # 发展时期,常见的如下
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',

            # 开发的目标用户
            'Intended Audience :: Developers',

            # 属于什么类型
            'Topic :: Software Development :: Build Tools',

            # 许可证信息
            'License :: OSI Approved :: MIT License',

            # 目标 Python 版本
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
        ]
)
