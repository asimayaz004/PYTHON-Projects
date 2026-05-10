import os
import subprocess


# -----------------------------------
# Display Current Directory
# -----------------------------------

def show_path():
    return os.getcwd()


# -----------------------------------
# Main Shell
# -----------------------------------

def shell():
    print("===== MINI PYTHON SHELL =====")
    print("Type 'exit' to quit.")

    while True:
        command = input(f"{show_path()} > ")

        if command.lower() == "exit":
            print("Exiting shell...")
            break

        # Change Directory
        elif command.startswith("cd "):
            path = command[3:]

            try:
                os.chdir(path)
            except FileNotFoundError:
                print("Directory not found.")

        # List Files
        elif command == "ls":
            files = os.listdir()

            for file in files:
                print(file)

        # Make Directory
        elif command.startswith("mkdir "):
            folder = command[6:]

            try:
                os.mkdir(folder)
                print("Folder created.")
            except:
                print("Unable to create folder.")

        # Remove File
        elif command.startswith("rm "):
            filename = command[3:]

            try:
                os.remove(filename)
                print("File deleted.")
            except:
                print("Unable to delete file.")

        # Run System Commands
        else:
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    text=True,
                    capture_output=True
                )

                print(result.stdout)

                if result.stderr:
                    print(result.stderr)

            except Exception as e:
                print("Error:", e)


# -----------------------------------
# Run Shell
# -----------------------------------

if __name__ == "__main__":
    shell()