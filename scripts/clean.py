import pandas as pd

# given more time i would automate these cleaning functions and create them as a class

argos = pd.read_csv("../data/raw_extract/jurassic_argos_products.csv")
amazon = pd.read_csv("../data/raw_extract/jurassic_amazon_products.csv")
smyths = pd.read_csv("../data/raw_extract/jurassic_smythstoys_products.csv")



# preprocess amazon:
amazon.head()
# clean price:
amazon['price'] = amazon['price'].str.extract(r'(\d+\.\d+)', expand=False).astype(float)
amazon["brand"] = amazon["brand"].str.split("the ").str[1].str.split(" Store").str[0]

# associated brands:
amazon_associated_brands = [x for x in amazon["brand"].unique() if pd.notna(x)]

# preprocess argos:
argos.head()
argos['identifcation_number'] = argos['identifcation_number'].str.split(":").str[1].str.replace(".", "").astype(int)
argos["brand"] = argos["brand"].str.split(":").str[1].str.replace(".", "").astype(str)
argos[["currency", "price"]] = argos["price"].str.extract(r"^(\D+)([\d\.]+)$")

# preprocess smyths toys
smyths.head()
smyths["brand"] = smyths["product_name"].str.split().str[:2].str.join(" ")
smyths[["currency", "price"]] = smyths["product_price"].str.extract(r"^(\D+)([\d\.]+)$")
smyths["identification_number"] = smyths['indentification_number'].str.split(":").str[1].astype(int)
smyths['customer_rating'] = smyths['customer_rating'].str.extract(r'(\d+\.\d+)').astype(str) + "/5"
smyths_selected = smyths.loc[:, ["product_name", "customer_rating", "identification_number", "brand", "currency", "price"]]
smyths['customer_rating'] = smyths['customer_rating'].str.extract(r'(\d+\.\d+)').astype(str) + "/5"

