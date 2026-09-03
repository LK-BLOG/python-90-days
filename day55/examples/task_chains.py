\"\"\"任务链和工作流\"\"\"

from celery import Celery, chain, group, chord

celery_app = Celery(
    \"workflows\",
    broker=\"redis://localhost:6379/1\",
    backend=\"redis://localhost:3179/2\",
)


@celery_app.task
def extract(url: str) -> dict:
    print(f\"Extracting data from {url}\")
    return {\"source\": url, \"records\": [1, 2, 3, 4, 5]}


@celery_app.task
def transform(data: dict) -> dict:
    print(f\"Transforming {len(data.get('records', []))} records\")
    data[\"records\"] = [r * 2 for r in data.get(\"records\", [])]
    return data


@celery_app.task
def validate(data: dict) -> dict:
    print(\"Validating data...\")
    data[\"valid\"] = True
    return data


@celery_app.task
def load(data: dict) -> str:
    print(f\"Loading {len(data.get('records', []))} records to DB\")
    return f\"Loaded {len(data.get('records', []))} records\"


@celery_app.task
def aggregate(results: list) -> dict:
    print(f\"Aggregating {len(results)} results\")
    return {\"total\": sum(r for r in results if isinstance(r, (int, float)))}


# 工作流示例
def run_etl_pipeline(url: str):
    \"\"\"ETL管道: extract -> transform -> validate -> load\"\"\"
    workflow = chain(
        extract.s(url),
        transform.s(),
        validate.s(),
        load.s(),
    )
    return workflow.apply_async()


def run_parallel_processing(items: list):
    \"\"\"并行处理\"\"\"
    workflow = group(
        transform.s({\"records\": [item]}) for item in items
    )
    return workflow.apply_async()


def run_parallel_with_aggregation(data: dict):
    \"\"\"并行计算 + 汇总\"\"\"
    workflow = chord(
        [transform.s({\"records\": [i]}) for i in range(10)],
        aggregate.s()
    )
    return workflow.apply_async()
