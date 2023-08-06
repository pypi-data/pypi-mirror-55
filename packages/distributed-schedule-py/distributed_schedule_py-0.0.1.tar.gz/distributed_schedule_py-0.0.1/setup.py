from setuptools import setup, find_packages

setup(
    name='distributed_schedule_py',
    version='0.0.1',
    description='This is a distributed_schedule system',   # 简单描述
    author='xiaowuzidaxia',  # 作者
    author_email='609310949@qq.com',  # 作者邮箱
    # packages=['distributed_schedule'],                 # 包
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'taskserver=distributed_schedule.server:server_run',
            'taskclient=distributed_schedule.client:main',
        ],
    },
    install_requires=[
        'click==7.0',
    ],
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Topic :: Software Development',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
    ]
)