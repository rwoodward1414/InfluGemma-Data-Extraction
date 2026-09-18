# Data Extraction Unit

This unit of InfluGemma sets up the database, collects, processes, and cleans data to be used by the model.

InfluGemma-Data-Extraction/
├── database/
│   ├── database_connect.py
│   ├── datebase_update.py
│   └── init.sql
├── demographic-data/
│   ├── demo.py
│   └── us_demo.sh
├── docker-compose.yml
├── helper/
│   └── states.py
├── LICENSE
├── README.md
├── scripts/
│   ├── googletrends.py
├── surveillence-data/
│   ├── data/
│   ├── process_live_aus_surv.py
│   ├── process_old_aus_surv.py
│   └── process_us_surv.py
└── vaccination-data/
    ├── data/
    ├── process_aus_vacc.py
    ├── process_new_us_vacc.py
    └── process_us_vacc.py
