from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as file:
	long_description = file.read()

link = 'https://github.com/alx0rr/kyodo/archive/refs/heads/main.zip'
ver = '0.9.3.5'

setup(
	name = "kyodo",
	version = ver,
	url = "https://github.com/alx0rr/kyodo",
	download_url = link,
	license = "MIT",
	author = "alx0rr",
	author_email = "anon.mail.al@proton.me",
	description = "Library for creating kyodo bots and scripts.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	keywords = [
		"kyodo.py",
		"kyodo",
		"kyodo-py",
		"kyodo-bot",
		"api",
		"python",
		"python3",
		"python3.x",
		"alx0rr",
		"official",
		"async",
	],
	install_requires = [
		"logging",
		"colorama",
		"aiohttp",
		"pyjwt",
		"aiofiles",
		"orjson"
	],
	packages = find_packages()
)