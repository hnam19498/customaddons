<template>
    <div style="margin-bottom: 15px">
        <div class="installation-btn">
            <button class="btn" id="btn-home" @click="redirectToDashboard">Home</button>
            <button class="btn" id="btn-themes" @click="handleThemeCustomization">Go to Themes Customization</button>
        </div>
        <div id="congratulation">CONGRATULATION! YOU HAVE CREATED WIDGET SUCCESSFULLY!</div>
        <div id="now">Now please follow these steps below to display it on your product pages</div>
        <div id="content">
            <p>1. Lorem ipsum is placeholder text commonly used in the graphic, print</p>
            <p>2. and publishing industries for previewing layouts and visual mockups.</p>
            <p>3. Lorem ipsum is placeholder text commonly used in the graphic, print, and publishing industries for
                previewing layouts and visual mockups.</p>
        </div>
        <div style="width: 100%; display: flex; justify-content: center; margin-top: 60px">
            <video controls height="60%" width="60%">
                <source src="/bought_together/static/app/video/honkai.mp4" type="video/mp4">
            </video>
        </div>
    </div>
</template>
<script>
export default {
    emits: ['changeTab'],
    data() {
        return {}
    },
    props: {shop_url: String},
    methods: {
        handleThemeCustomization() {
            window.open(this.shop_url + '/admin/themes/current/editor', '_blank')
        },
        redirectToDashboard() {
            this.$emit('changeTab', 'Dashboard')
        }
    }
}
</script>
<style scoped>
.installation-btn {
    text-align: right;
    margin-top: 15px;
    margin-right: 30px;
}

#btn-home {
    align-items: center;
    padding: 4px 12px;
    gap: 4px;
    width: 62px;
    height: 32px;
    color: black;
    font-style: normal;
    font-weight: 700;
    border: #E2E2E2;
    cursor: pointer;
    margin-right: 20px;
    font-size: 14px;
    line-height: 24px;
    background: #E2E2E2;
    border-radius: 5px;
}

#btn-themes {
    align-items: center;
    padding: 4px 12px;
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    border: #1D1E21;
    line-height: 24px;
    color: white;
    flex: none;
    order: 1;
    flex-grow: 0;
    cursor: pointer;
    gap: 4px;
    width: fit-content;
    height: 32px;
    background: #1D1E21;
    border-radius: 5px;
    margin-right: 25px;
}

#congratulation {
    height: 24px;
    font-style: normal;
    font-weight: 700;
    text-align: center;
    margin-top: 114px;
    font-size: 20px;
    line-height: 22px;
    color: black;
}

#now {
    color: black;
    text-align: center;
    font-style: normal;
    font-weight: 700;
    font-size: 14px;
    margin-top: 22px;
    line-height: 22px;
    height: 22px;
}

#content {
    margin-top: 60px;
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    margin-left: 200px;
    margin-right: 200px;
}

#content p {
    line-height: 22px;
    color: black;
}
</style>