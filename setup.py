from setuptools import setup, find_packages

setup(
	name             = 'MCServer Tools',
	version          = '1.0.0.0',
	description      = 'Minecraft Server tools for vanilla and Forge modded servers.',
	author           = 'Cadyyan',
	url              = 'https://github.com/cadyyan/mcserver-tools',
	packages         = find_packages(),
	scripts          = ['bin/mcserver'],
	install_requires = [
		'daemon',
		'PyBullet',
		'tmuxp',
	],
)

