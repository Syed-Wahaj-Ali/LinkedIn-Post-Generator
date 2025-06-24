import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm

def preprocessing(data_dir:json,save_path:json='data/processed_data.json')->json:
    """
    The Data Directory takes the path of your json file.
    The Save_Path saves your preprocessed json file
    """
    co_post_data = []
    # Reading the file
    print("Loading the data....!")
    with open(data_dir,encoding='utf-8') as file:
        posts = json.load(file)
        
        print('Data Loaded ✔')
        print('Preprocessing....!')
        
    for post in posts:
        post_txt_data = post['text'].encode('utf-8', 'replace').decode('utf-8') # This hectic line of code it due to encoding issue our text contains 2 types of ecoding patterns
        meta_data = meta_data_extractor(post_txt_data)
        post_meta_data = post | meta_data
        co_post_data.append(post_meta_data)

    unified_tags = get_unified_tags(co_post_data)

    for post in co_post_data:
        current_tags = post['tags']
        new_tags = {unified_tags[tags] for tags in current_tags} # Using Dict comprehension (i.e. {}) to avoid duplicates
        post['tags'] = list(new_tags)
    
    print('Tags Updated...')
    print('Preprocessing Done ✔')

    with open(save_path,encoding='utf-8',mode='w') as outfile:
        json.dump(co_post_data,outfile,indent=4)
        print(f'File Saved Successfully at {save_path}')

# Our meta data extractor takes help from llm to separate out the lines of interest from given text.
def meta_data_extractor(post_txt):
    # Giving Template to llm

    template = ''' 
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, language and tags. 
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means hindi + english)

    Here is the actual post on which you need to perform this task:  
    {post_txt}'''
    
    pt = PromptTemplate.from_template(template)

    chain = pt | llm

    response = chain.invoke(input={"post_txt":post_txt})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException as error:
        raise error("The output is too large unable to handle")
    
    return res


def get_unified_tags(post_with_meta_data):

    unique_tags = set()

    for post in post_with_meta_data:
        unique_tags.update(post['tags'])
    
    unique_tag_list = ', '.join(unique_tags)
    
    pmt = '''
    I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list. 
    Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
    Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
    Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
    Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
    2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
    3. Output should be a JSON object, No preamble
    3. Output should have mapping of original tag and the unified tag. 
    For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation}}
    
    Here is the list of tags: 
    {unique_tag_list}'''

    pmt = PromptTemplate.from_template(pmt)

    chain = pmt | llm

    response = chain.invoke(input={'unique_tag_list':unique_tag_list})

    try:
        output_parser = JsonOutputParser()
        res = output_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException('The input is unable to handle')
    
    return res
        
if __name__ == '__main__':
    dir_path = 'data/raw_posts.json'
    save_path = 'data/preprocessed_data.json'
    preprocessing(data_dir=dir_path,save_path=save_path)