// GETTING THE ACCESS TOKEN
const getToken = async () => {
  const res = await fetch("http://127.0.0.1:8000/api/token/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: "yash",
      password: "yash123",
    }),
  });

  const data = await res.json();
  return data.access;
};

// FETCHING ALL VENDORS
const fetchAllVendors = async () => {
  const accessToken = await getToken();

  const res = await fetch("http://127.0.0.1:8000/api/vendors/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  const data = await res.json();
  console.log(data);
};

// CREATING NEW VENDOR
const createNewVendor = async () => {
  const accessToken = await getToken();

  const res = await fetch("http://127.0.0.1:8000/api/vendors/", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: "Divya Jewellers",
      contact_details: "email:divya@eg.com",
      address: "Telibandha Raipur",
      city: "Raipur",
      vendor_code: "RAI050524211842SIV",
    }),
  });

  if (res.ok) {
    const data = await res.json();
    console.log(data);
  } else {
    console.log(res.statusText);
  }
};

// UPDATING NEW VENDOR
const updateVendor = async (vendor_id) => {
  const accessToken = await getToken();

  const res = await fetch(`http://127.0.0.1:8000/api/vendors/${vendor_id}`, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: 999,
      name: "Divya Jewellers",
      contact_details: "email:divya@eg.com",
      address: "Telibandha Raipur",
      city: "Raipur",
      vendor_code: "dajda f",
    }),
  });

  if (res.ok) {
    const data = await res.json();
    console.log(data);
  } else {
    console.log(res.statusText);
  }
};

// DELETE A VENDOR
const deleteVendor = async (vendor_id) => {
  const accessToken = await getToken();
  const res = await fetch(`http://127.0.0.1:8000/api/vendors/${vendor_id}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (res.ok) {
    const data = await res.json();
    console.log(data);
  } else {
    console.log(res.statusText);
  }
};

// FETCH VENDOR USING VENDOR_ID
const fetchVendor = async (vendor_id) => {
  const accessToken = await getToken();
  const res = await fetch(`http://127.0.0.1:8000/api/vendors/${vendor_id}`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (res.ok) {
    const data = await res.json();
    console.log(data);
  } else {
    console.log(res.statusText);
  }
};

// FETCHING ALL PURCHASE ORDERS
const fetchAllPuchaseOrders = async () => {
  const accessToken = await getToken();

  const res = await fetch("http://127.0.0.1:8000/api/purchase_orders/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  const data = await res.json();
  console.log(data);
};

// CREATE NEW PURCHASE ORDER
const createNewPurchaseOrder = async () => {
  const accessToken = await getToken();

  const res = await fetch("http://127.0.0.1:8000/api/purchase_orders/", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      vendor: 7, // Assuming vendor ID is 1
      delivery_date: "2024-05-31T08:00:00Z",
      items: [
        {
          item_name: "Product A",
          quantity: 5,
          unit_price: 10,
        },
        {
          item_name: "Product B",
          quantity: 10,
          unit_price: 20,
        },
      ],
      quantity: 2,
      status: "pending",
      quality_rating: 4.5,
      issue_date: "2024-05-06T08:00:00Z",
      acknowledgement_date: "2024-05-10T08:00:00Z",
    }),
  });

  if (res.ok) {
    const data = await res.json();
    console.log(data);
  } else {
    console.log(res.statusText);
  }
};

// FETCH PURCHASE ORDER USING PO_ID
const fetchPurchaseOrder = async (po_id) => {
  const accessToken = await getToken();
  const res = await fetch(
    `http://127.0.0.1:8000/api/purchase_orders/${po_id}`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  if (res.ok) {
    const data = await res.json();
    console.log(data);
  } else {
    console.log(res.statusText);
  }
};

// DELETE A VENDOR
const deletePurchaseOrder = async (po_id) => {
  const accessToken = await getToken();
  const res = await fetch(
    `http://127.0.0.1:8000/api/purchase_orders/${po_id}`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  if (res.ok) {
    const data = await res.json();
    console.log(data);
  } else {
    console.log(res.statusText);
  }
};

// UPDATING Purchase ORDER
const updatePurchaseOrder = async (po_id) => {
  const accessToken = await getToken();

  const res = await fetch(
    `http://127.0.0.1:8000/api/purchase_orders/${po_id}`,
    {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        vendor: 6,
        delivery_date: "2024-05-31T08:00:00Z",
        items: [
          {
            item_name: "Product A",
            quantity: 5,
            unit_price: 10,
          },
          {
            item_name: "Product B",
            quantity: 10,
            unit_price: 20,
          },
        ],
        quantity: 2,
        status: "completed",
        quality_rating: 5.0,
        issue_date: "2024-05-06T08:00:00Z",
        acknowledgement_date: "2024-05-10T08:00:00Z",
      }),
    }
  );

  if (res.ok) {
    const data = await res.json();
    console.log(data);
  } else {
    console.log(res.statusText);
  }
};

// FETCH VENDOR PERFORMANCE
const fetchVendorPerformance = async (vendor_id) => {
  const accessToken = await getToken();
  const res = await fetch(
    `http://127.0.0.1:8000/api/vendors/${vendor_id}/performance/`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  if (res.ok) {
    const data = await res.json();
    console.log(data);
  } else {
    console.log(res.statusText);
  }
};

// fetchAllVendors();
// createNewVendor()
// fetchVendor(7);
// updateVendor(8)
// deleteVendor(8);

// fetchAllPuchaseOrders();
// createNewPurchaseOrder();
// fetchPurchaseOrder(6);
// deletePurchaseOrder(5);
// updatePurchaseOrder(6);

// fetchVendorPerformance(3);
