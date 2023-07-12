from bs4 import BeautifulSoup
import requests


def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"class":'pdp-mod-product-badge-title'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()
        print(title_string)

    except AttributeError:
        title_string = ""

    return title_string


if __name__ == '__main__':

    # add your user agent  put your agent when use it
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37', 'Accept-Language': 'en-US, en;q=0.5'})

    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[], "link":[], "image_url":[],"category": "sunscreen"}





    # The webpage URL
    for i in range(1,6):
        URL = f"https://www.daraz.pk/catalog/?_keyori=ss&from=input&page={i}&q=sun%20cream&spm=a2a0e.searchlist.search.go.70e459a72GP9Uw"
        # HTTP Request
        webpage = requests.get(URL, headers=HEADERS)

        # Soup Object containing all data
        soup = BeautifulSoup(webpage.content, "html.parser")

        # Fetch links as List of Tag Objects
        links = soup.find_all("div", attrs={'class':''})
    
        
        # Store the links
        links_list = []
        
        # Loop for extracting links from Tag Objects
        for link in links:
                print("done done suncream")
                links_list.append(link.get('href'))
                print(link.get('href'))
                
                
                
        
        # Loop for extracting product details from each link 
        for link in links_list:
        
            new_webpage = requests.get("https://www.daraz.pk" + link, headers=HEADERS)

            new_soup = BeautifulSoup(new_webpage.content, "html.parser")
            # Function calls to display all necessary product information
            print(get_title(new_soup))
