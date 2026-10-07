from fastapi import FastAPI

app=FastAPI() #obj of fastapi class

@app.get("/") #defining a route for the endpoint using a decorator /...get signifies get request to fetch the data from the server...here if anyone hits website "/" then they will be at the home route...this route is listening to get method...the function if executed returns the dictionary
def hello():
    return{'message':'Hello World'}

@app.get('/about')
def about():
    return{'message':'Hi my name is Niladri Baksi and this is my first FastAPI api'}

#so "/" is the home endpoint and 
# "/about" is the abou0t endpoint
#"/docs" will take us to the interactive documentation of our api where we can see and interact with and about our endpoints