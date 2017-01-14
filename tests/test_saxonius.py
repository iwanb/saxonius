import unittest
from saxonius import *

class TestXQuery(unittest.TestCase):
    def setUp(self):
        p = Processor()
        self.p = p
    def test_xquery(self):
        xqc = self.p.xquery_compiler()
        v = xqc.compile('1 to 10').evaluate()
        assert isinstance(v, XdmValue)
        self.assertEqual(str(v), "\n".join(map(str, range(1, 11))))
        v = xqc.compile('1 to 9').evaluate()
        for (vx, vr) in zip(v, range(1, 10)):
            self.assertEqual(str(vx), str(vr))
    def test_single(self):
        xqc = self.p.xquery_compiler()
        v = xqc.compile('1 to 10').evaluate_single()
        assert isinstance(v, XdmItem)
        self.assertEqual(str(v), "1")
    def test_compile(self):
        xqc = self.p.xquery_compiler()
        with self.assertRaises(SaxonApiError):
            xqc.compile('Something invalid')
    def test_context(self):
        xqc = self.p.xquery_compiler()
        c = self.p.document_build('<nodes><node>Hello</node><node>world</node></nodes>')
        v = xqc.compile('/nodes/node/text()').evaluate(context_item=c)
        self.assertEqual(str(v), "Hello\nworld")
        self.assertEqual(str(v[0]), "Hello")
        with self.assertRaises(IndexError):
            v[2]

if __name__ == '__main__':
    unittest.main()
