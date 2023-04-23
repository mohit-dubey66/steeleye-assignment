"""
Unit Testing module for Steel Eye Assigment

"""

import unittest
from control_room import load_config_file
from helping_function import *
import os


class ProjectTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Class method calls once at the beginning of unit test
        """

        # loading the configuration
        config = load_config_file()
        cls.url = config.get("sourcefile", "xml_source_url")

        # Extracting csv file path
        cls.csv_path = config.get("csv", "csv_path")

        # Extracting the download path
        cls.download_path = config.get("download", "download_path")

        # Extracting the required s3 information from config
        cls.bucket_name = config.get("aws", "bucket_name")
        cls.aws_access_key_id = config.get("aws", "aws_access_key_id")
        cls.aws_secret_access_key = config.get("aws", "aws_secret_access_key")
        cls.region_name = config.get("aws", "region_name")

    def setUp(self):
        """
        Instance Method called everytime before a test case is executed
        """

        # Path to xml files
        self.xmlfilepath = os.path.join(os.getcwd(), ProjectTest.download_path)

        # Path to csv file
        self.csvfile = os.path.join(os.getcwd(), ProjectTest.csv_path)

    def testing_download(self):
        """Function to test download function"""

        # Test for all correct data
        self.assertEqual(
            download(ProjectTest.url, self.xmlfilepath, "sourcefile.xml"),
            self.xmlfilepath + os.sep + "sourcefile.xml",
        )

        # Test for incorrect url
        self.assertEqual(
            download("http://lame-website.com", self.xmlfilepath, "sourcefile.xml"), ""
        )

        # Test for different download path
        self.assertEqual(
            download(
                ProjectTest.url,
                os.path.join(os.getcwd(), "testWrongPath"),
                "sourcefile.xml",
            ),
            os.path.join(os.getcwd(), "testWrongPath") + os.sep + "sourcefile.xml",
        )

        # Test for incorrect download path
        self.assertEqual(download(ProjectTest.url, "E:", "sourcefile.xml"), "")

    def testing_parse_source_xml(self):
        """
        Function to test parse_source_xml function
        """

        # Path to the source xml
        file = self.xmlfilepath + os.sep + "sourcefile.xml"

        # Path to non existent source file
        in_file = self.xmlfilepath + os.sep + "sourcefile.mohit"

        # Test for correct data
        # NOTE : For this test case to pass the source xml file should be
        # present in the download path
        self.assertEqual(
            parse_source_xml(file),
            (
                "DLTINS_20210117_01of01.zip",
                "http://firds.esma.europa.eu/firds/DLTINS_20210117_01of01.zip",
            ),
        )

        # Test for incorrect data
        self.assertEqual(parse_source_xml(in_file), None)

    def testing_unzip_file(self):
        """
        Function to test unzip_file function
        """

        # Path to the compressed file
        zipped_file = os.path.join(self.xmlfilepath, "DLTINS_20210117_01of01.zip")

        # Test for correct data
        # NOTE : For this test case to pass the source xml zipped file
        # should be present in the download path
        self.assertTrue(unzip_file(zipped_file, self.xmlfilepath))

        # Test for wrong target path
        self.assertFalse(unzip_file(zipped_file, r"D:\\"))

        # Test for incorrect compressed file
        self.assertFalse(unzip_file("D:\somerandomfile", self.xmlfilepath))

    def testing_create_csv(self):
        """
        Function to test create_csv funtion
        """

        # absolute path to xml file to parse
        xml_file = os.path.join(self.xmlfilepath, "DLTINS_20210117_01of01.xml")

        # absolute path to the csv file to create
        csv_file = os.path.join(self.csvfile, "DLTINS_20210117_01of01.csv")

        # Test for correct data
        self.assertEqual(create_csv(xml_file, self.csvfile), csv_file)

        # Test for incorrect input xml file
        self.assertEqual(create_csv("somerandomfile", self.csvfile), None)

        # Test for incorrect path to write csv to
        self.assertEqual(create_csv(xml_file, r"D:\kqcA CK j "), None)

    def testing_aws_s3_upload(self):
        """
        Function to test aws_s3_upload function
        """

        # absolute path to the csv file to create
        csv_file = os.path.join(self.csvfile, "DLTINS_20210117_01of01.csv")

        # Test for correct data
        self.assertTrue(
            aws_s3_upload(
                csv_file,
                self.region_name,
                self.aws_access_key_id,
                self.aws_secret_access_key,
                self.bucket_name,
            )
        )

        # Test for non existent bucket
        self.assertFalse(
            aws_s3_upload(
                csv_file,
                "delhi-east",
                self.aws_access_key_id,
                self.aws_secret_access_key,
                self.bucket_name,
            )
        )

        # Test for non existent region
        self.assertFalse(
            aws_s3_upload(
                csv_file,
                self.region_name,
                self.aws_access_key_id,
                self.aws_secret_access_key,
                "old-bucket-name",
            )
        )

        # Test for incorrect keys
        self.assertFalse(
            aws_s3_upload(
                csv_file,
                self.region_name,
                "hehehehehehehehe",
                "hello my name is Mohit",
                self.bucket_name,
            )
        )


if __name__ == "__main__":
    unittest.main()
