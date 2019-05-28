# CheMondis Test 2

## Install

Install dependencies.


    pip3 install -r requirements.txt

Create or use existing `postgres` setting and make sure they are reflected in `settings.py`.

Run migrations.

    python3 manage.py migrate

Start server.

    python3 manage.py runserver


## API documentation

Register a user (interviewer).

    POST /api/v1/register/
    Content-Type    application/json
    {
        "email": "foo@example.com",
        "password1": "whatevs1234",
        "password2": "whatevs1234"
    }

Create an interview.

    POST /api/v1/interviews/
    Content-Type    application/json
    Authorization   Token 38ce43575326d84262ae765e9e30261721ac1284
    {
        "candidate_name": "foo bar",
        "candidate_email": "candidate@example.com"
    }

Create candidate slot(s).

    POST /api/v1/interviews/a0149d05-8d49-4247-ae60-f25429c1316e/slots/
    Content-Type    application/json
    {
        "slots": [
            {"date": "2000-10-10 10:00"}
        ]
    }

Create interviewer slot(s).

    POST /api/v1/interviews/a0149d05-8d49-4247-ae60-f25429c1316e/slots/
    Content-Type    application/json
    Authorization   Token 38ce43575326d84262ae765e9e30261721ac1284

    {
        "slots": [
            {"date": "2000-10-10 10:00"}
        ]
    }

Fetch the overlapping slots.

    GET /api/v1/interviews/a0149d05-8d49-4247-ae60-f25429c1316e/slots/