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
1. From postman hit the following url with a **POST** request: ```http://localhost:3015/user-query``` with a **json** payload of
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
2. Send a **POST** requst to the following endpoint ```http://localhost:3015/resume/upload``` with a resume.pdf file attached as a form-data payload. A sample resume can be found inside ```data/resume-sample``` directory.
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
3. Send a **GET** requst to the following endpoint ```http://localhost:3015/jobs/recommend-similar/686ab65d43d4d6cd3ff292fc``` to find similar jobs from the database. The params being the id of the job.
The output should look like the following.
```json
    {
    "data": [
        {
            "_id": "686ab65d43d4d6cd3ff292fc",
            "id": "bujhsos05Mw7LpP",
            "title": "Software Engineer (Java)",
            "company": "NICE",
            "location": "Hybrid - Pune",
            "experience": "2-4 Yrs",
            "experience_min_years": 2,
            "experience_max_years": 4,
            "post_date": "1 day ago",
            "link": "https://www.naukri.com/job-listings-software-engineer-java-nice-interactive-pune-2-to-4-years-050725016077",
            "key_skills": [
                "code versioning tools",
                "hibernate",
                "microservices",
                "cloud",
                "spring",
                "coding",
                "java",
                "computer science",
                "flex",
                "design",
                "product development",
                "english",
                "j2ee",
                "software engineering",
                "code review",
                "html",
                "software development",
                "engineering",
                "nice",
                "javascript",
                "spring boot",
                "microservices development",
                "scrum",
                "agile",
                "aws"
            ],
            "job_description": "<p></p><p><strong>So, what’s the role all about?</strong></p><p>We are looking for are developer with strong experience in design and coding, having a good understanding of developing Microservice application on cloud. Also, the person should have a keen focus on code quality, being able to write unit tests, do code reviews with a specific focus on security, and assisting, training, and coaching of other developers in writing secure software.</p><p><strong>How will you make an impact?</strong><strong>&nbsp;</strong></p><ul> <li>Deliver high quality, sustainable, maintainable code.Introduce security features and fixes in existing code base.</li> <li>Writing secure code and harden existing features.</li> <li>Participate in reviewing design and code (pull requests) for other team members – again with a secure code focus.</li> <li>Work as a member of an agile team responsible for product development and delivery.</li> <li>Adhere to agile development principles while following and improving all aspects of the scrum process.</li> <li>Follow established department procedures, policies, and processes.</li> <li>Adheres to the company Code of Ethics and CxOne policies and procedures.</li> <li>Excellent English and experience in working in international teams are required.</li></ul><p><strong>Have you got what it takes? </strong></p><ul> <li>BS or MS in Computer Science or related degree</li> <li>2+ years’ experience in software development</li> <li>Strong knowledge of Java.</li> <li>Strong knowledge of working and developing Microservices.</li> <li>Experience with AWS</li> <li>Extensive experience refactoring code and developing solutions with a minimum risk of regression.</li></ul><p><strong>What’s in it for you?</strong></p><p>Join an ever-growing, market disrupting, global company where the teams – comprised of the best of the best – work in a fast-paced, collaborative, and creative environment! As the market leader, every day at NICE is a chance to learn and grow, and there are endless internal career opportunities across multiple roles, disciplines, domains, and locations. If you are passionate, innovative, and excited to constantly raise the bar, you may just be our next NICEr!</p><p><strong>Enjoy NICE-FLEX! </strong></p><p>At NICE, we work according to the NICE-FLEX hybrid model, which enables maximum flexibility: 2 days working from the office and 3 days of remote work, each week. Naturally, office days focus on face-to-face meetings, where teamwork and collaborative thinking generate innovation, new ideas, and a vibrant, interactive atmosphere.</p><p><strong>Reporting into: </strong>Tech Manager, Engineering, CX<br><strong>Role Type: </strong>Individual Contributor</p><p>&nbsp;</p><p></p>"
        },
        {
            "_id": "686ab65d43d4d6cd3ff29317",
            "id": "qnyJRA5gcUUtG73",
            "title": "Software Engineer (Dot Net, AWS)",
            "company": "NICE",
            "location": "Hybrid - Pune",
            "experience": "2-4 Yrs",
            "experience_min_years": 2,
            "experience_max_years": 4,
            "post_date": "6 days ago",
            "link": "https://www.naukri.com/job-listings-software-engineer-dot-net-aws-nice-interactive-pune-2-to-4-years-300625007413",
            "key_skills": [
                "c#",
                "continuous integration",
                "cd",
                "development",
                "process",
                "analytical",
                "entity framework",
                "ci/cd",
                "relational databases",
                "ado",
                "azure devops",
                "sql",
                "microservices",
                "git",
                "application",
                ".net core",
                "collaboration",
                "design patterns",
                "writing",
                ".net",
                "troubleshooting",
                "software engineering",
                "aws",
                "communication skills"
            ],
            "job_description": "<p><strong>So, what’s the role all about?</strong></p><p>We are looking for a Software Engineer to join our growing team of highly skilled engineers working on a variety of applications and services to support our omni-channel, proactive communication platform. You will be working in multidisciplinary team with other professionals delivering high quality and secure software within an Agile delivery framework. The role will be based in Pune, India. Extensive collaboration and communication with UK and US based teams will be a key part of the job, so excellent communication skills are critical.&nbsp;</p><p><strong>How will you make an impact?</strong><strong> </strong></p><ul> <li>Write, test and maintain code which adheres to internal guidelines and industry best practices.</li> <li>Ensure applications are built to modern security standards.</li> <li>Write reusable code and libraries.</li> <li>Write automated tests to ensure code has the appropriate level of test coverage.</li> <li>Take part in code reviews (as reviewer and reviewee).&nbsp;</li> <li>Participate and contribute in team Scrum ceremonies.</li> <li>Create and maintain the required documentation.</li> <li>Responsible for defined tasks of low to medium complexity</li></ul><p><strong>Have you got what it takes? </strong></p><ul> <li>At least 3 years of software engineering experience.&nbsp;</li> <li>Strong C# experience including OOP and application of modern design patterns (2+ years).</li> <li>Strong in NetCore , Microservices,- EF/ Ado.Net</li> <li>Experience designing and building web-based products using the .NET Core framework.</li> <li>Experience working with public cloud platforms like AWS (preferred), Azure, and GCP.</li> <li>Strong relational database experience with proficiency in writing and troubleshooting SQL (preferably MySQL).</li> <li>Proficient in writing testable and reusable code and developing scalable applications.</li> <li>Proficient working with Git, Azure DevOps, CI/CD and other development process tooling.</li> <li>Excellent communication skills.</li> <li>Strong analytical and problem-solving skills.</li></ul><p><strong>What’s in it for you?</strong></p><p>Join an ever-growing, market disrupting, global company where the teams – comprised of the best of the best – work in a fast-paced, collaborative, and creative environment! As the market leader, every day at NICE is a chance to learn and grow, and there are endless internal career opportunities across multiple roles, disciplines, domains, and locations. If you are passionate, innovative, and excited to constantly raise the bar, you may just be our next NICEr!</p><p><strong>&nbsp;</strong></p><p><strong>Enjoy NICE-FLEX! </strong></p><p>At NICE, we work according to the NICE-FLEX hybrid model, which enables maximum flexibility: 2 days working from the office and 3 days of remote work, each week. Naturally, office days focus on face-to-face meetings, where teamwork and collaborative thinking generate innovation, new ideas, and a vibrant, interactive atmosphere.</p><p><strong><br>Reporting into: </strong>Tech Manager, Engineering, CX<br><strong>Role Type: </strong>Individual Contributor</p><p>&nbsp;</p>"
        },
        {
            "_id": "686ab65d43d4d6cd3ff29414",
            "id": "WbTelvWRid5TaSX",
            "title": "Software Engineer (Java, Angular)",
            "company": "NICE",
            "location": "Hybrid - Pune",
            "experience": "2-4 Yrs",
            "experience_min_years": 2,
            "experience_max_years": 4,
            "post_date": "3 weeks ago",
            "link": "https://www.naukri.com/job-listings-software-engineer-java-angular-nice-interactive-pune-2-to-4-years-130625028747",
            "key_skills": [
                "algorithms",
                "continuous integration",
                "fcc",
                "hibernate",
                "sql",
                "spring",
                "java",
                "git",
                "gcp",
                "design patterns",
                "j2ee",
                "jenkins",
                "data structures",
                "big data",
                "etl",
                "perforce",
                "jira",
                "communication skills",
                "annotation",
                "restful web",
                "software development",
                "microsoft azure",
                "nosql",
                "angular",
                "tableau",
                "ooad",
                "agile",
                "ioc",
                "aws",
                "etl process"
            ],
            "job_description": "<p>&nbsp;</p><p>&nbsp;</p><p><strong>So, what’s the role all about?</strong></p><p>A Java fullstack software developer is responsible for both frontend and backend development using Java-based technologies. Here's an overview of what you might expect in a job description for this role.</p><p><strong>How will you make an impact?</strong></p><ul> <li>Investigate, measure, and report on client's risk of suspicious or fraudulent financial activity.</li> <li>Follow SOPs as per anti-money laundering laws and carry out investigations. Identify areas for improving alert investigation process.</li> <li>Collaborate with auditors and regulators to minimize money-laundering risks to client’s business.</li> <li>Report and make notes and records of any suspicious transactions or activities in an efficient and timely manner.</li> <li>Proactive work on investigations within SLA and be a strong performer in the team</li> <li>Be well versed with FCC investigator solutions including Actimize (if possible)</li> <li>Work within service levels, KPI’s and in line with the regulatory best practice.</li> <li>Be up to date with trainings conducted for the investigation team, including workshops, conferences, and any certification or refresher training as required.</li> <li>Review risk and complete risk assessments as required.</li> <li>Maintain and update your knowledge of anti-money laundering compliance rules, regulations, laws, and best practices.</li> <li>Take part in and lead anti-money laundering compliance training on identifying suspicious activity to other team members.</li> <li>Indirect/direct consulting to clients.</li> <li>Provide domain expertise support during pre/post service sales process.</li></ul><p><strong>Have you got what it takes?</strong></p><ul> <li>Bachelor/Master of Engineering Degree in Computer Science, Electronic Engineering or equivalent from reputed institute</li> <li>2+ years of software development experience</li> <li>At least 2+ years of working experience in Core Java, proficient with Java algorithms and data structures</li> <li>Worked in high performance, highly available and scalable systems</li> <li>Strong experience with J2EE, Spring Framework, IOC, annotations</li> <li>Experience in any object-relational mapping (e.g. Hibernate)</li> <li>Strong knowledge of OOAD and Design patterns</li> <li>Development experience building solutions that leverage SQL and NoSQL databases</li> <li>Strong Development experience creating RESTful Web APIs</li> <li>Knowledge of BIG DATA and ETL Concepts (or BI tool like Tableau) will be added advantage</li> <li>Experience designing and developing scalable multi-tenant SaaS-based solutions</li> <li>Experience with public cloud infrastructure and technologies such as AWS/Azure/GCP etc</li> <li>Development experience in Angular</li> <li>Experience working in and driving Continuous Integration and Delivery practices using industry standard tools such as Jenkins</li> <li>Experience working in an Agile methodology development environment and using work item management tools like JIRA</li> <li>Experience with version control tools – GIT, Perforce</li> <li>Ability to work independently and collaboratively, good communication skill</li> <li>Bring a culture of Innovation to the job</li> <li>Ability to work under high pressure</li> <li>High attention to details and accuracy</li> <li>Experience with public cloud infrastructure and technologies such as AWS/Azure/GCP etc</li> <li>Experience working in and driving Continuous Integration and Delivery practices using industry standard tools such as Jenkins.</li> <li>Ability to work independently and collaboratively, good communication skill.</li> <li>Able to resolve problems of moderate scope which requires an analysis based on a review of a variety of factors.</li></ul><p><strong>You will have an advantage if you also have:</strong></p><ul> <li>Experience in Big data</li></ul><p><strong>What’s in it for you?</strong></p><p>Join an ever-growing, market disrupting, global company where the teams – comprised of the best of the best – work in a fast-paced, collaborative, and creative environment! As the market leader, every day at NiCE is a chance to learn and grow, and there are endless internal career opportunities across multiple roles, disciplines, domains, and locations. If you are passionate, innovative, and excited to constantly raise the bar, you may just be our next Nicer!</p><p><strong>Enjoy NiCE-FLEX! </strong></p><p>At NiCE, we work according to the NiCE-FLEX hybrid model, which enables maximum flexibility: 2 days working from the office and 3 days of remote work, each week. Naturally, office days focus on face-to-face meetings, where teamwork and collaborative thinking generate innovation, new ideas, and a vibrant, interactive atmosphere.</p><p><strong>Requisition ID: 7241<br>Reporting into: </strong>Tech Manager<br><strong>Role Type: </strong>Individual Contributor</p><p>&nbsp;</p>"
        }
    ],
    "count": 3
}
```
4. To scrape data from Naukri.com you may send a HTTP **POST** request to the following endpoint ```http://localhost:3015/scrape-jobs-naukri``` with a **json** payload of 
```json
{
    "search_query" : "Engineering Jobs",
    "start_page": 1,
    "end_page": 2
}
```
The data should be stored at ```data/naukri_output_merged.json``` location.

## ! Limitation
1. Couldn't scrape linkedin data due to security reasons.
3. The Job scoring mechanism is there but not fully functional so not implemented.

Thank you. Will keep on improving and implementing the other things.