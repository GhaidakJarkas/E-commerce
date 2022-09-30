var updateBtns = document.getElementsByClassName("update-cart");
debugger
for(var i=0; i < updateBtns.length; i++){
    debugger
    updateBtns[i].addEventListener("click", function(){
        var productID = this.dataset.product;
        var action = this.dataset.action;
        console.log(productID, action);

        console.log('User: ', user)
        if(user === "AnonymousUser"){
            console.log("User in not logged in")
        }else{
            updateUserOrder(productID, action)
        }
    });
}

function updateUserOrder(productID, action){
    console.log("User is logged in, sending data")

    var url = '/update_item/'

    fetch(url, {
        method: 'POST', 
        headers: {
            'Content-Type': "application/json",
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({"productID":productID, "action":action})
    })

    .then((response) => {
        return response.json();
    })

    .then((data) => {
        console.log(data);
        location.reload();
    })
}