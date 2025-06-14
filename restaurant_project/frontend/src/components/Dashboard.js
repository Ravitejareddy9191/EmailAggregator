import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/orders/', { withCredentials: true })
      .then(res => setOrders(res.data))
      .catch(() => alert('Failed to load orders'));
  }, []);

  return (
    <div>
      <h2>Order Dashboard</h2>
      <table>
        <thead>
          <tr>
            <th>email Date</th>
            <th>sender</th>
            <th>Order No</th>
            <th>Customer Name</th>
            <th>Mobile No</th>
            <th>Item Details</th>
            <th>Item Description</th>
            <th>Sub Total</th>
            <th>Delivery Charges</th>
            <th>GST</th>
            <th>Grand Total</th>
            <th>Pay Mode</th>
            <th>Delivery Date</th>
            <th>Station</th>
            <th>Train No</th>
            <th>Coach</th>
            <th>subject</th>
          </tr>
        </thead>
        <tbody>
          {orders.length === 0 ? (
            <tr><td colSpan="7">No orders found</td></tr>
          ) : (
            orders.map((order, index) => (
              <tr key={index}>
                <td>{order.email_Date}</td>
                <td>{order.sender}</td>
                <td>{order.Order_No}</td>
                <td>{order.Customer_Name}</td>
                <td>{order.Mobile_No}</td>
                <td>{order.Item_Details}</td>
                <td>{order.Item_Description}</td>
                <td>{order.Sub_Total}</td>
                <td>{order.Delivery_Charges}</td>
                <td>{order.GST}</td>
                <td>{order.Grand_Total}</td>
                <td>{order.Pay_Mode}</td>
                <td>{order.Delivery_Date}</td>
                <td>{order.Station}</td>
                <td>{order.Train_No_Name}</td>
                <td>{order.Coach}</td>
                <td>{order.subject}</td>

              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Dashboard;

