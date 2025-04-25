from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Task model
class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

# In-memory task list
tasks: List[Task] = []

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo List API!"}

# Create task
@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    for t in tasks:
        if t.id == task.id:
            raise HTTPException(status_code=400, detail="Task with this ID already exists")
    tasks.append(task)
    return task

# Get all tasks
@app.get("/tasks/", response_model=List[Task])
def get_tasks():
    return tasks

# Get single task by ID
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# Update a task
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            tasks[idx] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

# Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(idx)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
