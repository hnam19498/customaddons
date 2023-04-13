<template>
    <div id="header">
        <div style="display: flex">
            <button @click="auth_instagram" type="button" id="instagram-connection">
                <font-awesome-icon icon="fa-brands fa-instagram" style="margin-right: 5px; color: #ffffff"/>
                Connect with Instagram
            </button>
            <button @click="auth_facebook" type="button" id="facebook-connection">
                <font-awesome-icon icon="fa-brands fa-facebook-f" style="margin-right: 10px; margin-left: 10px; color: white"/>
                Connect with Facebook
            </button>
        </div>
        <div class="published-status-success" v-if="instagram_username">
            <span>Connected to <span>{{ instagram_username }}</span> with Instagram | <a
                    href="#">Change account</a></span>
        </div>
        <div class="login-facebook-success" v-if="facebook_username">
            <span>Connected to <span>{{ facebook_username }}</span> with Facebook | <a
                    href="#">Change account</a></span>
        </div>
    </div>
</template>

<script>
export default {
    name: "FeedHeader",
    methods: {
        auth_instagram() {
            window.open('https://odoo.website/instafeed/auth', '_blank')
        },
        auth_facebook() {
            window.open('https://odoo.website/facebook/auth', '_blank')
        }
    },
    mounted() {
        if (window.instafeed.users) {
            this.instagram_username = window.instafeed.users.instagram_username
            this.facebook_username = window.instafeed.users.facebook_username
        }
    },
    data() {
        return {
            instagram_username: '',
            facebook_username: ''
        }
    }
}
</script>

<style scoped>
#instagram-connection {
    background: rgb(0 128 96);
    border: .1rem solid transparent;
    box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37/5%), 0 0 0 0 transparent;
    border-radius: 5px;
    font-weight: 400;
    color: white;
    cursor: pointer;
    height: 40px;
    width: fit-content;
    display: flex;
    align-items: center;
    margin-right: 10px;
}

#facebook-connection {
    background: #1c67e9;
    border: .1rem solid transparent;
    box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37/5%), 0 0 0 0 transparent;
    border-radius: 5px;
    font-weight: 400;
    color: white;
    width: 200px;
    cursor: pointer;
    height: 40px;
    display: flex;
    align-items: center;
}

#instagram-connection:hover {
    background: rgb(1, 119, 89);
    border: .1rem solid #5400bb;
}

#facebook-connection:hover {
    background: #115ad7;
    border: .1rem solid #5400bb;
}

.published-status-success {
    font-size: 14px;
    color: #007B5C;
    margin-top: 5px;
    font-weight: bold;
}

.login-facebook-success {
    font-size: 14px;
    color: #1c67e9;
    margin-top: 5px;
    font-weight: bold;
}

#header {
    margin-right: 10px;
    margin-left: 10px;
    margin-top: 10px;
    border-radius: 5px;
    box-shadow: 0 0 0 1px rgba(63, 63, 68, .05), 0 1px 3px 0 rgba(63, 63, 68, .15);
    background: white;
}
</style>