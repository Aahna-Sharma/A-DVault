# server.py - Flask backend to launch local Python tools for ADVault
from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import subprocess, sys, platform, os

app = Flask(__name__, static_folder=None)

# EDIT THESE PATHS if your ADVault root differs
PROJECT_ROOT = Path(r"C:\\Users\\aahna\\OneDrive\\Desktop\\ADVault")
VENV_PY = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"

FRONTEND_DIR = Path(__file__).parent / "frontend"

TOOLS = {
    "CVSense.py": {"path": PROJECT_ROOT / "Professional Tools" / "CVSense.py", "use_venv": True},
    "WPM.py": {"path": PROJECT_ROOT / "Productivity Tools" / "WPM.py", "use_venv": False},
    "To-Do List.py": {"path": PROJECT_ROOT / "Productivity Tools" / "To-Do List.py", "use_venv": False},
    "Alarm Clock.py": {"path": PROJECT_ROOT / "Productivity Tools" / "Alarm Clock.py", "use_venv": False},
    "Password Generator.py": {"path": PROJECT_ROOT / "Productivity Tools" / "Password Generator.py", "use_venv": False},
    "Roulette Wheel.py": {"path": PROJECT_ROOT / "Gaming Tools" / "Roulette Wheel.py", "use_venv": False},
    "Guess the Number.py": {"path": PROJECT_ROOT / "Gaming Tools" / "Guess the Number.py", "use_venv": False},
    "Coin toss.py": {"path": PROJECT_ROOT / "Gaming Tools" / "Coin toss.py", "use_venv": False},
    "Rock Paper Scissors.py": {"path": PROJECT_ROOT / "Gaming Tools" / "Rock Paper Scissors.py", "use_venv": False},
    "Unit Conversion.py": {"path": PROJECT_ROOT / "Conversion Tools" / "Unit Conversion.py", "use_venv": False},
    "BMI Calculator.py": {"path": PROJECT_ROOT / "Conversion Tools" / "BMI Calculator.py", "use_venv": False},
    "Basic Calculator.py": {"path": PROJECT_ROOT / "Conversion Tools" / "Basic Calculator.py", "use_venv": False},
    "PDF Merger.py": {"path": PROJECT_ROOT / "PDF Tools" / "PDF Merger.py", "use_venv": False},
    "PDF Coverter.py": {"path": PROJECT_ROOT / "PDF Tools" / "PDF Coverter.py", "use_venv": False},
}

def get_python_for_tool(use_venv):
    if use_venv:
        py = VENV_PY
    else:
        py = Path(sys.executable)
    if platform.system() == 'Windows':
        pw = py.parent / 'pythonw.exe'
        if pw.exists():
            return str(pw)
    return str(py)

def launch_detached(script_path, use_venv):
    if not script_path.exists():
        return False, f'Script not found: {script_path}'
    python_exe = get_python_for_tool(use_venv)
    try:
        if platform.system() == 'Windows':
            flags = 0
            try:
                flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
            except Exception:
                flags = 0
            subprocess.Popen([python_exe, str(script_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)
        else:
            subprocess.Popen([python_exe, str(script_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        return True, 'Launched'
    except Exception as e:
        return False, str(e)

def capture_once(script_path, python_exe, timeout=12):
    if not script_path.exists():
        return False, {'error': 'script_missing', 'message': str(script_path)}
    try:
        proc = subprocess.run([python_exe, str(script_path)], capture_output=True, text=True, timeout=timeout)
        return True, {'returncode': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr}
    except subprocess.TimeoutExpired:
        return False, {'error': 'timeout', 'message': f'Timeout after {timeout}s'}
    except Exception as e:
        return False, {'error': 'exception', 'message': str(e)}

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)

@app.route('/run', methods=['POST'])
def run_tool():
    data = request.get_json() or {}
    filename = data.get('file')
    if not filename:
        return jsonify({'ok': False, 'error': 'no_filename'}), 400
    tool = TOOLS.get(filename)
    if not tool:
        return jsonify({'ok': False, 'error': 'tool_not_registered'}), 404
    ok, msg = launch_detached(Path(tool['path']), tool.get('use_venv', False))
    return jsonify({'ok': ok, 'message': msg})

@app.route('/diagnostics', methods=['POST'])
def diagnostics():
    data = request.get_json() or {}
    filename = data.get('file')
    if not filename:
        return jsonify({'ok': False, 'error': 'no_filename'}), 400
    tool = TOOLS.get(filename)
    if not tool:
        return jsonify({'ok': False, 'error': 'tool_not_registered'}), 404
    if tool.get('use_venv', False):
        python_for_diag = str(VENV_PY)
    else:
        python_for_diag = str(sys.executable)
    ok, result = capture_once(Path(tool['path']), python_for_diag, timeout=12)
    return jsonify({'ok': ok, 'result': result})

if __name__ == '__main__':
    print('Starting server on http://127.0.0.1:5000')
    app.run(host='127.0.0.1', port=5000, debug=True)