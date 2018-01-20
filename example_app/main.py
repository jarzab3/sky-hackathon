import re
import os
import json
import time
import random

ABS_FILE_PATH = os.path.dirname(os.path.realpath(__file__))


class FAQBot(object):
    """docstring for FAQBot"""

    with open(ABS_FILE_PATH + '/data/users.json') as json_data:
        user_database = json.load(json_data)

    with open(ABS_FILE_PATH + '/data/issues.json') as json_data:
        problems_database = json.load(json_data)

    random_status_msgs = ["An engineer is currently looking into this", "We are waiting on our provider to fix this"]

    def __init__(self, print_callback=None):
        super(FAQBot, self).__init__()

        self.started = False

        self.__memory_id = 0
        self.__memory_buffer = dict()

        self.print_buffer = []
        self.new_session_started = False
        self.print_callback = print_callback

    def __add_to_print_buffer(self, string):
        self.print_buffer.append(string)

    def __print(self):
        data_2_print = self.print_buffer
        self.print_buffer = []
        if not isinstance(self.print_callback, type(None)):
            self.print_callback(data_2_print)
        return data_2_print

    def reset_chat(self):
        self.started = False

    def start_new_session(self):
        self.new_session_started = False
        #self.__add_to_print_buffer("-"*50)
        self.__add_to_print_buffer("Hello, I am Sky Bot.")
        self.__add_to_print_buffer("Are you having some sort of problem that you want to talk to me about?")
        #return self.__print()

    def respond_to_user_request(self, user_input):
        if not self.started:
            self.started = True
            self.start_new_session()
        elif not self.new_session_started:
            regex = r'[\byes\b \bsure\b \byeah\b \bye\b]'
            if re.search(regex, user_input):
                #self.__add_to_print_buffer("")
                self.new_session_started = True
                self.__memory_id = 0
                self.__memory_buffer = dict()
                self.__process_data(user_input)
            else:
                self.__add_to_print_buffer("Ok, have a great day.")
                # self.start_new_session()
                self.started = False
        else:
            self.__process_data(user_input)
        return self.__print()

    def get_chat_state(self):
        if self.started:
            return [True]
        else:
            return [False]

    def __process_data(self, user_input):
        user_input = user_input.strip()
        if self.__memory_id == 0:
            self.__add_to_print_buffer("Ok, let me get some details so I can help you out")
            self.__add_to_print_buffer("Can you tell me your name, please?")
            self.__memory_id += 1
        elif self.__memory_id == 1:
            name = user_input
            self.__memory_buffer["user_name"] = name.lower()
            #self.__add_to_print_buffer("")
            self.__add_to_print_buffer("Lovely, thanks {name}".format(name=name))
            self.__add_to_print_buffer("Can you give me a title for your problem?")
            self.__memory_id += 1
        elif self.__memory_id == 2:
            self.__memory_buffer["title"] = user_input.lower()
            self.__add_to_print_buffer("Great, thanks for that")
            self.__add_to_print_buffer("Now, can you tell me what your issue is, in a bit more detail?")
            self.__memory_id += 1
        elif self.__memory_id == 3:
            self.__memory_buffer["description"] = user_input.lower()
            #self.__add_to_print_buffer("")
            self.__add_to_print_buffer("Ok, give me a second")
            self.__add_to_print_buffer("I'll just look into this for you...")
            #self.__print()

            successful = self.__process_question()
            if successful:
                self.__memory_id += 2
                self.__add_to_print_buffer("Thank you for using Kick ASS today")
                #self.__add_to_print_buffer("")
                # self.start_new_session()
                self.started = False
            else:
                #self.__add_to_print_buffer("")
                self.__add_to_print_buffer("Ok, I'm not sure I know how to handle your problem...")
                self.__add_to_print_buffer("So I'm passing it on to our customer service team")
                self.__report_problem()

                #self.__add_to_print_buffer("")
                self.__add_to_print_buffer("In the meantime, here are the top issues being reported:")
                #self.__add_to_print_buffer("")
                self.__show_top_questions()

                #self.__add_to_print_buffer("")
                self.__add_to_print_buffer("Would you like to speak to a real person about your problem?")
                self.__memory_id += 1
        elif self.__memory_id == 4:
            regex = r'[\byes\b \bsure\b \byeah\b \bye\b]'
            if re.search(regex, user_input):
                self.__add_to_print_buffer("OK.")
                self.__add_to_print_buffer("Redirecting conversion to human representative....")
                #self.__add_to_print_buffer("")
            
            self.__add_to_print_buffer("Thank you for using Kick ASS today")
            #self.__add_to_print_buffer("")
            # self.start_new_session()
            self.started = False
        else:
            #self.__add_to_print_buffer("")
            self.__add_to_print_buffer("?? Unknown request")
            self.__add_to_print_buffer("Thank you for using Kick ASS today")
            #self.__add_to_print_buffer("")
            # self.start_new_session()
            self.started = False

    def __process_question(self):
        found_question = False

        user_name     = self.__memory_buffer["user_name"]
        problem_title = self.__memory_buffer["title"]
        problem_body  = self.__memory_buffer["description"]

        if problem_title in self.problems_database.keys():
            found_question = True

            question = self.problems_database[problem_title]
            frequency = question["frequency"]
            self.problems_database[problem_title]["frequency"] += 1

            #self.__add_to_print_buffer("")
            self.__add_to_print_buffer("Ok, {0}".format(user_name.capitalize()))
            if frequency >= 1:
                self.__add_to_print_buffer("This is a known issue, I'm afraid")
                self.__add_to_print_buffer("{0} other users have also reported this issue today".format(frequency))
            else:
                self.__add_to_print_buffer("Thanks for contacting us with this issue")
                self.__add_to_print_buffer("I have reported it to our service team and they are going to look into it")

            #self.__add_to_print_buffer("")
            self.__add_to_print_buffer("Here is the current status from the service team:")
            self.__add_to_print_buffer("    {0}".format(question["status"]))
            #self.__add_to_print_buffer("")
            self.__add_to_print_buffer("I hope this has solved your problem...")
            self.__add_to_print_buffer("If not, please feel free to start a new chat")
            #self.__add_to_print_buffer("")

        return found_question

    def __report_problem(self):
        post_code     = ""#self.__memory_buffer["post_code"]
        
        title = self.__memory_buffer["title"]
        question = self.__memory_buffer["description"]
        update_time = time.time()
        keywords = [i.strip() for i in title.split(" ") if (len(i.strip()) > 0)]
        status = random.choice(self.random_status_msgs)

        self.problems_database[title] = {
            "question": question,
            "last_query_time": update_time,
            "keywords": keywords,
            "status": status,
            "frequency": 1
        }

        self.__save_issues()

    def __show_top_questions(self):
        top_questions = self.__get_top_questions()
        prefix = "    "

        #self.__add_to_print_buffer("")
        issue_string = ""
        i = 0
        for question in top_questions:
            issue_string += "{number}. Title: {title}, " \
                            "Issue: {issue}, " \
                            "Status: {status} ".format(number=i+1,
                                                       title=question['title'],
                                                       issue=question['question'],
                                                       status=question['status'])
            i += 1
            if i < len(top_questions):
                issue_string += "    +++++    "
            # #self.__add_to_print_buffer("-"*20)
            # self.__add_to_print_buffer("Title")
            # self.__add_to_print_buffer(prefix + question["title"])
            # self.__add_to_print_buffer("Issue")
            # self.__add_to_print_buffer(prefix + question["question"])
            # self.__add_to_print_buffer("Status")
            # self.__add_to_print_buffer(prefix + question["status"])
            # #self.__add_to_print_buffer("-"*20)
        self.__add_to_print_buffer(issue_string)

    def __get_top_questions(self, howmany=3):
        problems = self.problems_database.keys()

        sort_function = lambda x : self.problems_database[x]["frequency"]
        problems = sorted(problems, key=sort_function, reverse=True)

        response = []
        for index in range(min(len(problems), howmany)):
            problem = {
                "title": problems[index].capitalize(),
                "question": self.problems_database[problems[index]]["question"],
                "status": self.problems_database[problems[index]]["status"]
            }
            response.append(problem)

        return response

    def __save_users(self):
        with open(ABS_FILE_PATH + '/data/users.json', 'w') as json_file:
            json.dump(self.user_database, json_file, indent=4)

    def __save_issues(self):
        with open(ABS_FILE_PATH + '/data/issues.json', 'w') as json_file:
            json.dump(self.problems_database, json_file, indent=4)


def test():
    def print_callback(data):
        for data_2_print in data:
            print("::", data_2_print)

    my_bot = FAQBot()

    user_input = ""
    while True:
        print_callback(my_bot.respond_to_user_request(user_input))
        user_input = input(":: ")

if __name__ == '__main__':
    test()