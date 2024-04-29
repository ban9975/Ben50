import pandas as pd


def dataPartition(
    oriData: pd.DataFrame, split: float
) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = []
    partitionSize = int(split * oriData.shape[0])
    data.append(oriData[:partitionSize].reset_index(drop=True))
    data.append(oriData[partitionSize:].reset_index(drop=True))
    return tuple(data)


def fullFileDataPartition(
    oriData: list[pd.DataFrame], split: float
) -> tuple[list[pd.DataFrame], list[pd.DataFrame]]:
    data = [[], []]
    for od in oriData:
        partition = dataPartition(od, split)
        data[0].append(partition[0])
        data[1].append(partition[1])
    return tuple(data)
