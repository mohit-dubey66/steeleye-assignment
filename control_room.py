"""
Main controller module to perform the required steps
"""

import os  # For using the system paths
from logger import log  # For managing the logging of the project 
from configparser import RawConfigParser  # For loading th configuration file - config
from helping_function import *  # Importing all the functions from helping_functions

# Gloabl Variable to store configuration object - config            
config = None

    
def load_config_file():
    """This function loads the configuration file and                     
    Return(s):
        config (RawConfigParser) : RawConfigParser object
    """
    # Accessing the config variable
    global config
    try:
        log.info("loading the Config file.")

        # Loading the configuration file
        config = RawConfigParser()
        config.read("config.cfg")
        log.info("Config file loaded successfully.")

    except Exception as e:
        log.error(f"Error in loading the config file : {str(e)}.")

    return config


def main():
    """Function controlling the whole process from reading to uploading
    Return(s):
        True (bool) : If all the steps gets executed successfully.
    """
    try:
        log.info("Extracting the xml source file url")

        # Extract the source XML file URL
        url = config.get("sourcefile", "xml_source_url")

        log.info("Extracting the csv file path from config file")
        csv_path = os.path.join(os.getcwd(), config.get("csv", "csv_path"))

        log.info("Extracting the xml file download path")

        # Extract the download path and create absolute path
        download_path = os.path.join(
            os.getcwd(), config.get("download", "download_path")
        )

        log.info("Extracting AWS s3 bucket resource information from config file")

        # Extract required S3 information from the configuration file
        bucket_name = config.get("aws", "bucket_name")
        aws_access_key_id = config.get("aws", "aws_access_key_id")
        aws_secret_access_key = config.get("aws", "aws_secret_access_key")
        region_name = config.get("aws", "region_name")

        log.info("Calling download function")

        # Call the download helper function to download the file from helping_functions
        xml_file = download(url, download_path, "sourcefile.xml")

        # Verify if the file download was successful or not
        if not xml_file:
            print("Oops!! File Download Fail, Kindly check logs for more details")
            print("Exiting...")
            return

        log.info("Calling the parse_source_xml function")

        # Call the source XML file parser helper function to download the file.
        file_metadata = parse_source_xml(xml_file)

        # Check if the required file metadata extraction failed
        if not file_metadata:
            print("Oops!! File Parsing Failed, Kindly check logs for more details")
            print("Exiting...")
            return

        # Retrieve the file name and download link by parsing file_metadata
        filename, file_download_link = file_metadata

        log.info("Calling download function")

        # Call the download helper function to download the file
        xml_zip_file = download(file_download_link, download_path, filename)

        if not unzip_file(xml_zip_file, download_path):
            print("Extration Failed, Kindly check logs for more details")
            print("Exiting...")
            return

        # Create an absolute path to the XML file
        xml_file = os.path.join(download_path, filename.split(".")[0] + ".xml")

        log.info("Calling create csv function")

        # Call helper function to create CSV file
        csv_file = create_csv(xml_file, csv_path)

        if not csv_file:
            print("XML-CSV Conversion Failed, Kindly check logs for more details")
            print("Exiting...")
            return

        status = aws_s3_upload(
            csv_file, region_name, aws_access_key_id, aws_secret_access_key, bucket_name
        )

        if not status:
            print("Oops!! CSV file upload Failed, Kindly check logs for more details")
            print("Exiting...")
            return

        return True

    except Exception as e:
        log.error(f"Error in loading config file : {str(e)}.")


if __name__ == "__main__":

    # Check for the config file loading
    if not load_config_file():
        print("Error while loading config file, check logs for more!")
        print("Exiting...")
        # Exiting the script if the config files were not loaded
        exit(1)

    print("Pack your bags, becasue Execution has started...")

    if main():
        print("Hurray!! Execution completed successfully...")
    else:
        print("Execution Failed!!! Check logs for more details")
