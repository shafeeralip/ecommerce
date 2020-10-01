        var updateBtns =document.getElementsByClassName('update-cart')

for(var i=0;i < updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productid:',productId,'action:',action)
        console.log('User:',user)
        if(user == 'AnonymousUser'){
            addCookieItem(productId,action)
         }
        else{
            updateUserOrder(productId,action)
        }

    })
}

function addCookieItem( productId , action ){
    console.log("not logged in")
    if( action == 'add'){
        if(cart[ productId  ]== undefined ){
            cart[ productId ] = {'quantity':1}
        }else{
            cart[ productId ]['quantity'] += 1 
        }
    }

    if(action == 'remove'){
        cart[ productId ]['quantity'] -= 1 

        if(cart[ productId ]['quantity'] <= 0){
            console.log("remove item")
            delete cart[ productId ]
        }
      
    }
    if(action=='delete'){
        console.log("remom")
        delete cart[ productId ]
    }
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
    console.log("cart:", cart)

}

function updateUserOrder(productId,action){
    console.log("user logged in")
    var url ='/cart/update_item/'
    
    fetch(url, {
        method:'POST',
        headers:{'X-CSRFToken':csrftoken,
            'Content-Type':'application/json',
            

 
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data)=>{
       console.log('data:',data)
       location.reload()
    })

}