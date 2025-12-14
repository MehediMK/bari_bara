# HouseBox Django Project

This project has been converted to a Django application.

## Structure

- **housebox/**: Project configuration (`settings.py`, `urls.py`).
- **web/**: The main application.
  - `views.py`: Contains views for the index page and a generic page handler.
  - `urls.py`: URL routing.
- **templates/**: HTML templates.
  - `base.html`: The base template with header, footer, and common assets.
  - `web/`: Page templates.
    - `index.html`: The homepage, extending `base.html`.
    - Other `.html` files: Currently raw HTML with updated static paths.
- **static/**: Static assets (CSS, JS, Images).

## How to Manage

### Adding a New Page
1. Create a new HTML file in `templates/web/`.
2. To use the common layout, extend `base.html`:
   ```html
   {% extends "base.html" %}
   {% load static %}
   {% block content %}
     <!-- Your content here -->
   {% endblock %}
   ```
3. The page will be automatically available at `http://localhost:8000/your-page-name.html`.

### SEO and Social Sharing
The project uses `django-meta` for SEO tags.
- In `web/views.py`, the `index` view demonstrates how to pass meta data.
- To add meta data to other pages, create a specific view in `views.py` and pass a `Meta` object.

### Static Files
All static files are in the `static/` directory.
Use `{% static 'path/to/file' %}` in templates to refer to them.
Example: `<img src="{% static 'img/logo.png' %}">`

## Running the Server
```bash
source venv/bin/activate
python manage.py runserver
```
