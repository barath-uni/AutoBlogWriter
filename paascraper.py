import people_also_ask

def get_list_of_ques_answer(ques):
    list_of_qa = list(dict())

    questions = people_also_ask.get_related_questions(ques,10)

    for question in questions:
        val = people_also_ask.get_simple_answer(question, depth=True)
        list_of_qa.append({"question":question, "answer":val})
    return list_of_qa

if __name__ == "__main__":
    get_list_of_ques_answer("portable air cooler")
