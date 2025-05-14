from typing import List
from .schema import User, Driver, Team, Race, Score, DriverUpdateRequest
from fastapi import FastAPI, HTTPException
from ..database import MongoDBClient
from pymongo.errors import DuplicateKeyError

mongo_client = MongoDBClient("mongodb://root:example@localhost:27017/", "fantasyf1")

# FastAPI app
app = FastAPI(
    openapi_tags=[
        {
            "name": "FantasyF1-DB",
            "description": "All Fantasy Formula 1 API endpoints."
        }
    ]
)

# Routes for Users
@app.post(
    "/users/",
    response_model=User,
    tags=["Users"]
)
async def create_user(user: User):
    try:
        user_dict = user.model_dump(by_alias=True)
        user_dict["drivers"] = []
        user_dict["teams"] = []
        user_dict["bonuses"] = {}
        user_dict["total_points"] = 0.0
        user_dict["total_budget"] = 25.0
        return mongo_client.insert_one("users", user_dict)
    except DuplicateKeyError as e:
        print(e)
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists"
        )


@app.get(
    "/users/",
    response_model=List[User],
    tags=["Users"]
)
async def list_users():
    return mongo_client.find("users")


@app.get(
    "/users/{username}",
    response_model=User,
    tags=["Users"]
)
async def list_user(username: str):
    user = mongo_client.find_one("users", {"username": username})
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user


@app.delete(
    "/users/{username}",
    response_model=User,
    tags=["Users"]
)
async def delete_user(username: str):
    try:
        user = mongo_client.find_one("users", {"username": username})
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        count = mongo_client.delete("users", {"username": username})
        assert count == 1, f"Deleted {count} users, expected 1"
    except AssertionError as e:
        print(e)
    return user


# Routes for Drivers
@app.post(
    "/drivers/",
    response_model=Driver,
    tags=["Drivers"]
)
async def create_driver(driver: Driver):
    try:
        driver_dict = driver.model_dump(by_alias=True)
        driver_dict["championship_points"] = 0
        return mongo_client.insert_one("drivers", driver_dict)
    except DuplicateKeyError as e:
        print(e)
        raise HTTPException(
            status_code=409,
            detail="Driver already exists"
        )


@app.put(
    "/drivers/{driver_name}",
    response_model=Driver,
    tags=["Drivers"]
)
async def update_driver(driver_name: str, driver: DriverUpdateRequest):
    driver_dict = driver.model_dump(by_alias=True)
    cleaned_dict = {k: v for k, v in driver_dict.items() if v is not None}
    mongo_client.update_one("drivers", {"name": driver_name}, cleaned_dict)

    if driver := mongo_client.find_one("drivers", {"name": driver_name}):
        return driver
    
    raise HTTPException(
        status_code=404,
        detail="Driver not found"
    )


@app.get(
    "/drivers/",
    response_model=List[Driver],
    tags=["Drivers"]
)
async def list_drivers():
    return mongo_client.find("drivers")


@app.get(
    "/drivers/{driver_name}",
    response_model=Driver,
    tags=["Drivers"]
)
async def list_driver(driver_name: str):
    return mongo_client.find_one("drivers", {"name": driver_name})


@app.delete(
    "/drivers/{driver_name}",
    response_model=Driver,
    tags=["Drivers"]
)
async def delete_driver(driver_name: str):
    driver = mongo_client.find_one("drivers", {"name": driver_name})
    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )
    mongo_client.delete("drivers", {"name": driver_name})
    return driver


# Routes for Teams
@app.post(
    "/teams/",
    response_model=Team,
    tags=["Teams"]
)
async def create_team(team: Team):
    team_dict = team.model_dump(by_alias=True)
    return mongo_client.insert_one("teams", team_dict)


@app.get(
    "/teams/",
    response_model=List[Team],
    tags=["Teams"]
)
async def list_teams():
    return mongo_client.find("teams")


# Routes for Races
@app.post(
    "/races/",
    response_model=Race,
    tags=["Races"]
)
async def create_race(race: Race):
    race_dict = race.model_dump(by_alias=True)
    return mongo_client.insert_one("races", race_dict)


@app.get(
    "/races/",
    response_model=List[Race],
    tags=["Races"]
)
async def list_races():
    return mongo_client.find("races")


# Routes for Scores
@app.post(
    "/scores/",
    response_model=Score,
    tags=["Scores"]
)
async def create_score(score: Score):
    score_dict = score.model_dump(by_alias=True)
    return mongo_client.insert_one("scores", score_dict)


@app.get(
    "/scores/",
    response_model=List[Score],
    tags=["Scores"]
)
async def list_scores():
    return mongo_client.find("scores")
