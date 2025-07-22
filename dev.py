from watchfiles import run_process, DefaultFilter

class PythonOnlyFilter(DefaultFilter):
    def __call__(self, change, path: str) -> bool:
        return path.endswith('.py')

if __name__ == '__main__':
    run_process('main.py', target='python main.py', watch_filter=PythonOnlyFilter())