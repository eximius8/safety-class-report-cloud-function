from main import generate_waste_rep
import json

# @todo write tests

""" 
data = { "name": "Отход 1", \
             "fkko": "78 946 46",\
             "safety_class": "IV", \
             "k": "45456",
             'filename': 'tesss',
             'safe_components': [],
             "components": \
             {"кКомпонент гавностенкока фавылопаловфып выфапло фывпрвыа ыфвапрывп авфы": \
                 {   "concp": "20", \
                     "concr": "58", \
                     "xi": "65", \
                     "zi": "4564",
                     "lgw": "1578",
                     "w": "342",
                     "k": "15",
                     "props": [], \
                 }, \
             "кКомпонент гавностенкока фавыл2": \
                 {   "concp": "25.8", \
                     "concr": "58", \
                     "xi": "5789", \
                     "zi": "4564",
                     "lgw": "1578",
                     "w": "342",
                     "k": "5.5", 
                     "props": [], \
                 }, \
             } 
         }
context={'data': data}

generate_waste_rep(request=json.dumps(context)) 
"""

# # context='{"name": "Отход 1",\
# #  "fkko": "78 946 46",\
# #   "safety_class": "158", \
# #   "components": \
# #     "{"component1": \
# #         "{"concp": "20", \
# #           "concr": "58", \
# #           "xi": "65", \
# #           "k": "15" \
# #          }" \
# #     }" }')



""" 

// Example POST method implementation:
async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}




postData(url = 'http://localhost:8080/', data = { "name": "Отход 1", 
             "fkko": "78 946 46",
             "safety_class": "IV", 
             "k": "45456",
             'filename': 'tesss',
             'safe_components': [],
             "components": 
             {"кКомпонент гавностенкока фавылопаловфып выфапло фывпрвыа ыфвапрывп авфы": 
                 {   "concp": "20", 
                     "concr": "58", 
                     "xi": "65", 
                     "zi": "4564",
                     "lgw": "1578",
                     "w": "342",
                     "k": "15",
                     "props": [], 
                 }, 
             "кКомпонент гавностенкока фавыл2": 
                 {   "concp": "25.8", 
                     "concr": "58", 
                     "xi": "5789", 
                     "zi": "4564",
                     "lgw": "1578",
                     "w": "342",
                     "k": "5.5", 
                     "props": [],                  }, 
             } 
         
}).then(data => {
    console.log(data); // JSON data parsed by `data.json()` call
  }); """