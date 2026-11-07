from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

class PostIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    body: str = Field(min_length=1, max_length=5000)

class CommentIn(BaseModel):
    author: str = Field(min_length=1, max_length=40)
    body: str = Field(min_length=1, max_length=500)

def create_app() -> FastAPI:
    app = FastAPI(title="Blog API", version="1.0.0")
    app.state.posts: dict[int, dict] = {}
    app.state.next_id = 1

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/posts", status_code=201)
    def create_post(payload: PostIn):
        post = {"id": app.state.next_id, **payload.model_dump(), "comments": []}
        app.state.next_id += 1
        app.state.posts[post["id"]] = post
        return post

    @app.get("/posts")
    def list_posts():
        return list(app.state.posts.values())

    @app.get("/posts/{post_id}")
    def get_post(post_id: int):
        if post_id not in app.state.posts:
            raise HTTPException(404, "Post not found")
        return app.state.posts[post_id]

    @app.post("/posts/{post_id}/comments", status_code=201)
    def add_comment(post_id: int, payload: CommentIn):
        if post_id not in app.state.posts:
            raise HTTPException(404, "Post not found")
        comment = {"id": len(app.state.posts[post_id]["comments"]) + 1, **payload.model_dump()}
        app.state.posts[post_id]["comments"].append(comment)
        return comment

    return app

app = create_app()
