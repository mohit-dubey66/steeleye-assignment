# Assignment Of SteelEye
-------------------------
This is the project assigned by the SteelEye for a year internship as Python Engineer.
I have used Python language and AWS to complete this project.

# Tech Stack
* Python
* AWS - S3 Bucket Service

# Modules and Libraries Used
Following Modules of Python has been used for the project:
* For path validation - os
* For AWS connection - boto3
* For processing of file - xml.etree(to work with XML files) and unzipfile(to unzip the downloaded file)
* For connectivity - requests
* For configuration - configparser
* For logging - logger
* For testing - unittest2
* For editing the CSV file - pandas

Note: All the dependecies are freezed in the "requirements.txt" file.

# Configuration File(config.cfg)

* download_path: this by default takes the absolute or the realtive path from the localhost system.
* **csv_path**: this takes the relative path from the localhost system of the CSV files.
* **source_file**: this takes the URL of the XML file that is to downloaded via xml_source_url.
* **aws**: this has multiple variables for connecting with AWS like, 
* **bucket_name** - Provide the name of the S3 bucket to which file needs to be uploaded
* **aws_access_key_id** - Provide the AWS access key ID
* **aws_secret_access_key** - Provide the AWS secret access key
* **region_name** - Provide the AWS region in which the S3 bucket is hosted

# Files that are important
* **control_room.py**         : This is the module that controls the whole process of the project.
* **helping_function.py**     : This is the module that helps the control_room as all the functionalities are written in this file.
* **logger.py**               : This module initializes the logger which is keeping tracking of all the processes that is happening in control_room and maintaing the logs for the same.
* **testing_the_project.py**  : This module helps in testing the whole project based on certain testcases.

# Screenshot of the upload of the file to AWS S3 bucket.

* Firstly, I created the bucket on AWS:

![1](https://user-images.githubusercontent.com/63240844/234033246-231db345-2e76-48ec-90c8-5382ea8dcce4.png)

* Proof of the upload of the file to S3 bucket:

![2](https://user-images.githubusercontent.com/63240844/234033311-182890c4-220f-4a5f-8e5d-9ac154fc455b.png) 

