from setuptools import setup, find_packages

req_tests = ["pytest"]
req_lint = ["flake8", "flake8-docstrings"]
req_dev = req_tests + req_lint

with open('requirements.txt', 'r') as f:
    install_requires = [
        s for s in [
            line.split('#', 1)[0].strip(' \t\n') for line in f
        ] if s != ''
    ]

setup_options = {
    "name": "yirgachefe",
    "version": "0.1.0",
    "description": "Convenience of configuration and logging.",
    "package_data": {"yirgachefe": ["logger_.pyi"]},
    "packages": find_packages(),
    "python_requires": ">=3.7.3",
    "install_requires": install_requires,
    "extras_require": {
        "tests": req_tests,
        "lint": req_lint,
        "dev": req_dev
    },
    "package_dir": {"": "."},
}

setup(**setup_options)
