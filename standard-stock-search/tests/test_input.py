import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from read_input import read
FIXTURES=Path(sys.argv.pop(1))

class InputTests(unittest.TestCase):
    def test_valid_text_identifiers(self):
        r=read(FIXTURES/'valid.xlsx')[0]
        self.assertEqual(r['id'],'001')
        self.assertEqual(r['model'],'001-A')
        self.assertEqual(r['city'],'上海')

    def test_invalid_inputs(self):
        for name in ['missing_city','duplicate','negative','numeric_model','no_model','formula']:
            with self.subTest(name=name),self.assertRaises(ValueError):
                read(FIXTURES/(name+'.xlsx'))

    def test_batch_pending_and_duplicate_rows(self):
        mixed=read(FIXTURES/'mixed.xlsx',batch=True)
        self.assertEqual(len(mixed['requests']),2)
        self.assertEqual(mixed['requests'][0]['id'],'001')
        self.assertNotIn('status',mixed['requests'][0])
        self.assertEqual(mixed['requests'][1]['status'],'待补充')
        self.assertEqual(mixed['requests'][1]['id'],'002')
        task=read(FIXTURES/'missing_city.xlsx',batch=True)
        self.assertEqual(len(task['requests']),1)
        self.assertEqual(task['requests'][0]['status'],'待补充')
        self.assertTrue(task['questions'])
        task=read(FIXTURES/'duplicate.xlsx',batch=True)
        self.assertEqual(len(task['requests']),2)
        self.assertEqual(len({r['id'] for r in task['requests']}),2)
        self.assertTrue(all(r['status']=='待补充' for r in task['requests']))

if __name__=='__main__':unittest.main()
