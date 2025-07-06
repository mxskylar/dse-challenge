# Mobilize Event Pipelines

# Ingest Mobilize Events

Caches Mobilize event data so that it can later be inserted into GBQ offline.

To run the pipeline:
```bash
python ingest_mobilize_pipeline.py
```

# Insert GBQ Pipeline

Inserts cached Mobilize event data into GBQ. Can run offline.

To run the pipeline:
```bash
python insert_gbq_pipeline.py
```