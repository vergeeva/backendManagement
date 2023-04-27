from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from app.routers import users, auth, balanceCircle, userLists, typeOfCards, technicsSettings, taskInCards, kanbanCards, \
    ganttChartTasks, ganttChartTaskDuration, entryDailyPlanner, tasksList
from app.mail import email

app = FastAPI()


@app.get('/')
def root():
    return {'message': 'Hello World'}


@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*, *"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    # response.headers["Set-Cookie"] = "access_token, refresh_token,logged_in"
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(users.router, tags=['Users'], prefix='/api/users')
app.include_router(balanceCircle.router, tags=['Balance'], prefix='/api/balanceCircle')
app.include_router(userLists.router, tags=['userLists'], prefix='/api/userLists')
app.include_router(tasksList.router, tags=['tasksList'], prefix='/api/tasksList')
app.include_router(typeOfCards.router, tags=['typeOfCards'], prefix='/api/typeOfCards')
app.include_router(technicsSettings.router, tags=['technicsSettings'], prefix='/api/technicsSettings')
app.include_router(taskInCards.router, tags=['taskInCards'], prefix='/api/taskInCards')
app.include_router(kanbanCards.router, tags=['kanbanCards'], prefix='/api/kanbanCards')
app.include_router(ganttChartTasks.router, tags=['ganttChartTasks'], prefix='/api/ganttChartTasks')
app.include_router(ganttChartTaskDuration.router, tags=['ganttChartTaskDuration'], prefix='/api/ganttChartTaskDuration')
app.include_router(entryDailyPlanner.router, tags=['entryDailyPlanner'], prefix='/api/entryDailyPlanner')

app.include_router(email.router, tags=['email'], prefix='/email')