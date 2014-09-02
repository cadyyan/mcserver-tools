# MCServer Tools
Minecraft server administration tools

## Installation
You can use pip or easy_install to install the tools. Alternatively you could check out the repo and then use it directly like that but that's only recommended if you are doing development on the project.

## Commandline Usage
### Start Server
There are two methods to start the server. One is as a regular process the other is to launch the server as a daemon process. Both options require you to have an mcserver.settings file setup.

#### Normal
Simply use the following commmand:

	mcserver start --dir <dir>

The `--dir` option is only really needed if you aren't in the directory of the server already. This will start the server with whatever options are in the mcserver.settings file.

#### Daemon
To start the server as a daemon process (running in the background) you do the same as before but you add another option:

	mcserver start --dir <dir> --daemon

As before the `--dir` option is only needed if you are not in the server directory. The server will start in the background and the process ID will be written to server.pid in the server directory.

##### Launchers
Launchers allow you to launch the server in daemon mode via different methods. The recommended launcher to use is the `mcserver.launchers.TmuxServerLauncher` launcher but other launchers area viable. There are some built-in launchers that you can use and all are configured by setting the `class` attribute of the `launcher` section in the settings file. All other values that are in the `launcher` section are passed to the launcher to configure other settings with the launcher.

###### TmuxServerLauncher
This launchs the server in a tmux session (this means its not really a daemon but those are just symantics). You can configure this to be the launcher by setting the `class` attribute of the `launcher` section to `mcserver.launchers.TmuxServerLauncher` and then setting the `session_name` and `window_name` attributes. Both attributes are required to use this launcher.

###### DaemonServerLauncher
This launchs the server in a background process (this is actually a daemon so get off my back). You can configure this to be the launcher by setting the `class` attribute of the `launcher` section to `mcserver.launchers.DaemonServerLauncher`. No other attributes are required.

##### Developer Notes
If you're going to be developing your own launcher you should extend the `mcserver.launchers.ServerLauncher` class. You'll need to implement a couple of abstract methods but the interface is very simple.

#### Notes
You can configure a certain mode to always happen by default. If you always want to run the server as a `daemon` you can set the daemon attribute in the settings file to true and by default the server will be launched in daemon mode. You can force it to do the opposite of the setting value by giving the `--daemon` or `--no-daemon` options on the commandline.

### Stop
Put simply, stops the server. Simple usage:

	mcserver stop --dir <dir>

If you didn't see the pattern yet, `--dir <dir>` is optional.

### Restart
A combination of stop and start commands. Usage is the same including the optional `--daemon` and `--no-daemon` options.

### Backup
Creates a tarball of the world file. The world directory is selected based off of the `level-name` property of the server configuration file. All backups have a timestamp in the file name. Backups are stored in a directory that can be specified in your `mcserver.settings` file using the `backup_dir` attribute. By default this value is set to `backups`. If the directory does not exist the directory is created. Backups can be safely done on a server that is currently running. If the server is running the `save-off` command is sent to the server to prevent further writing to disk. After the tarball is created the `save-on` command is sent to continue saving to disk. Usage looks like this:

	mcserver backup --dir <dir>

I'm not going to mention the optional thing again...

## Admin Interfaces
Admin interfaces are a way to notify server admins about changes in the server. For instance if the server is started you may want to email the server admins that the server was started. Same would apply with stopping or restarting. Configuration of an interface is very similar to configuration of a launcher. A sample config could look like this:

	admin_interfaces: [
		{
			"class": "mcserver.admin.nofitications.PushBulletNotification",
			"auth_type": "basic",
			"access_token": "my_secret_token"
		},
		{
			"class": "mcserver.admin.nofitications.PushBulletNotification",
			"auth_type": "oauth",
			"client_id": "my_client_id",
			"client_secret": "my_client_secrent",
			"access_token": "my_access_token",
		},
		{
			"class": "some.class",
			"key1": "value1",
			"key2": "value2",
		},
		{
			"class": "some.other.class",
		}
	]

You can have as many interfaces as you want and you can have a single class showing up more than once. All configurations are passed to the interface when it is constructed. When developing an interface make sure to not block.

### PushBullet
PushBullet support for notifications is supported via the `mcserver.admin.notifications.PushBulletNotification` class. Configuration is pretty simple. Set the class to the afformentioned class and you can either provide and access token to act as a user or you can provide OAuth settings via the client_id, client_secret, and access_token to act on behalf of a user but with OAuth protection and logging. OAuth is the recommended way to go.

To select the authentication type you set the auth_type attribute to either basic or oauth.

#### Notes
When using OAuth the user you're acting on behalf of must grant you access to act as them. This is explained in the PushBullet documentation. You'll also need to be sure to register your app as a PushBullet client with them to get your client ID and secret.

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
		},
		"admin_interfaces": [
		]
	}

Everything in mcserver.settings is optional and if it is not specified a default value is given. The only exception to this rule is the launcher section. Different launchers are allowed to require different values.

