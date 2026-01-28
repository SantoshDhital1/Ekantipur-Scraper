from playwright.sync_api import sync_playwright
import json

# function to extract the entertainment news
def entertainment_section(page, section_name, base_url):
    print(f"Scraping {section_name}")

    page.goto(base_url)
    page.wait_for_timeout(3000)
    
    data = []
    
    # grab the first 5 article cards
    posts = page.locator("article").all()[:5]

    for post in posts:
        # use exception handling to handle error or exception if any error arise
        try:
            # to scroll the page to extract multiple articles
            post.scroll_into_view_if_needed()
            page.wait_for_timeout(800)

            # get title of the news
            title = post.locator("h2").first.inner_text().strip() or "N/A"

            # get image url
            image_url = post.locator("img").get_attribute('src') or "N\A"

            # get category
            category = "Entertainment"

            # get author
            author = post.locator('.author').inner_text().strip() or "N\A"

            # append the extracted data into the list
            data.append(
            { 
                "title": title,
                "image_url": image_url,
                "category": category,
                "author": author
            } 
        )
        except Exception as e:
            print(f"Error scraping entertainment news: {e}")

    return data

# function to extract the cartoon data
def cartoon_section(page, section_name, base_url):
    print(f"Scraping {section_name}")

    page.goto(base_url)
    page.wait_for_timeout(3000)

    data = []
    # grab cartoon section using div and cartoon content
    posts = page.locator("div.catroon-wrap").all()[:1]

    for post in posts:
        try:
            # Get title from alt text
            title_elem = post.locator("img").first
            title = title_elem.get_attribute("alt") if title_elem else "N/A"

            # Get image
            img_elem = post.locator("img").first
            image_url = img_elem.get_attribute("src") if img_elem else "N/A"

            # Get author 
            author_elem = post.locator(".cartoon-author span").first
            author = author_elem.inner_text().strip() if author_elem else "N/A"

            data.append(
                {
                    "title": title,
                    "image_url": image_url,
                    "author": author
                }
            )

        except Exception as e:
            print(f"Error scraping cartoon: {e}")

    return data

# insert the list data into dictionary
section_data = {
    "entertainment_news": [],
    "cartoon_news": []
}

# sync_playwright must be called to get the context manager
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Scrape Entertainment
    section_data['entertainment_news'] = entertainment_section(
        page, "Entertainment", "https://ekantipur.com/entertainment"
    )  

    # Scrape cartoon data
    section_data['cartoon_news'] = cartoon_section(
        page, "Cartoon", "https://ekantipur.com/cartoon"
    )

    browser.close()

# Save the data using output.json file
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(section_data, f, ensure_ascii=False, indent=2)

