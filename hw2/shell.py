import os
import shlex
import signal

class Job:
    def __init__(self, pid, command, background):
        self.pid = pid
        self.command = command
        self.background = background
        self.status = "Running"

jobs = {}
next_job_id = 1

while True:
    try:
        while True:
            pid, status = os.waitpid(-1, os.WNOHANG)

            if pid == 0:
                break

            for job_id, job in jobs.items():
                if job.pid == pid:
                    job.status = "Done"

    except ChildProcessError:
        pass

    command = input("myshell> ").strip()

    if command == "":
        continue

    background = command.endswith("&")

    if background:
        command = command[:-1].strip()

    args = shlex.split(command)

    if args[0] == "exit":
        break

    elif args[0] == "cd":
        os.chdir(args[1])

    elif args[0] == "jobs":
        for job_id, job in jobs.items():
            print(f"[{job_id}] {job.status} {job.command}")

    elif args[0] == "fg":
        job_id = int(args[1])
        job = jobs[job_id]

        print(job.command)
        os.waitpid(job.pid, 0)

        del jobs[job_id]

    elif args[0] == "kill":
        job_id = int(args[1])
        job = jobs[job_id]

        os.kill(job.pid, signal.SIGTERM)
        os.waitpid(job.pid, 0)

        print(f"[{job_id}] Terminated {job.command}")

        del jobs[job_id]

    else:
        pid = os.fork()

        if pid == 0:
            try:
                os.execvp(args[0], args)
            except FileNotFoundError:
                print(f"myshell: {args[0]}: command not found")
                os._exit(1)

        else:
            if background:
                jobs[next_job_id] = Job(pid, command, True)

                print(f"[{next_job_id}] {pid} {command}")

                next_job_id += 1

            else:
                os.waitpid(pid, 0)
