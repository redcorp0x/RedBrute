import pyfiglet
from colorama import Fore, Style, init
import config
import os
from datetime import datetime

init(autoreset=True)

banner = pyfiglet.figlet_format("RedBrute", font="slant")

print(Fore.RED + banner)

print(Fore.WHITE + Style.BRIGHT +
      "       HTTP Brute-Force & Security Testing Tool")

print(Fore.CYAN + "               Built by Redcorp\n")


print(Fore.WHITE + "  Version 1.0.1")
print(Fore.GREEN + "  [>] Automated HTTP Request Testing")
print(Fore.GREEN + "  Proxy Support | [>] GET URL | GET FORM | POST FORM")

print(Fore.RED + "-" * 59)
print(Fore.CYAN + "  Usage: Type redbrute --help to display available options.")
print(Fore.RED + "-" * 59)  
