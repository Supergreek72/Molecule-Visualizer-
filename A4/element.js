
function setTables(){
    //get the element table values
    $.get('/table-values', function(data) {
        var table = $('#elementTable');
        $('#elementTable').empty(); // clear all rows except for the first one (the header row)
        var counter = 0;
        var row = $('<tr>');
        $.each(data, function(outerIndex, innerArray) {
            $.each(innerArray, function(innerIndex, value) {
                row.append($('<td>').text(value));
                counter++;
                if (counter === 7) {
                    table.append(row);
                    row = $('<tr>');
                    counter = 0;
                }
            });
        });
        if (counter > 0) {
            table.append(row);
        }
    });
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
            $('#elementTable').empty()
            $('#elementSelect').empty()
        }
        );
      } else {
        // User clicked "Cancel"
        // Do nothing
      }
    
}

function populateDropDown(){
    //populate the dropdown table
    $.ajax({
        url: '/get-element-names',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            // Populate the select dropdown with the data
            var select = $('#elementSelect');
            $.each(data, function(index, value) {
                select.append($('<option>').text(value).attr('value', value));
            });
        },
        error: function(xhr, textStatus, errorThrown) {
            alert('Error: ' + errorThrown);
        }
    });
}

function containsSpecialChar(input) {
    const forbiddenChars = ['"', ';'];
    for (let i = 0; i < forbiddenChars.length; i++) {
      if (input.includes(forbiddenChars[i])) {
        return true;
      }
    }
    return false;
}

$(document).ready(function() {
    //fill the tables
    setTables();
    //button click for add element
    $('#addElement').click(function() {
        var dataToSend = {
          elementNum: $('#elementNum').val(),
          elementCode: $('#elementCode').val(),
          elementName: $('#elementName').val(),
          colour1: $('#colour1').val(),
          colour2: $('#colour2').val(),
          colour3: $('#colour3').val(),
          radius: $('#radius').val()
        };
        
        // Check if any of the required fields are blank
        if ($('#elementNum').val() === "" || $('#elementCode').val() === "" || $('#elementName') === "") {
            alert('Please enter a value for the element number, code, and name.');
            return; // Exit the function without sending the $.post request
        }

        //check for sql injection
        if (containsSpecialChar($('#elementNum').val()) || containsSpecialChar($('#elementCode').val()) || containsSpecialChar($('#elementName').val()) ||
            containsSpecialChar($('#colour1').val()) || containsSpecialChar($('#colour2').val()) || containsSpecialChar($('#colour3').val()) || containsSpecialChar($('#radius').val())) {
            alert('Input cannot contain semicolons or double quotes.');
            return; // Exit the function without sending the $.post request
        }
        
        $.post('/create-element.html', dataToSend, function(data, status) {
            alert( "Data: " + data + "\nStatus: " + status );
            setTables();
            $('#elementSelect').empty();
            populateDropDown();
            // clear all the text fields
            $('#elementNum').val('');
            $('#elementCode').val('');
            $('#elementName').val('');
            $('#colour1').val('');
            $('#colour2').val('');
            $('#colour3').val('');
            $('#radius').val('');
        });
        
      });

      //populate the drop down table for deletion
      populateDropDown()

      //listen for delete button click
      /* add a click handler for our button */
    $("#btnDelete").click(function(){
        /* ajax post */
        $.post("/delete-element.html",
            /* pass a JavaScript dictionary */
            {
                elName: $("#elementSelect").val(),	/* retreive value of name field */
            },
                function( data, status )
            {
                alert("Data: " + data + "\nStatus: " + status )
                $('#elementSelect').empty()
                populateDropDown();
                setTables();
            }
        );
    })


})
