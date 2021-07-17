HMS
- Clone project from github
- Run docker-compose up -d --build
- Run docker exec -it hms_web_1 bash
    - ./manage.py createsuperuser
    - enter credentials for admin
- Open page on http://localhost:8000/