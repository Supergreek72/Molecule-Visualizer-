
function rotateMolecule(){

    if ($('#degrees').val() === "") {
        alert('Please enter a value for the degrees.');
        return; // Exit the function without sending the $.post request
    }

    //check for sql injections
    if (containsSpecialChar($('#degrees').val())) {
        alert('Input cannot contain semicolons or double quotes.');
        return; // Exit the function without sending the $.post request
    }
    /* ajax post */
    $.post("/RotateMol.html",
    /* pass a JavaScript dictionary */
    {
        molName: $("#moleculeSelect").val(),	/* retreive value of name field */
        axis:    $("#rotateSelect").val(),
        degrees: $("#degrees").val(),
    },
        function( data, status )
    {
        $("#image-container").html(data)
        
        // Scale the SVG to fit the container
        const svg = $("#my-svg")[0]; // get the first element with id="my-svg"
        svg.setAttribute('viewBox', '0 0 100 100');
    }
);
}



function resetDatabase(){

    if (window.confirm("Are you sure you want to delete this item?")) {
        // User clicked "OK"
        // Delete the db
        /* ajax post */
        $.post("/clear-db.html",
        /* pass a JavaScript dictionary */
        {
            //do nothing, just send a signal to reset database
        },
            function( data, status )
        {
            alert("Data: " + data + "\nStatus: " + status )
            //reset all tables and selects
            $("#atomNum").text("")
            $("#bondNum").text("");
            $('#moleculeSelect').empty()
        }
        );
      } else {
        // User clicked "Cancel"
        // Do nothing
      }
    
}

function getAtoms(){

    /* ajax post */
    $.post("/get-atoms.html",
    /* pass a JavaScript dictionary */
    {
        molName: $("#moleculeSelect").val(),	/* retreive value of name field */
    },
        function( data, status )
    {
        $("#atomNum").text(data);
    }
    );
}

function getBonds(){

    /* ajax post */
    $.post("/get-bonds.html",
    /* pass a JavaScript dictionary */
    {
        molName: $("#moleculeSelect").val(),	/* retreive value of name field */
    },
        function( data, status )
    {
        $("#bondNum").text(data);
    }
    );
}



$(document).ready(function() {
    $.ajax({
        url: '/get-values',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            // Populate the select dropdown with the data
            var select = $('#moleculeSelect');
            $.each(data, function(index, value) {
                select.append($('<option>').text(value).attr('value', value));
            });
            getAtoms();
            getBonds();
        },
        error: function(xhr, textStatus, errorThrown) {
            alert('Error: ' + errorThrown);
        }
    });

    // Listen for changes on the dropdown menu
    $('#moleculeSelect').change(function() {
        getAtoms();
        getBonds();
    });


    /* add a click handler for our button */
    $("#displayMol").click(function(){
        // Access the button element by ID and enable it
        $("#Rotate").prop("disabled", false);
        /* ajax post */
        $.post("/displayMol.html",
            /* pass a JavaScript dictionary */
            {
                molName: $("#moleculeSelect").val(),	/* retreive value of name field */
            },
                function( data, status )
            {
                $("#image-container").html(data)
                
                // Scale the SVG to fit the container
                const svg = $("#my-svg")[0]; // get the first element with id="my-svg"
                svg.setAttribute('viewBox', '0 0 100 100');
            }
        );
    })


});

$(document).ready( 
    /* this defines a function that gets called after the document is in memory */
    function()
    {

        /* add a click handler for our button */
        $("#btnUpload").click(function(){

            //check for sql injections
            if (containsSpecialChar($('#molName').val())) {
                alert('Input cannot contain semicolons or double quotes.');
                return; // Exit the function without sending the $.post request
            }

            // Check if the file has a .sdf extension
            if (!$("#sdf_file").val().endsWith('.sdf')) {
                alert('Invalid file type. Please upload an SDF file.');
                return;
            }

            const fileReader = new FileReader();
            fileReader.addEventListener('load',() => {
                /* ajax post */
                $.post("/upload.html",
                    /* pass a JavaScript dictionary */
                    {
                        molName: $("#molName").val(),	/* retreive value of name field */
                        fileStuff: fileReader.result
                    },
                        function( data, status )
                    {
                        alert( "Data: " + data + "\nStatus: " + status );
                        //set the text area back to blank
                        $("#molName").val("")
                    }
                );
            });
            fileReader.readAsText(document.getElementById('sdf_file').files[0])
        });
    }
);

function containsSpecialChar(input) {
    const forbiddenChars = ['"', ';'];
    for (let i = 0; i < forbiddenChars.length; i++) {
      if (input.includes(forbiddenChars[i])) {
        return true;
      }
    }
    return false;
}
