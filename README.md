Reproducer for https://github.com/python/cpython/issues/92810

pip install -r requirements.txt

pytest test_performance.py --profile --log-cli-level=INFO
pytest test_performance_fix.py --profile --log-cli-level=INFO
