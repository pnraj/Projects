import os
import requests
import zipfile
import io

def get_file():
    url = 'https://github.com/PhonePe/pulse/archive/refs/heads/master.zip'
    response = requests.get(url)

    if response.status_code == 200:
        # create a file-like object from the content of the ZIP archive
        zip_file = io.BytesIO(response.content)

        # specify the path where you want to save the downloaded file
        save_path = '/opt/airflow/dags/src/data/'

        # check if the save path exists and create it if it doesn't
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # open the zip file for reading
        with zipfile.ZipFile(zip_file, 'a') as zip_ref:
            # extract all files to the specified directory
            zip_ref.extractall(save_path)
    else:
        print('Failed to fetch content:', response.status_code)

def main():
    try:
        get_file()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
