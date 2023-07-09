import asyncio
import logging

from grpc import aio

import proto.todo_pb2
import proto.todo_pb2_grpc
from piccolo.columns import Boolean, Varchar
from piccolo.table import Table, create_db_tables
from piccolo_conf import DB


class Todo(Table, db=DB):
    name = Varchar()
    completed = Boolean(default=False)


class TodoService(proto.todo_pb2_grpc.TodoServiceServicer):
    # all todos
    async def ListTodos(self, request, context):
        todo = await Todo.select()
        return proto.todo_pb2.ListTodosResponse(todos=todo)

    # single todo
    async def ReadTodo(self, request, context):
        todo = await Todo.select().where(Todo.id == request.id).first()
        return proto.todo_pb2.ReadTodoResponse(todo=todo)

    # create todo
    async def CreateTodo(self, request, context):
        todo = await Todo.insert(
            Todo(name=request.name, completed=request.completed)
        )
        return proto.todo_pb2.CreateTodoResponse(todo=todo[0])

    # update todo
    async def UpdateTodo(self, request, context):
        await Todo.update(
            {Todo.name: request.name, Todo.completed: request.completed}
        ).where(Todo.id == request.id)
        todo = await Todo.select().where(Todo.id == request.id).first()
        return proto.todo_pb2.UpdateTodoResponse(todo=todo)

    # delete todo
    async def DeleteTodo(self, request, context):
        await Todo.delete().where(Todo.id == request.id)
        return proto.todo_pb2.DeleteTodoResponse(success=True)


async def serve():
    server = aio.server()
    listen_addr = "[::]:50051"
    proto.todo_pb2_grpc.add_TodoServiceServicer_to_server(
        TodoService(), server
    )
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    # Table creating
    await create_db_tables(
        Todo,
        if_not_exists=True,
    )
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    print("gRPC server started")
    asyncio.run(serve())
