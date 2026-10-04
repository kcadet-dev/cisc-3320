import os


def main():
    print("PID:", os.getpid())

    print("PPID:", os.getppid())

    print("\nEnvironment Variables:")
    for key, value in os.environ.items():
        print(f"{key}={value}")

    print("\nDescriptors:")
    try:
        descriptors = os.listdir("/proc/self/fd")

        for d in descriptors:
            print(d)

    except OSError as error:
        print("Error reading descriptors:", error)


if __name__ == "__main__":
    main()
