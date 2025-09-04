# Playwright Tests

## Table of Contents

- [Introduction 📖](#introduction)
- [Requirements 🛠️](#requirements)
- [Getting Started 🚀](#getting-started)
- [Running the Tests ⚡](#running-the-tests)
- [Author 👤](#author)

---

## Introduction 📖

This project contains automated **end-to-end tests** built with **Playwright** and **Pytest** for the **Landing AI** platform.  

The tests validate the following workflows:
- Login to the platform.
- Create datasets from different sources.
- Upload and verify documents.
- Interact with document previews.
- Delete datasets and verify removal.

These tests run on **macOS**, **Windows**, or **Linux**.

---

## Requirements 🛠️

To run this project, you’ll need:

- **Python 3.8 or higher**
- Libraries:  

  ```bash
  pip install pytest playwright pytest-xdist
    ```

    - Install Playwright browsers (first time only):
    ```bash
    playwright install
    ```

    - Or, if you only want Chromium:
    ```bash
    playwright install chromium
    ```

---

## Getting Started 🚀

1. Clone the repository

```bash
git clone https://github.com/<your-repo>.git
cd <your-repo>
```

2. Create and activate a virtual environment

    - Windows

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

    - macOS/Linux

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
---

### Running the Tests ⚡

- **Run all tests:**
    ```bash
    pytest -s -v
    ```

- *Run a specific test file:*
    ```bash
    pytest -s -v tests/test_create_dataset_from_doc_source.py
    ```

- *Run tests in parallel (e.g., 2 at a time):*
    ```bash
    pytest -n 2
    ```
---

## Author 👤

> **Name:** Luisa Fernanda Aristizabal Giraldo  
> **Position:** Tester QA  
> **Team:** Quality Assurance / Testing Team  
> **Email:** luisa.aristizabal.external@landing.ai

---