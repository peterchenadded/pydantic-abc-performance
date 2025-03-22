Reproducer for https://github.com/python/cpython/issues/92810

```python
pip install -r requirements.txt

# Run below it takes long time
pytest test_performance.py --log-cli-level=INFO

# Run below it takes seconds
pytest test_performance_fix.py --log-cli-level=INFO
```
