import os
import globals as gb



def manage_files():
  serial = ''
  uuid = ''
  passw = ''
  default_conf = ''
  target_drive = ''

  with open('../../../target_drive.txt', 'r') as target_drive_source:
    target_drive = target_drive_source.readline() + gb.PATH_DIR_SD_DATA_FORISCONTROL

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
  with open(target_drive + '/SERIAL', 'w') as sd_serial_file:
    sd_serial_file.write(serial)

  with open(target_drive + '/UUID', 'w') as sd_uuid_file:
    sd_uuid_file.write(uuid)

  with open(target_drive + '/PASS', 'w') as sd_passw_file:
    sd_passw_file.write(passw)

  with open(target_drive + '/default_config.ini', 'w') as sd_config_file:
    sd_config_file.writelines(default_conf)

  try:
    os.remove(target_drive + '/._default_config.ini')
  except:
    pass

  # coming soon
  #with open(target_drive + '/default_config.ini', 'w') as sd_passw_file:
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