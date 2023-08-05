import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
	name="inclusive",
	version="0.0.2",
	author="RA",
	author_email="numpde@null.net",
	keywords="development range slice",
	description="Inclusive range and slice",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/numpde/inclusive",
	packages=setuptools.find_packages(),
	classifiers=[
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
	install_requires=[],

	test_suite="nose.collector",
	tests_require=["nose"],
)
