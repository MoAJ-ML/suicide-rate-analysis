import os
import tempfile
import unittest
import pandas as pd
import suicide_rate_analysis as analysis


class UnitTests(unittest.TestCase):
    def test_correlation_merge_uses_one_both_sexes_row(self):
        frame = pd.DataFrame({
            'country': ['A', 'A', 'A'], 'year': [2000] * 3,
            'sex': [' Both sexes', ' Male', ' Female'],
            'suicide_rate': [10.0, 15.0, 5.0],
        })
        with tempfile.TemporaryDirectory() as tmp:
            before = os.getcwd()
            os.chdir(tmp)
            try:
                pd.DataFrame({'country': ['A'], 'year': [2000], 'gdp_per_capita': [1000], 'population': [100]}).to_csv('gdp_population.csv', index=False)
                merged = analysis.merge_with_gdp_population(frame)
            finally:
                os.chdir(before)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged['suicide_rate'].iloc[0], 10)


if __name__ == '__main__':
    unittest.main()
