import pyZiagn as pz
import numpy as np
import unittest


class TestMethods(unittest.TestCase):
    Test = pz.uniaxialTensileTest()
    Test.loadExample()
    Test.changeUnits()

    def test_1_stressEng(self):
        self.Test.calcStressEng()
        self.assertAlmostEqual(self.Test.stressEng[100], 1.0)

    def test_2_strainEng(self):
        self.Test.calcStrainEng()
        self.assertAlmostEqual(self.Test.strainEng[100], 0.001)

    def test_3_stressTrue(self):
        self.Test.calcStressTrue()
        self.assertAlmostEqual(self.Test.stressTrue[100], 1.001)

    def test_4_strainTrue(self):
        self.Test.calcStrainTrue()
        self.assertAlmostEqual(self.Test.strainTrue[100], 0.0009995)

    def test_5_elasticModulus(self):
        self.Test.calcElasticModulus(strain0=0.01, strain1=0.02)
        self.assertAlmostEqual(self.Test.YoungsModulus, 1000)

    def test_6_RP02(self):
        self.Test.calcRP02()
        self.assertAlmostEqual(self.Test.stressRP02, 100.0)

    def test_7_linearLimit(self):
        self.Test.calcLinearLimit()
        self.assertAlmostEqual(self.Test.stressLinLimit, 100.0)

    def test_8_toughness(self):
        self.Test.calcToughnessModulus()
        self.assertAlmostEqual(self.Test.ToughnessModulus, 5.0)

    def test_9_resilience(self):
        self.Test.calcResilienceModulus()
        self.assertAlmostEqual(self.Test.ResilienceModulus, 5.0)


if __name__ == '__main__':
    unittest.main()
