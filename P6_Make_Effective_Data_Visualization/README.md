# Make Effective Data Visualization using d3.js and dimple.js

### Summary

This chart visualizes the percent distribution of flights arriving on-time at the ten most busiest US airports from 2003 to 2014 against US GDP per Capita. It illustrates the performances of these airports over time where there is a marked dip from 2003 to 2007, at which point things improve and peak at 2012 and recent trends from 2012 to 2014 show a steady decline. It appears that airport performace as described by percent flights arriving on-time is negatively correlated with GDP per Capita in the United States.

### Design

#### Initial

The dataset was downloaded from [RITA](http://www.transtats.bts.gov/OT_Delay/ot_delaycause1.asp?display=download&pn=0&month=7&year=2015) from 2003 till July, 2015, and the GDP data was downloaded from [WorldBank](http://data.worldbank.org/indicator/NY.GDP.PCAP.CD). Exploratory data analysis was conducted in Excel and Rstudio. The underlying hypothesis was that airport performance given by the percentage of timely flights would increase over time. I seemed logical that in a capitalist economy, customer happiness of flights departing on-time would be a driving force for airports and airlines. Initially, I surveyed the number of arrivals and delays at airports in Excel and decided that a line chart would be the best representation as opposed to a bar chart. I decided to remove 2015's data as the year is incomplete for the story I wanted to tell. In Rstudio, I produced a line chart faceted by airports as seen below:

![Starting R Plot](https://raw.githubusercontent.com/arvin-dwarka/Udacity_Data_Analyst/master/P6_Make_Effective_Data_Visualization/data/Rplot.png)

There was clearly too many, but it was a start. I then subsetted the dataset for arrivals to the 99th quantile to get the top ten airports. Plotting this dataset gave a much better visualization of the busiest airports and their performance over time:

![Final R Plot](https://raw.githubusercontent.com/arvin-dwarka/Udacity_Data_Analyst/master/P6_Make_Effective_Data_Visualization/data/final_plot.png)

I exported the dataset from Rstudio into `data.csv` file for easier javascript manipulation. I replicated the plot using d3.js and dimple.js in `index_initial.html`. I iterated on it multiple times so that I could get the best feedback from my interviewees. I suspected that the ten line plots would be too dense to interpret well. So I reduced the opacity and added some interactions with the line plots on mouse-over.

#### Final

The feedback that I received was mainly positive as they all were able to read and interpret the chart without my guidance. The only qualms seemed to be in aesthetics that can be improved upon. Based on the feedback, I isolated each concern and address them accordingly:

- `title placement`: Fixed this using css stylesheet for the `h1` tag.
- `sore eyes`: I thought that it was trivial at first, but some research revealed that bright white backgrounds with high contrast colours doesn't play well with the eyes. I changed the body background colour using the css stylesheet to a beige tone.
- `chart is a little busy`: I wrestled with this one a fair bit as I was concerned about **lie factor** with truncating the y-axis further. But, admittedly, the chart did look crowded in some places. I finally settled on using the lowest **valley** of 64% as y-axis' minimum value.
- `manually select lines`: This was a great idea, but took so long to implement! By looking at some dimple.js examples, I was able to draw some inspiration on how to make the graph even more interactive by allowing manual selection. 
- `causation of the trends`: I decided not to focus on this as the explanation to the trends observed is beyond the scope of this visualization. At the very least, it would have spurred readers to do their own research.


#### Final v2

This iteration was spurred by the feedback from my Udacity project evaluator. The comments were overall great, but the visualization didn't tell a proper story of airport performance by the economy's performance. I added a bar chart of `GDP per Capita` as a measure of the economy in a second y-axis. The main struggle was around the limitations of dimple.js where I had to implement some workaround given the nature of my dataset. 

I was also able to get a hold of interviewee #3 for another round of feedback. His comments help validate the there is enough information on the chart to tell a story of airport performance versus economic performance. There were no addition feedback to promt another iteration at this point.

### Feedback

I interviewed three people face-to-face to collect feedback, mainly focusing on the relationships, takeaways and confusions in the visualization. The following are transcripts of the three interviews that lasted about 5-10 minutes each.

*Interview #1*
> This looks cool! I like how clean it looks from the charts made in Excel! At first, I thought that there was a lot going on. But after a second or two, I could easily follow the trend of the overall data. The light coloured lines and the distinct data points helped me read the chart better. I can see the pattern in the data where it dips till 2007 and then bounces back up till 2012 and then it starts to fall again. I wonder what's going on in Houston airport lately?
> A couple feedback would be the title and the fact that my eyes feel a little strained. The title looks disconnected from the chart. I'm not sure what's up with my eye. Maybe from looking at all the cool animations for too long?

*Interview #2*
> Wow! I would never have guessed that Detroit would beat San Francisco  by 12 percentage points! You'd think somebody in Silicon Valley would have disrupted the airport logistic market by now...
> The animations make it look neat, but I feel that the chart is a little busy. I would have liked to focus on a select few lines so that I can compare them. Maybe, play with the y-axis a bit more? The data looks scrunched up in some places. Other than that it looks great!

*Interview #3*
> What's up with that title? It looks disconnected from everything else. I like the legends that you have! It lines up nicely and the colours help a lot. I can follow the trends - what happened in 2007? Can't be the recession, can it? I like that when I hover over a line it gets bolded. This was cool since the graph is dense in some places. Overall, it's a great graph. I like it!

*Interview #3 v2*
> This looks much better! It seemed that the recession did have an effect on flights arriving on time at major US airports. Strangely, it's a positive effect - except for Atlanta. Perhaps, it makes sense that more spending power would lead to more air travellers thus causing congestion and logistical nightmares at airports. I also like the changes you made. They make the graph look so much more polished. The contrast between the coloured lines and the grey bar chart helps me focus on each individual piece easily. Lastly, I really like how you scaled the other y-axis. It doesn't interfere with the line graphs at all.


### References
- [Negative CSS Selectors](http://stackoverflow.com/questions/726493/negative-css-selectors)
- [mbostock's blocks](http://bl.ocks.org/mbostock)
- [d3js documentation](http://d3js.org/)
- [Visual encoding](https://www.targetprocess.com/articles/visual-encoding/)
- [dimplejs documentation](dimplejs.org)
- [Udacity forum](discussions.udacity.com)
- [getbootstrap.com](http://getbootstrap.com/getting-started/)
- [High contrast visuals](http://ux.stackexchange.com/questions/23965/is-there-a-problem-with-using-black-text-on-white-backgrounds)