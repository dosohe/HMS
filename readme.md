HMS
- Clone project from github
- Run docker-compose up -d --build
- Run docker exec -it hms_web_1 bash
    - ./manage.py createsuperuser
    - enter credentials for admin
- Open page on http://localhost:8000/
- To upload the file (.csv) into the database they must open the page on http://localhost:8000/admin/service/reservations and click _import reservations_ button on that page