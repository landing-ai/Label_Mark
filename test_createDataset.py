import pytest
from playwright.sync_api import sync_playwright, expect
import os

def test_create_dataset_with_images():
    with sync_playwright() as p:
        # Launch Chromium in non-headless mode with slow motion enabled
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}  # Full HD resolution
        )
        page = context.new_page()

        # ---- LOGIN ----
        page.goto("https://label.landing.ai/")
        page.fill("input[name='identifier']", "luisa.aristizabal.external@landing.ai")
        page.fill("input[name='password']", "B2lL_LZS")
        page.click("button[type='submit']")
        page.wait_for_selector("h1")
        expect(page.locator("h1")).to_have_text("Document Extraction Benchmark", timeout=10000)
        page.wait_for_timeout(10000)

        # ---- CLICK ON "CREATE NEW DATASET" ----
        page.get_by_text("Create New Dataset").click(timeout=20000)

        # ---- VERIFY THAT THE MODAL OPENS ----
        dialog = page.locator("div[role='dialog']")
        expect(dialog).to_be_visible()

        # ---- ENTER DATASET NAME ----
        dataset_name = "QA-testing-Create Dataset"
        page.fill("input.flex.h-9.w-full.rounded-md.border", dataset_name)

        # ---- OPEN DATASET TYPE COMBOBOX ----
        page.get_by_role("combobox").click()

        # ---- SELECT "TABLE LABELING (BETA)" ----
        page.locator("div[role='option'] >> text='Table Labeling (Beta)'").click()

        # ---- SUBMIT ----
        page.get_by_role("button", name="Submit").click()
        page.wait_for_selector(f"text={dataset_name}")

        # ---- UPLOAD IMAGES ----
        file_input = page.locator("input[type='file']")
        images_path = "/Users/luisaaristizabal/Documents/Test_Label_Page/images"
        image_files = [
            os.path.join(images_path, f)
            for f in os.listdir(images_path)
            if f.endswith((".jpg", ".png", ".jpeg"))
        ]
        file_input.set_input_files(image_files)

        # Verify that each uploaded image appears in the UI
        for img in image_files:
            page.wait_for_selector(f"text={os.path.basename(img)}", timeout=10000)

        # ---- VERIFY TOTAL DOCUMENTS ----
        total_docs = page.locator("div.mr-4", has_text="total documents: 11")
        expect(total_docs).to_be_visible(timeout=20000)

        # ---- OPEN STATUS FILTER ----
        page.get_by_role("button", name="Status").click()
        page.get_by_role("menuitemcheckbox", name="Ready").click()
        expect(total_docs).to_be_visible(timeout=10000)

        # ---- NAVIGATE BACK TO HOMEPAGE ----
        page.goto("https://label.landing.ai/")
        expect(page.locator("h1")).to_have_text("Document Extraction Benchmark", timeout=10000)

        # ---- SEARCH FOR DATASET ----
        search_input = page.locator("input[placeholder*='Search by dataset name']")
        search_input.fill(dataset_name)
        page.wait_for_selector(f"div.cursor-pointer >> text={dataset_name}")

        # ---- VERIFY DATASET EXISTS AND BELONGS TO LUISA ----
        dataset_entry = page.locator(f"div.cursor-pointer >> text={dataset_name}")
        expect(dataset_entry.first).to_be_visible()
        expect(
            page.locator("td").filter(has_text="luisa.aristizabal.external@landing.ai").nth(0)
        ).to_be_visible(timeout=5000)

        # ---- DELETE THE DATASET ----
        delete_icon = page.locator("svg.size-4.text-red-500")
        delete_icon.click()

        delete_modal = page.locator("div[role='dialog']")
        expect(delete_modal).to_be_visible()
        confirm_button = delete_modal.get_by_role("button", name="Confirm")
        confirm_button.click()

        # ---- RELOAD AND VERIFY DATASET NO LONGER EXISTS ----
        page.reload()
        search_input = page.locator("input[placeholder*='Search by dataset name']")
        search_input.fill(dataset_name)
        page.wait_for_timeout(2000)  # short wait for filtering results
        expect(page.locator(f"div.cursor-pointer >> text={dataset_name}")).not_to_be_visible()



    
