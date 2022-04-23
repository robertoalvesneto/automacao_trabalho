from api.driverAPI import DriverAPI
from handle_folder.folder import Files

if __name__ == '__main__':
    files = Files()
    driverAPI = DriverAPI()
    
    d_filenames = files.main()
    
    for name, values in d_filenames.items():
        driverAPI.upload_image(values['month'], name, values['path'])
    
    files.remove_all_files()