from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
# What will this do?
# Get a list of [paa-links, Intro, Outro, Article-Reviews(Raw),
#  Images-from-stablediffusion, Extra-Graphs/performance based content items, short-summary]
# Convert to a .html 

# Interface for all possible actions - Link it with the Main BlogEngine that will take (connector(async), html-wrapper(), possible-places(top, middle, bottom))
# Each interface(eg.paa-links), 
# should return a <div></div> or a list of <p></p> tag (Stringifies anything that comes)
# Interface are fired with (Possible-input) 
# -> keyword(Is this is the only connecting mechanism?)
# -> Before paragraph (Can we get any context from this?)
#
# Introduce a bit of randomness in this stage(Don't do the same order of items)
# 
driver = webdriver.Chrome(ChromeDriverManager().install())

# Multi-threaded(Main thread), wih a single - file that gets written with content
class BlogEngine(object):

    def __init__(self, config) -> None:
        # Driver
        self.config = config
    
    def start():
        # Initialize all the locations based on config
        #  - Path to write for the main file
        #  - Image - storage location
        #  - Number of available workers and their type (paa, image, short-summary) instantiate
        pass

    def write(content:str):
        # Writes the content to the file (Additional checks if needed) - 
        # Has hold of the file at any given point in time
        pass

    def brain():
        pass
        # Only 3 things - What to write, where to write, 
        # randomness-> choice of the content that has to be written is chosen based on this
        # Pick from the following 
        #                           -> Meta-data generator - Description, Title Generator (Once for meta-data (other))
        #                           -> Get all reviews
        #                           -> Intro/outro(only once can be called), 
        #                           -> Image(Can be called once per review)
        #                           -> Paa-Links (Can be added before/after a heading - randomness will decide)
        #                           -> My common lines (Can be called anytime within a Review)
        #                           -> Comparison content (Gets generated from the reviews
        #                                  -> (Price based comparison, performance based comparison)) lines
        #                           
    # def what_next():
    #     pass
