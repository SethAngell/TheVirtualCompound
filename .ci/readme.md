# Continuous Integration Strategy

To simplify the deployment process, I want to try and consolidate as much of the building and configuration into a series of github actions. That way I can define a simple startup bash script to run at start, and then package the system in a docker container. I'll simply need an action to ssh into my host, pull the container, and restart with the fresh image. 

The sequence is as shown below:

```mermaid
graph TD;
    1[Open Pull Request Into Main] --> 2[Trigger Github Action];
    2 --> 3[Create Base Container];
    3 --> 4[Run Makemigrations];
    4 --> 5[Run Collectstatic];
    5 --> 6[Create Deployment Container];
    6 --> 7[Null Out Sensistive Environment Variables];
    7 --> 8[Push Container To Github Container Registry];
    8 --> 9[SSH Into Prod Server And Curl Deploy Script];
    9 --> 10[Run Deploy Script];
    10 --> 11[Wait For Docker Completion];
    11 --> 12[Notify Via Twilio Status Of Deployment];
```
