import os
import subprocess

def setup_gateway():
    if os.name == "nt":
        activate_script = "activate.bat"
    else:
        activate_script = "activate"
    gateway_path = os.path.join(os.path.dirname(__file__), "gateway")
    print(gateway_path)
    subprocess.run("nodeenv node".split(), cwd=gateway_path)
    activate_cmd = os.path.join(gateway_path, "node", "Scripts", activate_script)
    subprocess.run("nodeenv node".split(), cwd=gateway_path)
    subprocess.run([activate_cmd] + " & npm install".split(), cwd=gateway_path)
    os.environ["GATEWAY_PATH"] = gateway_path