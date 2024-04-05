from subprocess import run as foo

# This function will echo the print the messages in the terminal.
def echo(arg: str):
    system(f'echo -e "{arg}"')


# This function will determine the input as True or False or YesForAll.
def yon(arg:str, simple=True) -> bool:
    response = input(arg)

    if simple: return True if "y" in response else False

    if "yes" or "y" in response: return "true"

    if response == "skip" or response == "s": return "false"

    if "all" in response: return "all"


# Just modifying the subprocess.run() to give desired outputs.
def run(arg:str):
    try: 
        print(f"\n\nExecuting [{arg}]\n")
        foo(arg, shell=True, check=True) # This foo is subprocess.run()
    except Exception:
        echo(f"\n\n{red}While executing the command {nocolor}'{arg}'{red}, the above error occured.{nocolor}")
        proceed = yon(
                "\nWell, I can't possibly know what error you enountered. "
                "If you don't want to proceed, the script will abort.\n"
                "Do you want to proceed? Yes or No: "
            )
        if not proceed: 
            print("Okay, aborted!")
            exit()