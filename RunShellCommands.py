import subprocess

install = 'flockf'
host = install + '.ssh.wpengine.net'

#keyFile = 'wpengine_ed25519'

# Each pathname will need to look like "ssh install@install.wpengine.net"
def update_wordpress():
    print("Update WordPress...")
    cmd = 'wp core update'
    process = subprocess.Popen(f"ssh {install}@{host} {cmd}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()

    if process.returncode != 0:
        print("Error: " + str((process.returncode, output, error)))
    else:
        print(str((output)))

def update_theme(theme):
    print("Update Active Theme...")
    cmd = 'wp theme update ' + theme

update_wordpress()

update_theme('yootheme')

# if (process[1] == ''):
#     print('Success: ' + str(process[0]))
# else:
#     print('Error: ' + str(process[1]))

# subprocess.check_output(
#     "ssh flockf@flockf.ssh.wpengine.net; exit 0;",
#     stderr=subprocess.STDOUT,
#     shell=True)