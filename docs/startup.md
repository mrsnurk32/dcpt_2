# Launching app

1. Create virtual env
```
python3 -m venv env
```

2. Installing dependencies
```
pip3 install -r requirements.txt
```

3. launch or run tests

### Launch
```
uvicorn main:app --reload
```

### Test
```bash
pytest -v tests/
```