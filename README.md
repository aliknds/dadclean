# dadclean

The idea of **dadclean** (Drag-and-Drop Cleaning) is to make a UI based program (that will run on Windows/Linux/Mac) to reduce the data cleaning part of the job based on common patterns that can be found in specific .csv files that should be cleared. 

For example, you have a .xslx file that have a ton of sub .xslx files into it and you should be able to extract those .xslx files separately (if you want to work with them as .csv files). This kind of job has to be done if there is a necessity in visualizing them as internal Excel based capabilities are limited compared to what Python matplotlib.pyplot offers. In this case, you can use **dadclean**, which will offer the features to work with your data and clean them in seconds according to your wishes.

Also, program should be able to handle .csv files in variety of languages and translate them into English, so it could be easier to work with data further, for example, in Tableau.

# UI
![image](https://github.com/aliknds/dadclean/assets/132540921/6214feed-1999-400a-9cba-06f702a98259)

**dadclean** uses [tkinter](https://docs.python.org/3/library/tkinter.html#module-tkinter) as its UI library. Also, there should be web interface in the future that will be able to run in localhost and cloud.
