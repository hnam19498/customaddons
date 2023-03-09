<template>
    <div class="sidebar-menu">
        <div class="company-icon">
            <img src="/bought_together/static/app/img/LogoNestScale.png" class="black-circle">
            <p class="company-name">NestScale</p>
        </div>
        <div class="menu-item">
            <div class="item">
                <font-awesome-icon icon="fas fa-circle"/>
                Kiana
            </div>
            <div class="item">
                <font-awesome-icon icon="fas fa-circle"/>
                Mei
            </div>
            <div class="item">
                <font-awesome-icon icon="fas fa-circle"/>
                Bronya
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {}
    }
}
</script>
<style scoped>
.sidebar-menu {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 24px 20px 0 20px;
    gap: 32px;
    min-height: 100%;
    width: 276px;
    background-color: #EFEFEF;
}

.company-icon {
    flex: none;
    display: flex;
    order: 0;
    background-color: #EFEFEF;
    flex-grow: 0;
}

.black-circle {
    width: 46px;
    height: 46px;
    border-radius: 50%;
}

.company-name {
    width: 123px;
    height: 24px;
    font-style: normal;
    font-weight: 600;
    text-align: center;
    font-size: 27px;
    line-height: 24px;
    margin: auto;
    color: #17181A;
    flex: none;
    order: 1;
    flex-grow: 0;
}

.item {
    display: flex;
    align-items: center;
    margin-bottom: 16px;
}

.item svg {
    color: #D9D9D9;
    font-size: 32px;
}
</style>