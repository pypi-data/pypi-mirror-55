#!/usr/bin/env python3
import subprocess
import sys

def checkInstalled(package):
        result = subprocess.run(["dpkg","-s",package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if result.returncode == 0:
            return True
        else:
            return False

def main():
    if len(sys.argv) == 1:
        print("Usage: jdAptDirReinstall <directory>")
        sys.exit(1)

    output = subprocess.run(["apt-file","search","-l",sys.argv[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    lines = output.stdout.splitlines()

    if len(lines) == 0:
        print("No packages found for this directory")
        sys.exit(0)

    installCommand = ["sudo","apt","install","--reinstall"]
    for i in lines:
        if checkInstalled(i):
            installCommand.append(i)

    if len(installCommand) == 4:
        print("No package installed that use this directory")
        sys.exit(0)

    subprocess.call(installCommand)
    sys.exit(0)

if __name__ == '__main__':
    main()
