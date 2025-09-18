## Database Setup

In project I use PostgreSQL as database. Make sure you have PostgreSQL installed and running on your machine.

## Env file

Create a `.env` file in the root directory of the project and add the following environment variables:

```
DB_NAME=<YOUR_DB_NAME>
DB_USER=<YOUR_DB_USER>
DB_PASSWORD=<YOUR_DB_PASSWORD>
DB_HOST=<YOUR_DB_HOST>
DB_PORT=<YOUR_DB_PORT>
```

## Deploy

To start application in dev mode, run the following commands in the project directory:

```bash
pip install django python-dotenv django-cors-headers psycopg2-binary requests
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initial_data.json
python manage.py runserver
```

## Api Endpoints

- `GET /api/cats/` - Retrieve a list of all cats.
- `POST /api/cats/<int:cat_id>/` - Create new cat in database.
- `PUT /api/cats/<int:cat_id>/` - Change cat in database.
- `DELETE /api/cats/<int:cat_id>/` - Delete cat from database.
- `POST /missions/` - Creates a mission and immediately sets its targets.
- `GET /missions/` - List of all missions.
- `GET /missions/<int:id>/` - One mission with targets.
- `PUT /missions/<int:id>/` - Mission update + target update (but prohibited if the mission has been completed).
- `DELETE /missions/<int:id>/` - Deletes the mission (if not linked to a cat).
- `PATCH /missions/<int:id>/` - You can assign a cat to a mission.

## Postman Collection

`POST /api/cats/<int:cat_id>/`
```
{
    "id": 1,
    "name": "Tom",
    "breed": "Siamese",
    "years_of_experience": 3,
    "salary": 2000
}
```

`PUT /api/cats/<int:cat_id>/`
```
{
    "id": 1,
    "name": "Whiskers",
    "breed": "Tabby",
    "years_of_experience": 5,
    "salary": 1000
}
```

`POST /api/missions/`
```
{
  "name": "Catch the Red Dot",
  "description": "Top secret mission to chase the red dot in the living room",
  "is_completed": false,
  "cat": null,
  "targets": [
    {
      "name": "Laser Point 1",
      "country": "Living Room",
      "notes": "Behind the sofa",
      "is_completed": false
    },
    {
      "name": "Laser Point 2",
      "country": "Kitchen",
      "notes": "Near the fridge",
      "is_completed": false
    }
  ]
}
```

`PUT /api/missions/1/`
```
{
  "name": "Catch the Red Dot - Phase 2",
  "description": "Updated mission with more intel",
  "targets": [
    {
      "id": 1,
      "notes": "Moved under the table",
      "is_completed": true
    },
    {
      "id": 2,
      "notes": "Still near the fridge"
    }
  ]
}
```

`PATCH /api/missions/1/`
```
{
  "cat": 3
}
```
