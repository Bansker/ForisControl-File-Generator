import os
import sys
import uuid
import csv
import random
import shutil

import src.globals as gb


# --- CONSTANTS --- #
BATFILE = 'manage_files.bat'
BATFILE_CONTENT = '@echo off\n..\..\..\python_3_11_7\python ..\..\..\manage_files.py'


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
    amount = int(input('Stückzahl: ').strip())
    serial = input('Erste Serien-NR (Format XXXX-XXXX): ').strip()

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
    device_info_writer = csv.writer(device_info, delimiter='\t')
    device_info_writer.writerows(device_data)



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
    print(filepath_serial)

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

      print(device_data[row])
    
    except FileExistsError:
      print(f'Files for SN {full_serial} already exist.')

  
    
def debug():
  pass

DEBUG = 0
if __name__ == '__main__' and DEBUG == 0: main()
elif __name__ == '__main__' and DEBUG == 1: debug()
