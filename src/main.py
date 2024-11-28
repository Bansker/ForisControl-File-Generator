# 
# FORIS Control Data Generation
# von Yannick
#
# Hi Oli, sourcecode ist hacky, ich weiss. war in eile :D
#


import os
import sys
import uuid
import csv
import random
import shutil

import globals as gb


# --- CONSTANTS --- #
BATFILE = 'manage_files.bat'
BATFILE_CONTENT = '@echo off\n..\..\..\python_3_11_7\python ..\..\..\src\manage_files.py'


# --- FUNCTION DEFINITIONS --- #
def gen_passw_12():
  """ -----------------------------------------------------------
  Function Name: gen_passw_12\n
  Description: generates a random 12 Char Letter and Number password 
  """

  ASCII_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  ASCII_NUMS    = '0123456789'
  pw = ''
  for i in range(6):
    pw = pw + random.choice(ASCII_LETTERS) + random.choice(ASCII_NUMS)
    pw = ''.join(random.sample(pw, len(pw)))

  return pw


def create_device_list(serial, rows):
  """ -----------------------------------------------------------
  Function Name: create_device_list

  Arguments:
  * serial
  * rows
  """

  serial_index_after_hyphen = serial.find('-') + 1
  serial_higher = int(serial[:4])                                                         # cuts to the first 4 digits of the SN before the hyphen and converts to int
  serial_lower = int(serial[serial_index_after_hyphen : serial_index_after_hyphen + 4])   # cuts to the last 4 digits of the SN after the hyphen and converts to int

  device_data = []
  for row in range(rows):
    device_data.append([f'{serial_higher:04}-{serial_lower:04}', str(uuid.uuid4()), gen_passw_12()])
    serial_lower = serial_lower + 1
    
  return device_data




# === MAIN ======================================================= #
def main():
  if len(sys.argv) > 1:
    args = sys.argv[1:]
    amount = int(args[0].strip())
    serial = args[1].strip()


  else:

    # --- Userinput Drive Letter of target drive 
    # --- SD Card Partition containing /foriscontrol/ directory
    while True:
      target_drive_letter = input('Laufwerkbuchstabe von Zielordner eingeben (beispiel: g): ').strip().upper()

      if target_drive_letter == '':
        print('Fehlerhafte eingabe!')
        continue

      else:
        # --- Create / edit file containing target drive letter 
        # --- (for easier access if drive letter changes during a series of file copying)
        with open('target_drive.txt', 'w') as target_drive:
          target_drive.write(target_drive_letter)

        break

    # --- Userinput Device Count 
    # --- must be greater than 0, ask again if input is below 1
    while True:
      amount = int(input('Stückzahl: ').strip())
      if amount < 1 or not isinstance(amount, int):
        print('Eingabe muss eine Zahl grösser als 0 sein')
        continue
      else:
        break

    # --- Userinput Serial Number 
    # --- User must input the first serial number from a series of neighbouring serials 
    # --- Theres no error handling for wrong input, so, be careful dear user.
    serial = input('Erste Serien-NR (Format XXXX-XXXX): ').strip()

  # --- Generate a arbitrary length 2D list containing the following format: [[SERIAL, UUID, PASSWORD], [etc...]]
  device_data = create_device_list(serial, amount)

 

  # --- Create Folderstructure
  try:
    os.mkdir(gb.PATH_DIR_MAIN)
    os.mkdir(gb.PATH_DIR_CSV)
    os.mkdir(gb.PATH_DIR_CONFIGS)
  except FileExistsError:
    pass
  


  # --- Create CSV File with all the device infos
  with open(gb.PATH_DIR_CSV + '/device_info.csv', 'a') as device_info:
    # Tab seperated mode for easy pasting to dokuwiki device list
    device_info_writer = csv.writer(device_info, delimiter='\t')
    device_info_writer.writerows(device_data)


  # --- just a newline for better readability
  print()

  # --- Create Serial specific Folders and Files and batfile to execute manage_files.py script
  for row in range(amount):
    full_serial = device_data[row][0]
    uuid_ = device_data[row][1]
    passw = device_data[row][2]

    path_device_configs = gb.PATH_DIR_CONFIGS + '/' + full_serial
    filepath_serial = path_device_configs + '/SERIAL'
    filepath_uuid = path_device_configs + '/UUID'
    filepath_pass = path_device_configs + '/PASS'
    filepath_batfile = path_device_configs + '/' + BATFILE

    

    try:
      os.mkdir(path_device_configs)
    
      with open(filepath_serial, 'w') as file_serial:
        file_serial.write(f'{full_serial}')

      with open(filepath_uuid, 'w') as file_uuid:
        file_uuid.write(f'{uuid_}')  

      with open(filepath_pass, 'w') as file_pass:
        file_pass.write(f'{passw}')

      # Create Batfile in every Serial specific Folder
      with open(filepath_batfile, 'w') as batfile:
        batfile.write(BATFILE_CONTENT) 

      # Copy config from root dir
      shutil.copyfile('./default_config.ini', path_device_configs + '/default_config.ini')

      print(f"\033[0;32m  Verzeichnis und Daten für SN \033[0;34m{full_serial}\033[0;32m wurden erstellt\033[0;37m")
    
    except FileExistsError:
      print(f'\033[0;33m  Verzeichnis \033[0;34m{full_serial}\033[0;33m existiert bereits.\033[0;37m')

  input('\nDateien und Ordner wurden erfolgreich generiert.\nEnter drücken um dieses Fenster zu schliessen.')

  
    
def debug():
  pass

DEBUG = 0
if __name__ == '__main__' and DEBUG == 0: main()
elif __name__ == '__main__' and DEBUG == 1: debug()
