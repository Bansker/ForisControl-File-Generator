import os
import src.globals as gb



def manage_files():
  serial = ''
  uuid = ''
  passw = ''
  default_conf = ''

  # Local Dir file read operations
  with open('SERIAL', 'r') as serial_file:
    serial = serial_file.readline()

  with open('UUID', 'r') as uuid_file:
    uuid = uuid_file.readline()

  with open('PASS', 'r') as passw_file:
    passw = passw_file.readline()

  with open('default_config.ini', 'r') as config_file:
    default_conf = config_file.readlines()


  # SD Card Dir file write operations
  with open(gb.PATH_DIR_SD_DATA_FORISCONTROL + '/SERIAL', 'w') as sd_serial_file:
    sd_serial_file.write(serial)

  with open(gb.PATH_DIR_SD_DATA_FORISCONTROL + '/UUID', 'w') as sd_uuid_file:
    sd_uuid_file.write(uuid)

  with open(gb.PATH_DIR_SD_DATA_FORISCONTROL + '/PASS', 'w') as sd_passw_file:
    sd_passw_file.write(passw)

  with open(gb.PATH_DIR_SD_DATA_FORISCONTROL + '/default_config.ini', 'w') as sd_config_file:
    sd_config_file.writelines(default_conf)

  try:
    os.remove(gb.PATH_DIR_SD_DATA_FORISCONTROL + '/._default_config.ini')
  except:
    pass

  # coming soon
  #with open(gb.PATH_DIR_SD_DATA_FORISCONTROL + '/default_config.ini', 'w') as sd_passw_file:
  #  pass





def main():
  check = ''
  try:
    with open('check', 'r') as check_file:
      check = check_file.readline()
  except:
    pass
  
  if check == 'true':
    print('Diese configs wurden schon einmal auf eine SD Karte geschrieben!')

  else:
    manage_files()

    with open('check', 'w') as check_file:
      check_file.write('true')

    print('Fertig.')

  input('Enter drücken, um dieses Fenster zu schliessen')




if __name__ == '__main__': main()