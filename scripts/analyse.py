import pandas as pd

# Tables:
amazon = pd.read_csv("../data/cleaned/jurassic_amazon.csv")
argos = pd.read_csv("../data/cleaned/jurassic_argos.csv").rename({"identifcation_number":"identification_number"}, axis=1)
smyths = pd.read_csv("../data/cleaned/jurassic_smyths.csv")



# Are there any individual products that are listed across the 3 sites? 
# If so, please provide a list with links to each site. 

# amazon uses the ASIN to identify products and I was not able to find another identifier. Given more time I would likely do more cleanup on the name string and attempt a join there
merged_df = argos.merge(smyths, on="identification_number")
# argos and smyths did not return any common values on identification EAN numbers
# This means the scope of data that I scraped, did not overlap and due to a time constraint, I can not scrape more data.
# I also believe that the EAN numbers are represented differently across both sites.
# The config is set up with the built crawler to allow to get more data but time is a constraint.







# Which brands/manufacturers are associated to the products?
# associated brands:
brands = []
amazon_associated_brands = [x for x in amazon["brand"].unique() if pd.notna(x)]
argos_associated_brands = [x for x in argos["brand"].unique() if pd.notna(x)]
smyths_associated_brands = [x for x in smyths["brand"].unique() if pd.notna(x)]
# the associated brands i found are:
#  'LEGO',
#  'WOW! STUFF',
#  'WOW! PODS',
#  'Posh Paws',
#  'JoyKip',
#  'Mattel',
#  "Rubie's",
#  'Mattel Games',
#  'Fisher-Price',
#  'Clementoni'
# 'Jurassic World',
#  'Heroes of',
#  'Ravensburger Jurassic',
#  'Jurassic World:',
#  'LEGO DUPLO',
#  'LEGO Jurassic',
#  'Imaginext Jurassic',
#  'Jurassic Park'
#  'LEGO DUPLO'
#  'LEGO Jurassic World'

# Bonus question: Can you identify any specific IP or movie characters are part of the products
# (i.e. “Blue” Raptor from Jurassic World) from each of the products?
def extract_dinosaur_words(*lists):
    result = []
    for lst in lists:
        for string in lst:
            split_string = string.split("Dinosaur")
            if len(split_string) > 1:
                word = split_string[0].split()[-1]
                result.append(word)
    return list(filter(None, result))

smyths_product_names = smyths["product_name"].unique().tolist()
amazon_product_names = amazon["name"].unique().tolist()
argos_product_names = argos["name"].unique().tolist()
smyths_ips = list(set(extract_dinosaur_words(smyths_product_names)))
amazons_ips = list(set(extract_dinosaur_words(amazon_product_names)))
argos_ips = list(set(extract_dinosaur_words(argos_product_names)))
# 'Triceratops',
#  'Apatosaurus',
#  'Iguanodon',
#  'Sinotyrannus',
#  'Sorna',
#  'Raptor',
#  'Sinoceratops',
#  'Elaphrosaurus',
#  'Siamosaurus',
#  'Dreadnoughtus',
#  'Eocarcharia',
#  'Diabloceratops',
#  'Atrociraptor',
#  'Ichthyovenator',
#  'Pteranodon',
#  'World',
#  'Dryptosaurus',
#  "'Bumpy'",
#  'Plush',
#  'Chase',
#  'Nothosaurus',
#  'Mask',
#  'Sounds',
#  'Atrociraptor',
#  'Triceratops',
#  'Rex',
#  'Kronosaurus',
#  'Indoraptor',
#  'Rex',
#  'Mosasaurus',
#  'Rex',
#  'Spinosaurus',
#  'Toro',
#  'Giga'

# amazon ips:
#  'Atrociraptor',
#  'Therizinosaurus',
#  'Dominion',
#  'Sinoceratops',
#  'Rex',
#  'Pteranodon',
#  'Ichthyovenator',
#  'KWINY',
#  'Mighty',
#  'Dominion',
#  'Megaraptor',
#  'Iguanadon',
#  'Instincts',
#  'Triceratops',
#  'JoyKip',
#  'Fanbusa',
#  'Ankylosaurus',
#  'Ampelosaurus',
#  'Atrociraptor',
#  'Skorpiovenator',
#  'Siamosaurus',
#  'Kentrosaurus',
#  'Yangchuanosaurus',
#  'Spinosaurus',
#  'Rajasaurus',
#  'Quetzalcoatlus',
#  'Pyroraptor',
#  'Velociraptor',

# argos ips:
# rex
# atrociraptor






#  What other additional interesting insights you think may be relevant to the Jurassic Park
#  Franchise owners (NBC Universal)?