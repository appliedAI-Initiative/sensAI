import logging

import pandas as pd
import pytest
import sklearn.datasets

from sensai import InputOutputData, VectorClassificationModel
from sensai.evaluation import VectorClassificationModelEvaluator

log = logging.getLogger(__name__)


class IrisDataSet:
    _iod = None

    @classmethod
    def getInputOutputData(cls):
        if cls._iod is None:
            d = sklearn.datasets.load_iris()
            inputs = pd.DataFrame(d["data"], columns=d["feature_names"])
            targetNames = d["target_names"]
            outputs = pd.DataFrame({"class": [targetNames[x] for x in d["target"]]})
            cls._iod = InputOutputData(inputs, outputs)
        return cls._iod


class ClassificationTestCase:
    def __init__(self, data: InputOutputData):
        self.data = data

    def testMinAccuracy(self, model: VectorClassificationModel, minAccuracy: float):
        ev = VectorClassificationModelEvaluator(self.data, testFraction=0.2)
        ev.fitModel(model)
        resultData = ev.evalModel(model)
        stats = resultData.getEvalStats()
        #stats.plotConfusionMatrix().savefig("cmat.png")
        log.info(f"Results for {model.getName()}: {stats}")
        assert stats.getAccuracy() >= minAccuracy


@pytest.fixture(scope="session")
def irisDataSet():
    return IrisDataSet()


@pytest.fixture(scope="session")
def irisClassificationTestCase(irisDataSet):
    return ClassificationTestCase(irisDataSet.getInputOutputData())
