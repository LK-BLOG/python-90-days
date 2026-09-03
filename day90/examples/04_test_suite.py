# Day 90 示例 4: 测试套件
class TestSuite:
    def __init__(self, runtime): self.runtime = runtime; self.results = []
    def test_basic(self):
        try: r = self.runtime.run('1+1'); return {'test': 'basic', 'passed': r is not None}
        except Exception as e: return {'test': 'basic', 'passed': False, 'error': str(e)}
    def test_tools(self):
        passed = hasattr(self.runtime, 'tools') and len(self.runtime.tools) > 0
        return {'test': 'tools', 'passed': passed}
    def test_safety(self):
        if hasattr(self.runtime, 'safety'):
            ok, _ = self.runtime.safety.validate_input('test')
            return {'test': 'safety', 'passed': ok}
        return {'test': 'safety', 'passed': False}
    def run_all(self):
        self.results = [self.test_basic(), self.test_tools(), self.test_safety()]
        passed = sum(1 for r in self.results if r['passed'])
        return {'total': len(self.results), 'passed': passed, 'score': f'{passed/len(self.results)*100:.0f}%'}

if __name__ == '__main__':
    class MockRuntime:
        tools = {'calc': None}
        class safety:
            @staticmethod
            def validate_input(t): return True, 'OK'
        def run(self, t): return 'ok'
    suite = TestSuite(MockRuntime())
    print(suite.run_all())
