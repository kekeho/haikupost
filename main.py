import fastapi
from fastapi import HTTPException
import db
import schema
import bcrypt
import json
from sqlalchemy.orm import sessionmaker
from typing import List


with open("config.json") as f:
    j = json.load(f)

    hp = j.get("password")
    if hp is None:
        raise ValueError('HAIKU_HASHED_PASSWORD not found in os environment')
    HASHED_PASSWORD = hp.encode()

app = fastapi.FastAPI()


db.Base.metadata.create_all(bind=db.db_engine)


@app.get('/')
def get(offset: int = 0, limit: int = 50) -> List[schema.Haiku]:
    s = sessionmaker(bind=db.db_engine)()
    haikulist = s.query(db.Haiku).order_by(db.Haiku.id.desc()).offset(offset).limit(limit)

    result: List[schema.Haiku] = []
    for db_h in haikulist:
        h = schema.Haiku(
            id=db_h.id, content=db_h.content,
            created_at=db_h.created_at
        )
        result.append(h)

    return result


@app.post('/post')
def post(haikupost: schema.HaikuPost):
    passcheck = bcrypt.checkpw(
        password=haikupost.password.encode(),
        hashed_password=HASHED_PASSWORD
    )
    if passcheck is False:
        raise HTTPException(
            status_code=401,
            detail="Password check is failed."
        )
    # TODO: password auth
    s = sessionmaker(bind=db.db_engine)()
    h = db.Haiku()
    h.content = haikupost.haiku
    s.add(h)
    s.commit()


@app.delete('/')
def delete(id: int):
    s = sessionmaker(bind=db.db_engine)()
    h = s.query(db.Haiku).get(id)
    if h is None:
        raise HTTPException(
            status_code=404, detail="Not Found"
        )
    s.delete(h)
    s.commit()
