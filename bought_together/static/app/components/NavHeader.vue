<template>
    <div class="nav-bar" style="font-size: 30px;">
        <div class="frame-50">
            <font-awesome-icon icon="fa-solid fa-circle-question"/>
            <font-awesome-icon icon="fa-regular fa-bell"/>
            <img src="https://i.pinimg.com/736x/1b/13/ad/1b13ad4e67b8a75e38f3fc6628f7a970.jpg">
        </div>
    </div>
</template>
<script>
export default {
    name: 'compNavHeader',
    data() {
        return {}
    }
}
</script>
<style scoped>
.nav-bar {
    z-index: -1;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    height: 83px;
    background: #EFEFEF;
}

.frame-50 {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    align-items: center;
    padding: 0;
    gap: 26px;
    width: 133px;
    height: 34px;
    right: 25px;
}

.frame-50 img {
    width: 34px;
    height: 34px;
    flex: none;
    order: 2;
    margin-right: 30px;
    flex-grow: 0;
    border-radius: 50%;
}

.frame-50 svg {
    width: 17px;
    height: 34px;
}
</style>