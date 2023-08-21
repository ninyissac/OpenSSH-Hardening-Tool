# OpenSSH Hardening Tool

The OpenSSH Hardening Tool is a Python program designed to harden an OpenSSH server based on the operational context of the server system. The tool uses various templates depending on the context of the system. For example, hardening an SSH service on a web server is not the same as hardening it on a backup server, and the hardening requirements for a revision control system may be different.

## Dependencies

Before running the OpenSSH Hardening Tool, ensure that all the required dependencies are installed by running the following command:

```shell
pip3 install -r requirements.txt
```

## Configuraion of the program
The OpenSSH Hardening Tool consists of the following components:

- 'contexts/ folder': contains all the operational context template files.
- 'program/ folder': contains the main code of the program.
- 'program/config.ini': the main configuration file.

You can customize the settings in the config.ini file to suit your specific needs. The contexts/ folder contains templates for different types of servers and systems. You can modify these templates or add new ones as necessary, but make sure to edit config.ini accordingly.


## Running the program

To run the program, follow these steps:

   -  Download or clone the project onto the GNU/Linux server that you wish to harden the OpenSSH service on.
   -  Navigate to the project directory and execute ./run.

Run the program using the following command:
```bash
./run
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License
GNU General Public License v3.0 or later

See [COPYING](https://choosealicense.com/licenses/gpl-3.0/) to see the full text.
