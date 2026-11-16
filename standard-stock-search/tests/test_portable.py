import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from openpyxl import load_workbook

BASE=Path(__file__).resolve().parents[1]

class PortableTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.skill=self.root/'isolated-skill';self.skill.mkdir()
        for name in json.loads((BASE/'manifest.json').read_text()):
            dest=self.skill/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(BASE/name,dest)
        self.request={'id':'001','name':'模拟商品','brand':'模拟品牌','model':'0001-A','quantity':20,'unit':'个','country':'中国','city':'武汉'}
        c={'complete':True,'queries':['离线模拟'],'scope':'测试','stop_reason':'测试完成'}
        self.task={'requests':[self.request],'quotes':[{'request_id':'001','channel':'模拟渠道','region':'CN','brand':'模拟品牌','model':'0001-A','url':'https://example.com/test','checked_at':'2026-11-15T10:00:00+08:00','evidence':'模拟记录，非真实报价','exact':True,'original_verified':True,'conditions_met':True,'pack_units':10,'stock_packs':3,'moq_packs':1,'multiple_packs':1,'price_pack':100,'currency':'CNY','tier_min_packs':1,'tax':'含税','notes':'=1+1'}],'coverage':{'001':{'mainland':c}}}
        (self.root/'task.json').write_text(json.dumps(self.task,ensure_ascii=False))

    def tearDown(self):self.tmp.cleanup()

    def run_cli(self,*args):
        return subprocess.run([sys.executable,str(self.skill/'scripts/workbook_portable.py'),*map(str,args)],cwd=self.skill,capture_output=True,text=True)

    def test_no_artifact_runtime(self):
        p=subprocess.run([sys.executable,str(self.skill/'scripts/check_runtime.py')],cwd=self.skill,capture_output=True,text=True)
        state=json.loads(p.stdout)
        self.assertEqual(p.returncode,0)
        self.assertEqual(state['checks']['excel_generator']['backend'],'portable-python')

    def test_report_matches_shared_data(self):
        output=self.root/'report.xlsx'
        p=self.run_cli('report',self.root/'task.json',output);self.assertEqual(p.returncode,0,p.stderr)
        model=json.loads(subprocess.check_output(['node',str(self.skill/'scripts/export_data.mjs'),'report',str(self.root/'task.json')],text=True))
        w=load_workbook(output);self.assertEqual(w.sheetnames,[s['name'] for s in model])
        for spec in model:
            ws=w[spec['name']]
            self.assertEqual([ws.cell(4,i+1).value for i in range(len(spec['labels']))],spec['labels'])
            for i,row in enumerate(spec['rows'],5):
                for j,value in enumerate(row,1):
                    cell=ws.cell(i,j);self.assertEqual(cell.value,value or None if value=='' else value)
                    self.assertEqual(cell.alignment.horizontal,'center');self.assertEqual(cell.alignment.vertical,'center')
        ws=w['渠道报价明细'];self.assertEqual(ws['A5'].value,'001');self.assertEqual(ws['G5'].value,'0001-A');self.assertEqual(ws['N5'].value,10)
        self.assertEqual(ws['AH5'].value,'=1+1');self.assertEqual(ws['AH5'].data_type,'s')
        before=output.read_bytes();self.assertNotEqual(self.run_cli('report',self.root/'task.json',output).returncode,0);self.assertEqual(before,output.read_bytes())

    def test_questions_leave_decisions_blank(self):
        qs={'questions':[{'issue_id':f'Q{i}','request_id':f'P{i}','question':'是否允许拼单'} for i in range(6)]}
        p=self.root/'questions.json';p.write_text(json.dumps(qs));out=self.root/'questions.xlsx'
        result=self.run_cli('questions',p,out);self.assertEqual(result.returncode,0,result.stderr)
        ws=load_workbook(out)['待确认清单'];self.assertEqual(ws.max_row,10)
        self.assertTrue(all(ws.cell(i,6).value is None for i in range(5,11)))

    def test_incomplete_search_refused_without_output(self):
        self.task['coverage']={};(self.root/'task.json').write_text(json.dumps(self.task));out=self.root/'invalid.xlsx'
        self.assertNotEqual(self.run_cli('report',self.root/'task.json',out).returncode,0);self.assertFalse(out.exists())

    def test_template_byte_identical(self):
        out=self.root/'blank.xlsx';self.assertEqual(self.run_cli('template',out).returncode,0)
        self.assertEqual(out.read_bytes(),(BASE/'assets/采购需求模板.xlsx').read_bytes())

if __name__=='__main__':unittest.main()
