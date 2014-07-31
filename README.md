# MCServer Tools
Minecraft server administration tools

## Installation
This is a work inprogress since I haven't done anything to do installation yet...

## Usage
### Start Server
There are two methods to start the server. One is as a regular process the other is to launch the server as a daemon process. Both options require you to have an mcserver.settings file setup.

#### Normal
Simply use the following commmand:

	mcserver start --dir <dir>

The `--dir` option is only really needed if you aren't in the directory of the server already. This will start the server with whatever options are in the mcserver.settings file.

TODO: This documentation reflects the old method and needs to be updated

#### Daemon
To start the server as a daemon process (running in the background) you do the same as before but you add another option:

	mcserver start --dir <dir> --daemon

As before the `--dir` option is only needed if you are not in the server directory. The server will start in the background and the process ID will be written to server.pid in the server directory.

##### Launchers
TODO

## Settings File
You can store settings for running the server in the `mcserver.settings` file. One use for this file is storing the options that are used to start the server. The file is formatted as a JSON file. A sample can be found below:

	{
		"jvm": "java",
		"heap": "1G",
		"stack": "1G",
		"perm_gen": "32m",
		jar": "minecraft_server_1.7.2.jar",
		"extra_start_args": "nogui",
		"launcher": {
			"class": "mcserver.launchers.TmuxServerLauncher",
			"session_name": "minecraft",
			"window_name": "My Minecraft Server"
		}
	}

Everything in mcserver.settings is optional and if it is not specified a default value is given.
