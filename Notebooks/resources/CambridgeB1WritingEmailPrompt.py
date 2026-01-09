

from resources.CambridgeAssessmentCriteria import CambridgeAssessmentCriteria


class CambridgeB1WritingEmailPrompt:
    def __init__(self):
        self.criteria = {
            CambridgeAssessmentCriteria.Content.value: "Does the answer fulfill the task requirements? Is the response relevant and complete? Ensure the TaskAnswer is not just a repetition of the TaskAssessment. If it is, deduct points and provide feedback.",
            CambridgeAssessmentCriteria.CommunicativeAchievement.value: "Is the language appropriate for the task? Does the answer address the context? Check for originality and appropriate extensions of the TaskAssessment.",
            CambridgeAssessmentCriteria.Organization.value: " Is the response coherent and well-organized? Are ideas logically connected? If the answer repeats the TaskAssessment, penalize for lack of coherence.",
            CambridgeAssessmentCriteria.Language.value: " Is the grammar accurate and vocabulary appropriate for the level? Ensure that new vocabulary or grammar structures are used in the answer compared to the task.",
        }

    def get(self, question: str = '', answer: str = '') -> str:
        return f"""
        
        Task: The input consists of a standard rubric, an email and a set of four prompts presented as notes linked by lines to the appropriate parts of the input email text.
              The task gives candidates the context, who they are writing to, why they are writing, and four key content points.
              Candidates must include the four content points in a response of around 100 words.
              The task requires candidates to demonstrate the ability to handle the language of functions. For example, agreeing, disagreeing, giving an opinion, offering and explaining.

        
        Context:
         - The response must be evaluated based on Cambridge's B1 assessment criteria:
                {self.get_assessment_criteria()}
         - You are expected to provide a score (0-5) for each criterion and brief constructive feedback (Not more than 5 sentenses). 
         - The task answer and a few-shot example of evaluations have been provided to guide your assessment.
         - Use Cambridge Assessment  B1 Preliminary Handbook with which you have been trained to support your evaluation
         - Use the Common European Framework of Reference with which you have been trained to support your evaluation
         - Only reply for each assessment criteria doesnt add anyting else.    
        
        Criteria Score band Descriptors:
       
        
        **{CambridgeAssessmentCriteria.Content.value} Subscale for Writing Assessment:**

        Band 5:
         - **{CambridgeAssessmentCriteria.Content.value}:** All content is relevant to the task. Target reader is fully informed.
         - **Explanation:** The writer included everything that the task required them to include. The reader has all the necessary information. The target reader is clearly identified (for example: the readers of a magazine or the writer’s English teacher).
        
        Band 3:
         - **{CambridgeAssessmentCriteria.Content.value}:** Minor irrelevances and/or omissions may be present. Target reader is on the whole informed.
         - **Explanation:** Would the reader have all the information they need? The task always tells the candidate what information to include. Some of these content requirements do not need much development (for example, say what...) and some parts require more development (for example, describe... or explain...).
        
        Band 1:
         - **{CambridgeAssessmentCriteria.Content.value}:** Irrelevances and misinterpretation of task may be present. Target reader is minimally informed.
         - **Explanation:** The writer clearly didn’t understand something in the task. (For example: a Part 2 task asked the candidate to write about what makes them laugh, but instead they wrote about things they enjoy in general.) The writer included something that wasn’t necessary or related to the task.
        
        Band 0:
         - **{CambridgeAssessmentCriteria.Content.value}:** Content is totally irrelevant. Target reader is not informed.
         - **Explanation:** The writer did not include anything relevant to the task.
        
        **{CambridgeAssessmentCriteria.CommunicativeAchievement.value} Subscale for Writing Assessment:**
        
        Band 5:
         - **{CambridgeAssessmentCriteria.CommunicativeAchievement.value}:** Uses the conventions of the communicative task to hold the target reader's attention and communicate straightforward ideas.
         - **Explanation:** These include genre, format, register, and function. For example, a personal letter should not look like a formal report, and an email to a teacher would probably be more formal and polite than an email to a close friend.  
           This is a good thing! It means the reader is interested, not distracted, and it’s not difficult for the reader to make sense of the text.
        
        Band 3:
         - **{CambridgeAssessmentCriteria.CommunicativeAchievement.value}:** Uses the conventions of the communicative task in generally appropriate ways to communicate straightforward ideas.
         - **Explanation:** These are usually concrete, limited in subject, and are communicated with relatively simple style, words, and grammar.
        
        Band 1:
         - **{CambridgeAssessmentCriteria.CommunicativeAchievement.value}:** Produces text that communicates simple ideas in simple ways.
         - **Explanation:** These typically require only one or a few words to communicate. For example, "I like pop music" or "Let’s go next week."
        
        **{CambridgeAssessmentCriteria.Organization.value} Subscale for Writing Assessment:**
        
        Band 5:
         - **{CambridgeAssessmentCriteria.Organization.value}:** Text is generally well-organised and coherent, using a variety of linking words and cohesive devices.
         - **Explanation:** Not in every way or every case, but most of the time.  
           Easy to understand because the ideas and sentences are well connected.
        
        Band 3:
         - **{CambridgeAssessmentCriteria.Organization.value}:** Text is connected and coherent, using basic linking words and a limited number of cohesive devices.
         - **Explanation:** Basic linking words show an explicit connection between ideas and sentences. These include "for example," "because," "finally," and so on.  
           Linking words are one type of cohesive device, but cohesive devices include other words and phrases that connect ideas and words within a text, such as pronouns (she, theirs, etc.), substitution (the last one, this, etc.), relative clauses (...which is why...) and so on.
        
        Band 1:
         - **{CambridgeAssessmentCriteria.Organization.value}:** Text is connected using basic, high-frequency linking words.
         - **Explanation:** High-frequency linking words include "and," "so," "because," "first of all," and so on.
        
        **{CambridgeAssessmentCriteria.Language.value} Subscale for Writing Assessment:**
        
        Band 5:
         - **{CambridgeAssessmentCriteria.Language.value}:** Uses a range of everyday vocabulary appropriately, with occasional inappropriate use of less common lexis.  
           Uses a range of simple and some complex grammatical forms with a good degree of control.  
           Errors do not impede communication.
         - **Explanation:** Everyday vocabulary means words or phrases that are used often in the context mentioned in the task. For example, when talking about a picnic in the park, people often mention a *blanket* and *snacks*.  
           Less common lexis is vocabulary that is understandable but not often used in this context, such as *gourmet food* or *seating arrangements*.  
           This means the writer seems to be in control of their grammar – they are not making lucky guesses! They can consistently use grammar that is accurate and suits the context.
        
        Band 3:
         - **{CambridgeAssessmentCriteria.Language.value}:** Uses everyday vocabulary generally appropriately, while occasionally overusing certain lexis.  
           Uses simple grammatical forms with a good degree of control.  
           While errors are noticeable, meaning can still be determined.
         - **Explanation:** Vocabulary is appropriate when it fits the context of the task and the other words around it. For example, if a candidate writes *Big snow makes getting around the city difficult* in an article, the expression *getting around the city* is appropriate for the style of an article, but *big snow* is not appropriate because the usual expression is *heavy snow*.  
           Sometimes, candidates repeat the same word or phrase a lot because they don’t seem to know other vocabulary they could use to express their ideas.  
           *Big snow* is a good example of an error which does not impede communication. The reader can probably understand what the writer means, but they might be distracted for a moment while they think about it.
        
        Band 1:
         - **{CambridgeAssessmentCriteria.Language.value}:** Uses basic vocabulary reasonably appropriately.  
           Uses simple grammatical forms with some degree of control.  
           Errors may impede meaning at times.
         - **Explanation:** This is the kind of vocabulary you need for basic survival – simple transactions, for example.

    
        Few Shots Examples:
        Example 1:
        <TaskAssessment>
            Rubric: 
              Write your answer in about 100 words in an appropriate style on the opposite page.
              Read this email from your English teacher, Mrs Rose, and the notes you have made.
                
            From: Mrs Rose
            Subject: New film club
            Body: 
                I’d like to start an after-school Film Club.
                We can meet either on Monday or Friday afternoon. Which one would you prefer?
                Which types of film would you like to see?
                I want to provide some food and drink during the films. Is this a good idea?
                Please let me know what you think.
                Many thanks!
             Notes: 
              - Note 1:
                Note: That's great
                Email Part: I’d like to start an after-school Film Club.
              - Note 2:
                Note: Explain
                Email Part: We can meet either on Monday or Friday afternoon. Which one would you prefer?
              - Note 3:
                Note: Explain which
                Email Part: Which types of film would you like to see?
              - Note 4:
                Note: Give your opinion
                Email Part: I want to provide some food and drink during the films. Is this a good idea?
        </TaskAssessment>
        <TaskAnswer> 
        Good afternoon Mrs Rose
        I just got your email and I think it’s really great idea becase I think lots of people like watching films.
        I personally would prefer Mondays because on Fridays I often have other plans with my family
        I would really love to see some detective or some action films but I relly do’t mind watching something different.
        I think it’s good idea to have some food or drink during the film because lots of people are used to it because in cinemas they always eat something so i think it would be great
        Have a nice day
        </TaskAnswer>  
        Result: {{
            "{CambridgeAssessmentCriteria.Content.value}": {{
                "score": 5,
                "feedback": "
                - All content is relevant to the task.
                - The target reader is fully informed about all the points in the task and there is a direct and clear response to each one in turn.
                - The candidate covers the first point, I think it’s really great idea, and clearly says which day they would prefer and explains why. The candidate explains which types of films they would like to see, and gives an opinion about providing food and drink during the films.
                - This script therefore obtains a 5 for content as the content points are addressed and appropriately developed."
            }},
            "{CambridgeAssessmentCriteria.CommunicativeAchievement.value}": {{
                "score": 5,
                "feedback": "
                - The conventions of an email are used, with opening and closing salutations appropriate for the candidate’s context, and there is also a reference to the input email at the beginning: I just got your email. The register is consistent and appropriate.
                - The email holds the reader’s attention throughout, and communicates straightforward ideas in direct response to the input email. Points are expressed and explained very clearly."
            }},
            "{CambridgeAssessmentCriteria.Organization.value}": {{
                "score": 4,
                "feedback": "
                - The email is well organised and always coherent, with a clearly demarcated short paragraph for each point.
                - There is some use of referencing as a cohesive device: lots of people are used to it; so I think it would be great, and the text flows naturally, although there is over-reliance on some linking words, such as because."
            }},
            "{CambridgeAssessmentCriteria.Language.value}": {{
                "score": 4,
                "feedback": "
                 - A range of everyday vocabulary appropriate for the topic is used: detective or some action films; I personally would prefer; other plans with my family.
                 - There is a good degree of control of language: but I really don’t mind watching something different; lots of people are used to it; in cinemas they always eat something. There are very few errors and none which impede communication.
                 - The candidate could improve their language mark by evidencing more use of complex grammatical forms, and more variety in sentence structure."
            }}
        }}

       
        
        Task to evaluate: 
        <TaskAssessment>{question}</TaskAssessment> 
        <TaskAnswer>{answer}</TaskAnswer>
    
        Desired Output Format:
            - The output format should be JSON 
            - Mantain camel case and spaces format for criteria. 
        """

    def get_assessment_criteria(self):
        if isinstance(self.criteria, dict):
            return '\n\t\t'.join(f"--{key}: \"{value}\"" for key, value in self.criteria.items())
        return ""
