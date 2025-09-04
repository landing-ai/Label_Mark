import pytest
from playwright.sync_api import sync_playwright, expect

def test_label_task():
    """
    Automated test to validate the labeling workflow in the Label AI platform.

    Test flow:
    1. Login to the platform.
    2. Search for a specific dataset.
    3. Open the dataset and validate its title.
    4. Navigate to the 'To be labeled' section.
    5. Open the first image in the list.
    6. Draw a bounding box on the image.
    7. Verify that the bounding box was created successfully.
    """

    # Initialize Playwright and launch Chromium browser
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)  # Visible browser with delay between actions
        context = browser.new_context()  # New browser context (isolated session)
        page = context.new_page()        # Open a new page/tab

        # ---- LOGIN ----
        page.goto("https://label.landing.ai/")  # Navigate to login page
        page.fill("input[name='identifier']", "luisa.aristizabal.external@landing.ai")  # Enter email
        page.fill("input[name='password']", "B2lL_LZS")  # Enter password
        page.click("button[type='submit']")  # Click login button
        page.wait_for_selector("h1")  # Wait for header to appear
        expect(page.locator("h1")).to_have_text("Document Extraction Benchmark", timeout=10000)  # Validate header text

        # ---- SEARCH DATASET ----
        search_input = page.locator("input[placeholder*='Search by dataset name']")  # Locate search input
        search_input.fill("Testing  QA- Luisa")  # Type dataset name
        page.keyboard.press("Enter")  # Press Enter to search

        # Validate first result
        first_result = page.locator("td a div.cursor-pointer").first
        expect(first_result).to_have_text("Testing  QA- Luisa")  # Validate text of first result

        # Open the dataset
        first_result.click()

        # ---- VALIDATE TASK ENTRY ----
        task_title = page.locator("div.text-3xl.font-semibold")
        expect(task_title).to_have_text("Testing  QA- Luisa")  # Validate task title

        # ---- NAVIGATE TO 'TO BE LABELED' SECTION ----
        page.click("button:has-text('To be labeled')")  # Go to images to be labeled

        # ---- OPEN FIRST IMAGE ----
        page.locator("img[alt*='http']").first.click()  # Open first image

        # ---- DRAW A BOUNDING BOX ----
        canvas = page.locator("svg#annotations")  # Locate annotations canvas
        box = canvas.bounding_box()  # Get canvas dimensions

        if box:
            # Coordinates for bounding box
            start_x = box["x"] + 100
            start_y = box["y"] + 100
            end_x = box["x"] + 300
            end_y = box["y"] + 250

            # Simulate drag-and-drop to draw rectangle
            page.mouse.move(start_x, start_y)
            page.mouse.down()
            page.mouse.move(end_x, end_y)
            page.mouse.up()

        # Validate that bounding box was created
        drawn = page.locator("svg#annotations polygon").first
        expect(drawn).to_be_visible()

        # Close browser
        browser.close()


