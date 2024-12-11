# Photo gallery
A web application inspired by Pinterest, featuring a photo gallery and user management. Users can create posts with multiple photos, comment on and like posts and comments. Reactions include three types: heart, laugh, and like, offering a dynamic and engaging social experience. Each post is categorized into one of 30 various categories, and users can search for posts by title, category, or the poster's name.

## Our application meets the following criteria

### Project setup and documentation
- Clear structure and organized directories
- Comprehensive README with setup instructions and features
- Version control with meaningful commits

### Backend
- API Design: RESTful principles and dynamic server-driven updates using HTMX
- Database: PostgreSQL
- Security: Authentication, authorization, data validation, protection against vulnerabilities using Django

### Frontend
- Mobile-first, fully responsive layout created with Tailwind CSS
- User Experience: Intuitive UI/UX, accessible navigation
- State Management: Efficient handling of app state or data
- API Integration: Smooth backend integration

### Best Practices and Code Quality
- Code Quality: Clean, modular, and readable code
- Error Handling: Comprehensive error handling

### Testing
- Unit tests
- Integration tests
- Load tests

### Containerization
- Docker for consistent development and deployment environments

### Innovation/Extras
- Server-side rendering and partial page updates with HTMX

# Application Setup and Run
## Prerequisites
Make sure the following tools are installed on your system:

- Docker
- Docker Compose

## Build and run Docker
### Start the Containers
```bash
docker-compose up
```
Application is running on `localhost:8000`

### Stop the Containers
Stops and remove containers
```bash
docker-compose down
```

### Rebuild Containers
If you make changes to the Dockerfile or dependencies:
```bash
docker-compose up --build
```

### Pause and start again (no changes applied)
```bash
docker-compose stop
docker-compose start
```

## Run Management Commands
You can run any Django management command inside the web container. For example:

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```
