
# SEC Investment Adviser XML Feed Parser

A robust Python application that downloads, processes, and analyzes SEC Investment Adviser XML feed data, converting complex XML structures into easily analyzable CSV format.

The link for XML endpoint can not be dynamically generated. You must get the updated link from [the SEC website.](https://adviserinfo.sec.gov/compilation#:~:text=in%20XML%20format.-,INVESTMENT%20ADVISER%20REPRESENTATIVES%20REPORT,-Report%20as%20of)

## Overview

This application automates the process of retrieving and processing SEC Investment Adviser data by:
- Downloading XML feed data from the SEC's official website
- Handling ZIP file extraction automatically
- Parsing complex XML structures efficiently
- Converting hierarchical XML data into a flattened CSV format
- Providing comprehensive logging for process monitoring

## Technical Details

### Architecture
The application is structured into four main components:
1. Data Retrieval (`download_and_extract_zip`)
2. XML Parsing (`parse_xml_to_dataframe`)
3. Data Processing (`process_folder_to_csv`)
4. Main Execution Pipeline

### Data Structure
The parser extracts the following information:
- Individual Information:
  - `indvlPK`: Unique identifier
  - `lastNm`: Last name
  - `firstNm`: First name
  - `midNm`: Middle name
  - `sufNm`: Name suffix
  - `actvAGReg`: Active registration status
  - `link`: Related SEC link

- Employment Information:
  - `orgNm`: Organization name
  - `orgPK`: Organization identifier
  - `city`: Employment city
  - `state`: Employment state

- Registration Details:
  - `regAuth`: Registration authority
  - `regCat`: Registration category
  - `st`: State
  - `stDt`: Start date

- Examination Records:
  - `exmCd`: Exam code
  - `exmNm`: Exam name
  - `exmDt`: Exam date

## Requirements

### Python Packages
```
pandas
requests
```

## Usage

### Basic Usage
Simply run the main script:
```bash
python main.py
```

### Process Flow
1. The script downloads the ZIP file from the SEC website
2. Extracts XML files to the 'extracted_xml' directory
3. Processes all XML files in the directory
4. Generates 'flattened_data.csv' with the processed data

### Output
The resulting CSV file ('flattened_data.csv') contains all extracted data in a tabular format, making it suitable for:
- Data analysis
- Database import
- Spreadsheet manipulation
- Reporting purposes

## Error Handling and Logging

The application includes comprehensive error handling and logging:
- All major operations are logged with timestamps
- Error messages include detailed information for troubleshooting
- Log levels: INFO for normal operations, ERROR for issues
- Console output provides real-time process status

## Performance Considerations

- Uses `iterparse` for memory-efficient XML processing
- Implements batch processing for large XML files
- Optimized DataFrame operations for better performance

## Limitations

- Requires stable internet connection for initial data download
- Processing time depends on the size of XML feed
- Memory usage scales with input data size
- Link for XML endpoint can not be dynamically generated

## License

This project is available under the MIT License. See the LICENSE file for details.
