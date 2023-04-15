<template>
    <div>
        <div id="loading-btn">
            <div id="loading-btn-cancel"></div>
            <div id="loading-btn-save"></div>
        </div>
        <div id="loading-setting-widget"></div>
        <div id="loading-manual-recommendation"></div>
        <div id="loading-recommendation-product"></div>
        <div id="loading-excluded-product"></div>
    </div>
</template>
<script>
export default {
    name: 'Loading',
    data() {
        return {}
    }
}
</script>
<style scoped>
#loading-btn {
    float: right;
    margin-top: -35px;
    margin-right: 30px;
    display: flex;
}

#loading-btn-save {
    padding: 4px 12px;
    background: linear-gradient(110deg, #ececec 8%, #f5f5f5 18%, #ececec 33%);
    gap: 4px;
    width: 62px;
    animation: 1.5s shine linear infinite;
    border-radius: 4px;
    height: 32px;
    background-size: 200% 100%;
}

#loading-btn-cancel {
    padding: 4px 12px;
    background: linear-gradient(110deg, #ececec 8%, #f5f5f5 18%, #ececec 33%);
    gap: 4px;
    height: 32px;
    animation: 1.5s shine linear infinite;
    border-radius: 4px;
    width: 71px;
    margin-right: 25px;
    background-size: 200% 100%;
}

@keyframes shine {
    to {
        background-position-x: -200%;
    }
}

#loading-setting-widget {
    width: 246px;
    height: 22px;
    animation: 1.5s shine linear infinite;
    border-radius: 4px;
    background-size: 200% 100%;
    margin-top: 50px;
    margin-left: 34px;
    background: linear-gradient(110deg, #ececec 8%, #f5f5f5 18%, #ececec 33%);
    background-size: 200% 100%;
}

#loading-manual-recommendation {
    margin-top: 15px;
    margin-left: 20px;
    height: 22px;
    width: 300px;
    animation: 1.5s shine linear infinite;
    border-radius: 4px;
    background: linear-gradient(110deg, #ececec 8%, #f5f5f5 18%, #ececec 33%);
    background-size: 200% 100%;
}

#loading-recommendation-product {
    height: 340px;
    margin-right: 37px;
    margin-left: 20px;
    margin-top: 10px;
    background: linear-gradient(110deg, #ececec 8%, #f5f5f5 18%, #ececec 33%);
    animation: 1.5s shine linear infinite;
    border-radius: 4px;
    background-size: 200% 100%;
}

#loading-excluded-product {
    height: 340px;
    margin-right: 37px;
    margin-left: 20px;
    margin-top: 14px;
    background: linear-gradient(110deg, #ececec 8%, #f5f5f5 18%, #ececec 33%);
    animation: 1.5s shine linear infinite;
    border-radius: 4px;
    background-size: 200% 100%;
}
</style>