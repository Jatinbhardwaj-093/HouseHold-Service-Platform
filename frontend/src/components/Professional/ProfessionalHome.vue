<template>
    <div>
        <div class="grid">
        <div class="table1">
            <h1>New Requests</h1>
            <table>
                <thead>
                <tr class="headrow">
                    <th>S.No</th>
                    <th>Customer</th>
                    <th style="width: 40%;">Address</th>
                    <th>Pincode</th>
                    <th>Date Of Request</th>
                    <th>Action</th>
                    
                </tr>
                </thead>

                <tbody>
                <tr>
                    <td>1</td>
                    <td>2</td>
                    <td>3</td>
                    <td>4</td>
                    <td>5</td>
                    <td><div class="option">
                        <button class="acceptBtn">Accept</button>
                        <button class="rejectBtn">Reject</button>
                    </div></td>
                    
                </tr>
                </tbody>
            </table>
        </div>
        <div class="table2">
            <h1>Ongoing Requests</h1>
            <table>
                <thead>
                <tr class="headrow">
                    <th>S.No</th>
                    <th>Customer</th>
                    <th style="width: 40%;">Address</th>
                    <th>Pincode</th>
                    <th>Date Of Request</th>
                    <th>Status</th>
                </tr>
                </thead>

                <tbody>
                <tr>
                    <td>1</td>
                    <td>2</td>
                    <td>3</td>
                    <td>4</td>
                    <td>5</td>
                    <td><div class="option">
                        <button class="closeBtn">Mark Complete</button>
                        <p class="completed">Completed</p>
                    </div></td>
                </tr>
                </tbody>
            </table>    
        </div>
    </div>
    </div>
</template>

<style scoped>
.grid{
    display: grid;
    grid-template-rows: 1fr 1fr;
    grid-row-gap: 1rem;
    height: 80vh;
    width: 95vw;
    margin: auto;
    
}

.grid > div{
    overflow: auto;
    scrollbar-width: none;
    background-color: rgba(255, 255, 255, 0.06);
    box-shadow: 5px 5px 10px rgb(0, 0, 0);
    border-radius: 1rem;
    padding: 1rem;
}



h1{
    text-align: center;
    color: #fff;
    font-size: 2rem;    
    font-weight: bolder;
    margin-bottom: 1rem;
}
table{
    width: 100%;
    border: none;
    border-collapse: separate; 
    border-spacing: 0; 
    border-radius: 0.5rem; 
    margin: auto;
    overflow: hidden; 
    
}

th,td{
    padding: 4px;
    text-align: center;
    border-bottom: 1px solid #f5f5dc;
}

tr:last-child td{
    border-bottom: none;
}

tr:nth-child(even) {
    background-color: #2f2c2c;
}

.headrow{
    color: white;
    background-color: hsla(21, 100%, 50%, 0.85);
}

tr{
    color: #f5f5dc;
    background-color: #3C3C3C;
}

.option{
    display: flex;
    gap: 5px;
    justify-content: center;
    align-items: center;
}

button{
    border: none;
    border-radius: .2rem;
    width: 4rem;
    color: white;
    cursor: pointer;
}

.closeBtn{
background-color: #6A94FF;
}

.completed{
    color: #3fe33c;
}
</style>