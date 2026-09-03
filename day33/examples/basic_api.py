\"\"\"FastAPI 基础示例\"\"\"

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Task API", version="0.1.0")

# 数据模型
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    priority: int = Field(0, ge=0, le=5)

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: int
    completed: bool

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None

# 内存存储
tasks_db: list[dict] = []
next_id = 1

@app.get("/")
async def root():
    return {"message": "Task API v0.1"}

@app.get("/tasks", response_model=list[TaskResponse])
async def list_tasks(completed: Optional[bool] = None):
    result = tasks_db
    if completed is not None:
        result = [t for t in result if t["completed"] == completed]
    return result

@app.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate):
    global next_id
    new_task = {"id": next_id, "completed": False, **task.model_dump()}
    tasks_db.append(new_task)
    next_id += 1
    return new_task

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, updates: TaskUpdate):
    for task in tasks_db:
        if task["id"] == task_id:
            update_data = updates.model_dump(exclude_unset=True)
            task.update(update_data)
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    global tasks_db
    original_len = len(tasks_db)
    tasks_db = [t for t in tasks_db if t["id"] != task_id]
    if len(tasks_db) == original_len:
        raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
