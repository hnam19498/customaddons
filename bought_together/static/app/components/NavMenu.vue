<template>
    <div class="nav-menu">
        <div :key="tab"
             @click="changeTab(tab)"
             class="nav-item"
             v-for="tab in navtabs"
             :class="{ active: tab == currentTab }">
            {{ tab }}
        </div>
    </div>
</template>
<script>
export default {
    emits:['changeTab'],
    name: "NavMenu",
    data() {
        return {}
    },
    props: {
        navtabs: Array,
        currentTab: String
    },
    methods: {
        changeTab(tab) {
            this.$emit('changeTab', tab)
        }
    }
}
</script>
<style scoped>
.nav-menu {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    padding: 3px;
    margin-top: 14px;
    width: 560px;
    margin-left: auto;
    margin-right: auto;
    height: 42px;
    justify-content: center;
    background: #C8C8C8;
    border-radius: 4px;
}

.nav-item {
    box-sizing: border-box;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    padding: 6px 16px;
    width: 184.67px;
    height: 36px;
    border-radius: 4px;
    cursor: pointer;
    flex: none;
    order: 0;
    flex-grow: 1;
    background-color: #C8C8C8;
    color: white;
}

.nav-menu .active {
    background: white;
    color: black;
}
</style>