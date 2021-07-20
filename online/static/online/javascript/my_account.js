



    function click_me(){
        if (document.getElementById('show_table').style.display === 'none'){
            document.getElementById('show_table').style.display = 'block';
            document.getElementById('change_name').style.display = 'none';
            document.getElementById('change_name_button').innerHTML = 'Change my name';
        }
        else{
            document.getElementById('show_table').style.display = 'none';
            document.getElementById('change_name').style.display = 'block';
            document.getElementById('change_name_button').innerHTML = 'Go back';
        };
    };

    function click_me2(){
        if (document.getElementById('show_table').style.display === 'none'){
            document.getElementById('show_table').style.display = 'block';
            document.getElementById('change_name').style.display = 'none';
            document.getElementById('change_name_button2').innerHTML = 'Change my name';
        }
        else{
            document.getElementById('show_table').style.display = 'none';
            document.getElementById('change_name').style.display = 'block';
            document.getElementById('change_name_button2').innerHTML = 'Go back';
        };
    };