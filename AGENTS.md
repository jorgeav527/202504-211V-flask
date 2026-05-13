# AGENTS.md — 202504-211V-flask

## Comandos

```bash
uv sync                          # instalar dependencias
uv run flask --app app/main.py run --debug  # servidor de desarrollo
python init.py                   # crear DB y sembrar datos
```

## Arquitectura

- Flask app factory via `app/__init__.py:create_app()`. Entrypoint: `app/main.py`
- 3 Blueprints: `base` (`/`), `post` (`/post`), `comments` (`/comments`)
- SQLite + Flask `g` context (`app/database.py`). DB file: `basedatos.db` (gitignorado)

## Rutas clave

| Ruta | Método | Función | Descripción |
|---|---|---|---|
| `/` | GET | `base.root` | Página raíz |
| `/home` | GET | `base.home` | Página home |
| `/post/list` | GET | `post.get_all_posts` | Lista todos los posts |
| `/post/api/list` | GET | `post.get_posts_partial` | HTML parcial para htmx |
| `/post/api/posts` | GET | `post.get_all_posts_json` | JSON API |
| `/post/<id>` | GET | `post.get_single_post` | Detalle de post |
| `/post/create` | GET/POST | `post.create_post` | Crear post |
| `/post/update/<id>` | GET/POST | `post.update_post` | Actualizar post |
| `/post/delete/<id>` | POST | `post.delete_one_post` | Eliminar post |
| `/post/delete/<id>/htmx` | DELETE | `post.delete_one_post_htmx` | Eliminar vía htmx |
| `/comments/list` | GET | `comments.get_all_comments` | Placeholder |

## Convenciones y detalles

- **Form fields**: nombres `title_title` y `content_content` (no `title`/`content`) en create/update
- **Bug conocido**: `templates/post/update.html:13` muestra `single_post['title']` en textarea de content — debería ser `single_post['content']`
- **Frontend**: Bootstrap 5.3 (CDN), htmx 2.0.10, SweetAlert2
- **DB**: tabla `posts` con columnas `id`, `created_at`, `title`, `content`. Seed en `init.py`
- **Estilo**: `.htmx-swapping` animation en `app/static/main.css`
- **No hay**: tests, linting, typechecking, CI, ni pre-commit configurados
