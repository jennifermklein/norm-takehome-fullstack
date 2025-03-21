# Westeros Capital Group

Welcome! Please follow the instructions below to run the application.

![image](./app/kingdoms_of_westeros_by_keyser94_dd03kjv-414w-2x.jpg)

### Prerequisites

- Clone the repository

- Generate an API key from [OpenAI](https://platform.openai.com/settings/organization/api-keys) and add it to an .env file in your root directory as `OPENAI_API_KEY=<key>`.

- Make sure you have [Docker](https://docs.docker.com/engine/install/) installed and running.

### Build and Run

- Build the docker image by running: `docker build -t westeros .`

- Run the service via command: `docker run -p 8000:80 --env-file .env westeros`. This will run the server on port 8000 and make the api key you added to .env accessible.

- Access the FastAPI endpoints locally via the Swagger UI at: [http://localhost:8000/docs]()

- Enter a query string into the `laws/query` endpoint and click "Execute". Scroll to the Response body section to see the query, response, and citations.

### Reflective Response Section

<i>What unique challenges do you foresee in developing and integrating AI regulatory agents for legal
compliance from a full-stack perspective? How would you address these challenges to make the system
robust and user-friendly?</i>

During my decade-long career as a lawyer, I always felt that the legal industry was severely underutilizing technology. I even had a law school professor who never learned how to type. The conservative and risk-averse culture of the field makes people hesitant to try new things, and the billable hours model incentivizes taking on time-consuming and tedious tasks. Despite these long-standing norms, many lawyers are starting to see the value of AI and are eager to integrate it into their workflows.

From a full-stack perspective, one of the biggest challenges in developing AI regulatory agents for legal compliance is the diversity and unpredictability of regulations with respect to their language, formatting, and scope. An industry may be subject to regulations from various agencies and levels of government, and there are no guarantees that regulatory documents will provide consistent clues to their meaning. This exercise, while only providing one short PDF as a source, demonstrates the nature of the challenge. The PDF has a few idiosyncrasies to take into account while parsing. For example, the document has a citations section at the end; some subsections contain legal content (e.g. 3.1. The Widow's Law...), while other subsections serve only as headers for additional content(e.g. 4.1 Trials of the Crown). In this document, bolded font indicates a major section or subsection, which is helpful for parsing. If the subsections had not been bolded, or if there had been inconsistent type formatting in the document, the parsing would have been even more challenging.

Using LLM models, while incredibly useful, also poses challenges. In this case, we see that the citation numbering returned by the LLM is somewhat confusing—the citations do not always appear in order, and the citations list includes sources that may not have actually been considered. We can, of course, add logic to reformat the citations, but the model itself may change with respect to its output, or we may switch to a different model, requiring us to update our parsing logic and related UI. LLM responses may also be difficult to evaluate and maintain, as they are not necessarily deterministic and may change as the model is updated or retrained—an especially significant challenge when serving lawyers, who may demand higher levels of accuracy than professionals in other fields.

To address these challenges, I would attempt to build a parsing system based on heuristics, likely with a human in the loop, to attain the level of accuracy desired by lawyers. To make the system robust, it would be helpful to implement a feedback loop, allowing users to indicate when responses are inadequate so the system can be updated to account for any edge cases undermining performance. Additionally, making the system user-friendly would involve tailoring the sources to the industry or company using the service. For example, an energy company would likely need to know about environmental regulations, while those regulations might be less relevant to a financial firm.

It will be exciting to follow developments in legal tech and see how the industry is transformed by AI and the powerful tools emerging in its wake.
