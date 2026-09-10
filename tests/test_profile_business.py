import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from contextlib import redirect_stdout
spec=importlib.util.spec_from_file_location('icons',Path(__file__).parents[1]/'scripts/gen_image.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class CredentialTests(unittest.TestCase):
    def test_actual_client_consumes_profile_key_without_printing_it(self):
        def response(request,**kwargs):
            self.assertEqual(request.get_header('Authorization'),'Bearer TEST_ONLY_ICON')
            return io.BytesIO(json.dumps({'data':[{'b64_json':'dGVzdA=='}]}).encode())
        with tempfile.TemporaryDirectory() as directory,patch.dict(os.environ,{'OPENAI_API_KEY':'TEST_ONLY_ICON'}),patch.object(sys,'argv',['gen_image','--prompt','test','--out',str(Path(directory)/'out.png')]),patch.object(module.urllib.request,'urlopen',side_effect=response),redirect_stdout(io.StringIO()) as out:
            module.main()
            self.assertNotIn('TEST_ONLY_ICON',out.getvalue())
            self.assertEqual((Path(directory)/'out.png').read_bytes(),b'test')
