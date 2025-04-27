from typing import List
from .schema import User, Driver, Team, Race, Score
from fastapi import FastAPI
from ..database import MongoDBClient

mongo_client = MongoDBClient("mongodb://root:example@localhost:27017/", "fantasyf1")

# FastAPI app
app = FastAPI()

# Routes for Users
@app.post(
    "/users/",
    response_model=User
)
async def create_user(user: User):
    user_dict = user.model_dump(by_alias=True)
    return mongo_client.insert_one("users", user_dict)

@app.get(
    "/users/",
    response_model=List[User]
)
async def list_users():
    return mongo_client.find_all("users")

# Routes for Drivers
@app.post(
    "/drivers/",
    response_model=Driver
)
async def create_driver(driver: Driver):
    driver_dict = driver.model_dump(by_alias=True)
    return mongo_client.insert_one("drivers", driver_dict)

@app.get(
    "/drivers/",
    response_model=List[Driver])
async def list_drivers():
    return mongo_client.find_all("drivers")

# Routes for Teams
@app.post(
    "/teams/",
    response_model=Team
)
async def create_team(team: Team):
    team_dict = team.model_dump(by_alias=True)
    return mongo_client.insert_one("teams", team_dict)

@app.get(
    "/teams/",
    response_model=List[Team]
)
async def list_teams():
    return mongo_client.find_all("teams")

# Routes for Races
@app.post(
    "/races/",
    response_model=Race
)
async def create_race(race: Race):
    race_dict = race.model_dump(by_alias=True)
    return mongo_client.insert_one("races", race_dict)

@app.get(
    "/races/",
    response_model=List[Race]
)
async def list_races():
    return mongo_client.find_all("races")

# Routes for Scores
@app.post(
    "/scores/",
    response_model=Score
)
async def create_score(score: Score):
    score_dict = score.model_dump(by_alias=True)
    return mongo_client.insert_one("scores", score_dict)

@app.get(
    "/scores/",
    response_model=List[Score]
)
async def list_scores():
    return mongo_client.find_all("scores")
