<script setup>

</script>


<template>
    <div>
        <div class="bookingContainer">
        <h1>BOOKING</h1>
        <table>
            <thead>
            <tr class="headrow">
                <th>S.No</th>
                <th>Service</th>
                <th>Professional</th>
                <th>Date of Request</th>
                <th>Date of Completion</th>
                <th>Status</th>
                <th>Action</th>
                <th></th>
            </tr>
            </thead>

            <tbody>
            <tr>
                <td>1</td>
                <td>Plumber</td>
                <td>John Doe</td>
                <td>10-10-2021</td>
                <td>10-10-2021</td>
                <td>Pending</td>
                <td><button class="closeBtn" type="submit">Close</button></td>
                <td><svg fill="#ffffff" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g data-name="37 rating" id="_37_rating"> <path d="M42.83,3.5H21.17a6,6,0,0,0-6,6V28.66a6,6,0,0,0,6,6H23.4l7.84,9.23a1,1,0,0,0,1.1.29.992.992,0,0,0,.66-.94V34.66h9.83a6,6,0,0,0,6-6V9.5A6,6,0,0,0,42.83,3.5Zm4,25.16a4,4,0,0,1-4,4H32a1,1,0,0,0-1,1v6.86l-6.38-7.51a1.011,1.011,0,0,0-.76-.35H21.17a4,4,0,0,1-4-4V9.5a4,4,0,0,1,4-4H42.83a4,4,0,0,1,4,4Z"></path> <path d="M44.66,10.75a1,1,0,0,1-1,1H20.34a1,1,0,0,1,0-2H43.66A1,1,0,0,1,44.66,10.75Z"></path> <path d="M44.66,14.92a1,1,0,0,1-1,1H20.34a1,1,0,0,1,0-2H43.66A.99.99,0,0,1,44.66,14.92Z"></path> <path d="M44.66,19.08a1,1,0,0,1-1,1H20.34a1,1,0,0,1,0-2H43.66A1,1,0,0,1,44.66,19.08Z"></path> <path d="M44.66,23.25a1,1,0,0,1-1,1H28.67a1,1,0,0,1,0-2H43.66A.99.99,0,0,1,44.66,23.25Z"></path> <path d="M44.66,27.41a1,1,0,0,1-1,1H28.67a1,1,0,0,1,0-2H43.66A1,1,0,0,1,44.66,27.41Z"></path> <path d="M18.65,46.55a1.009,1.009,0,0,0-.95-.69H13.57l-1.28-3.93a1,1,0,0,0-1.9,0L9.11,45.86H4.98a1,1,0,0,0-.59,1.81L7.73,50.1,6.46,54.02a1,1,0,0,0,.95,1.31A1.01,1.01,0,0,0,8,55.14l3.34-2.43,3.34,2.43a1,1,0,0,0,1.54-1.11L14.94,50.1l3.35-2.43A1.012,1.012,0,0,0,18.65,46.55Zm-5.83,3.47.55,1.7-1.44-1.05a.99.99,0,0,0-1.18,0L9.31,51.72l.55-1.7a.992.992,0,0,0-.36-1.11L8.06,47.86H9.84a1.009,1.009,0,0,0,.95-.69l.55-1.7.55,1.7a1,1,0,0,0,.95.69h1.78l-1.44,1.05A.977.977,0,0,0,12.82,50.02Z"></path> <path d="M39.31,51.71a1,1,0,0,0-.95-.69H34.23l-1.28-3.93a1,1,0,0,0-1.9,0l-1.28,3.93H25.64a1,1,0,0,0-.59,1.81l3.35,2.43-1.28,3.93a1.012,1.012,0,0,0,.36,1.12,1.022,1.022,0,0,0,1.18,0L32,57.88l3.34,2.43a1.011,1.011,0,0,0,1.18,0,1.012,1.012,0,0,0,.36-1.12L35.6,55.26l3.35-2.43A1,1,0,0,0,39.31,51.71Zm-5.83,3.48.55,1.69-1.44-1.05a1.011,1.011,0,0,0-1.18,0l-1.44,1.05.55-1.69a.992.992,0,0,0-.36-1.12l-1.44-1.05H30.5a1,1,0,0,0,.95-.69L32,50.64l.55,1.69a1,1,0,0,0,.95.69h1.78l-1.44,1.05A.992.992,0,0,0,33.48,55.19Z"></path> <path d="M59.97,46.55a.991.991,0,0,0-.95-.69H54.89l-1.28-3.93a1,1,0,0,0-1.9,0l-1.28,3.93H46.3a1,1,0,0,0-.59,1.81l3.35,2.43-1.28,3.93a1,1,0,0,0,1.54,1.11l3.34-2.43L56,55.14a1.01,1.01,0,0,0,.59.19.967.967,0,0,0,.59-.19.987.987,0,0,0,.36-1.12L56.27,50.1l3.34-2.43A1,1,0,0,0,59.97,46.55Zm-5.83,3.47.55,1.7-1.44-1.05a.988.988,0,0,0-.59-.19,1.01,1.01,0,0,0-.59.19l-1.44,1.05.55-1.7a.977.977,0,0,0-.36-1.11l-1.44-1.05h1.78a1,1,0,0,0,.95-.69l.55-1.7.55,1.7a1.009,1.009,0,0,0,.95.69h1.78L54.5,48.91A.992.992,0,0,0,54.14,50.02Z"></path> </g> </g></svg></td>
            </tr>
            </tbody>
        </table>
    </div>
    </div>
</template>

<style scoped>
.bookingContainer{
    width: 95%;
    background-color: rgba(255, 255, 255, 0.06);
    box-shadow: 5px 5px 10px rgb(0, 0, 0);
    border-radius: 1rem;
    padding: 1rem;
    margin: auto;

}

h1{
    text-align: center;
    color: #fff;
    font-size: 2.5rem;    
    font-weight: bolder;
    margin-bottom: 1rem;
}


table{
    width: 95%;
    margin: auto;
    padding: .2rem;
    overflow: hidden;
}

table{
    width: 100%;
    border: none;
    border-collapse: separate; 
    border-spacing: 0; 
    border-radius: 1rem; 
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

tr:last-child{
    border-bottom: none;
}

.closeBtn{
    background-color: #6A94FF;
    border: none;
    border-radius: .2rem;
    width: 3rem;
    color: white;
    cursor: pointer;
}
svg{
    width: 30px;
    height: 30px;
    
}

</style>