  $(document).ready(function(){ //Disable submit button when option not selected
    const select = document.getElementById('dis'); // get item with id 'dis' 
    const submitButton = document.getElementById('enab'); // get item with id enab
    document.getElementById('dis').addEventListener('change', () => { //if there is a change in value in item with dis id
      if (select.value === '') {
        submitButton.disabled = true;  //if value empty disable submit 
      } else {
        submitButton.disabled = false; // else enable 
      }
    });
  });
