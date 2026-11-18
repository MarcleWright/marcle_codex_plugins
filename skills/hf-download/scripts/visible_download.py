"""Launch HF in a visible Windows console. Standard library only; no token storage."""

import argparse
import base64
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from urllib.parse import urlsplit


def read_job(path):
    job = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    allowed = {"hf_executable", "repo_id", "repo_type", "revision", "local_dir",
               "include", "exclude", "endpoint", "http_proxy", "https_proxy", "dry_run"}
    if not isinstance(job, dict) or set(job) - allowed:
        raise ValueError("Unknown configuration fields; credentials are not supported")
    for key in ("hf_executable", "local_dir"):
        if not isinstance(job.get(key), str) or not Path(job[key]).is_absolute():
            raise ValueError(f"{key} must be an absolute path")
    if not Path(job["hf_executable"]).is_file():
        raise ValueError("HF executable does not exist")
    if not isinstance(job.get("repo_id"), str) or not job["repo_id"].strip() or job["repo_id"].startswith("-"):
        raise ValueError("repo_id must be a repository ID")
    if job.get("repo_type", "model") not in ("model", "dataset", "space"):
        raise ValueError("Unsupported repository type")
    if "dry_run" in job and not isinstance(job["dry_run"], bool):
        raise ValueError("dry_run must be a boolean")
    if "revision" in job and not isinstance(job["revision"], str):
        raise ValueError("revision must be a string")
    for key in ("include", "exclude"):
        values = job.get(key, [])
        if not isinstance(values, list) or not all(isinstance(v, str) and v for v in values):
            raise ValueError(f"{key} must be a list of nonempty strings")
    for key in ("endpoint", "http_proxy", "https_proxy"):
        if key in job:
            value = job[key]
            if not isinstance(value, str):
                raise ValueError(f"{key} must be a string")
            if not value and key != "endpoint":
                continue
            parsed = urlsplit(value)
            if not parsed.scheme or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
                raise ValueError(f"{key} requires a URL without credentials, query or fragment")
    return job


def command(job):
    args = [job["hf_executable"], "download", job["repo_id"],
            "--repo-type", job.get("repo_type", "model"), "--local-dir", job["local_dir"]]
    if job.get("revision"):
        args += ["--revision", job["revision"]]
    for key in ("include", "exclude"):
        for pattern in job.get(key, []):
            args += ["--" + key, pattern]
    if job.get("dry_run", False):
        args.append("--dry-run")
    return args


def status(path, state, **extra):
    data = {"state": state, "updated_at": datetime.now(timezone.utc).isoformat(), **extra}
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    for attempt in range(10):
        try:
            temporary.replace(path)
            return
        except PermissionError:
            if attempt == 9:
                raise
            time.sleep(0.05)


def worker(config):
    record = Path(config).parent / "status.json"
    try:
        job = read_job(config)
        env = os.environ.copy()
        for key, name in (("endpoint", "HF_ENDPOINT"), ("http_proxy", "HTTP_PROXY"), ("https_proxy", "HTTPS_PROXY")):
            if key in job:
                env.pop(name.lower(), None)
                if job[key]:
                    env[name] = job[key]
                else:
                    env.pop(name, None)
        status(record, "running", worker_pid=os.getpid(), local_dir=job["local_dir"])
        print("HF download: " + job["repo_id"], flush=True)
        print("Press Ctrl+C to interrupt. This window stays open after completion.", flush=True)
        result = subprocess.run(command(job), env=env, shell=False)
        interrupted = result.returncode in (130, -1073741510, 3221225786)
        state = "cancelled" if interrupted else ("completed" if result.returncode == 0 else "failed")
        status(record, state, exit_code=result.returncode, dry_run=job.get("dry_run", False))
        print(f"\nHF exited: {result.returncode}. Status: {record}", flush=True)
        return result.returncode
    except KeyboardInterrupt:
        status(record, "cancelled")
        print("\nInterrupted; existing download data was preserved.", flush=True)
        return 130
    except Exception as exc:
        # Do not persist provider messages, URLs, environment values or credentials.
        status(record, "failed", error_type=type(exc).__name__)
        print(f"Download worker failed ({type(exc).__name__}). See {record}", flush=True)
        return 1


def launch(config, shell):
    if os.name != "nt":
        raise ValueError("Visible terminal launch requires Windows")
    job = read_job(config)
    powershell = shutil.which("pwsh.exe") or shutil.which("powershell.exe")
    if shell == "powershell" and not powershell:
        raise ValueError("PowerShell was not found")
    run_dir = Path(tempfile.mkdtemp(prefix="hf-download-"))
    frozen = run_dir / "job.json"
    frozen.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8")
    arguments = [sys.executable, str(Path(__file__).resolve()), "--worker", str(frozen)]
    if shell == "powershell":
        quoted = ["'" + value.replace("'", "''") + "'" for value in arguments]
        script = "& " + " ".join(quoted)
        encoded = base64.b64encode(script.encode("utf-16-le")).decode("ascii")
        args = [powershell, "-NoLogo", "-NoProfile", "-NoExit", "-EncodedCommand", encoded]
    else:
        # CMD expands percent variables even in quotes. Reject unrepresentable paths.
        if any(any(c in value for c in '%!"\r\n') for value in arguments):
            raise ValueError("These paths cannot safely be launched in CMD; use PowerShell")
        line = " ".join('"' + value + '"' for value in arguments)
        # Pass a raw command line: list2cmdline uses CRT backslash quoting, which
        # CMD does not understand for its /K command string.
        prefix = [os.environ.get("COMSPEC", "cmd.exe"), "/D", "/V:OFF", "/K"]
        args = subprocess.list2cmdline(prefix) + ' "' + line + '"'
    record = run_dir / "status.json"
    status(record, "launching")
    try:
        process = subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=run_dir)
    except Exception as exc:
        status(record, "failed", error_type=type(exc).__name__)
        raise
    print(json.dumps({"pid": process.pid, "run_dir": str(run_dir), "status_file": str(record)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--config", help="UTF-8 job JSON; creates a visible terminal")
    mode.add_argument("--worker", help=argparse.SUPPRESS)
    parser.add_argument("--shell", choices=("powershell", "cmd"), default="powershell")
    options = parser.parse_args()
    if options.worker:
        sys.exit(worker(options.worker))
    launch(options.config, options.shell)
