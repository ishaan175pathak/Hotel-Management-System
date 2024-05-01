// JavaScript for quantity buttons

var itemLists = [];

let checkLists = () => {
  if (itemLists.length == 0) {
    return true;
  }
};

// sending the data to backend

let submitData = async (room_no, items_dictionary) => {
  alert(room_no);

  let body = {
    room_number: room_no,
    items: items_dictionary,
    user: user_info,
  };

  try {
    let options = {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify(body),
    };

    console.log(options);

    let result = await fetch(
      `http://127.0.0.1:8000/order%20food%20api/${room_no}`,
      (options = options)
    );
    let data = await result.json();
    data = JSON.parse(data);
    alert(data.status);
    if (data.status === "received Data") {
      fetch("http://127.0.0.1:8000/logout/");
      window.location = "http://127.0.0.1:8000/";
    }
  } catch (error) {
    alert("Error occured try again");
  }
};

// creating the final order receipt

let generateReceipt = () => {
  let items_dictionary_list = new Array();

  let room = document.getElementById("room_number");
  let room_no = room.options[room.selectedIndex].value;
  let main_div = document.getElementById("OrderPlacementModal");
  let div = document.createElement("div");
  let table = document.createElement("table");

  div.classList.add("container-fluid");

  table.classList.add("table");

  let thead = document.createElement("thead");

  thead.innerHTML = `
    <tr> 
      <th>index</th>
      <th>Item</th>
      <th>Quantity</th>
      <th>Price</th>
    </tr>
  `;

  thead.classList.add("thead-light");
  table.append(thead);

  let total_price = 0;

  itemLists.forEach((value, index) => {
    let tr = document.createElement("tr");

    tr.innerHTML = `
      <td>${index}</td>
      <td>${value.name}</td>
      <td>${Math.floor(value.pricing.total / value.pricing.base)}</td>
      <td>${value.pricing.base}</td>
    `;

    items_dictionary_list.push([
      value.name,
      Math.floor(value.pricing.total / value.pricing.base),
      value.pricing.base,
    ]);

    total_price += value.pricing.total;

    table.append(tr);
  });

  let total_tr = document.createElement("tr");

  total_tr.innerHTML = `
    <td colspan = '3'>Total</td>
    <td>${total_price}</td>
  `;

  table.append(total_tr);

  let submitMenuBtn = document.createElement("tr");
  console.log(items_dictionary_list);
  submitMenuBtn.innerHTML = `
    <td colspan='4'> <button id="placeOrder" class = 'centeredButton' > Place Order </button> </td>
  `;

  table.append(submitMenuBtn);
  div.append(table);
  main_div.append(div);

  let placeOrder = document.getElementById("placeOrder");
  placeOrder.onclick = () => {
    submitData(room_no, items_dictionary_list);
  };
};

Array.from(document.getElementsByClassName("input-group-append")).forEach(
  (value) => {
    let qunatityName =
      value.parentElement.parentElement.parentElement.querySelector(
        ".card-title"
      ).textContent;

    value.lastElementChild.addEventListener("click", (e) => {
      // updating the values on the frontend
      let parent_sibling_value = value.previousElementSibling;
      parent_sibling_value.value = parseInt(parent_sibling_value.value) + 1;

      // updating the values for the final list to calculating the price
      let itemIndex = 0;
      for (let index = 0; index < itemLists.length; index++) {
        if (itemLists[index].name == qunatityName) {
          itemIndex = index;
          break;
        }
      }
      let currentItem = itemLists[itemIndex];
      currentItem.pricing.total += currentItem.pricing.base;
    });
  }
);

Array.from(document.getElementsByClassName("form-group")).forEach((element) => {
  let minus_btn = element.querySelector(
    ".input-group-prepend"
  ).firstElementChild;

  let add_quantity = element.querySelector(".btn.btn-primary.btn-block");
  let quantityGroup = element.querySelector(".input-group");

  let qunatityName =
    element.parentElement.querySelector(".card-title").textContent;

  minus_btn.addEventListener("click", (e) => {
    let itemIndex = 0;
    for (let index = 0; index < itemLists.length; index++) {
      if (itemLists[index].name == qunatityName) {
        itemIndex = index;
        break;
      }
    }

    let currentItem = itemLists[itemIndex];
    let quantityElement = element.querySelector(".form-control.text-center");

    if (parseInt(quantityElement.value) > 1) {
      quantityElement.value -= 1;
      currentItem.pricing.total -= currentItem.pricing.base;
    } else {
      add_quantity.style.display = "block";
      quantityGroup.style.display = "none";
      itemLists.splice(itemIndex, 1);

      // checking and disabling the submit button if the items list is empty

      if (checkLists()) {
        document
          .getElementById("submitMenu")
          .firstElementChild.setAttribute("disabled", "true");
      }
    }

    console.table(itemLists);
  });
});

Array.from(document.getElementsByClassName("col-md-6 mb-4")).forEach(
  (value) => {
    let addButton = value.querySelector(".btn.btn-primary.btn-block");
    addButton.onclick = (e) => {
      // JavaScript to toggle visibility of quantity buttons

      let quantityGroup = value.querySelector(".input-group");
      let qunatityName = value.querySelector(".card-title").textContent;
      let qunatityPrice = value.querySelector(".card-text").textContent;

      let items = {};

      if (quantityGroup.style.display === "none") {
        quantityGroup.style.display = "flex";
        addButton.style.display = "none";
        let submitMenuBtn =
          document.getElementById("submitMenu").firstElementChild;

        submitMenuBtn.removeAttribute("disabled");

        let price = qunatityPrice.match(/\d+/)[0];
        items["name"] = qunatityName;
        items["pricing"] = { base: parseInt(price), total: parseInt(price) };

        itemLists.push(items);
        console.table(itemLists);
      }
    };
  }
);

let submitMenuBtn = document.getElementById("submitMenu").firstElementChild;
let orderPlacementModal = document.getElementById("OrderPlacementModal");
let modalHeaderHide = document.getElementById("modalHeaderHide");

submitMenuBtn.onclick = () => {
  submitMenuBtn.classList.add("disapperingAnimation");
  orderPlacementModal.style.display = "block";
  generateReceipt();
};

// enabling the close icon

document.getElementById("modalHeaderHide").addEventListener("click", (e) => {
  orderPlacementModal.style.display = "none";
  submitMenuBtn.classList.remove("disapperingAnimation");
  orderPlacementModal.removeChild(orderPlacementModal.lastElementChild);
});
