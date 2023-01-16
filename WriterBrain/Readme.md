# AutoBlogWriter




### What does this DO? - This Package takes care of the "Actual" Content Generation

## What are the available components

1. Rich Information Generator

    a. GPT Generator

    b. Sentiment Analyser

## What does the Brain DO

1. Implements a BlackBoard Pattern -> There is an expert/module that fires only when a certain condition is met
2. The overall Goal is **WC(Word Count)** followed by the following Module Satisfaction
   
   a. Outline (Given a Topic, Title, Content Desc) -> Create a {Heading:Para} JSON and append

   b. Sentiment(Fine Grained, will receive only after some Data Analysis)

   c. Vocabulary Check(Is the Vocabulary good enough and not bland)
   
   d. First-Person Counter(I,WE, YOU)
   
   e. Observation Generator (Joke/Observation)
   
   f. Content Generation (Primary Model that generates Content within each subheading)

### Module and the GPT Interface

The package also primarily involves a simple Interface to connect to Different GPT versions. 

1. Outline -> GPT-3 (Davinci-002 or higher)
2. Content Generation -> GPT-3 (Davinci-002 or higher)
3. Eloborate -> GPT-2/GPT-3 (ada/curie) cheaper versions
4. Sentiment Tilter -> GPT-2 or GPT-3 (ada/curie)
5. Observation/Joke generation -> Experiment with GPT-2 or GPT-3(ada/curie)


### BlackBoard Initialization

1. To init the brain of the writer, just hold an instance of the class __Blackboard()__ and that should be fine. 

    a. write_article -> title, topic, description

2. Pre-process to Do some Topic, Title, Description Cleaning (Given these 3, do they really make sense to generate content on) -> Should be a manual process for now
3. Post-Process -> After an Article is generated, interface the JSON to send it for HTML creation, be aware of the fact that we would have to generate Image
   
    a. As the first step in this process, after a JSON is created, it is sent to IMAGE-BRAIN pipeline where an Image is generated

    b. After the Image is created, move it for HTML conversion

