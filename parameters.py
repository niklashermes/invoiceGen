import glob
import os
import pathlib
from datetime import date

########################################################
# setup basic variables and the working directory
########################################################

# set hourly wage
wage = "22"
shipping_cost = "8"
install_fee = "35"

path = pathlib.Path(__file__).parent.resolve()
os.chdir(path)


if "vulfpeck" in str(path):
    running_on = 'server'
    khard_prefix = "sudo -u www-data /var/www/.local/pipx/venvs/khard/bin/"
else:
    running_on = 'desktop'
    khard_prefix = ""


# set the year for the correct folder
year = str(date.today().year)

# calculate next invoice_number based on filetree
folder_path = "../rechnungen_{year}/".format(year=year)

# check if folder exists and of not create one
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# cd into the folder
os.chdir(folder_path)

invoice_numbers = []
if not glob.glob(str(os.getcwd()) + '/*'):
    os.chdir("../rechnungen_{year}/".format(year=int(year)-1))
for i in glob.glob(str(os.getcwd()) + '/*'):
    temp = i.split("/")[-1].split("_")[1]
    try:
        int(temp)
        if len(temp) > 5:
            invoice_numbers.append(temp)
    except ValueError:
        continue
invoice_number = sorted(invoice_numbers)[-1:][0]
invoice_number = int(invoice_number[4:]) + 1
invoice_number = year + str(invoice_number)
os.chdir("../invoiceGen/")
