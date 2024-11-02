<template>
    <div>
        <div class="navbar">
        <div class="professionalDetail">
            <div class="img"></div>
            <div class="professionalName">Professional</div>
        </div>
        <div class="menu">
            <div class="home">
                <svg fill="#ffffff" viewBox="0 -0.06 512.125 512.125" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g id="_05_Home" data-name="05 Home" transform="translate(0.063 -0.001)"> <path id="Path_8" data-name="Path 8" d="M502.688,198.484,313.579,9.391c-7.217-7.248-16.9-10.044-26.368-9.263H224.789c-9.466-.781-19.151,2.015-26.368,9.263l-38.4,38.4V.128H64.049V143.764L9.312,198.484C2.064,205.732-.716,215.4.065,224.852v63.2a31.984,31.984,0,0,0,31.991,31.993H64.048V480.006A31.983,31.983,0,0,0,96.04,512H415.96a31.983,31.983,0,0,0,31.992-31.992V320.048h31.991a31.984,31.984,0,0,0,31.992-31.993v-63.2C512.717,215.4,509.937,205.732,502.688,198.484Zm-54.736,57.579H383.968V448.014H319.985V320.048H192.017V448.015H128.033V256.063H64.049V238.317L238.255,64.111h35.491L447.952,238.317Z" fill-rule="evenodd"></path> </g> </g></svg>
                <p>Home</p>
                <div class="position"></div>
            </div>
            <div class="history">
                <svg fill="#ffffff" viewBox="0 0 512 512" id="_x30_1" version="1.1" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <path d="M437.11,74.98c-99.974-99.974-262.064-99.973-362.038,0.001l0,0c-12.09-12.09-32.776-5.827-36.129,10.939L24.801,156.63 c-2.996,14.979,10.211,28.186,25.19,25.19l70.711-14.142c16.766-3.353,23.029-24.039,10.939-36.129l0,0 c68.622-68.622,180.279-68.622,248.901-0.001c68.9,68.899,68.9,180.003,0,248.903c-68.623,68.622-180.279,68.622-248.901-0.001 C97.329,346.14,80.174,301.07,80.174,256h-0.082c0-22.215-18.109-40.2-40.37-39.998c-22.076,0.2-39.694,18.688-39.629,40.765 c0.194,65.26,25.187,130.46,74.98,180.253c99.974,99.974,262.064,99.974,362.038,0.001C536.84,337.291,536.84,174.709,437.11,74.98 z"></path> <path d="M336.837,267.978l-50.746-29.298v-88.596c0-16.569-13.431-30-30-30h0c-16.569,0-30,13.431-30,30V256 c0,11.103,6.036,20.79,15.002,25.978l-0.002,0.003l65.746,37.958c14.349,8.284,32.696,3.368,40.981-10.981v0 C356.102,294.61,351.186,276.262,336.837,267.978z"></path> </g> </g></svg>
                <p>History</p>
                <!-- <div class="position"></div> -->
            </div>
            <div class="stats">
                <svg fill="#ffffff" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M1.75 13.25V1.5H.5v12a1.24 1.24 0 0 0 1.22 1H15.5v-1.25z"></path><path d="M3.15 8H4.4v3.9H3.15zm3.26-4h1.26v7.9H6.41zm3.27 2h1.25v5.9H9.68zm3.27-3.5h1.25v9.4h-1.25z"></path></g></svg>
                <p>Statistics</p>
                <!-- <div class="position"></div> -->
            </div>
        </div>
        <div class="logout">
            <p>Logout</p>
            <svg fill="#ffffff" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" class="icon"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M868 732h-70.3c-4.8 0-9.3 2.1-12.3 5.8-7 8.5-14.5 16.7-22.4 24.5a353.84 353.84 0 0 1-112.7 75.9A352.8 352.8 0 0 1 512.4 866c-47.9 0-94.3-9.4-137.9-27.8a353.84 353.84 0 0 1-112.7-75.9 353.28 353.28 0 0 1-76-112.5C167.3 606.2 158 559.9 158 512s9.4-94.2 27.8-137.8c17.8-42.1 43.4-80 76-112.5s70.5-58.1 112.7-75.9c43.6-18.4 90-27.8 137.9-27.8 47.9 0 94.3 9.3 137.9 27.8 42.2 17.8 80.1 43.4 112.7 75.9 7.9 7.9 15.3 16.1 22.4 24.5 3 3.7 7.6 5.8 12.3 5.8H868c6.3 0 10.2-7 6.7-12.3C798 160.5 663.8 81.6 511.3 82 271.7 82.6 79.6 277.1 82 516.4 84.4 751.9 276.2 942 512.4 942c152.1 0 285.7-78.8 362.3-197.7 3.4-5.3-.4-12.3-6.7-12.3zm88.9-226.3L815 393.7c-5.3-4.2-13-.4-13 6.3v76H488c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8h314v76c0 6.7 7.8 10.5 13 6.3l141.9-112a8 8 0 0 0 0-12.6z"></path> </g></svg>
        </div>
    </div>
    </div>
</template>


<style scoped>

.navbar{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    height: 10vh;
    background-color: hsla(21, 100%, 50%, 0.8);
    margin: 1rem;
    margin-right: 1rem;
    padding: 1rem;
    border-radius: 1rem;
    box-shadow: 8px 8px 25px rgba(0, 0, 0, 0.8) ;
}

.professionalDetail{
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 0.7rem;
}

.img{
    height: 3rem;
    width: 3rem;
    background-color: #ece3e3;
    border-radius: 50%;
    box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.6);
}

.professionalName{
    color: #fff;
    font-size: 1.5rem;
    font-weight: bolder;
    font-style: italic;
    padding-top: 1rem;
}

.menu{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    color: #fff;
    font-size: 1rem;
    font-weight: bolder;
    font-style: italic;
    margin-top: 0.5rem;
}

svg{
    height: 1.5rem;
    width: 1.5rem;
}
.position{
    background-color: #fff;
    height: 3px;
    width: 1.5rem;
    border-radius: 1rem;
    margin-top: 8px;
    
}

.home,.history,.stats{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}



.home:hover,.history:hover,.stats:hover{
    transform: scale(1.1);
    transition: ease-in-out 0.2s;
}

.logout{
    display: flex;
    gap: 0.5rem;
    color: #fff;
    font-size: 1.5rem;
    font-weight: bolder;
    font-style: italic;
    cursor: pointer;
}
</style>