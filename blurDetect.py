import cv2
import os
import pandas as pd

from PIL import Image
import piexif

def get_gps_metadata(image_path):
    # Open the image file
    gpsData = []
    img = Image.open(image_path)
    
    # Extract EXIF data
    exif_data = img._getexif()
    for x in range(2):
        i = 2
        if exif_data[34853][i*(x+1)-1] == 'N' or  exif_data[34853][i*(x+1)-1] == 'E':
            mult = 1
        else:
            mult = -1
        gpsLog = exif_data[34853][i*(x+1)]
        gpsCoord = (gpsLog[0]+(float(gpsLog[1])/60)+(float(gpsLog[2])/3600))*mult
        gpsData.append(gpsCoord)
        i += 2
    return gpsData



def detect_blur(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()

    return laplacian_var


def list_files(directory):
    # Check if the directory exists
    if not os.path.exists(directory):
        print("The specified directory does not exist.")
        return []
    
    # List all files and directories in the given directory
    files = os.listdir(directory)
    
    # Filter out directories, keep only files
    files = [file for file in files if os.path.isfile(os.path.join(directory, file))]
    return files

def list_directories_in_directory(directory_path):
    dirArr = []
    try:
        # List all files and directories in the specified path
        files_and_dirs = os.listdir(directory_path)
        
        # Filter out only directories
        directories = [d for d in files_and_dirs if os.path.isdir(os.path.join(directory_path, d))]
        
        print(f"Directories in '{directory_path}':")
        for dir_name in directories:
            dirArr.append(dir_name)
        return dirArr
    except Exception as e:
        print(f"An error occurred: {e}")




d = {'fileName':[], 'blurLev': [], 'N': [], 'W':[]}
df = pd.DataFrame(data=d)

direct = "D:/DCIM/"
for folder in list_directories_in_directory(direct):
    directInt = ""+direct+folder+"/"
    for each in (list_files(directInt)):
        if each[-1] == 'y' or 'V' in each or each[-1] == 'v':
            continue
        arr = []
        arr.append(each)
        arr.append((detect_blur(each)))

        # Retrieve GPS metadata
        gps_metadata = get_gps_metadata(each)
        arr.append(gps_metadata[0])
        arr.append(gps_metadata[1])
        df.loc[len(df)] = arr

df.loc[len(df)] = ['lowEndPlaceHolder',0,df['N'].mean(),df['W'].mean()]

print(df)
df.to_csv('out.csv', index=False)  


