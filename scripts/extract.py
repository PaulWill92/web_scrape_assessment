# Extract data from various web based sources so that it can be later louded into a
import pandas as pd
from bs4 import BeautifulSoup
import requests
import yaml
import ast

# Use the config.yaml file to generate run process this is a good way to automate processes



class ProductExtract:
    """
    
    This class is responsible for extracting data from user specific sources.
    For now it's only functionality is webscraping but in the future it will allow for
    API calls and other methods of extraction. For now this class can only scrape 1 single page per site
    
    This class is for product data.
    
    Arguments:
    customer_name : (str) name of website you will scrape
    customer_region : (str) region code of website you are scraping
    website : (str) property / homepage of website you are scraping
    scrape_count : (int) number of pages you want to scrape / iterate over
    list_of_products : (list) a list of products you are interested in scraping
    example_url : (list) page type you are scraping and example of url with search terms or variables replaced with empty {}
    page_types_to_scrape : (list) page types which you previously defined in example_url that you will scrape
    
    """
    
    
    def __init__(self, filename ):
        with open(filename, "r") as f:
            config = yaml.safe_load(f)
        
        self.customer_name = self._dtype_validator(config.get("customer_name"), str)
        self.customer_region = self._dtype_validator(config.get("customer_region"), str)
        self.website = self._dtype_validator(config.get("website"), str)
        self.scrape_page_count = self._dtype_validator(config.get("scrape_count"), int)
        self.list_of_products = self._dtype_validator(config.get("list_of_products"), list)
        self.example_url = self._dtype_validator(config.get("example_url"), dict)
        self.page_types_to_scrape = [k for k in self.example_url.keys()]
        self.url_space_delim = self._dtype_validator(config.get("url_space_delim"), str)
        self.is_selenium = self._dtype_validator(config.get("sel_fetch"), bool)
        self.scrape_params = self._dtype_validator(config.get("scrape_params"), dict)
    
    # product urls:
        self.prod_joins = self.prod_joins()
        self.prod_urls = self.generate_urls()
    
        # create search pages from product list pages:
    def prod_joins(self):
        """
        replaces whitepace of urls with the user defined delim. 

        Returns:
            list : list of joined products to urls. 
        """
        joined_prods = []
        for product in self.list_of_products:
            joined_prod = product.replace(" ", self.url_space_delim)
            joined_prods.append(joined_prod)
        return joined_prods
            
    
    def generate_urls(self):
        """
        joins products to urls that contain {}

        Args:
            example_url : self (dict) a dictionary that defines an example url and page type
            prod_joins : self (list) a list of joined products
            
        Returns:
            dict : a dictionary of product links
        """
        generated_urls = {}
        
        for page_type, example_url in self.example_url.items():
            urls = []
            for product in self.prod_joins:
                url = example_url.format(product)
                urls.append(url)
            generated_urls[page_type] = urls
        return {k: list(set(v)) for k, v in generated_urls.items()} # dedupe any urls 
        
                
    
        
    def _dtype_validator(self, value, datatype):
        """
        validates entries on the yaml file and throws error if there are incorrect data types or formating

        Args:
            value : value found in yaml config file.
            datatype : determined data type of the given dimensions that you are comparing the value with. 

        Raises:
            ValueError: if there is a mismatch of value and data type, an error will be raised.

        """
        if not isinstance(value, datatype):
            raise ValueError(f"The given argument: {value} must be a {datatype}") 
        return value
    
    
    # def product_link_extractor(self, soup, link_selector, website, url_space_delim):
    
    #     # soup would be a dict that looks like this {"page_type": "soup"} product listing page type will always hold product links so this is hardcoded
        
    #     link_container = soup.select(link_selector)
    #     links = link_container.select("a")
        
                                
    #     return [website + link.get("href").replace(" ", url_space_delim) for link in links]
    
    def product_link_extractor(self, soup, link_selector, website, url_space_delim):
        """
        
        extracts urls from a soup object using a link_selector defined by user in the config.yaml file
        
        """
        # soup would be a dict that looks like this {"page_type": "soup"} product listing page type will always hold product links so this is hardcoded
        link_container = soup.select(link_selector)
        links = []
        for container in link_container:
            for link in container.select("a"):
                links.append(website + link.get("href").replace(" ", url_space_delim))
                                    
        return links
    
    def quick_soup(self, product_urls_dict, header=None):
        """
        
        creates a soup object for product listing pages and above in hierarchy so that they can be used to loop and find links.
        
        """
        # quick soup = proudct listing page info that can be extracted fast
        # urls = urls stored on product listing pages

            if self.is_selenium == False:
                soup_holder = []
                quick_soup = {}
                product_urls_list = []
                for category, product in product_urls_dict.items():
                    soup_list = []
                    for url in product:
                        response = requests.get(url, headers=header)
                        soup_list.append(BeautifulSoup(response.content, 'html.parser'))
                    quick_soup[category] = soup_list
                    
                return quick_soup

            else:
                print("WARNING: using the selenium fetcher so cant view a quick soup!")
    
    
    def extract_info_from_selector(self, soup, selector):
        """
        Note: likely wont use for this task but it could be a useful function to extract more data
        on a need basis. Such as the tables in the amazon product pages.
        example selector: amazon product table selector: #prodDetails > div > div:nth-child(1) > div:nth-child(1) > div > div.a-expander-content.a-expander-extend-content > div > div'
        
        Extracts information from the items under the given selector in the BeautifulSoup object.
        
        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the HTML.
            selector (str): The CSS selector for the element containing the desired information.
            
        Returns:
            A list of strings containing the extracted information.
        """
        info_list = []
        selector_element = soup.select_one(selector)
        if selector_element:
            for item in selector_element.find_all():
                if item.string:
                    info_list.append(item.string.strip())
        return info_list
    
    
    def extract_product_data(self, url_list, header=None):
        
        """
        
        extracts product data from list of product urls and creates user defined dataframe object.
        
        """
        
        
        product_data = []
        for url in url_list:
            try:
                response = requests.get(url, headers=header)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                product_name = soup.select_one(self.scrape_params["name"]).get_text(strip=True) if 'name' in self.scrape_params else None
                product_price = soup.select_one(self.scrape_params["price"]).get_text(strip=True) if 'price' in self.scrape_params else None
                product_brand = soup.select_one(self.scrape_params["brand"]).get_text(strip=True) if 'brand' in self.scrape_params else None
                product_instock = soup.select_one(self.scrape_params["instock"]).get_text(strip=True) if 'instock' in self.scrape_params else None
                # product_bar_code = soup.select_one(self.scrape_params["product_bar_code"]).get_text(strip=True) if 'product_bar_code' in self.scrape_params else None
                product_rating = soup.select_one(self.scrape_params["customer_rating"]).get_text(strip=True) if 'customer_rating' in self.scrape_params else None
                product_rating_count = soup.select_one(self.scrape_params["rating_count"]).get_text(strip=True) if 'rating_count' in self.scrape_params else None
                
                product_data.append({'name': product_name , 
                                    'price': product_price, 
                                    'brand': product_brand,
                                    'instock': product_instock, 
                                    #  'identifcation_number': product_bar_code,
                                    'rating': product_rating,
                                    'rating_count':product_rating_count})
            except AttributeError:
                print(f"WARNING: skipping {url} due to NoneType object attribute")

        return product_data
    







