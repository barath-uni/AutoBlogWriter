# This file is to build a simple script that pulls in a lot of long tails as topic titles (Enough Search Volume, min in SERP 1-3)

# Get words, find low DA, low search volume keyword

# Clean-up manually (Edit the ones to better formed titles)

# Get the title

# Pull PAA

# Use the answers as additional info for steering the article

# Return a JSON - [{"keyword":{title:"What is the best ding dong", answers:[s,a,v]}}]
import people_also_ask
import json
import time
def get_paa_question_answers(title, count=5):
    answer=list()
    for question in people_also_ask.generate_related_questions(title):
        time.sleep(20)
        print(question) # print question + get_answer's() answer object
        answer_rec = people_also_ask.get_answer(question)
        time.sleep(20)
        if 'response' in answer_rec.keys():
            print("ANSWER RECEIVED")
            print(answer_rec)
            answer.append(answer_rec['response'])
            if len(answer) >= count:
                break
    print("ENDING")
    return answer

def generate_paa_title_answers(titles):
    dict_resp = list(dict())
    for title in titles:
        answers = get_paa_question_answers(title)
        dict_resp.append({title:{"title":title, "answer":answers}})
    with open('processor/processingkeyword.json', 'w') as f:
        json.dump(dict_resp, f)
    return dict_resp