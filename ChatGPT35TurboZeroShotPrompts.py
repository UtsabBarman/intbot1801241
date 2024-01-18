from openai import OpenAI
import json


class ChatGPT35:

    def inits(self, key: str):
        self.client = OpenAI(
            api_key=key,
        )

    def generate_interview_questions(self, your_profile: dict, job_des: str, temp: float, wc: int,
                                     extra_text: str = ""):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": "You will be provided with a profile of a data scientist in JSON. "
                               "You will also be provided a job description in plain text. "
                               "Your task is to write ask 10 interview questions as an interviewer for the job described in "
                               "backticks."
                               "Generate the output in json array, each element will be a dictionary with a key called 'q'.\n"
                               f"{extra_text}"
                               f"target job description: ```{job_des}```\n"
                               f"candidate profile: {str(your_profile)}\n"
                               f"interview questions for the job ==> \n"
                },

            ],
            temperature=temp,
            max_tokens=wc
        )
        return response.choices[0].message.content

    def generate_one_shot_summary(self, job_des: str, temp: float, wc: int):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": "You will be provided with job description in plain text. "
                               "Your task is to summarize the job requirements in english. "
                               "Generate the output in text with bullet points.\n"
                               f"target job description: ```{job_des}```\n"
                               f"summary:"
                },

            ],
            temperature=temp,
            max_tokens=wc
        )
        return response.choices[0].message.content

    def generate_one_shot_linkedin_summary_topic(self, topic: dict, temp: float, wc: int):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": "You will be provided with JSON within back ticks."
                               "Your task is to summarize output in plain text as if you are writing your resume."
                               f"```{topic}```\n"
                               f"summary:"
                },

            ],
            temperature=temp,
            max_tokens=wc
        )
        return response.choices[0].message.content


    def answer_interview_questions(self, your_profile: dict,  question:str, temp: float, wc: int):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": "You will be provided with a profile of a candidate in JSON. "
                               "Your task is to answer ask interview questions as the candidate. Be less formal. D"
                               "Generate the output in plain text.\n"
                               f"question: {question}"
                               f"candidate profile: {str(your_profile)}\n"
                               f"answer ==> \n"
                },

            ],
            temperature=temp,
            max_tokens=wc
        )
        return response.choices[0].message.content


    def evaluate_answer(self, answer: dict,  question:str, temp: float, wc: int):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": "You will be provided with a question and an answer. "
                               "Your task is to score the answer on the scale of 0.0-1.0. "
                               "Generate the output in plain text.\n"
                               f"question: {question}"
                               f"candidate answer: {str(answer)}\n"
                               f"score ==> \n"
                },

            ],
            temperature=temp,
            max_tokens=wc
        )
        return response.choices[0].message.content
