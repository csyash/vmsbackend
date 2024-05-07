# A backend application for Vendor Management System built using django, with real time performance metrics.

### USAGE:

### 1.  Create a virtual environment:
```
python3 -m venv env

```

### 2.  Activate the virtual environment:
```
env\Scripts\activate
```

### 3. Install Dependencies:
```
pip install requirements.txt
```

### 4. Create super user:
* On command terminal create super user using:
```
python manage.py createsuperuser
```

### 5. Login to Admin panel to create Users, Vendors, Purchase Orders and Historical Performance metrics by going to /admin.

## RUN TESTS

## 1. Run base app's tests:
```
python manage.py test base
```

## 2. Run api app's tests:
```
python manage.py test api
```


## API Endpoints Documentation:

* ### A frontend.js is provided with sample code samples to run apis.

### 1) Obtain JWT Token:
*   URL: /api/token/
*   Method: POST
*   Description: Obtain JWT tokens (access and refresh tokens) for authentication.
*   Usage:
```
// Code Sample
const response = await fetch('/api/token/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'your_username',
    password: 'your_password'
  })
});
```

### 2) Refresh JWT Token:
*   URL: /api/token/refresh/
*   Method: POST
*   Description: Refresh JWT access token using the refresh token.
*   Usage:
```
// Example usage in JavaScript
const response = await fetch('/api/token/refresh/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${refreshToken}`
  }
});
```

### 3) List All Vendors and Create New Vendor:
* URL: /api/vendors/
* Methods: GET, POST
* Description: List all vendors and create a new vendor.
* Usage:
```
// Example usage in JavaScript
// Fetch all vendors
const response = await fetch('/api/vendors/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

// Create a new vendor
const response = await fetch('/api/vendors/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Vendor Name',
    contact_details: 'Contact Details',
    // Add other vendor details here
  })
});
```

### 4) Retrieve, Update, and Delete Specific Vendor:
* URL: /api/vendors/<vendor_id>/
* Methods: GET, PUT, DELETE
* Description: Retrieve, update, or delete a specific vendor by vendor_id.
* Usage:
```
// Example usage in JavaScript
// Retrieve a specific vendor
const response = await fetch(`/api/vendors/${vendorId}`, {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});


// Update a specific vendor
const response = await fetch(`/api/vendors/${vendorId}`, {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Updated Vendor Name',
    // Add other fields to update here
  })
});

// Delete a specific vendor
const response = await fetch(`/api/vendors/${vendorId}`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});
```

### 5) List Vendor Performance:
*   URL: /api/vendors/<vendor_id>/performance/
*   Method: GET
*   Description: List performance information of a specific vendor by vendor_id.
*   Usage:
```
// Example usage in JavaScript
const response = await fetch(`/api/vendors/${vendorId}/performance/`, {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});
```

### 6) List All Purchase Orders and Create New Purchase Order:
*   URL: /api/purchase_orders/
*   Methods: GET, POST
*   Description: List all purchase orders and create a new purchase order.
*   Usage
```
// Example usage in JavaScript
// Fetch all purchase orders
const response = await fetch('/api/purchase_orders/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

// Create a new purchase order
const response = await fetch('/api/purchase_orders/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    vendor: vendorId,
    delivery_date: '2024-05-31T08:00:00Z',
    // Add other purchase order details here
  })
});
```

### 7) List All purchase orders filter by vendor_id
URL: /api/purchase_orders?vendor_id=<vendor_id>
*   Methods: GET, POST
*   Description: List all purchase orders and create a new purchase order.
*   Usage
```
// Example usage in JavaScript
// Fetch all purchase orders
const response = await fetch('/api/purchase_orders?vendor_id=<vendor_id>', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});
```

### 8) Retrieve, Update, and Delete Specific Purchase Order:
*   URL: /api/purchase_orders/<po_id>/
*   Methods: GET, PUT, DELETE
*   Description: Retrieve, update, or delete a specific purchase order by po_id.
*   Usage:
```
// Example usage in JavaScript
// Retrieve a specific purchase order
const response = await fetch(`/api/purchase_orders/${poId}`, {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

// Update a specific purchase order
const response = await fetch(`/api/purchase_orders/${poId}`, {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    vendor: vendorId,
    delivery_date: '2024-05-31T08:00:00Z',
    // Add other fields to update here
  })
});

// Delete a specific purchase order
const response = await fetch(`/api/purchase_orders/${poId}`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});
```

### 9) Acknowledge Purchase Order:
*   URL: /api/purchase_orders/<po_id>/acknowledge/
*   Method: POST
*   Description: Acknowledge a purchase order by po_id and vendor_id, initiating recalculation of average response time for the vendor.
*   Usage:
```
// Example usage in JavaScript
const response = await fetch(`/api/purchase_orders/${poId}/acknowledge/`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type' : 'application/json',
  },
  body: JSON.stringify({ vendor_id: vendor_id }),
});
```

