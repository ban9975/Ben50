import pandas as pd
import os
from ElbowKnee_all_nSensors import *
import openpyxl

gestureDict = {"down": 0, "up": 1, "open": 2}


def loadRawDataFile(fileName: str, sheetName: list[str] = []) -> tuple[list[pd.DataFrame], list[str]]:
    data = []
    xls = pd.ExcelFile(
        os.path.join(os.getcwd(), "Excel_data/v8/Time_series", f"{fileName}.xlsx")
    )
    if sheetName == []:
        sheetName = xls.sheet_names
    for name in sheetName:
        data.append(xls.parse(name))
    return data, sheetName


def translateRawData(fileName: str):
    workbook = openpyxl.load_workbook(fileName)
    for sheet in workbook.worksheets:
        if sheet.title == "Sheet":
            workbook.remove(sheet)
            continue
        for cell in sheet["A"]:
            if cell.value == 999 or cell.value == "neutral":
                cell.value = -1
            elif cell.value == "down":
                cell.value = 0
            elif cell.value == "up":
                cell.value = 1
            elif cell.value == "open":
                cell.value = 2
    workbook.save(fileName)


if __name__ == "__main__":
    # exportEKFile('band2_0115', 'band2_0115_processed')
    translateRawData(
        os.path.join(
            os.getcwd(), "Excel_data/v8/Time_series/rick/raw_data/band4_0128.xlsx"
        )
    )
