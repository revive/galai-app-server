Simple app server for Galai
===========================

This is a simple application server built on top of the [galai project](https://github.com/paperswithcode/galai). You may need to install galai first and make sure that it can run locally.

It requires the [Falcon web framework](https://falconframework.org/).

## How to run

An ASGI server is required to run this app. Uvicorn is a popular choice.

Install the uvicorn server:
```bash
pip install uvicorn
```

Run the application
```bash
uvicorn galai-app-server.asgi:app
```

Visit the following URLs (example with httpie):
1. Submit the question, the response contains a string of UUID, which can be used to visit the answer.
```bash
http post localhost:8000/generate query="describe the Schroedinger equation"
```
2. Check the answer with the given UUID
```bash
http get localhost:8000/generate/b8ed438c-c2b3-4816-9fb3-e4b41ab0baf6
```

The response looks like:
```json
{
    "answer": "escribe the Schroedinger equation for the \\(\\phi^{4}\\) theory.\n\n# 2.1 The \\(\\phi^{4}\\) theory\n\nThe \\(\\phi^{4}\\) theory is defined by",
    "question": "describe the Schroedinger equation"
}
```
