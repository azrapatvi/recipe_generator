from boltiotai import openai #type:ignore
import os
import markdown  #type:ignore
from apikey import OPENAI_API_KEY
from flask import Flask,request,render_template_string #type:ignore

openai.api_key=OPENAI_API_KEY

def generate_tutorial(components):
    response=openai.chat.completions.create(
        model="gpt-3.5-turbo",

        messages=[{"role":"system","content":"you are a helpful assistant"},
                  {"role":"user","content":f"Suggest a recipe using the items listed as available. Make sure you have a nice name for this recipe listed at the start. Also, include a funny version of the name of the recipe on the following line. Then share the recipe in a step-by-step manner. In the end, write a fun fact about the recipe or any of the items used in the recipe. Here are the items available: {components}, Haldi, Chilly Powder, Tomato Ketchup, Water, Garam Masala, Oil"}]

    )

    return response['choices'][0]['message']['content']



app=Flask(__name__)



@app.route("/",methods=['GET','POST'])
def hello():
    output=""
    if request.method=="POST":
        
        components=request.form['components']
        result = generate_tutorial(components)
        output = markdown.markdown(result)  # Convert Markdown to HTML
        #the hello() function is simply initializing an empty string output. If the request method is POST, meaning that the user has submitted a form with data, the function retrieves the value of the 'components' field from the form using request.form['components'] and calls a function named generate_tutorial() with that value.

    return render_template_string('''

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-LN+7fdVzj6u52u30Kp6M/trliBMCMKTyK833zpbD+pXdCLuTusPj697FH4R/5mcr" crossorigin="anonymous">

    <title>Recipe generator</title>
</head>

<body class="bg-white">
    <nav class="navbar navbar-expand-lg bg-dark border-bottom border-body" data-bs-theme="dark">
  <div class="container-fluid">
    <a class="navbar-brand" href="/">Recipe Generater</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="/">Home</a>
        </li>
        
      </form>
    </div>
  </div>
</nav>
                                  <h1 class="text-center mt-4 mb-5 fw-bold text-black">What's Cookin'? 👩‍🍳 Instant Recipe Generator</h1>

   <form  class="container mt-4 bg-light p-4" method="POST" action="/"> <div class="mb-3">
    <span class="fs-5">enter your ingredients:</span>
  <input type="text" class="form-control" name="components" placeholder="e.g., Onion, Potatoes" required>
</div>
<div class="mb-3">
  <input type="submit" class="btn btn-secondary" value="generate recipe" >
</div>
         
    <div class="card-body mt-4 container">
        <h4 class="fw-bold">Generated Recipe:</h4>
         <div id="output" class="mb-1 fs-5 text" style="white-space: pre-wrap">
{{ output|safe }}</div>
    </div>  
    </form>                      
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/js/bootstrap.bundle.min.js" integrity="sha384-ndDqU0Gzau9qJ1lfW4pNLlhNTkCfHzAVBReH9diLvGRem5+R9g2FzA8ZGN954O5Q" crossorigin="anonymous"></script>

    <script>

    </script>
</body>

</html>

''',output=output)

if __name__ == '__main__':
    app.run(debug=True) #app.run(host='0.0.0.0', port=8080)
