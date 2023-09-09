fetch("products.json")
.then(function(response){
    return response.json();
})
.then(function(products){
    let placeholder  = document.getElementById("tableData");
    let out= "";
    let count = 1 ;
    for(let product of products){
        inner = product.time
        out += `
            <tr>
                <td> ${count} </td>
                <td>${product.VehicleNo}</td>
                <td>${inner.slice(0,16)}</td>
                <td><img src=${product.imagee} width = "150px" height="50px"></td>
            </tr>
        `;
        count++;
    }
    placeholder.innerHTML= out;
});