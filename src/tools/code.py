import subprocess
import tempfile
from os import getenv

def send_to_env(content: str) -> dict:
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_file.write(content.encode('utf-8'))
        temp_file.flush()

        user = getenv("REMOTE_USER", "user")
        remote_file = getenv("REMOTE_FILE", "/path/to/destination/a.py")
        remote_ip = getenv("REMOTE_IP", "remote")

        try:
            res = subprocess.run(
                ['scp', temp_file.name, f'{user}@{remote_ip}:{remote_file}'],
                check=True,
                capture_output=True,
                text=True,
            )
            
            res = execute_script()
            return {
                "status": "success",
                "returncode": res.returncode,
                "stdout": res.stdout or "file sent and executed successfully",
                "stderr": res.stderr,
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": "error",
                "returncode": e.returncode,
                "stdout": e.stdout,
                "stderr": e.stderr,
            }
    
    
def execute_script() -> subprocess.CompletedProcess:
    """
    Executes a script on the environment.
    Returns:
        str: The output from the script execution.
    """
    user = getenv("REMOTE_USER", "user")
    remote_ip = getenv("REMOTE_IP", "remote")
    remote_path = getenv("REMOTE_PATH", "/path/to/destination/script.sh")
    
    result = subprocess.run(['ssh', f'{user}@{remote_ip}', '&', 'sh', f'{remote_path}/test.sh'], capture_output=True, text=True, check=True)
    cat = subprocess.run(['ssh', f'{user}@{remote_ip}', 'cat', f'{remote_path}/output.log'], capture_output=True, text=True, check=True)
    return cat