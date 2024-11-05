# API Collection: Both Auth and Multiple DB

This is a Postman collection that demonstrates how to interact with an API that includes authentication and multiple databases. The collection contains requests for user registration, login, fetching, posting, updating, deleting products, and more.

## Table of Contents

- [API Overview](#api-overview)
- [Requests](#requests)
  - [Register](#register)
  - [Login](#login)
  - [Get Products](#get-products)
  - [Post Products - Manager and Admin Only](#post-products---manager-and-admin-only)
  - [Update, Delete, Get Single Product](#update-delete-get-single-product)
  - [Ordering Based on Price and Pagination to 2nd Page](#ordering-based-on-price-and-pagination-to-2nd-page)
  - [Splitting to Pages Based on Content](#splitting-to-pages-based-on-content)
  - [Search with Name](#search-with-name)

---

## API Overview

This API demonstrates the following:

- **User authentication** using JWT tokens.
- **Product management** including creation, update, deletion, and retrieval.
- **Role-based access control** (i.e., certain actions are restricted to managers and admins).
- **Pagination** and **search functionality** for fetching products.

---

## Requests

### Register

**POST** `http://localhost:8000/api/accounts/register/`

This request registers a new user with a `username`, `password`, `role`, and `company` information. Example payload:

```json
{
    "username": "testuser2",
    "password": "password123",
    "role": "user",
    "company": "company1"
}
