from fastapi import FastAPI

app = FastAPI()

# @app.on_event("startup") wywoła tę funkcję automatycznie gdy serwer startuje.
# Tu będzie init_db() — odkomentuj gdy database.py będzie gotowy.
# from database import init_db
# @app.on_event("startup")
# def startup():
#     init_db()

# Router z endpointami /items podepniesz tutaj gdy routes/items.py będzie gotowy:
# from routes.items import router
# app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
