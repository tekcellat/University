from subprocess import check_output
import subprocess
import hashlib
import os.path

def get_checksum():
    result = subprocess.run("cat /var/lib/dbus/machine-id", stdout=subprocess.PIPE, shell=True, check=True)
    machine_id = result.stdout.decode().strip()
    return hashlib.sha512(machine_id.encode('utf-8')).hexdigest()


def check_checksum(filename):
    if not os.path.isfile(filename):
        return False
    with open(filename, "r") as license:
        if license.readline() == get_checksum():
            return True
        else:
            return False


def create_license(filename):
    with open(filename, "w+") as license:
        license.write(get_checksum())


if __name__ == "__main__":
    create_license("license.key")
    '''with open("license.key", "r") as license:
        print(license.readline())'''