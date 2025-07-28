from setuptools import setup, find_packages

setup(
    name="trip-planner",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "langgraph",
        "langchain",
        "huggingface_hub",
        "requests",
    ],
    python_requires=">=3.9",
)
