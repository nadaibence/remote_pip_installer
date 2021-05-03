Remote pip how to docs
===

Remote pip installer is a tool, which can install python packages on remote machines where there are no internet connection. Using a linux docker container it downloads all the necessary pip wheels and copies them to the remote host and installs them using a user defined pip path.

Prerequisites
---

1. [Docker](https://www.docker.com/products/docker-desktop) installed

Instructions
---

1. Clone the repository to your local machine

```bash
git clone https://github.com/nadaibence/remote_pip_installer.git
```

2. Add the **./bin** folder to your _$PATH_ so you will be able to call the **remote_pip.sh** script from anywhere on your local machine.

3. Create a new project and create a folder for your config files.

4. Based on the **./dummy_cfg** folder, create a **requirements.txt** and a **config.cfg** file and populate them with your credentials.

```
[HOST]
host = <hostname>
dest = <path on host where the setup files will be copied>

[PIP_PATH]
path = <pip_path>

[CREDS]
username = <remote SSH username>
password = <remote SSH password>
```

5. Run the bash script with the command line arguments **-h** and **-c**.

```bash
remote_pip.sh -h <hostname> -c <path to the config folder you created in step 4>
```
