import importlib.util
from pathlib import Path
import tempfile
import unittest
import hashlib

source=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('installer',source/'scripts/install_agent.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class InstallTests(unittest.TestCase):
    def test_profiles_and_refusal(self):
        for agent,directory in m.PROFILES.items():
            with self.subTest(agent=agent),tempfile.TemporaryDirectory() as t:
                p=Path(t)/'项目 with spaces';p.mkdir()
                preview=m.install(agent,p)
                self.assertFalse(Path(preview['target']).exists())
                result=m.install(agent,p,True)
                target=Path(result['target'])
                self.assertEqual(target,p.resolve()/directory/'skills/standard-stock-search')
                self.assertTrue((target/'assets/采购需求模板.xlsx').is_file())
                self.assertFalse((target/'node_modules').exists())
                before=hashlib.sha256((target/'SKILL.md').read_bytes()).digest()
                with self.assertRaises(ValueError):m.install(agent,p,True)
                self.assertEqual(before,hashlib.sha256((target/'SKILL.md').read_bytes()).digest())

    def test_missing_resource_before_write(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);src=root/'source';src.mkdir();project=root/'project';project.mkdir()
            (src/'manifest.json').write_text('["missing.txt"]')
            with self.assertRaises(ValueError):m.install('comate',project,True,src)
            self.assertFalse((project/'.comate').exists())

    def test_desktop_not_qwen_code(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(ValueError):m.install('qwen-desktop',t,True)

if __name__=='__main__':unittest.main()
