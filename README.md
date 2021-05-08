# 2021_Spring_finals

## Project Design

By using Monte Carlo simulation, we want to design a program and study the click-through rate of mobile apps in the whole Chicago city. We will focus on a certain app, which is Tinder. If we are a developer of Tinder, we want to know how many people will open this app and the usage of Tinder. Depending on the weather, consumers' app preferences, consumers' economic conditions, and consumers' social groups, we will simulate how many people will open Tinder monthly and how these variables affect people's choices. We will assume that there are one million people in Chicago and do one million simulations to verify our hypothesis.

## Data Collection and analyze
To analyze the click-through rate of Tinder, we've collected related data from website.
In addition, we used "Pillow" package to convert the heat map into pixels since they have different colors. Then, we calculated the number of pixels in differnt colors, and we found distributions of each range and generate percentage.
### Population density

![image](https://user-images.githubusercontent.com/58837457/117296106-3f515b80-aea7-11eb-9c0c-df244b898117.png)

http://afterburnham.com/settlements/3-5-06-city-of-chicago-population-density-circa-2010/

### Household income

![image](https://user-images.githubusercontent.com/58837457/117296288-77589e80-aea7-11eb-9aa1-15fc5f6fd6f1.png)

https://www.reddit.com/r/dataisbeautiful/comments/5qcslz/income_distribution_in_chicago_oc/

### Age

![image](https://user-images.githubusercontent.com/58837457/117296325-850e2400-aea7-11eb-945f-210e542d2598.png)

http://proximityone.com/metros/pp17031_2010_001.htm


### User preference for different apps

There are no solid data online. Thus we make reasonable assumptions by ourselves.

![image](https://user-images.githubusercontent.com/58837457/117296519-bc7cd080-aea7-11eb-9d71-39e38f56eb78.png)


## App interface

We used pygame package to design this app, and designed the fonts by ourselves.

![image](https://user-images.githubusercontent.com/58837457/117295793-d9fd6a80-aea6-11eb-97b3-947cea9e2a94.png)

![image](https://user-images.githubusercontent.com/58837457/117296577-cd2d4680-aea7-11eb-9232-d50ef7422e23.png)

## Hypothesis

### H1: The daily click-through rate of Tinder app is less than 10%.

The daily click-through rate of tinder is 8.7%, less than 10%.

![image](https://user-images.githubusercontent.com/58837457/117296681-ea621500-aea7-11eb-8764-1566256a1320.png)


### H2: The weather affects consumers' choices.

To analyze the impact of weather, we added temperature variable into the model.

![image](https://user-images.githubusercontent.com/58837457/117296846-1a111d00-aea8-11eb-994d-52f089bfe519.png)

The trend of weather impact on click-through rate is looks like below.

![image](https://user-images.githubusercontent.com/58837457/117296971-3f9e2680-aea8-11eb-952d-c846e2e6ab31.png)

There is high correlation between weather and app click-through rate.



### H3: From an overall perspective, the different situations of consumers affect the choice of app they want to open.

Concluding from all the analysis above and the model we created. The different situations of consumers affect the choice of app they want to open.
