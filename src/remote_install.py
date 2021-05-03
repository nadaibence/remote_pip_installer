import paramiko
import configparser
import subprocess
import os
import time



class RemotePip():

    def __init__(self, config_path='/app/config.cfg', reqs_path='/app/requirements.txt', delete_files=True):
        self.config_path = config_path
        self.reqs_path = reqs_path
        self.delete_files = delete_files
        
        cfg = configparser.ConfigParser()
        cfg.read(self.config_path)
        self.host = cfg.get('HOST', 'host')
        self.user = cfg.get('CREDS', 'username')
        self.pw = cfg.get('CREDS', 'password')
        self.pip_path = cfg.get('PIP_PATH', 'path')
        self.dest = cfg.get('HOST', 'dest')

        self.remote_client = paramiko.SSHClient()
        self.remote_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.remote_client.connect(hostname=self.host, username=self.user, password=self.pw)

   
    def copy_files_to_remote(self):
        out = subprocess.run([
            'sshpass',
            '-p',
            f'{self.pw}',
            'scp',
            '-r',
            '/app/python_packages.tgz',
            f'{self.user}@{self.host}:{self.dest}'
        ])

        if out.returncode == 0:
            print('Successfully copied TAR file to remote host!')
        else:
            msg = 'ERROR: cant copy TAR file to host!'
            raise Exception(msg)

    
    def install_packages(self):
        stdin, stdout, stderr = self.remote_client.exec_command(f'mkdir {self.dest}/python_packages')
        stdin, stdout, stderr = self.remote_client.exec_command(f'tar xvfz {self.dest}/python_packages.tgz -C {self.dest}')

        for res in stdout:
            print(res)

        folder = self.dest + '/python_packages'
        stdin, stdout, stderr = self.remote_client.exec_command(f'ls {folder}')

        for fname in stdout:
            fname = fname.strip()
            print('#### FILE TO INSTALL ####', fname)
            _, out, err = self.remote_client.exec_command(f'{self.pip_path} install {folder}/{fname} -f ./ --no-index --no-deps')

            if out.channel.recv_exit_status() == 0:
                for line in out:
                    print(line)
            
            else:
                for line in err:
                    print(line)


    def remove_files(self):
        _, _, _ = self.remote_client.exec_command(f'rm {self.dest}/python_packages.tgz')
        _, _, _ = self.remote_client.exec_command(f'rm -r {self.dest}/python_packages')

    
    def run(self):
        self.copy_files_to_remote()
        self.install_packages()

        if self.delete_files:
            self.remove_files()
        




if __name__ == '__main__':
    rm_pip = RemotePip()
    rm_pip.run()