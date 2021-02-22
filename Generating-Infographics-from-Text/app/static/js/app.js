/*-----------------------------------------------------------
 * App's main JavaScript file | app/static/js/app.js
 *----------------------------------------------------------- */

// retrieves specified input field 
const searchBarInputField = document.getElementById('searchBar');
console.log(searchBar);

// executes function when user releases key on keyboard
searchBar.addEventListener('keyup', (e) => {
    const searchString = e.target.value;

    // Trigger element action with a keyboardevent key property
    if(e.keyCode === "Enter") {
        alert("You've pressed the 'ENTER' key!")
    }
}) 

/* Detects an onclick event on button "btnGenSimpleWordcloud" - triggers an image display to show up */
const btnGenSimpleWordcloud = document.getElementById('btnGenSimpleWordcloud');     console.log(btnGenSimpleWordcloud);
btnGenSimpleWordcloud.addEventListener("click", generateSimpleWordcloud);           console.log(generateSimpleWordcloud);

function generateSimpleWordcloud() {
    var simpleWordcloudWrapper = document.getElementById("wrapperSimpleWordcloud");
    console.log(wrapperSimpleWordcloud);

    if(simpleWordcloudWrapper.style.display === "none") {
        simpleWordcloudWrapper.style.display = "block";
    } 
    else {
        simpleWordcloudWrapper.style.display = "none";
    }
}

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

// Fetch request of page, includes the query of data element 

fetch('/infogen/${query}')
    .then(function(response){
        return response.text();
    }).then(function (text) {
        console.log('GET response text:');
        console.log(text); 
    });