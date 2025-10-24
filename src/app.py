"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
static_files = StaticFiles(directory=os.path.join(Path(__file__).parent, "static"))

# Set up root redirect with high priority
@app.get("/", include_in_schema=True)
async def root():
    return RedirectResponse(url="/static/index.html", status_code=307)

# Mount static files after root route is defined
app.mount("/static", static_files, name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team practice and games",
        "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu", "nina@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Recreational soccer practices and weekend scrimmages",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["carlos@mergington.edu", "leah@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "matt@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops, play rehearsals, and stage production",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["oliver@mergington.edu", "mia@mergington.edu"]
    },
    "Debate Team": {
        "description": "Public speaking and competitive debating skills",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["noah@mergington.edu", "anna@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Design, build, and program robots for competitions",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 12,
        "participants": ["ethan@mergington.edu", "grace@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html", status_code=307)


@app.get("/activities")
def get_activities():
    return activities

@app.get("/activities")


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        return JSONResponse(
            status_code=404,
            content={"detail": "Activity not found"}
        )

    # Get the specific activity
    activity = activities[activity_name]
    
    # Validate student is not already signed up
    if email in activity["participants"]:
        return JSONResponse(
            status_code=400,
            content={"detail": "Student already signed up for this activity"}
        )

    # Add student
    activity["participants"].append(email)
    return JSONResponse(
        status_code=200,
        content={"message": f"Signed up {email} for {activity_name}"}
    )
    
@app.delete("/activities/{activity_name}/participant/{email}")
def unregister_participant(activity_name: str, email: str):
    """Unregister a participant from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        return JSONResponse(
            status_code=404,
            content={"detail": "Activity not found"}
        )

    # Get the specific activity
    activity = activities[activity_name]

    # Validate participant is registered
    if email not in activity["participants"]:
        return JSONResponse(
            status_code=404,
            content={"detail": "Participant not found"}
        )

    # Remove participant
    activity["participants"].remove(email)
    return JSONResponse(
        status_code=200,
        content={"message": f"Removed {email} from {activity_name}"}
    )
