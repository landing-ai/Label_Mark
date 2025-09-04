import pytest
from playwright.sync_api import sync_playwright, expect
import os


def test_create_dataset_from_doc_source():
    """
    Automated test using Playwright to:
    1. Log into the Landing AI Label platform.
    2. Create a new dataset from the "Doc Source" section.
    3. Select multiple chunks from the document explorer and add them to the dataset.
    4. Verify the dataset contains the correct number of documents.
    5. Interact with a document inside the dataset.
    6. Delete the dataset and verify removal.
    """

    with sync_playwright() as p:
        # Launch browser (non-headless, Full HD viewport)
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

        # ---- CREATE NEW DATASET ----
        page.get_by_text("Create New Dataset").click(timeout=20000)

        # Verify modal opened
        dialog = page.locator("div[role='dialog']")
        expect(dialog).to_be_visible()

        # Enter dataset name
        dataset_name = "QA-testing-Create Dataset - Source Page"
        page.fill("input.flex.h-9.w-full.rounded-md.border", dataset_name)

        # Select dataset type
        page.get_by_role("combobox").click()
        page.locator("div[role='option'] >> text='Table Labeling (Beta)'").click()

        # Submit form
        page.get_by_role("button", name="Submit").click()
        page.wait_for_selector(f"text={dataset_name}")

        # ---- NAVIGATE TO DOC SOURCE ----
        page.goto("https://label.landing.ai/")
        expect(page.locator("h1")).to_have_text("Document Extraction Benchmark", timeout=10000)
        page.get_by_text("Doc Source").click()

        # Verify Document Explorer opened
        expect(page.get_by_text("Document Explorer")).to_be_visible(timeout=5000)

        # ---- SELECT CHUNKS AND ADD TO DATASET ----
        page.locator("input[type='radio'][value='chunk']").check()
        page.get_by_label("table").check()
        page.get_by_role("button", name="Select to Add to Dataset").click()
        expect(page.locator("h2:has-text('Select items (0 selected)')")).to_be_visible(timeout=5000)

        # Select first 3 chunks
        page.get_by_role("img", name="Chunk preview").nth(0).click(force=True)
        page.get_by_role("img", name="Chunk preview").nth(1).click(force=True)
        page.get_by_role("img", name="Chunk preview").nth(2).click(force=True)

        # Add selected chunks to dataset
        page.get_by_role("button", name="Add 3 to Dataset").click()
        page.locator("input[placeholder='Search datasets by name, creator, or type...']").fill(dataset_name)
        expect(page.locator("h4.font-medium", has_text=dataset_name)).to_be_visible(timeout=5000)

        # Open dataset card
        page.locator(
            f"div.rounded-lg.border.p-3.transition-colors:has-text('{dataset_name}')"
        ).click()
        page.get_by_role("button", name="Add to Dataset").click()

        # ---- VERIFY DATASET CONTENT ----
        page.goto("https://label.landing.ai/")
        expect(page.locator("h1")).to_have_text("Document Extraction Benchmark", timeout=10000)
        search_box = page.locator("input[placeholder='Search by dataset name or creator email...']")
        search_box.fill(dataset_name)
        page.locator("div.cursor-pointer", has_text=dataset_name).click()
        expect(page.locator("div.mr-4")).to_have_text("total documents: 3", timeout=5000)

        # Ensure at least 1 document preview is visible
        page.locator("div.group.relative.flex.flex-1.cursor-pointer").first.wait_for(timeout=10000)

        # Click on the first document image
        page.locator("div.group.relative.flex.flex-1.cursor-pointer img").first.click(force=True)

        # Verify "View in Doc Source" button appears
        expect(page.get_by_role("button", name="View in Doc Source")).to_be_visible(timeout=15000)

        # ---- DELETE DATASET ----
        page.goto("https://label.landing.ai/")
        expect(page.locator("h1")).to_have_text("Document Extraction Benchmark", timeout=10000)
        search_box = page.locator("input[placeholder='Search by dataset name or creator email...']")
        search_box.fill(dataset_name)

        # Delete process
        delete_icon = page.locator("svg.size-4.text-red-500")
        delete_icon.click()
        delete_modal = page.locator("div[role='dialog']")
        expect(delete_modal).to_be_visible()
        confirm_button = delete_modal.get_by_role("button", name="Confirm")
        confirm_button.click()

        # Verify dataset no longer exists
        page.reload()
        search_box = page.locator("input[placeholder='Search by dataset name or creator email...']")
        search_box.fill(dataset_name)
        page.wait_for_timeout(2000)  # brief wait for results filtering
        expect(page.locator(f"div.cursor-pointer >> text={dataset_name}")).not_to_be_visible()
