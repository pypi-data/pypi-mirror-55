import os
import sys
from datetime import datetime
import subprocess
import threading
from hashlib import sha256

class Box(object):
    def __init__(self, config):
        self.filename = sha256((datetime.now().strftime("%Y%m%d%H%M%S")+config['filename']).encode('utf-8')).hexdigest()[-25:]+'_'+config['filename']
        self.box_name = self.filename[:-3]
        # user's code
        self.code = config['code']
        # std_input
        self.input = config['input']
        self.input_name = 'input_' + self.filename[:-3]
        self.memory = config['memory']
        self.timeout = config['timeout']
        self.type = config['type']
        self.dependency = config['dependency']
        self.cpu = config['cpu']
        self.pids_limit = config['pids_limit']
        self.host_path = config['host_path']
        self.container_path = config['container_path']
        self.image = config['image']

    def check_path_exist(self):
        assert os.path.exists(self.host_path), f'Path {self.host_path} not found'
        return True

    def prepare(self):
        if self.check_path_exist():
            # code file
            with open(self.host_path+'/'+self.filename, 'w') as f:
                f.write(self.code)
            # challenge input
            if self.input:
                with open(self.host_path+'/'+self.input_name, 'w') as f:
                    f.write(self.input)
        return 'create file success'

    def run(self):
        #TODO: create code file
        self.prepare()
        #TODO: docker run parameters
        cmd = (
            f"/usr/bin/docker run --rm -a stdout -a stderr "
            f"--memory {self.memory} "
            f"--cpus {self.cpu} "
            f"--pids-limit {self.pids_limit} "
            f"-v {self.host_path}:{self.container_path} "
            f"--name {self.box_name} "
        )
        if self.input:
            cmd = cmd + f"{self.image} /bin/sh -c \"cat /tmp/{self.input_name} | {self.type} /tmp/{self.filename}\"" # cat "/tmp/inputname | python3 "/tmp/filename"
        else:
            cmd = cmd + f"{self.image} {self.type} /tmp/{self.filename}" # python3 "/tmp/filename"

        #TODO:return result
        try:
            def kill_docker():
                nonlocal timeout_flag
                try:  # catch race 
                    timeout_flag = True
                    subprocess.check_output(f"/usr/bin/docker kill {self.box_name}", stderr=subprocess.STDOUT, shell=True)
                except:
                    return "are you kidding me?"
            timeout_flag = False
            finished_flag = False
            t = threading.Timer(self.timeout, kill_docker)
            t.start()
            out_bytes = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
            try: # container killed 
                t.cancel()
            except:
                pass
            return out_bytes.decode().strip()
        except subprocess.CalledProcessError as e: # timeout or error
            if timeout_flag: # timeout
                return f'timeout! you only have {self.timeout} seconds'
            # other error
            try: # container killed 
                t.cancel()
            except:
                pass
            out_bytes = e.output       # Output generated before error
            code      = e.returncode   # Return code
            return out_bytes.decode(), self.filename

    def clear_file(self):
        os.system(f"rm {self.host_path}/{self.filename}")
        if self.input:
            os.system(f"rm {self.host_path}/{self.input_name}")

