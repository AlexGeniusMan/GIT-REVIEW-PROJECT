# GIT-REVIEW
🤍 Reviews GitHub accounts by theirs usernames 

## Launching project in production mode
#### Git, Docker and Docker Compose must be installed

1. Clone project

```
git clone https://github.com/AlexGeniusMan/GIT-REVIEW-PROJECT git-review
cd git-review
```

2. Generate new DJANGO_SECRET_KEY and paste it to backend service as SECRET_KEY environment variable in docker-compose.yml

> To generate new DJANGO_SECRET_KEY use this instruction: https://stackoverflow.com/a/57678930/14355198

```
services:
  backend:
    environment:
      - SECRET_KEY=NEW_DJANGO_SECRET_KEY
```

3. Launch project

```
docker-compose up --build
```

> Done! Project launched on 80 port!

<!---

-->

This project was made by Alexander Chentsov.