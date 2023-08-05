from .Setup_Connection import setup
from importlib import import_module
import os
from ...generic import Logger

def initLogger(output_directory, study_region):
    path = output_directory + '/' + study_region
    if not os.path.exists(path):
        os.mkdir(path)
    logger = Logger()
    logger.create(path)
    return logger

def export(inputObj):
    """ Exports data from Hazus legacy. Can export CSVs, Shapefiles, PDF Reports, and Jsondatetime A combination of a date and a time.
    
    Keyword arguments:
        inputObj: dictionary -- {
            opt_csv: boolean -- export CSVs |
            opt_shp: boolean -- export Shapefile(s) |
            opt_report: boolean -- export report |
            opt_json: boolean -- export Json |
            study_region: str -- name of the Hazus study region (HPR name) |
            ?title: str -- title on the report |
            ?meta: str -- sub-title on the report (ex: Shakemap v5) |
            output_directory: str -- directory location for the outputs
        }
    """

    logger = initLogger(inputObj['output_directory'], inputObj['study_region'])
    logger.log('Establishing connection to SQL Server')
    comp_name, cnxn, date, modules = setup(inputObj)
    logger.log('Connection established and modules identified')
    inputObj.update({'created': date})
    logger.log('Importing result module')
    result_module = import_module('.'+modules['result_module'], package='hazus.legacy.exporting.results')
    logger.log('Result module imported')
    logger.log('Fetching data from SQL Server')
    hazus_results_dict, subcounty_results, county_results, damaged_essential_facilities = result_module.read_sql(comp_name, cnxn, inputObj)
    logger.log('SQL quiries returned and data parsed')
    if inputObj['opt_csv']:
        logger.log('Exporting CSVs')
        result_module.to_csv(hazus_results_dict, subcounty_results, county_results, damaged_essential_facilities, inputObj)
        logger.log('CSVs saved')
    if inputObj['opt_shp']:
        logger.log('Exporting Shapefile(s)')
        gdf = result_module.to_shp(inputObj, hazus_results_dict, subcounty_results)
        logger.log('Shapefile(s) saved')
    if inputObj['opt_report']:
        try:
            len(gdf)
        except:
            logger.log('Creating gdf for report')
            gdf = result_module.to_shp(inputObj, hazus_results_dict, subcounty_results)
            logger.log('Gdf created')
        logger.log('Importing report module')
        report_module = import_module('.'+modules['report_module'], package='hazus.legacy.exporting.reports')
        logger.log('Report module imported')
        logger.log('Creating and exporting report')
        report_module.generate_report(gdf, hazus_results_dict, subcounty_results, county_results, inputObj)
        logger.destroy()

class Exporting():
    """ Export class for Hazus legacy. Can export CSVs, Shapefiles, PDF Reports, and Jsondatetime A combination of a date and a time.
    
    Keyword arguments:
        inputObj: dictionary -- {
            opt_csv: boolean -- export CSVs |
            opt_shp: boolean -- export Shapefile(s) |
            opt_report: boolean -- export report |
            opt_json: boolean -- export Json |
            study_region: str -- name of the Hazus study region (HPR name) |
            ?title: str -- title on the report |
            ?meta: str -- sub-title on the report (ex: Shakemap v5) |
            output_directory: str -- directory location for the outputs
        }
    """
    def __init__(self, inputObj):
        self.inputObj = inputObj
        self.logger = Logger()
    
    def setup(self):
        self.comp_name, self.cnxn, self.date, self.modules = setup(self.inputObj)
        self.inputObj.update({'created': self.date})
        self.result_module = import_module('.'+modules['result_module'], package='hazus.legacy.exporting.results')

    def getData(self):
        self.hazus_results_dict, self.subcounty_results, self.county_results, self.damaged_essential_facilities = self.result_module.read_sql(self.comp_name, self.cnxn, self.inputObj)
    
    def toCSV(self):
        self.result_module.to_csv(self.hazus_results_dict, self.subcounty_results, self.county_results, self.damaged_essential_facilities, self.inputObj)

    def toShapefile(self):
        self.gdf = self.result_module.to_shp(self.inputObj, self.hazus_results_dict, self.subcounty_results)
    
    def toReport(self):
        try:
            len(self.gdf)
        except:
            self.toShapefile()
        self.report_module = import_module('.'+modules['report_module'], package='hazus.legacy.exporting.reports')
        self.report_module.generate_report(self.gdf, self.hazus_results_dict, self.subcounty_results, self.county_results, self.inputObj)

