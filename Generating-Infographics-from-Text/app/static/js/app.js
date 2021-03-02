/*-----------------------------------------------------------
 * App's main JavaScript file | app/static/js/app.js
 *----------------------------------------------------------- */

 /* Fired when initial HTML document been completely loaded & parsed */
 document.addEventListener("DOMContentLoaded", function(event){
     btnGenerators = document.querySelectorAll("btnGenerators").disabled = true;
 });

let isFunctionWorking = false;

/* Detects an onclick event on button "btnGenSimpleWordcloud" - triggers an image display to show up */
let btnGenSimpleWordcloud = document.getElementById('btnGenSimpleWordcloud');    
console.log(btnGenSimpleWordcloud);

if (btnGenSimpleWordcloud) {
    btnGenSimpleWordcloud.addEventListener("click", generateSimpleWordcloud);          
    console.log(generateSimpleWordcloud);
}

/* Fetch () call awaits the response from Flask's /infogen endpoint */
fetch('/infogen')
    .then(function(response){
        
        if(response.ok) {
            // successfully return response object
            // return response.text()
            return generateSimpleWordcloud()

        } else {
            throw new Error ("Oops! Something went wrong here")
        }
    })

    // .then(() => generateSimpleWordcloud()) 
    // console.log('GET response text:');
    //  console.log(text);
    
    .catch((error) => {
        console.log(error)
});

/* Triggers the HTML button elements to be "active" */
function generateSimpleWordcloud() {
    isFunctionWorking = true
    let wrapperWordcloud = document.getElementById("wrapperSimpleWordcloud");
    console.log(wrapperSimpleWordcloud);
    

    if (btnGenSimpleWordcloud.disabled == true) {
        btnGenSimpleWordcloud.disabled = false
        
        btnGenSimpleWordcloud.style.cursor = "pointer"
    
        if (wrapperWordcloud.style.display === "none") {
            wrapperWordcloud.style.display = "block";
        } 
        else {
            wrapperWordcloud.style.display = "none";
        }
    }
}



/* Detects an onclick event on HTML button "btnGenTimeline" */
let btn = document.getElementById('btnGenTimeline');
if (btn) { btn.addEventListener("click", generateTimeline); }

function generateTimeline() {

    if(btn.disabled == true) {
        btn.disabled = false

        let wrapperTimeline = document.getElementById("wrapperTimeline")
        console.log(wrapperTimeline);

        if(wrapperTimeline.style.display === "none") {
            wrapperTimeline.style.display = "block";
        
        } else {
            wrapperTimeline.style.display = "none";
        }
    }
}

// retrieves specified input field 
/* const searchBarInputField = document.getElementById('searchBar');
console.log(searchBar);

// executes function when user releases key on keyboard
searchBar.addEventListener('keyup', (e) => {
    const searchString = e.target.value;

    // Trigger element action with a keyboardevent key property
    if(e.keyCode === "Enter") {
        alert("You've pressed the 'ENTER' key!")
    }
})  */



/* Detects an onclick event on button "btnGenSimpleWordcloud" - triggers an image display to show up */
// const btnGenStyledWordcloud = document.getElementById('btnGenSimpleWordcloud');     console.log(btnGenStyledWordcloud);
// btnGenStyledWordcloud.addEventListener("click", generateStyledWordcloud);           console.log(generateStyledWordcloud)
// function generateStyledWordcloud() {
//     var maskedWordcloudWrapper = document.getElementById("wrapperMaskedWordcloud");
//     console.log(wrapperMaskedWordcloud);

//     if(maskedWordcloudWrapper.style.display === "none") {
//         maskedWordcloudWrapper.style.display = "block";
//     }
//     else {
//         styledWordcloudWrapper.style.display = "none";
//     }
// }

// /* Detects onclick event on button "btnGenMapVisualisation" - triggers an image display to show up */
// const btnGenMapVisual = document.getElementById('btnGenMapVisualisation');      console.log(btnGenMapVisual);
// btnGenMapVisual.addEventListener("click", generateMapVisual);

// function generateMapVisual() {
//     var wrapperMappedVisual = document.getElementById("wrapperMapVisualisation");
//     console.log(wrapperMappedVisual);

//     if(wrappedMappedVisual.style.display === "none"){
//         wrappedMappedVisual.style.display = "block";
//     }
//     else {
//         wrappedMappedVisual.style.display = "none";
//     }
// }

// fetches data from HTML /infogen page
// fetch('/infogen')
//     .then(function(response) {
//         return response.json();
//     }).then(function(text) {
//         console.log('GET response: ');
//         console.log(text.greeting);
//     });

// function display_query_results() {
//     fetch('/infogen')
//         .then(function(response){
//             return response.text();
//         }).then(function (text)) {
//             console.log('GET response text: ');
//             console.log(text);
//         });


// }

/* Fetch () call awaits the response from Flask's /infogen/${query} endpoint */
// fetch('/page/${query}')
//     .then(function(response){
//         if(response.ok) {
//             // successfully return response object
//             // response.text();
//             return displayImage() 
//         } else {
//             throw new Error ("Oops! Something went wrong here")
//         }
//     })
//     .catch((error) => {
//         console.log(error)
// });

// /* Detects an onclick event on button "btnDisplay" - triggers an image display to show up */
// const btn = document.getElementById('btnDisplay');    
// btn.addEventListener("click", displayImage);          

// function displayImage() {
//     var wrapperImage = document.getElementById("wrapperImage");
//     console.log(wrapperImage);
    
//     if(btn.disabled == true) {
//         btn.disabled = false
       
//         btn.style.cursor = "pointer"

//         if(wrapperImage.style.display === "none") {
//                 wrapperImage.style.display = "block";
//         } 
//         else {
//                 wrapperImage.style.display = "none";
//         }
//     }
// }