# DTrades Solutions

PTrans

## Build

- clone this repository
- make a python virtual environement
```bash
python3 -m venv env
```

- activate the virtual environement
```bash
source env/bin/activate
```

- install dependencies
```bash
pip install -r requirements.txt
```

- train the model
```bash
cd training
python AAPL.py
```

joblib files are now available in `training/` folder

## Run

- make env file. e.g. `init_env_vars.sh`
```
#!/bin/bash

# Reddit API
export CLIENT_ID='<client id>'
export CLIENT_SECRET='<client secret>'
export USER_AGENT='<username>'
```

- make it executable
```bash
chmod +x init_env_vars.sh
```

- run it
```bash
. production/init_env_vars.sh
```

- run app

```bash
./production/news_predictor.py
```

