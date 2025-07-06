# Joblo.ai assignment

## Prerequisites
- A mongoDB database server should be running on port 27017
- Python 3.12+ should be present

## How to setup and start running
1. Create venv by running ```python -m venv .venv```
2. Activate venv (by running ```source .venv/bin/activate``` or ```.\.venv\Scripts\activate```)
3. Upgrade pip by running ```python -m pip install -U pip```
4. Install all python dependencies by running ```pip install -r requirements.txt```
5. Install patchright chromium headless by running ```patchright install chromium``` (This is only required for scrapping naukri data)
6. To test I already have scrapped data which you may want to seed before starting the server.
To do so run ```python seed_data.py``` _Note: The mongoDB database shoulde be running on the mentioned port. Otherwise, it may cause error._
7. Add a ```.env``` file at the project location and add the ```GOOGLE_API_KEY``` environment variable.
8. Now finally run ```python start-server.py``` to start the server at port **3015**.

## Sample inputs (From postman)
1. From postman hit the following url: ```http://localhost:3015/user-query``` with a **json** payload of
```
{
    "query" : "Find me software developer jobs in bengaluru"
}
```
The output should look like the following:
```json
{
    "data": [
        {
            "_id": "686ab65d43d4d6cd3ff2935d",
            "id": "GzfiOsB0kTHf_WR",
            "title": "Software Developer Engineer 1- Digital Banking - Regional Sales",
            "company": "Kotak Life Insurance",
            "location": "Bengaluru",
            "experience": "0-4 Yrs",
            "experience_min_years": 0,
            "experience_max_years": 4,
            "post_date": "1 week ago",
            "link": "https://www.naukri.com/job-listings-software-developer-engineer-1-digital-banking-regional-sales-kotak-mahindra-life-insurance-company-limited-bengaluru-0-to-4-years-230625906207",
            "key_skills": [
                "Software development",
                "Java",
                "Mongo",
                "Node",
                "Junit",
                "SQL server",
                "Dynamo",
                "springboot",
                "microservices",
                "RabbitMQ",
                "Digital Banking",
                "load testing",
                "TDD",
                "MySQL",
                "Regional Sales",
                "Spring boot",
                "Oracle",
                "Postgress"
            ],
            "job_description": "<div><p>Technical Skills:<br>Experienced in building microservices using Node or similar (e.g: Java springboot) , api implementations (Spring boot, Node etc), Middleware (RabbitMQ etc..)<br>Experienced in using design patterns to address backend design problems<br>Excellent analytical, problem solving and debugging skills, perf analysis and remediation.<br>Hands-on experience in RDS (Oracle, Postgress, MySQL, SQL server etc) NoSQL (Mongo, Dynamo etc..)<br>Experienced on configuring and deploying services to be consumed using API gateways (AWS native, Kong etc) service discoverability, service security, service throttling etc<br>Hands on Experience in unit and feature testing, TDD, load testing Unit testing experience using Junit or similar.<br>Keeps updated with emerging back end technology innovations, improvements.<br></p><p>General Skills:<br>Detail oriented. Takes initiative, and ready to take ownership, displays commitment.<br>Should be open to work in a startup environment and have confidence to deal with complex issues and tackle high pressure situations focussed on solutions.<br>Education &amp; Experience:<br>At least an undergraduate degree in Computer Science, Engineering, or Mathematics, preferably from a Tier 1 college. BE preferred.<br>0-4 years of front-end experience</p></div>"
        }],
    "count": 6
}
```
2. Hit the following endpoint as ```http://localhost:3015/resume/upload``` with a resume.pdf file attached as a form-data payload. A sample resume can be found inside ```data/resume-sample``` directory.
It will return something like the following.
```json
{
    "data": [
        {
            "_id": "686ab65d43d4d6cd3ff29384",
            "id": "sXLv6gEiK6J-Q5X",
            "title": "Full Stack Software Engineer - React Native Development",
            "company": "Emperen Technologies",
            "location": "Bengaluru",
            "experience": "4-6 Yrs",
            "experience_min_years": 4,
            "experience_max_years": 6,
            "post_date": "1 week ago",
            "link": "https://www.naukri.com/job-listings-full-stack-software-engineer-react-native-development-emperen-technologies-bengaluru-4-to-6-years-250625920625",
            "key_skills": [
                "React Native",
                "TypeScript",
                "Mobile Application Architecture",
                "Java",
                "JavaScript",
                "SWIFT",
                "iOS",
                "Android",
                "Kotlin"
            ],
            "job_description": "<p></p><p><b>About the Role : </b><br><br>We are seeking a highly motivated and experienced Full Stack Software Engineer with a strong focus on React Native development to join our growing team in Pune.<br><br>In this role, you will be responsible for designing, developing, and maintaining high-quality mobile applications for both Android and iOS platforms, while also contributing to backend development.<br><br>You will work closely with other engineers, product managers, and designers to deliver exceptional user experiences.<br><br><b>Responsibilities : </b><br><br>- Develop and maintain cross-platform mobile applications using React Native.<br><br>- Implement front-end features and UI components with a focus on performance and user experience.<br><br>- Integrate mobile applications with backend services via RESTful APIs.<br><br>- Contribute to backend development, as needed, using appropriate technologies.<br><br>- Write clean, well-documented, and testable code.<br><br>- Participate in code reviews and contribute to improving code quality.<br><br>- Collaborate with designers to implement UI/UX specifications.<br><br>- Instrument applications with analytics frameworks (e.g., Google Analytics, Mixpanel).<br><br>- Troubleshoot and debug issues across different platforms.<br><br>- Stay up-to-date with the latest trends and best practices in mobile and web development.<br><br>- Effectively communicate technical designs and considerations to peers and product leadership.<br><br>- Own tasks and resolve ambiguity in requirements.<br><br>- Adapt to evolving development tasks and priorities.<br><br>- Balance trade-offs between speed and quality based on business priorities.<br><br><b></b></p><p><b>Qualifications : </b><br><br>- 4+ years of experience as a software engineer.<br><br>- 3+ years of experience with React Native or a similar JavaScript/TypeScript framework.<br><br>- 3+ years of experience in mobile development for Android and/or iOS.<br><br>- 3+ years of experience with Swift, Java, and/or Kotlin.<br><br>- Experience instrumenting applications with an analytics framework like Google Analytics or Mixpanel.<br><br>- Strong foundation in object-oriented or functional programming.<br><br>- Experience consuming RESTful APIs.<br><br>- Solid understanding of the full development life cycle.<br><br>- Hands-on knowledge of a version control system such as Git (including commands like cherry-pick and rebase).<br><br>- Disciplined approach to development, testing, and quality assurance.<br><br>- Desire for a deep technical understanding of systems and architecture.<br><br>- Continuous learning mindset, keeping current on development best practices and trends.<br><br>- Excellent communication and collaboration skills.<br><br>- Ability to reason with and adapt to evolving development tasks and priorities.<br><br>- Ability to balance trade-offs between speed and quality based on business priorities.<br><br><b>Bonus Points : </b><br><br>- Experience with other mobile development frameworks (e.g., Flutter, Ionic).<br><br>- Experience with cloud platforms (e.g., AWS, Azure, GCP).<br><br>- Experience with testing frameworks (e.g., Jest, Detox).<br><br>- Contributions to open-source projects.</p>"
        },
        {
            "_id": "686ab65d43d4d6cd3ff293bf",
            "id": "qKcXM85mdA1cmHD",
            "title": "Senior Dot Net Software Engineer",
            "company": "Ascendion",
            "location": "Hyderabad, Bengaluru",
            "experience": "5-9 Yrs",
            "experience_min_years": 5,
            "experience_max_years": 9,
            "post_date": "6 days ago",
            "link": "https://www.naukri.com/job-listings-senior-dot-net-software-engineer-ascendion-engineering-hyderabad-bengaluru-5-to-9-years-300625003357",
            "key_skills": [
                "C#",
                "Dotnet Development",
                "dotnet core",
                "Azure",
                "React"
            ],
            "job_description": "<p> Location: Bangalore, Hyderabad </p><p>Notice Period: Immediate to 20 days </p><p>Experience: 5+ years </p><p>Relevant Experience: 5+ years </p><p>Skills: Dotnet, Dotnet core, C#, React, Azure</p>"
        },
        {
            "_id": "686ab65d43d4d6cd3ff29447",
            "id": "n7p75T55GqE169z",
            "title": "Software Engineer (.Net Fullstack)",
            "company": "A.P. Moller Maersk",
            "location": "Hybrid - Bengaluru",
            "experience": "5-8 Yrs",
            "experience_min_years": 5,
            "experience_max_years": 8,
            "post_date": "3 weeks ago",
            "link": "https://www.naukri.com/job-listings-software-engineer-net-fullstack-a-p-moller-maersk-bengaluru-5-to-8-years-291124015779",
            "key_skills": [
                "C#",
                ".Net Core",
                "Azure",
                "Cloud",
                "SQL",
                "React",
                "Angular"
            ],
            "job_description": "<p> </p><p>Maersk is set to be the global integrated logistics carrier of choice and a huge part of this strategy involves the supply chain management platform. Although supply chain is traditionally an asset heavy business; a new wave of digital innovation has meant that assets alone are no longer differentiators. Customers are asking for more visibility and deeper integration with their supply chain capabilities. The capabilities we offer is what is really going to make us stand apart. Maersks supply chain platform team is on an ambitious journey to build truly world class supply chain management capabilities which provide our global client list the flexibility they seek.</p><p><strong>We Offer -</strong><br><strong>Joining Maersk will embark you on a great journey with career development in a global organization.&nbsp;</strong><br>Designs, develops, tests, delivers, maintains and improves business applications as a member of a team. The software engineer can works across the full stack or be specialized in e.g. the frontend or the backend - through the entire software development lifecycle.<br></p><p><strong>We are looking for</strong><br>Strong working experience Full stack developer in C#, JavaScript/typescript and any framework(Angular/React/Vue) and Agile.<br>Experience building scalable web application using ASP.NET Core<br>Seasoned developer with excellent understanding on EF core, and SQL server,<br>Solid understanding on DevOps methodologies(CICD/Docker or Kubernetes) &amp; Unit testing/Integration testing.<br>Experience in code versioning on git<br>• Hands on experience in developing scalable, resilient, secure, and quality engineering products; preferably in logistics space<br>• Strong belief and demonstrated ability to iterate and evolve architecture<br>• A solid understanding of cloud native architectures<br>• Strong opinions loosely held<br>• Experience with building and managing microservices through its life cycle (versioning, backward compatibility)<br>• Experience with cloud platforms (Azure/AWS/GCP); preferably in Azure<br>• Comfortable with Agile / DevOps practices and tools<br>• Exposure to distributed caching, failure detection algorithms &amp; application failover strategies is desirable.</p><p>Experience with building self-healing, automatic fault detection and recovery mechanisms is good to have.<br>• Masters Degree in Computer Science, Computer Engineering, or alternatively Bachelor's Degree or higher in an IT related discipline.<br>• A great team player and a strong collaborator<br>• Excellent English verbal and written communication is a must<br> <br><strong>Key Responsibilities:</strong><br>• Work within engineering teams and contribute in delivering quality products on time and continuously retire technical debt<br>• Technically analyze business requirements and be able to convert them into software solutions.<br>• Work on complete end to end software development/implementation with adequate unit testing, automation testing and monitoring.<br>• Able to troubleshoot technical challenges in software designs and any production incidents that may arise for delivered business solutions.<br>• Follow DevOps and be able to make any configuration changes to support necessary deployments for business deliverables.<br>• Participates in building, supporting and operating software in a DevOps model<br>• Making more productive, effective, and efficient business deliverables possible by working closely and in collaboration with the team.<br>• Coach team members to be more productive, effective, and efficient by showing the way</p><p>Having substantial operations in over 130 countries, we work across continents, across cultures and with individuals from all walks of life. This drives our ambition, to create equitable and inclusive workplaces where every individual can have a sense of belonging.</p>"
        }
    ],
    "count": 3
}
```


## ! Limitation
1. The Docx format resume is not supported yet.
2. Couldn't scrape linkedin data due to security reasons.
3. The Job scoring mechanism is there but not fully functional so not implemented.
4. The similar job recommendation is yet to be implemented.

Thank you. Will keep on improving and implementing the other things.