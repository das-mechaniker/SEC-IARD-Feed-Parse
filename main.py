import os
import requests
import zipfile
import xml.etree.ElementTree as ET
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Hardcoded URL for the Investment Adviser Representatives Report
HARDCODED_URL = "https://reports.adviserinfo.sec.gov/reports/CompilationReports/IA_INDVL_Feed_02_24_2025.xml.zip"

# Step 1: Download and unzip the XML file
def download_and_extract_zip(url, extract_to="."):
    zip_path = "IA_INDVL_Feed.zip"
    try:
        logger.info(f"Downloading ZIP file from {url}")
        response = requests.get(url)
        with open(zip_path, "wb") as f:
            f.write(response.content)
        logger.info("Download completed.")

        logger.info(f"Extracting ZIP file to {extract_to}")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        os.remove(zip_path)
        logger.info("Extraction completed and ZIP file removed.")
    except Exception as e:
        logger.error(f"Failed to download or extract ZIP file: {e}")

# Step 2: Parse XML and flatten data
def parse_xml_to_dataframe(xml_path):
    logger.info(f"Parsing XML file: {xml_path}")
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        data = []

        # Loop through each 'Indvl' element
        for indvl in root.findall(".//Indvl"):
            indvl_data = {
                "indvlPK": indvl.find("Info").attrib.get("indvlPK", ""),
                "lastNm": indvl.find("Info").attrib.get("lastNm", ""),
                "firstNm": indvl.find("Info").attrib.get("firstNm", ""),
                "midNm": indvl.find("Info").attrib.get("midNm", ""),
                "sufNm": indvl.find("Info").attrib.get("sufNm", ""),
                "actvAGReg": indvl.find("Info").attrib.get("actvAGReg", ""),
                "link": indvl.find("Info").attrib.get("link", ""),
            }

            # Process Current Employers
            for crnt_emp in indvl.findall(".//CrntEmps/CrntEmp"):
                emp_data = indvl_data.copy()
                emp_data.update(
                    {
                        "orgNm": crnt_emp.attrib.get("orgNm", ""),
                        "orgPK": crnt_emp.attrib.get("orgPK", ""),
                        "city": crnt_emp.attrib.get("city", ""),
                        "state": crnt_emp.attrib.get("state", ""),
                    }
                )

                # Process Current Registrations
                for crnt_rgstn in crnt_emp.findall(".//CrntRgstns/CrntRgstn"):
                    reg_data = emp_data.copy()
                    reg_data.update(
                        {
                            "regAuth": crnt_rgstn.attrib.get("regAuth", ""),
                            "regCat": crnt_rgstn.attrib.get("regCat", ""),
                            "st": crnt_rgstn.attrib.get("st", ""),
                            "stDt": crnt_rgstn.attrib.get("stDt", ""),
                        }
                    )
                    data.append(reg_data)

            # Process Exams
            for exm in indvl.findall(".//Exms/Exm"):
                exam_data = indvl_data.copy()
                exam_data.update(
                    {
                        "exmCd": exm.attrib.get("exmCd", ""),
                        "exmNm": exm.attrib.get("exmNm", ""),
                        "exmDt": exm.attrib.get("exmDt", ""),
                    }
                )
                data.append(exam_data)

        logger.info(f"Completed parsing XML file: {xml_path}")
        return pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Error parsing XML file {xml_path}: {e}")
        return pd.DataFrame()

# Step 3: Process all XML files and save to CSV
def process_folder_to_csv(folder_path, output_csv="flattened_data.csv"):
    all_data = pd.DataFrame()

    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            xml_path = os.path.join(folder_path, filename)
            df = parse_xml_to_dataframe(xml_path)
            all_data = pd.concat([all_data, df], ignore_index=True)
            logger.info(f"Data from {filename} added to DataFrame.")

    try:
        all_data.to_csv(output_csv, index=False)
        logger.info(f"All data successfully saved to {output_csv}")
    except Exception as e:
        logger.error(f"Failed to save data to CSV: {e}")

# Step 4: Run the full pipeline
folder_path = "extracted_xml"

# Download and extract XML files using the HARDCODED URL
download_and_extract_zip(HARDCODED_URL, extract_to=folder_path)

# Process XML files in the specified folder and export to CSV
process_folder_to_csv(folder_path)
