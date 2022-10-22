import typing as t

import grpc
from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse
from google.protobuf.json_format import MessageToDict

import proto.todo_pb2
import proto.todo_pb2_grpc

app = FastAPI()


async def grpc_channel():
    channel = grpc.aio.insecure_channel("localhost:50051")
    client = proto.todo_pb2_grpc.TodoServiceStub(channel)
    return client


@app.get("/")
async def list_todos(client: t.Any = Depends(grpc_channel)) -> JSONResponse:
    todos = await client.ListTodos(proto.todo_pb2.ListTodosRequest())
    return JSONResponse(MessageToDict(todos))


@app.get("/{id:int}")
async def single_todo(
    id: int,
    client: t.Any = Depends(grpc_channel),
) -> JSONResponse:
    todo = await client.ReadTodo(proto.todo_pb2.ReadTodoRequest(id=id))
    return JSONResponse(MessageToDict(todo))


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(
    name: str,
    completed: bool,
    client: t.Any = Depends(grpc_channel),
) -> JSONResponse:
    todo = await client.CreateTodo(
        proto.todo_pb2.CreateTodoRequest(
            name=name,
            completed=completed,
        )
    )
    return JSONResponse(MessageToDict(todo))


@app.patch("/{id:int}")
async def update_todo(
    id: int,
    name: str,
    completed: bool,
    client: t.Any = Depends(grpc_channel),
) -> JSONResponse:
    todo = await client.UpdateTodo(
        proto.todo_pb2.UpdateTodoRequest(
            id=id,
            name=name,
            completed=completed,
        )
    )
    return JSONResponse(MessageToDict(todo))


@app.delete("/{id:int}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: int, client: t.Any = Depends(grpc_channel)) -> None:
    await client.DeleteTodo(proto.todo_pb2.DeleteTodoRequest(id=id))
