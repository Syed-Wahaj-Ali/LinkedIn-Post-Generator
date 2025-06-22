import json

def preprocessing(data_dir:json,save_path:json='data/processed_data.json')->json:
    """
    The Data Directory takes the path of your json file.
    The Save_Path saves your preprocessed json file
    """
    co_post_data = []
    # Reading the file
    with open(data_dir,encoding='utf-8') as file:
        posts = json.load(file)
        for post in posts:
            post_txt_data = post['text'].encode('utf-8', 'replace').decode('utf-8') # This hectic line of code it due to encoding issue our text contains 2 types of ecoding patterns
            meta_data = meta_data_extractor(post_txt_data)
            post_meta_data = post | meta_data
            co_post_data.append(post_meta_data)
    for epost in co_post_data:
        print(epost)

# Our meta data extractor takes help from llm to separate out the lines of interest from given text.
def meta_data_extractor(text):
    return {
        'Num_lines':100,
        'Language': 'English',
        'type': ['mental health','job hunting']
    }
    
if __name__ == '__main__':
    dir_path = 'data/raw_posts.json'
    save_path = 'data/preprocessed_data.json'
    preprocessing(data_dir=dir_path,save_path=save_path)