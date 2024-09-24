import logging
import argparse
import os
import time
from glob import glob
from prometheus_client import start_http_server, Gauge

# Logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Setting the arguments
parser = argparse.ArgumentParser()

# required arg
parser.add_argument('-f', '--folder', required=True, help="target folder")
args = parser.parse_args()

class CustomExporter:
    def __init__(self, folder:str) -> None:
        self.folder = folder
        self.metric_dict = {}
        

    def count_file_in_folder(self) -> int:
        '''
        DOCSTRING: Count the number of files 
        INPUT: folder:str
        OUTPUT: number (int)
        '''
        try:
            # Check if folder exists and is a directory
            if not os.path.isdir(self.folder):
                raise FileNotFoundError(f"The directory '{self.folder}' does not exist.")
            
            lst = os.listdir(self.folder)
            logging.info(f'Founds {len(lst)} file(s) in folder {self.folder}')
            return len(lst)

        except FileNotFoundError as fnf_error:
            logging.error(fnf_error)
            raise
        
        except PermissionError as perm_error:
            logging.error(f"Permission denied: {perm_error}")
            raise

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise


    def create_gauge_for_metric(self, metric_name):
        if self.metric_dict.get(metric_name) is None:
            self.metric_dict[metric_name] = Gauge(metric_name, f"number of files in {self.folder}")
    
    def set_value(self, metric_name):
        self.metric_dict[metric_name].set(self.count_file_in_folder())

    def main(self):
        exporter_port = int(os.environ.get("EXPORTER_PORT", "9877"))
        start_http_server(exporter_port)
        if '.' in self.folder or '-' in self.folder:
            metric_folder_name_dot=self.folder.replace('.', '/')
            metric_folder_name=metric_folder_name_dot.replace('-', '/')    
            metric_name = f"cust_files_in{metric_folder_name.replace('/', '_')}"
        else:
            metric_name = f"cust_files_in{self.folder.replace('/', '_')}"
        
        while True:
            self.create_gauge_for_metric(metric_name)
            self.set_value(metric_name)
            time.sleep(10)

if __name__ == "__main__":
    folder = args.folder
    c = CustomExporter(folder)
    c.main()
