import os.path

from linkedin_api import Linkedin
from ChatGPT35TurboZeroShotPrompts import ChatGPT35

class LinkedinInstance:

    def __init__(self, usr:str, pwd:str, gpt:ChatGPT35):
        self.usr = usr
        self.pwd = pwd
        self.api = Linkedin(usr, pwd)
        self.gpt = gpt

    def get_linkedin_data(self, pub_url:str):
        if pub_url.endswith("/"):
            pub_url = pub_url[:len(pub_url)-1]
        pub_url = pub_url[pub_url.rindex("/")+1:]
        print("public-id:",pub_url)
        profile = self.api.get_profile(pub_url)
        return profile

    def get_job_description(self, jobid:str):
        print("job-id:", jobid)
        return self.api.get_job(jobid).get("description").get("text")

    def get_refined_profile(self, profile:dict, temp:float, wc:int):
        op = {}
        op["name"] = profile.get("firstName")+ " " + profile.get("lastName")
        for k, v in profile.items():
            if k == "location":
                continue
            if k in "industryName":
                op[k] = v
            if k in "locationName":
                op[k] = v
            if k in "public_id":
                op[k] = v
            if k in "languages":
                if len(v)>0:
                    print("GPT-Lang Call ...")
                    op[k] = self.gpt.generate_one_shot_linkedin_summary_topic(
                        topic={"language": v}, temp=temp, wc=20
                    )
                else:
                    op[k] = v
            if k in "summary":
                op[k] = v
            if k in "headline":
                op[k] = v
            if k in "experience":
                l = []
                for elm in v:
                    if "$anti_abuse_metadata" in elm.keys():
                        continue
                    if "projects" in elm.keys():
                        del elm["projects"]
                    if "entityUrn" in elm.keys():
                        del elm["entityUrn"]
                    if "geoLocationName" in elm.keys():
                        del elm["geoLocationName"]
                    if "geoUrn" in elm.keys():
                        del elm["geoUrn"]
                    if "company" in elm.keys():
                        del elm["company"]
                    if "region" in elm.keys():
                        del elm["region"]
                    if "companyUrn" in elm.keys():
                        del elm["companyUrn"]
                    if "companyLogoUrl" in elm.keys():
                        del elm["companyLogoUrl"]
                    l.append(elm)
                if len(l)>0:
                    print("GPT-Exp Call ...")
                    op[k] = self.gpt.generate_one_shot_linkedin_summary_topic(
                        topic={"experience": l}, temp=temp, wc=300
                    )
                else:
                    op[k] = l
            if k in "education":
                l = []
                for elm in v:
                    if "entityUrn" in elm.keys():
                        del elm["entityUrn"]
                    if "fieldOfStudyUrn" in elm.keys():
                        del elm["fieldOfStudyUrn"]
                    if "honors" in elm.keys():
                        del elm["honors"]
                    if "schoolUrn" in elm.keys():
                        del elm["schoolUrn"]
                    if "degreeUrn" in elm.keys():
                        del elm["degreeUrn"]
                    if "school" in elm.keys():
                        del elm["school"]
                    if "projects" in elm.keys():
                        del elm["projects"]
                    l.append(elm)
                if len(l)>0:
                    print("GPT-Edu Call ...")
                    op[k] = self.gpt.generate_one_shot_linkedin_summary_topic(
                        topic={"education":l}, temp=temp, wc=200
                    )
                else:
                    op[k] = l
            if k in "publications":
                l = []
                for elm in v:
                    if "description" in elm.keys():
                        del elm["description"]
                    del elm["authors"]
                    l.append(elm)
                op[k] = l
                if len(l) > 0:
                    print("GPT-Pub Call ...")
                    op[k] = self.gpt.generate_one_shot_linkedin_summary_topic(
                        topic={"publication": l}, temp=temp, wc=100
                    )
                else:
                    op[k] = l
            if k in "certifications":
                l = []
                for elm in v:
                    if "company" in elm.keys():
                        del elm["company"]
                    if "displaySource" in elm.keys():
                        del elm["displaySource"]
                    if "companyUrn" in elm.keys():
                        del elm["companyUrn"]
                    l.append(elm)
                op[k] = l
                if len(l) > 0:
                    print("GPT-Cert Call ...")
                    op[k] = self.gpt.generate_one_shot_linkedin_summary_topic(
                        topic={"certifications": l}, temp=temp, wc=100
                    )
                else:
                    op[k] = l
            if k in "honors":
                l = []
                for elm in v:
                    if "occupation" in elm.keys():
                        del elm["occupation"]
                    l.append(elm)
                op[k] = l
                if len(l) > 0:
                    print("GPT-Hons Call ...")
                    op[k] = self.gpt.generate_one_shot_linkedin_summary_topic(
                        topic={"honors": l}, temp=temp, wc=50
                    )
                else:
                    op[k] = l
        return op