# I Would normally import class into a separate python script to run process but to keep everything in one file and to save time I will run the processes just below:
# I Would also normally create a transformation script to clean all the data but I will also do my data transforms here:
# amazon:
amazon_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
amazon = ProductExtract(filename="../config/amazon_config.yaml")
amazon_quick_soup = amazon.quick_soup(amazon.prod_urls, header=amazon_header)
# amazon_product_links= amazon.product_link_extractor(amazon_quick_soup["Product_list_page"][0], amazon.scrape_params["product_link_selector"], amazon.website, amazon.url_space_delim)
amazon_link_container = amazon_quick_soup["Product_list_page"][0].select(amazon.scrape_params["product_link_selector"])
amazon_product_links = [amazon.website+link["href"].replace(" ", amazon.url_space_delim) for link in amazon_link_container]
# extract product data:
amazon_product_data = pd.DataFrame(amazon.extract_product_data(amazon_product_links, amazon_header))
amazon_product_data.to_csv("../data/jurassic_amazon_products.csv")

# argos:
argos_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
argos = ProductExtract(filename="../config/argos_config.yaml")
argos_quick_soup= argos.quick_soup(argos.prod_urls, header=argos_header)
argos_product_links = argos.product_link_extractor(argos_quick_soup["Product_list_page"][0], argos.scrape_params["product_link_container"], argos.website, argos.url_space_delim)
# clean unneeded links:
argos_product_links_clean = []
for link in argos_product_links:
    if argos.list_of_products[0].replace(" ", argos.url_space_delim) in link:
        argos_product_links_clean.append(link)
    else:
        print(f"{link} not a product link")
argos_product_data = pd.DataFrame(argos.extract_product_data(argos_product_links_clean, argos_header))
argos_product_data.to_csv("../data/jurassic_argos_products.csv")

# smythstoys
# smythstoys_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
# smythstoys = ProductExtract(filename="../config/smythstoys_config.yaml")
# smythstoys_quick_soup = smythstoys.quick_soup(smythstoys.prod_urls, header=smythstoys_header)





# to improve given more time:
# an automative way to rotate user agents
# bash script that loads the config files from the config folder to automate the process
# Extract Load pipeline into a postgresql database
# a transformation layer script on its own.
# make it crawl through multiple pages (to note: some pages use java script so would have to integrate selenium headless fetcher to get this to work on both)
