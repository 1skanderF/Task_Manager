from pydantic import BaseModel, ConfigDict, Field

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    tag: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    tag: str | None = None


class TagOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class TasksOut(BaseModel):
    id: int
    user_task_number: int
    title: str
    description: str | None
    tag: TagOut | None = None
    model_config = ConfigDict(from_attributes=True)

class Filter(BaseModel):
    tag: str | None = None
    limit: int = Field(default=10, ge=1, le=20)