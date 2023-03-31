# web_scrape_assessment
 webscraping system that extracts retail data to analyze


# Assesment answers and notes:

## Data & system context:

- context: I built a webscraping system that would allow the user to create a config.yaml file based on the retail customer they want to scrape and define the parameters they want to create their data tables on. For instance;   
                      - name : ''
                      - price : ''
                      - brand : ''
                      - instock : ''
                      - product_bar_code : ''
                      - customer_rating : ''
                      - rating_count : ''
                      - product_link_selector : ''
    The Yaml file asks the user for extra data that was not used in this assesment as I wanted to create a extract process load pipeline combined with postgresql and some of that data would be used to create my fact and dimension tables when modeling the data in a star schema. Effectively I have set it up in a way that I can create a data lake.

    Once the yaml file is occupied by the appropriate information, the user is able to scrape the data automatically and extract it into a csv table. I would then have liked to add the load aspect here.
    
- problems: I ran into user-agent issues with smythstoys domain and was not able to bypass the bot detection mechanism and run the config through this system to extract the data. Given more time, to work around this problem I would have created a system to automatically try and rotate different user-agents until the appropriate one was found for the task.

To continue on through the assesment, I used an in browser webscraping extension for google chrome to get this information. (it basically acted like a selenium browser).

I planed on adding selenium functionality into the scraping system but due to time I just stuck with bs4 and requests scrape. In the future this can be added.

- The data: To avoid error handling time restraints and having to deal with java script page loading which would inevitably make me have to design the selenium crawl, I kept my crawl to one page only and because of that argos only had 10 rows of data. The other two had respectively 70+ rows.

- the data extraction is done by the `extract.py` script. Ideally I would have fleshed this out so that the processes would be run by a bash script file.



## The answers:

1. Are there any individual products that are listed across the 3 sites? If so, please provide a list with links to each site. 
    
    - Using the EAN and other variant of the number was not reliable. Amazon for instance, uses the ASIN to identify products so I was not able to make a join between these tables as there was not an equivalent data point to join on. In the future I would have used an ASIN to EAN converter.
    - Argos and Smythstoys both had EAN numbers but within the scope of my argos data (10 records) I found no products that shared links across multiple sites. If I was to do this again and have more time, I would scrape a large multipage data set from argos and to truly zero in on product names I could also use string manipulation to create search terms of products on each site in order to ensure that cross site products exist.

2. Which brands/manufacturers are associated to the products?

    - I found that on some of the sites, there was no explicit container that had the "brand" column. So I had to create this column by string manipulation. The name of the product for some of the sites also listed the brand so I split the `name` column and created a `brand` column for the ones that didn't have the explicit container.
    - I got the list by effectively taking the uniques of this `brand` column and dropping the nulls.
    - the list:
      - 'LEGO',
      - 'WOW! STUFF',
      - 'WOW! PODS',
      - 'Posh Paws',
      - 'JoyKip',
      - 'Mattel',
      - "Rubie's",
      - 'Mattel Games',
      - 'Fisher-Price',
      - 'Clementoni'
      - 'Jurassic World',
      - 'Heroes of',
      - 'Ravensburger Jurassic',
      - 'Jurassic World:',
      - 'LEGO DUPLO',
      - 'LEGO Jurassic',
      - 'Imaginext Jurassic',
      - 'Jurassic Park'
      - 'LEGO DUPLO'
      - 'LEGO Jurassic World'

    - This can be found in the `analyse.py` script
    - I would improve this by creating a transformation layer script to automate some of the transformations done in this script but the bulk of my time went into engineering the scraper.
  
   3. Bonus question: Can you identify any specific IP or movie characters are part of the products (i.e. “Blue” Raptor from Jurassic World) from each of the products?

    - I created a function that the product name on dinosaurs under the assumption that the word before dinosuars is likely an IP.
    - To improve this system I would have created a map of IP names in jurassic park (potentially scraped that from another website) and then used the logic along the lines of: `if in my_map then is ip`.

    - the list:
      - smyths ips:
        - 'Triceratops',
        - 'Apatosaurus',
        - 'Iguanodon',
        - 'Sinotyrannus',
        - 'Sorna',
        - 'Raptor',
        - 'Sinoceratops',
        - 'Elaphrosaurus',
        - 'Siamosaurus',
        - 'Dreadnoughtus',
        - 'Eocarcharia',
        - 'Diabloceratops',
        - 'Atrociraptor',
        - 'Ichthyovenator',
        - 'Pteranodon',
        - 'Dryptosaurus',
        - 'Bumpy',
        - 'Chase',
        - 'Nothosaurus',
        - 'Atrociraptor',
        - 'Triceratops',
        - 'Kronosaurus',
        - 'Indoraptor',
        - 'Mosasaurus',
        - 'Spinosaurus',
        - 'Toro',
        - 'Giga'
  
   - amazon ips:
       - 'Atrociraptor',
       - 'Therizinosaurus',
       - 'Dominion',
       - 'Sinoceratops',
       - 'Rex',
       - 'Pteranodon',
       - 'Ichthyovenator',
       - 'KWINY',
       - 'Mighty',
       - 'Dominion',
       - 'Megaraptor',
       - 'Iguanadon',
       - 'Instincts',
       - 'Triceratops',
       - 'JoyKip',
       - 'Fanbusa',
       - 'Ankylosaurus',
       - 'Ampelosaurus',
       - 'Atrociraptor',
       - 'Skorpiovenator',
       - 'Siamosaurus',
       - 'Kentrosaurus',
       - 'Yangchuanosaurus',
       - 'Spinosaurus',
       - 'Rajasaurus',
       - 'Quetzalcoatlus',
       - 'Pyroraptor',
       - 'Velociraptor',
  
   - argos ips:
       - atrociraptor



## data source:

the code sources can be found on my github link : https://github.com/PaulWill92/web_scrape_assessment

the github layout is:
* config -> yaml files for each customer you plan on scraping
* data ->
  * raw_extract -> the raw data that gets scraped the first pass through by the `../scripts/extract.py` extraction layer script.
  * cleaned -> the data that is processed with the `../scripts/clean.py` pseudo transformation layer script.
* scripts -> all the script files used to extract, clean, and analyse the data.
